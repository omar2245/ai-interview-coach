import json
import random
import time
from textwrap import dedent

from fastapi import HTTPException, status
from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    OpenAI,
)
from pydantic import ValidationError

from app.core.config import settings
from app.schemas.analysis import AnalyzeRequest, AnalyzeResponse


RETRYABLE_STATUS_CODES = {408, 429, 500, 502, 503, 504}


def build_analysis_prompt(request: AnalyzeRequest) -> str:
    return dedent(
        f"""
        請比較以下履歷與職缺說明，並以繁體中文提供具體、務實的求職分析。

        規則：
        - match_score 必須是 0 到 100 的整數。
        - 每個陣列提供 2 到 5 項，內容簡潔且不可重複。
        - summary 不超過 250 個中文字。
        - 只根據提供的內容判斷，不可捏造履歷中沒有的經驗。

        履歷：
        {request.resume_text}

        職缺說明：
        {request.job_description}
        """
    ).strip()


def parse_analysis_response(analysis_text: str) -> AnalyzeResponse:
    return AnalyzeResponse.model_validate_json(analysis_text)


def retry_delay(attempt: int) -> float:
    return min(2**attempt, 8) + random.uniform(0, 0.5)


def call_gemini_chat(client: OpenAI, prompt: str) -> str:
    last_error: Exception | None = None

    for attempt in range(settings.gemini_max_retries + 1):
        try:
            response = client.chat.completions.create(
                model=settings.gemini_model,
                messages=[
                    {
                        "role": "system",
                        "content": "你是專業的履歷與職缺匹配分析顧問。",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=settings.gemini_max_output_tokens,
                reasoning_effort=settings.gemini_reasoning_effort,
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "job_fit_analysis",
                        "strict": True,
                        "schema": AnalyzeResponse.model_json_schema(),
                    },
                },
            )
            content = response.choices[0].message.content
            if not content:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Gemini 沒有回傳分析內容。",
                )
            return content
        except APIStatusError as exc:
            last_error = exc
            if (
                exc.status_code in RETRYABLE_STATUS_CODES
                and attempt < settings.gemini_max_retries
            ):
                time.sleep(retry_delay(attempt))
                continue
            if exc.status_code == 429:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=(
                        "Gemini 請求或 Token 額度已達限制，請稍後再試。"
                        "若持續發生，請檢查 Google AI Studio 的 RPM、TPM 與每日額度。"
                    ),
                ) from exc
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Gemini 服務暫時無法完成分析（HTTP {exc.status_code}）。",
            ) from exc
        except (APITimeoutError, APIConnectionError) as exc:
            last_error = exc
            if attempt < settings.gemini_max_retries:
                time.sleep(retry_delay(attempt))
                continue
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Gemini 連線逾時，請稍後再試。",
            ) from exc

    raise HTTPException(
        status_code=status.HTTP_502_BAD_GATEWAY,
        detail=f"Gemini 分析失敗：{type(last_error).__name__}",
    )


def generate_gemini_analysis(request: AnalyzeRequest) -> AnalyzeResponse:
    if not settings.gemini_api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="GEMINI_API_KEY 尚未設定。",
        )

    client = OpenAI(
        api_key=settings.gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        timeout=settings.gemini_timeout_seconds,
        max_retries=0,
    )

    analysis_text = call_gemini_chat(
        client=client,
        prompt=build_analysis_prompt(request=request),
    )

    try:
        return parse_analysis_response(analysis_text=analysis_text)
    except (json.JSONDecodeError, ValidationError) as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Gemini 回傳的分析格式不正確，請重新嘗試。",
        ) from exc

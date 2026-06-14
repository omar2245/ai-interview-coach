import json
import time
from textwrap import dedent

from fastapi import HTTPException, status
from openai import OpenAI, OpenAIError
from pydantic import ValidationError

from app.core.config import settings
from app.schemas.analysis import AnalyzeRequest, AnalyzeResponse


def build_analysis_prompt(request: AnalyzeRequest) -> str:
    return dedent(
        f"""
        請根據以下履歷與職缺，產生繁體中文分析結果。

        回傳 JSON 格式必須符合：
        {{
          "match_score": 78,
          "summary": "整體匹配摘要",
          "strengths": ["履歷強項"],
          "matched_requirements": ["職缺需求命中點"],
          "gaps": ["可能缺口"],
          "recommendations": ["建議補強"],
          "interview_focus": ["面試前準備重點"]
        }}

        規則：
        - match_score 必須是 0 到 100 的整數
        - 每個陣列請回傳 2 到 5 筆
        - 不要回傳 JSON 以外的文字

        履歷：
        {request.resume_text}

        職缺：
        {request.job_description}
        """
    ).strip()


def parse_analysis_response(analysis_text: str) -> AnalyzeResponse:
    analysis_data = json.loads(analysis_text)
    return AnalyzeResponse.model_validate(analysis_data)


def is_gemini_quota_error(error: OpenAIError) -> bool:
    error_text = str(error)
    return (
        "429" in error_text
        or "RESOURCE_EXHAUSTED" in error_text
        or "Quota exceeded" in error_text
    )


def call_gemini_chat(client: OpenAI, messages: list[dict[str, str]]) -> str:
    for attempt in range(2):
        try:
            response = client.chat.completions.create(
                model=settings.gemini_model,
                messages=messages,
            )
            content = response.choices[0].message.content

            if not content:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Gemini 沒有回傳內容",
                )

            return content
        except OpenAIError as exc:
            if attempt == 0 and "503" in str(exc):
                time.sleep(2)
                continue

            if is_gemini_quota_error(error=exc):
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Gemini 免費額度或請求次數暫時用完，請稍後再試。",
                ) from exc

            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Gemini 分析服務呼叫失敗：{exc}",
            ) from exc

    raise HTTPException(
        status_code=status.HTTP_502_BAD_GATEWAY,
        detail="Gemini 分析服務呼叫失敗",
    )


def repair_analysis_json(client: OpenAI, invalid_text: str) -> str:
    return call_gemini_chat(
        client=client,
        messages=[
            {
                "role": "system",
                "content": (
                    "你是一位 JSON 修復助手。"
                    "請只回傳修復後的 JSON，不要使用 Markdown，不要加上 ```。"
                ),
            },
            {
                "role": "user",
                "content": dedent(
                    f"""
                以下內容原本應該是履歷分析 JSON，但格式不符合要求。
                請修正成合法 JSON，並且必須符合欄位：
                match_score, summary, strengths, matched_requirements,
                gaps, recommendations, interview_focus

                原始內容：
                {invalid_text}
                """
                ).strip(),
            },
        ],
    )


def generate_gemini_analysis(request: AnalyzeRequest) -> AnalyzeResponse:
    if not settings.gemini_api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="GEMINI_API_KEY 尚未設定",
        )

    client = OpenAI(
        api_key=settings.gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    analysis_text = call_gemini_chat(
        client=client,
        messages=[
            {
                "role": "system",
                "content": (
                    "你是一位專業的求職履歷與職缺匹配分析助手。"
                    "請只回傳 JSON，不要使用 Markdown，不要加上 ```。"
                ),
            },
            {
                "role": "user",
                "content": build_analysis_prompt(request=request),
            },
        ],
    )

    try:
        return parse_analysis_response(analysis_text=analysis_text)
    except (json.JSONDecodeError, ValidationError):
        repaired_text = repair_analysis_json(
            client=client,
            invalid_text=analysis_text,
        )

    try:
        return parse_analysis_response(analysis_text=repaired_text)
    except (json.JSONDecodeError, ValidationError) as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Gemini 回傳內容無法修復成有效的分析 JSON",
        ) from exc

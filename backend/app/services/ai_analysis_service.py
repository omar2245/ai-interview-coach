from fastapi import HTTPException, status
from openai import OpenAI

from app.core.config import settings
from app.schemas.analysis import AnalyzeRequest, AnalyzeResponse


def generate_ai_analysis(request: AnalyzeRequest) -> AnalyzeResponse:
    if not settings.openai_api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="OPENAI_API_KEY 尚未設定",
        )

    client = OpenAI(api_key=settings.openai_api_key)

    response = client.responses.create(
        model=settings.openai_model,
        input="請用繁體中文回覆：OpenAI 分析服務已連線成功。",
    )

    print(response.output_text)

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="OpenAI 分析服務已連線，但分析功能尚未完成",
    )

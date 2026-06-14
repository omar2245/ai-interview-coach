from fastapi import HTTPException, status

from app.core.config import settings
from app.schemas.analysis import AnalyzeRequest, AnalyzeResponse
from app.services.ai_analysis_service import generate_ai_analysis
from app.services.fake_analysis_service import generate_fake_analysis
from app.services.gemini_analysis_service import generate_gemini_analysis


def analyze_resume(request: AnalyzeRequest) -> AnalyzeResponse:
    if not request.job_description.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="職缺描述不可為空",
        )

    if not request.resume_text or not request.resume_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="履歷內容不可為空",
        )

    if settings.analysis_provider == "fake":
        return generate_fake_analysis(request=request)

    if settings.analysis_provider == "openai":
        return generate_ai_analysis(request=request)

    if settings.analysis_provider == "gemini":
        return generate_gemini_analysis(request=request)

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="分析服務設定錯誤",
    )

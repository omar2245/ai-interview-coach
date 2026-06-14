from fastapi import APIRouter, File, Form, UploadFile

from app.schemas.analysis import AnalyzeRequest, AnalyzeResponse
from app.services.analysis_service import analyze_resume
from app.services.resume_parser_service import parse_resume_file

router = APIRouter(prefix="/api", tags=["analysis"])


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_resume_endpoint(
    job_description: str = Form(...),
    resume_text: str | None = Form(None),
    resume_file: UploadFile | None = File(None),
    role_type: str | None = Form(None),
    language: str = Form("zh-TW"),
) -> AnalyzeResponse:
    if resume_file:
        resume_text = await parse_resume_file(resume_file=resume_file)

    return analyze_resume(
        request=AnalyzeRequest(
            job_description=job_description,
            resume_text=resume_text,
            role_type=role_type,
            language=language,
        )
    )

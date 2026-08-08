import logging

from fastapi import APIRouter, File, Form, Request, UploadFile

from app.schemas.analysis import AnalyzeRequest, AnalyzeResponse, ResumeSource
from app.services.analysis_service import analyze_resume
from app.services.history_service import save_analysis
from app.services.resume_parser_service import parse_resume_file

router = APIRouter(prefix="/api", tags=["analysis"])
logger = logging.getLogger(__name__)


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_resume_endpoint(
    http_request: Request,
    job_description: str = Form(...),
    resume_text: str | None = Form(None),
    resume_file: UploadFile | None = File(None),
    job_title: str | None = Form(None),
    company_name: str | None = Form(None),
    role_type: str | None = Form(None),
    language: str = Form("zh-TW"),
) -> AnalyzeResponse:
    resume_source: ResumeSource = "file" if resume_file else "text"
    original_filename = resume_file.filename if resume_file else None
    if resume_file:
        resume_text = await parse_resume_file(resume_file=resume_file)

    analysis_request = AnalyzeRequest(
        job_description=job_description,
        resume_text=resume_text,
        job_title=job_title,
        company_name=company_name,
        role_type=role_type,
        language=language,
    )
    result = analyze_resume(request=analysis_request)

    engine = http_request.app.state.history_engine
    if engine is None:
        return result

    try:
        history_id = save_analysis(
            engine=engine,
            request=analysis_request,
            result=result,
            resume_source=resume_source,
            original_filename=original_filename,
        )
    except Exception as error:
        logger.error("Failed to persist completed analysis (%s)", type(error).__name__)
        return result.model_copy(
            update={"history_id": None, "history_status": "failed"}
        )

    return result.model_copy(
        update={"history_id": history_id, "history_status": "saved"}
    )

from datetime import datetime, timezone

from sqlalchemy import Engine
from sqlalchemy.orm import Session

from app.models.analysis_history import AnalysisHistory
from app.schemas.analysis import AnalyzeRequest, AnalyzeResponse, ResumeSource


def save_analysis(
    *,
    engine: Engine,
    request: AnalyzeRequest,
    result: AnalyzeResponse,
    resume_source: ResumeSource,
    original_filename: str | None,
) -> int:
    job_title = _optional_trimmed(request.job_title)
    company_name = _optional_trimmed(request.company_name)
    job_description = request.job_description.strip()
    resume_text = (request.resume_text or "").strip()

    record = AnalysisHistory(
        job_title=job_title,
        company_name=company_name,
        display_title=job_title or _fallback_title(job_description),
        resume_text=resume_text,
        job_description=job_description,
        resume_source=resume_source,
        original_filename=original_filename,
        match_score=result.match_score,
        summary=result.summary,
        strengths=result.strengths,
        matched_requirements=result.matched_requirements,
        gaps=result.gaps,
        recommendations=result.recommendations,
        interview_focus=result.interview_focus,
        created_at=datetime.now(timezone.utc).isoformat(),
    )

    with Session(engine) as session, session.begin():
        session.add(record)
        session.flush()
        history_id = record.id

    return history_id


def _optional_trimmed(value: str | None) -> str | None:
    if value is None:
        return None
    trimmed = value.strip()
    return trimmed or None


def _fallback_title(job_description: str) -> str:
    first_nonblank_line = next(
        (line.strip() for line in job_description.splitlines() if line.strip()),
        "Unnamed role",
    )
    return first_nonblank_line[:80]

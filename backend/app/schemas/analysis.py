from typing import Literal

from pydantic import BaseModel

ResumeSource = Literal["text", "file"]


class AnalyzeRequest(BaseModel):
    job_description: str
    resume_text: str | None = None
    job_title: str | None = None
    company_name: str | None = None
    role_type: str | None = None
    language: str = "zh-TW"


class AnalyzeResponse(BaseModel):
    match_score: int
    summary: str
    strengths: list[str]
    matched_requirements: list[str]
    gaps: list[str]
    recommendations: list[str]
    interview_focus: list[str]
    history_id: int | None = None
    history_status: Literal["saved", "disabled", "failed"] = "disabled"

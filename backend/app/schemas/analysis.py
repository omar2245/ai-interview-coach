from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    job_description: str
    resume_text: str | None = None
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

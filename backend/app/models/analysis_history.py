from sqlalchemy import JSON, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class AnalysisHistory(Base):
    __tablename__ = "analysis_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    job_title: Mapped[str | None] = mapped_column(String(200))
    company_name: Mapped[str | None] = mapped_column(String(200))
    display_title: Mapped[str] = mapped_column(String(80))
    resume_text: Mapped[str] = mapped_column(Text)
    job_description: Mapped[str] = mapped_column(Text)
    resume_source: Mapped[str] = mapped_column(String(10))
    original_filename: Mapped[str | None] = mapped_column(String(255))
    match_score: Mapped[int] = mapped_column(Integer)
    summary: Mapped[str] = mapped_column(Text)
    strengths: Mapped[list[str]] = mapped_column(JSON)
    matched_requirements: Mapped[list[str]] = mapped_column(JSON)
    gaps: Mapped[list[str]] = mapped_column(JSON)
    recommendations: Mapped[list[str]] = mapped_column(JSON)
    interview_focus: Mapped[list[str]] = mapped_column(JSON)
    created_at: Mapped[str] = mapped_column(String(32))

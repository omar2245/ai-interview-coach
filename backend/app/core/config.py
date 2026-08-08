import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    analysis_provider: str = os.getenv("ANALYSIS_PROVIDER", "fake")
    history_enabled: bool = os.getenv("HISTORY_ENABLED", "false").lower() in {
        "1",
        "true",
        "yes",
        "on",
    }
    database_url: str = os.getenv(
        "DATABASE_URL", "sqlite:///./data/analysis-history.db"
    )
    allowed_origins: list[str] = [
        origin.strip()
        for origin in os.getenv(
            "ALLOWED_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173",
        ).split(",")
        if origin.strip()
    ]
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    gemini_api_key: str | None = os.getenv("GEMINI_API_KEY")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
    gemini_timeout_seconds: float = float(os.getenv("GEMINI_TIMEOUT_SECONDS", "45"))
    gemini_max_retries: int = int(os.getenv("GEMINI_MAX_RETRIES", "2"))
    gemini_max_output_tokens: int = int(os.getenv("GEMINI_MAX_OUTPUT_TOKENS", "1200"))
    gemini_reasoning_effort: str = os.getenv("GEMINI_REASONING_EFFORT", "low")
    max_resume_chars: int = int(os.getenv("MAX_RESUME_CHARS", "20000"))
    max_job_description_chars: int = int(
        os.getenv("MAX_JOB_DESCRIPTION_CHARS", "12000")
    )


settings = Settings()

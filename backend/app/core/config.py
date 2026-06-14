import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    analysis_provider: str = os.getenv("ANALYSIS_PROVIDER", "fake")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    gemini_api_key: str | None = os.getenv("GEMINI_API_KEY")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")


settings = Settings()

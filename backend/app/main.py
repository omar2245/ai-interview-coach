from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.analysis import router as analysis_router
from app.core.config import settings


def create_app(*, history_enabled: bool | None = None) -> FastAPI:
    history_is_enabled = (
        settings.history_enabled if history_enabled is None else history_enabled
    )
    application = FastAPI(
        title="JobFit Analyzer API",
        description="Backend API for resume and job description matching analysis.",
        version="0.1.0",
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(analysis_router)

    @application.get("/health")
    def health_check() -> dict[str, str]:
        return {"status": "ok"}

    @application.get("/api/capabilities")
    def get_capabilities() -> dict[str, bool]:
        return {"history_enabled": history_is_enabled}

    return application


app = create_app()

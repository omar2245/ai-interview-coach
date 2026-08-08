from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.analysis import router as analysis_router
from app.core.config import settings
from app.database import build_engine, verify_migrated_schema


def create_app(
    *,
    history_enabled: bool | None = None,
    database_url: str | None = None,
) -> FastAPI:
    history_is_enabled = (
        settings.history_enabled if history_enabled is None else history_enabled
    )
    configured_database_url = database_url or settings.database_url
    engine = build_engine(configured_database_url) if history_is_enabled else None

    @asynccontextmanager
    async def lifespan(application: FastAPI):
        if engine is not None:
            verify_migrated_schema(engine)
        yield
        if engine is not None:
            engine.dispose()

    application = FastAPI(
        title="JobFit Analyzer API",
        description="Backend API for resume and job description matching analysis.",
        version="0.1.0",
        lifespan=lifespan,
    )
    application.state.history_engine = engine

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

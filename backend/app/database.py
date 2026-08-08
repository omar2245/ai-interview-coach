from pathlib import Path

from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import Engine, create_engine, inspect


def build_engine(database_url: str) -> Engine:
    return create_engine(database_url)


def current_database_revision() -> str:
    config = Config()
    config.set_main_option(
        "script_location", str(Path(__file__).resolve().parents[1] / "migrations")
    )
    revision = ScriptDirectory.from_config(config).get_current_head()
    if revision is None:
        raise RuntimeError("Alembic has no head migration configured.")
    return revision


def verify_migrated_schema(engine: Engine) -> None:
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    if "alembic_version" not in table_names:
        raise RuntimeError(
            "History is enabled, but the database is not migrated. "
            "Run `alembic upgrade head` from the backend directory."
        )

    with engine.connect() as connection:
        revision = connection.exec_driver_sql(
            "SELECT version_num FROM alembic_version"
        ).scalar_one_or_none()

    if revision != current_database_revision():
        raise RuntimeError(
            "History database migration is out of date. "
            "Run `alembic upgrade head` from the backend directory."
        )

    if "analysis_history" not in table_names:
        raise RuntimeError(
            "History database schema is incomplete. "
            "Run `alembic upgrade head` from the backend directory."
        )

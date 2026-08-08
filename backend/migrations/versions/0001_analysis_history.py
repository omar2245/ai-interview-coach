"""Create the analysis history aggregate."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001_analysis_history"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "analysis_history",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("job_title", sa.String(length=200), nullable=True),
        sa.Column("company_name", sa.String(length=200), nullable=True),
        sa.Column("display_title", sa.String(length=80), nullable=False),
        sa.Column("resume_text", sa.Text(), nullable=False),
        sa.Column("job_description", sa.Text(), nullable=False),
        sa.Column("resume_source", sa.String(length=10), nullable=False),
        sa.Column("original_filename", sa.String(length=255), nullable=True),
        sa.Column("match_score", sa.Integer(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("strengths", sa.JSON(), nullable=False),
        sa.Column("matched_requirements", sa.JSON(), nullable=False),
        sa.Column("gaps", sa.JSON(), nullable=False),
        sa.Column("recommendations", sa.JSON(), nullable=False),
        sa.Column("interview_focus", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.String(length=32), nullable=False),
        sa.CheckConstraint(
            "resume_source IN ('text', 'file')",
            name="ck_analysis_history_resume_source",
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("analysis_history")

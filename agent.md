# Agent Notes

This file records how we will work on this project together.

## Collaboration Style

- Work slowly and explain each step.
- Prefer small changes that are easy to understand.
- After each meaningful step, explain:
  - what changed
  - why it changed
  - how to test it
- For coding changes, do not push to GitHub until the user has reviewed and approved the changes.
- Avoid adding advanced features before the MVP works.
- Keep the project beginner-friendly.

## Product Direction

The product is an AI interview preparation tool.
The first MVP is a resume and job description matching analyzer.

The core user flow is:

```txt
resume + job description -> AI analysis -> structured result
```

## MVP Boundaries

Build now:

- one-page web app
- resume input
- job description input
- AI match analysis
- structured result display
- basic validation and error states

Build in v0.2:

- local single-user analysis history
- runtime capability gate that is disabled by default
- SQLite persistence managed through explicit migrations
- history list, detail, deletion, and reuse flows

Do not build yet:

- login
- payment
- user accounts
- mock interview chat
- voice features
- WebSocket
- multi-resume management

## Technical Defaults

Unless we decide otherwise later, prefer:

- Vue 3 for the frontend web app
- TypeScript for safer frontend code
- Tailwind CSS for styling
- shadcn-vue for reusable UI components
- @lucide/vue for icons
- FastAPI for the backend API
- a single backend endpoint for MVP analysis
- simple local state for the first UI
- no database in version 1
- no permanent file storage in version 1

## v0.2 Persistence Architecture

- Local analysis history is disabled by default and is intended for a single
  local user until authentication and ownership exist.
- SQLite stores parsed resume text, job-description text, source metadata, and
  complete structured analysis results; uploaded PDF/DOCX binaries are never
  persisted.
- SQLAlchemy 2.0 maps the aggregate, while Alembic migrations are the only
  mechanism that creates or evolves its schema.
- An enabled application validates the Alembic revision during startup and
  fails with an actionable migration command when the database is not ready.
- A persistence failure does not discard an already completed AI analysis; the
  response reports `saved`, `disabled`, or `failed` together with a nullable
  history ID.

## API Contract

The MVP API should expose:

```http
POST /api/analyze
```

Expected inputs:

- `job_description`
- `resume_file` optional
- `resume_text` optional
- `role_type` optional
- `language` default `zh-TW`

Expected output:

- `match_score`
- `summary`
- `strengths`
- `matched_requirements`
- `gaps`
- `recommendations`
- `interview_focus`

## Safety Rules

Do not batch delete files or directories.

Do not use:

- `del /s`
- `rd /s`
- `rmdir /s`
- `Remove-Item -Recurse`
- `rm -rf`

When deleting is necessary, delete only one explicit file path at a time.

Correct example:

```powershell
Remove-Item "C:\path\to\file.txt"
```

If many files need to be deleted, stop and ask the user to delete them manually.

## Documentation Rule

When a major decision changes, update `Readme.md` or this file so the project remains easy to follow.

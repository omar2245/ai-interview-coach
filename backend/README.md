# Backend

FastAPI backend for JobFit Analyzer.

## Local Development

Create a virtual environment:

```powershell
python -m venv .venv
```

Install dependencies:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

For development, install the test dependencies instead:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

Run the API server:

```powershell
.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Health check:

```http
GET http://localhost:8000/health
```

Runtime capabilities:

```http
GET http://localhost:8000/api/capabilities
```

Analysis history is disabled by default. Set `HISTORY_ENABLED=true` only for
local development. Public deployments should leave it disabled until history
has an authentication and ownership model.

## Local analysis history

History uses SQLite through SQLAlchemy 2.0. Alembic owns the schema; the app
never creates tables automatically. From the `backend` directory, migrate the
default local database before enabling history:

```powershell
.venv\Scripts\python.exe -m alembic upgrade head
$env:HISTORY_ENABLED = "true"
.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

The default database is `backend/data/analysis-history.db` and is ignored by
Git because it contains resume and job-description data. To choose another
location, use the same `DATABASE_URL` for both migration and application:

```powershell
$env:DATABASE_URL = "sqlite:///C:/data/jobfit-history.db"
.venv\Scripts\python.exe -m alembic upgrade head
```

If history is enabled against an unmigrated or outdated database, startup
fails with an instruction to run `alembic upgrade head`.

## Tests

Run the backend API tests:

```powershell
.venv\Scripts\python.exe -m pytest -q
```

The API tests force the fake analysis provider, so they do not call Gemini or
consume API quota.

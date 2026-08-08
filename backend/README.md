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

## Tests

Run the backend API tests:

```powershell
.venv\Scripts\python.exe -m pytest -q
```

The API tests force the fake analysis provider, so they do not call Gemini or
consume API quota.

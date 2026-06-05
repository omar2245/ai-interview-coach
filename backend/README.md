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

Run the API server:

```powershell
.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Health check:

```http
GET http://localhost:8000/health
```

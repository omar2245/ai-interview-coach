import os
from io import BytesIO

from docx import Document
from fastapi.testclient import TestClient
from reportlab.pdfgen import canvas

os.environ["ANALYSIS_PROVIDER"] = "fake"

from app.main import app, create_app


client = TestClient(app)


def test_health_check_reports_service_is_available() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_capabilities_report_history_is_disabled_by_default() -> None:
    response = client.get("/api/capabilities")

    assert response.status_code == 200
    assert response.json() == {"history_enabled": False}


def test_disabled_app_does_not_expose_history_routes() -> None:
    response = client.get("/api/history")

    assert response.status_code == 404


def test_capabilities_report_history_is_enabled_for_enabled_app() -> None:
    enabled_client = TestClient(create_app(history_enabled=True))

    response = enabled_client.get("/api/capabilities")

    assert response.status_code == 200
    assert response.json() == {"history_enabled": True}


def test_analyze_returns_structured_job_fit_result() -> None:
    response = client.post(
        "/api/analyze",
        data={
            "job_description": "Build and maintain Vue applications.",
            "resume_text": "Frontend engineer with three years of Vue experience.",
        },
    )

    assert response.status_code == 200
    assert response.json()["match_score"] == 78
    assert set(response.json()) == {
        "match_score",
        "summary",
        "strengths",
        "matched_requirements",
        "gaps",
        "recommendations",
        "interview_focus",
    }


def test_analyze_rejects_blank_job_description() -> None:
    response = client.post(
        "/api/analyze",
        data={
            "job_description": "   ",
            "resume_text": "Frontend engineer with Vue experience.",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"]


def test_analyze_rejects_missing_resume() -> None:
    response = client.post(
        "/api/analyze",
        data={"job_description": "Build and maintain Vue applications."},
    )

    assert response.status_code == 400
    assert response.json()["detail"]


def test_analyze_accepts_utf8_text_resume_upload() -> None:
    response = client.post(
        "/api/analyze",
        data={"job_description": "Build and maintain Vue applications."},
        files={
            "resume_file": (
                "resume.txt",
                "Frontend engineer with Vue experience.".encode(),
                "text/plain",
            )
        },
    )

    assert response.status_code == 200
    assert response.json()["match_score"] == 78


def test_analyze_rejects_unsupported_resume_file_type() -> None:
    response = client.post(
        "/api/analyze",
        data={"job_description": "Build and maintain Vue applications."},
        files={"resume_file": ("resume.csv", b"Vue,TypeScript", "text/csv")},
    )

    assert response.status_code == 400
    assert response.json()["detail"]


def test_analyze_rejects_resume_larger_than_five_megabytes() -> None:
    response = client.post(
        "/api/analyze",
        data={"job_description": "Build and maintain Vue applications."},
        files={
            "resume_file": (
                "resume.txt",
                b"a" * (5 * 1024 * 1024 + 1),
                "text/plain",
            )
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"]


def test_analyze_rejects_blank_text_resume_upload() -> None:
    response = client.post(
        "/api/analyze",
        data={"job_description": "Build and maintain Vue applications."},
        files={"resume_file": ("resume.txt", b"  \n\t", "text/plain")},
    )

    assert response.status_code == 400
    assert response.json()["detail"]


def test_analyze_rejects_non_utf8_text_resume_upload() -> None:
    response = client.post(
        "/api/analyze",
        data={"job_description": "Build and maintain Vue applications."},
        files={"resume_file": ("resume.txt", b"\xff\xfe\xfa", "text/plain")},
    )

    assert response.status_code == 400
    assert response.json()["detail"]


def test_analyze_accepts_valid_docx_resume_upload() -> None:
    document_bytes = BytesIO()
    document = Document()
    document.add_paragraph("Frontend engineer with Vue experience.")
    document.save(document_bytes)

    response = client.post(
        "/api/analyze",
        data={"job_description": "Build and maintain Vue applications."},
        files={
            "resume_file": (
                "resume.docx",
                document_bytes.getvalue(),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        },
    )

    assert response.status_code == 200
    assert response.json()["match_score"] == 78


def test_analyze_accepts_valid_pdf_resume_upload() -> None:
    document_bytes = BytesIO()
    document = canvas.Canvas(document_bytes)
    document.drawString(72, 720, "Frontend engineer with Vue experience.")
    document.save()

    response = client.post(
        "/api/analyze",
        data={"job_description": "Build and maintain Vue applications."},
        files={
            "resume_file": (
                "resume.pdf",
                document_bytes.getvalue(),
                "application/pdf",
            )
        },
    )

    assert response.status_code == 200
    assert response.json()["match_score"] == 78

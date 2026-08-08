from io import BytesIO
from pathlib import Path

from docx import Document
from fastapi import HTTPException, UploadFile, status
from pypdf import PdfReader

MAX_RESUME_FILE_SIZE = 5 * 1024 * 1024
SUPPORTED_RESUME_EXTENSIONS = {".pdf", ".docx", ".txt"}


async def parse_resume_file(resume_file: UploadFile) -> str:
    filename = resume_file.filename or ""
    extension = Path(filename).suffix.lower()

    if extension not in SUPPORTED_RESUME_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="履歷檔案只支援 PDF、DOCX、TXT",
        )

    file_bytes = await resume_file.read()

    if len(file_bytes) > MAX_RESUME_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="履歷檔案不可超過 5MB",
        )

    if extension == ".txt":
        resume_text = parse_txt_resume(file_bytes=file_bytes)
    elif extension == ".pdf":
        resume_text = parse_pdf_resume(file_bytes=file_bytes)
    else:
        resume_text = parse_docx_resume(file_bytes=file_bytes)

    if not resume_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="無法從履歷檔案中讀取文字，請改用可選取文字的 PDF/DOCX，或直接貼上履歷文字",
        )

    return resume_text


def parse_txt_resume(file_bytes: bytes) -> str:
    try:
        return file_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="TXT 檔案必須使用 UTF-8 編碼",
        ) from exc


def parse_pdf_resume(file_bytes: bytes) -> str:
    try:
        reader = PdfReader(BytesIO(file_bytes))
        page_texts = [page.extract_text() or "" for page in reader.pages]
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="PDF 履歷解析失敗，請確認檔案可以正常開啟",
        ) from exc

    return "\n".join(page_texts).strip()


def parse_docx_resume(file_bytes: bytes) -> str:
    try:
        document = Document(BytesIO(file_bytes))
        paragraph_texts = [paragraph.text for paragraph in document.paragraphs]
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="DOCX 履歷解析失敗，請確認檔案可以正常開啟",
        ) from exc

    return "\n".join(paragraph_texts).strip()

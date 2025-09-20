"""Utilities for extracting raw text from uploaded resume files."""

from pathlib import Path
from io import BytesIO

import fitz  # PyMuPDF
from docx import Document


def _extract_text_from_pdf(file_like: BytesIO) -> str:
    """Read a PDF from an in‑memory buffer and return all page text."""
    text = ""
    with fitz.open(stream=file_like.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text


def _extract_text_from_docx(file_like: BytesIO) -> str:
    """Read DOCX from an in‑memory buffer and return concatenated paragraph text."""
    document = Document(file_like)
    return "\n".join(p.text for p in document.paragraphs)


def extract_text(uploaded_file) -> str:
    """Detect file type from the uploaded_file name and extract text."""
    suffix = Path(uploaded_file.name).suffix.lower()

    if suffix == ".pdf":
        return _extract_text_from_pdf(uploaded_file)
    elif suffix in {".docx", ".doc"}:
        return _extract_text_from_docx(uploaded_file)
    elif suffix == ".txt":
        return uploaded_file.read().decode("utf‑8", errors="ignore")
    else:
        raise ValueError(f"Unsupported file format: {suffix}")
# src/backend/pdf_loader.py

from typing import List
import PyPDF2
import pdfplumber
import threading

# -------- Timeout wrapper (Windows safe) --------
def run_with_timeout(func, args=(), timeout=3):
    result = {}

    def wrapper():
        try:
            result["value"] = func(*args)
        except Exception as e:
            result["error"] = e

    thread = threading.Thread(target=wrapper)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        return None  # Timeout happened

    if "error" in result:
        return None

    return result.get("value")


# -------- Text extractors --------
def extract_with_pdfplumber(path: str):
    text_parts = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text_parts.append(page.extract_text() or "")
    return "\n".join(text_parts).strip()


def extract_with_pypdf(path: str):
    reader = PyPDF2.PdfReader(path)
    texts = []
    for page in reader.pages:
        texts.append(page.extract_text() or "")
    return "\n".join(texts).strip()


def extract_text_from_pdf(path: str) -> str:
    """
    Extract text robustly WITHOUT freezing.
    """

    # -------- Try pdfplumber with timeout --------
    text = run_with_timeout(extract_with_pdfplumber, args=(path,), timeout=3)
    if text and len(text) > 20:
        return text

    print("⚠️ pdfplumber timed out or empty → using PyPDF2")

    # -------- Fallback to PyPDF2 --------
    try:
        text = extract_with_pypdf(path)
        if text:
            return text
    except:
        pass

    print("⚠️ PyPDF2 failed → returning empty text")
    return ""


# -------- Chunker (character-based) --------
def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    if not text or len(text.strip()) == 0:
        return [""]

    chunks = []
    start = 0
    length = len(text)

    while start < length:
        end = min(start + chunk_size, length)
        chunks.append(text[start:end])
        start = end - overlap

    return chunks
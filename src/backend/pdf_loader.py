# src/backend/pdf_loader.py
from typing import List
import PyPDF2
import os
from pathlib import Path
from dotenv import load_dotenv
import math

load_dotenv()

def extract_text_from_pdf(path: str) -> str:
    reader = PyPDF2.PdfReader(path)
    texts = []
    for page in reader.pages:
        texts.append(page.extract_text() or "")
    return "\n".join(texts)

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Simple whitespace chunker that attempts to not split words.
    """
    words = text.split()
    chunks = []
    i = 0
    n = len(words)
    while i < n:
        j = min(n, i + chunk_size)
        chunk = " ".join(words[i:j])
        chunks.append(chunk)
        i = j - overlap if j < n else j
    return chunks
# tests/test_retrieval.py
from src.backend.pdf_loader import chunk_text

def test_chunking():
    text = " ".join([str(i) for i in range(1000)])
    chunks = chunk_text(text, chunk_size=100, overlap=10)
    assert len(chunks) > 0
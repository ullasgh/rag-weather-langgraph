# src/backend/retriever.py
from typing import List
from .embeddings import VectorStore

vs = VectorStore()

def add_pdf_to_store(pdf_path: str, doc_id: str, chunk_size=500, overlap=50):
    from .pdf_loader import extract_text_from_pdf, chunk_text
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
    docs = []
    for i, c in enumerate(chunks):
        docs.append({
            "id": f"{doc_id}_{i}",
            "text": c,
            "metadata": {"source": pdf_path, "chunk": i}
        })
    vs.upsert_documents(docs)
    return len(docs)

def retrieve_for_question(question: str, k: int = 4):
    hits = vs.query(question, limit=k)
    contexts = [h["payload"]["text"] for h in hits if h["payload"] and "text" in h["payload"]]
    return contexts, hits
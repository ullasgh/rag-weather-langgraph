# tests/test_embeddings.py
import pytest
from src.backend.embeddings import VectorStore, COLLECTION_NAME
import uuid

def test_upsert_query_local():
    vs = VectorStore()
    doc_id = f"test_{uuid.uuid4().hex}"
    docs = [{"id": doc_id, "text": "Hello world. This is a test doc about pizza.", "metadata": {"topic": "pizza"}}]
    vs.upsert_documents(docs)
    hits = vs.query("pizza", limit=2)
    assert len(hits) >= 1
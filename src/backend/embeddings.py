# src/backend/embeddings.py
import os
from typing import List, Dict
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PayloadSchemaType
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings

load_dotenv()

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "pdf_docs")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

class VectorStore:
    def __init__(self):
        self.client = QdrantClient(url=f"http://{QDRANT_HOST}:{QDRANT_PORT}")
        # create collection if doesn't exist
        try:
            self.client.get_collection(COLLECTION_NAME)
        except Exception:
            self.client.recreate_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
            )
        self.embed = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    def upsert_documents(self, docs: List[Dict]):
        """
        docs: List of dicts { 'id': str, 'text': str, 'metadata': {...} }
        """
        vectors = []
        payloads = []
        ids = []
        for d in docs:
            emb = self.embed.embed_query(d["text"])
            vectors.append(emb)
            payloads.append({"text": d["text"], **(d.get("metadata") or {})})
            ids.append(d["id"])
        self.client.upsert(collection_name=COLLECTION_NAME, points=list(zip(ids, vectors, payloads)))

    def query(self, query_text: str, limit: int = 4):
        qv = self.embed.embed_query(query_text)
        hits = self.client.search(collection_name=COLLECTION_NAME, query_vector=qv, limit=limit)
        # normalized
        return [{"id": h.id, "score": h.score, "payload": h.payload} for h in hits]

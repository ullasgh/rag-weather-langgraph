# src/backend/embeddings.py
import os
import uuid
from typing import List, Dict
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from qdrant_client.http import models as qmodels
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()

COLLECTION_NAME = os.getenv("COLLECTION_NAME", "pdf_docs")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

# Default vector size for text-embedding-3-small is 1536
VECTOR_SIZE = 3072


class VectorStore:
    def __init__(self):
        # Run Qdrant fully in-memory (no Docker needed)
        self.client = QdrantClient(":memory:")

        # Create collection if missing
        try:
            self.client.get_collection(collection_name=COLLECTION_NAME)
        except Exception:
            self.client.recreate_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=VECTOR_SIZE,
                    distance=Distance.COSINE
                )
            )

        # OpenAI embeddings
        self.embed = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    def upsert_documents(self, docs: List[Dict]):
        """
        Upsert docs into Qdrant using proper PointStruct format.
        This is REQUIRED for in-memory mode.
        """
        points = []
        for d in docs:
            vec = self.embed.embed_query(d["text"])
            points.append(
                qmodels.PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vec,
                    payload={"text": d["text"], **(d.get("metadata") or {})}
                )
            )
    
        self.client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )

    def query(self, query_text: str, limit: int = 4):
        qv = self.embed.embed_query(query_text)
        hits = self.client.search(
            collection_name=COLLECTION_NAME,
            query_vector=qv,
            limit=limit
        )
        return [{"id": h.id, "score": h.score, "payload": h.payload} for h in hits]
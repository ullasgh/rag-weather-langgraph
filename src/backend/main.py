# src/backend/main.py
import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from .retriever import add_pdf_to_store
from .langgraph_node import decision_node
from dotenv import load_dotenv
import uuid

load_dotenv()

app = FastAPI(title="RAG + Weather Demo")

class AskReq(BaseModel):
    question: str

@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    contents = await file.read()
    tmp_dir = "/tmp/rag_uploads"
    os.makedirs(tmp_dir, exist_ok=True)
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    path = os.path.join(tmp_dir, filename)
    with open(path, "wb") as f:
        f.write(contents)
    count = add_pdf_to_store(path, doc_id=uuid.uuid4().hex)
    return {"status": "ok", "chunks_added": count, "path": path}

@app.post("/ask")
async def ask(req: AskReq):
    res = decision_node(req.question)
    return JSONResponse(content=res)

@app.get("/health")
async def health():
    return {"status": "ok"}
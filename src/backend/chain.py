# src/backend/chain.py
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from typing import List, Dict
from dotenv import load_dotenv
from .langsmith_logger import LangSmithLogger

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.0))

# LangSmith logger wrapper (no-op if not configured)
logger = LangSmithLogger()

def answer_with_pdf_context(question: str, contexts: List[str]) -> str:
    """
    Build a prompt combining top retrieved contexts and ask the LLM to answer.
    """
    chat = ChatOpenAI(model_name=MODEL_NAME, temperature=TEMPERATURE, openai_api_key=OPENAI_API_KEY)
    system = SystemMessage(content="You are a helpful, concise assistant that answers questions using the provided context. If the answer is not in the context, say so.")
    # Combine contexts
    combined = "\n\n---\n\n".join(contexts)
    human_content = f"Context:\n{combined}\n\nQuestion: {question}\n\nAnswer concisely and cite source chunk numbers if possible."
    human = HumanMessage(content=human_content)
    # Log request to LangSmith
    logger.log_request({"question": question, "contexts_count": len(contexts)})
    resp = chat([system, human])
    # Log response
    logger.log_response({"answer": resp.content})
    return resp.content
# src/backend/langsmith_logger.py
import os
try:
    from langsmith import Client as LangSmithClient
except Exception:
    LangSmithClient = None

class LangSmithLogger:
    def __init__(self):
        self.api_key = os.getenv("LANGSMITH_API_KEY")
        if self.api_key and LangSmithClient:
            self.client = LangSmithClient(api_key=self.api_key)
        else:
            self.client = None

    def log_request(self, meta: dict):
        if self.client:
            try:
                self.client.log_event({"type": "request", "meta": meta})
            except Exception:
                pass

    def log_response(self, meta: dict):
        if self.client:
            try:
                self.client.log_event({"type": "response", "meta": meta})
            except Exception:
                pass
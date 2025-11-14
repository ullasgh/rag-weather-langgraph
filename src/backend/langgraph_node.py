# src/backend/langgraph_node.py
from typing import Dict
import re
from .weather import fetch_current_weather_by_city
from .retriever import retrieve_for_question
from .chain import answer_with_pdf_context

WEATHER_KEYWORDS = ["weather", "temperature", "rain", "snow", "wind", "humidity", "forecast"]

def is_weather_question(question: str) -> bool:
    q = question.lower()
    # crude heuristic: mention city + weather keywords OR starts with what's the weather in / weather in
    if re.search(r"(what('?s| is) the weather in|weather in|forecast for|temperature in)", q):
        return True
    for kw in WEATHER_KEYWORDS:
        if kw in q:
            # ensure there's a location token nearby optionally
            return True
    return False

def decision_node(question: str) -> Dict:
    """
    Decision node that returns:
    {
        "route": "weather" or "pdf",
        "payload": ...
    }
    """
    if is_weather_question(question):
        # Extract possible city name (very naive) — user should be prompted for location if ambiguous
        # Try pattern 'in <City>'
        m = re.search(r"in\s+([A-Za-z\s,]+)", question.lower())
        city = None
        if m:
            city = m.group(1).strip().split()[0].title()
        if city is None:
            city = "London"  # fallback or you can raise prompt to user
        weather = fetch_current_weather_by_city(city)
        return {"route": "weather", "payload": weather}
    else:
        # Use RAG pipeline
        contexts, hits = retrieve_for_question(question)
        answer = answer_with_pdf_context(question, contexts)
        return {"route": "pdf", "payload": {"answer": answer, "hits": hits}}
# RAG + Weather Demo (LangChain + Qdrant + OpenAI + Streamlit)

## Overview
This project demonstrates a small agent pipeline that:
- fetches real-time weather via OpenWeather,
- answers questions about an uploaded PDF using Retrieval-Augmented Generation (RAG) with OpenAI embeddings stored in Qdrant,
- exposes a FastAPI backend and a Streamlit UI,
- logs (optionally) to LangSmith.

## Features
- LangGraph-compatible decision node (see `src/backend/langgraph_node.py`) that routes between weather API and PDF RAG.
- Embeddings stored in Qdrant (via `qdrant-client`).
- LLM via OpenAI (LangChain wrappers).
- Streamlit UI to showcase the chat interaction.

## Requirements
- Docker & docker-compose
- Python 3.11
- OpenAI API key
- OpenWeather API key (free tier available)
- (optional) LangSmith API key

## Quickstart (local)
1. Copy `.env.example` -> `.env` and fill the keys.
2. Start Qdrant:
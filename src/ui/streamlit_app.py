# src/ui/streamlit_app.py
import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="RAG + Weather Demo", layout="wide")

st.title("RAG + Weather Demo")

with st.sidebar:
    st.header("Upload & Index PDF")
    uploaded = st.file_uploader("Upload PDF to index", type=["pdf"])
    if uploaded:
        files = {"file": (uploaded.name, uploaded.getvalue(), "application/pdf")}
        resp = requests.post(f"{BACKEND_URL}/upload_pdf", files=files)
        if resp.ok:
            st.success(f"Indexed {resp.json().get('chunks_added')} chunks")
        else:
            st.error("Upload failed")

st.header("Ask a question")
question = st.text_input("Type a question (weather or about uploaded PDF)")

if st.button("Ask") and question:
    resp = requests.post(f"{BACKEND_URL}/ask", json={"question": question})
    if resp.ok:
        data = resp.json()
        route = data.get("route")
        st.subheader(f"Route: {route}")
        if route == "weather":
            payload = data.get("payload")
            st.write(f"**City**: {payload.get('city')}")
            st.write(f"**Weather**: {payload.get('weather')}")
            st.write(f"**Temp**: {payload.get('temp')} °C")
            st.json(payload.get("raw"))
        else:
            payload = data.get("payload")
            st.write("**Answer**")
            st.write(payload.get("answer"))
            st.write("**Source hits**")
            st.write(payload.get("hits"))
    else:
        st.error("Request failed")
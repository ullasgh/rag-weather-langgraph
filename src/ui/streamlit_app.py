# src/ui/streamlit_app.py

import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:9000")

st.set_page_config(page_title="RAG + Weather Demo", layout="wide")

st.title("RAG + Weather Demo")

# =========== SIDEBAR =============
with st.sidebar:
    st.header("Upload & Index PDF")

    uploaded = st.file_uploader("Choose PDF", type=["pdf"])
    
    # IMPORTANT: Only upload when button is clicked
    if uploaded and st.button("Upload PDF"):
        files = {"file": (uploaded.name, uploaded.getvalue(), "application/pdf")}
        try:
            resp = requests.post(f"{BACKEND_URL}/upload_pdf", files=files, timeout=60)
            if resp.ok:
                st.success(f"Indexed {resp.json().get('chunks_added')} chunks")
            else:
                st.error("Upload failed")
        except Exception as e:
            st.error(f"Error: {e}")

# =========== MAIN AREA ============
st.header("Ask a question")
question = st.text_input("Ask about weather or your PDF")

if st.button("Ask") and question:
    try:
        resp = requests.post(f"{BACKEND_URL}/ask", json={"question": question}, timeout=60)
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
                st.write("### Answer")
                st.write(payload.get("answer"))
                st.write("### Source hits")
                st.json(payload.get("hits"))
        else:
            st.error("Request failed")
    except Exception as e:
        st.error(f"Error: {e}")
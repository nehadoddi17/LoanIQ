import requests
import streamlit as st

API = "http://localhost:8000"
st.title("📄 Ask Your Docs (RAG)")

uploaded = st.file_uploader("Upload a PDF", type="pdf")
if uploaded and st.button("Ingest"):
    r = requests.post(f"{API}/upload", files={"file": (uploaded.name, uploaded.getvalue())})
    st.success(f"Ingested {r.json()['chunks']} chunks!")

question = st.text_input("Ask a question")
if st.button("Ask") and question:
    with st.spinner("Thinking..."):
        r = requests.post(f"{API}/ask", json={"question": question})
    st.write(r.json()["answer"])


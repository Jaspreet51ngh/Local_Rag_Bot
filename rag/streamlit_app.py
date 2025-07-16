import streamlit as st
import requests
import os
from io import StringIO

API_URL = "http://localhost:8000/ask"
UPLOAD_URL = "http://localhost:8000/upload"

# --- Custom CSS for modern look ---
st.markdown(
    """
    <style>
    body {background-color: #18122B;}
    .stApp {background: linear-gradient(135deg, #635985 0%, #18122B 100%); color: #F3F8FF;}
    .main-title {font-size: 2.8rem; font-weight: 800; color: #F3F8FF; margin-bottom: 0.5em;}
    .subtitle {font-size: 1.2rem; color: #A3C7D6; margin-bottom: 2em;}
    .upload-section {background: #393053; border-radius: 1em; padding: 1.5em; margin-bottom: 2em;}
    .question-section {background: #443C68; border-radius: 1em; padding: 1.5em;}
    .answer-section {background: #393053; border-radius: 1em; padding: 1.5em; margin-top: 2em;}
    .stButton>button {background-color: #A3C7D6; color: #18122B; font-weight: bold; border-radius: 0.5em;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">🦄 FastAPI RAG Bot Prototype</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload your documents and ask questions!<br>Modern, beautiful, and easy to use.</div>', unsafe_allow_html=True)

# --- Upload Section ---
st.markdown('<div class="upload-section">', unsafe_allow_html=True)
st.subheader("📤 Upload Document")
uploaded_file = st.file_uploader("Choose a .txt or .pdf file", type=["txt", "pdf"])

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if uploaded_file is not None:
    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
    response = requests.post(UPLOAD_URL, files=files)
    if response.status_code == 200:
        st.success(f"Uploaded and ingested: {uploaded_file.name}")
    else:
        st.error(f"Upload failed: {response.text}")
st.markdown('</div>', unsafe_allow_html=True)

# --- Model Selection ---
model_options = ["gemma", "llama3", "mistral"]
model_name = st.selectbox("Choose Ollama Model", model_options, index=0)

# --- Question/Answer Section ---
st.markdown('<div class="question-section">', unsafe_allow_html=True)
st.subheader("💬 Ask a Question")
question = st.text_input("Enter your question:", "What is artificial intelligence?")
ask = st.button("Ask")
st.markdown('</div>', unsafe_allow_html=True)

# --- Answer Section & Chat History ---
if ask and question.strip():
    with st.spinner("Thinking..."):
        payload = {"question": question, "model_name": model_name}
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            data = response.json()
            st.session_state.chat_history.clear()
            st.session_state.chat_history.append({
                "question": question,
                "answer": data["answer"],
                "sources": data["sources"],
                "processing_time": data["processing_time"]
            })
            st.rerun()
        else:
            st.error(f"Error: {response.status_code} - {response.text}")

# --- Main area chat history display ---
if st.session_state.chat_history:
    for entry in st.session_state.chat_history:
        st.markdown(f"**Q:** {entry['question']}")
        st.markdown(f"**A:** {entry['answer']}")
        if entry['sources']:
            st.markdown(f"**Sources:** {', '.join(entry['sources'])}")
        st.markdown("---")

# --- Sidebar for Chat History ---
with st.sidebar:
    st.title("🗂️ Chat History")
    if st.session_state.chat_history:
        for i, entry in enumerate(st.session_state.chat_history[::-1]):
            st.markdown(f"**Q{i+1}:** {entry['question']}")
            st.markdown(f"**A:** {entry['answer']}")
            st.markdown(f"**Sources:** {', '.join(entry['sources']) if entry['sources'] else 'N/A'}")
            st.markdown("---")
    else:
        st.info("No chat history yet.") 
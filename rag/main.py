import nltk.data
if not hasattr(nltk.data, 'load_orig'):
    nltk.data.load_orig = nltk.data.load
def patched_load(resource_name, *args, **kwargs):
    if 'punkt_tab' in resource_name:
        return nltk.data.load_orig('tokenizers/punkt', *args, **kwargs)
    return nltk.data.load_orig(resource_name, *args, **kwargs)
nltk.data.load = patched_load
from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from ragbot_fastapi.core.qa_engine import QAEngine, QAEngineConfig
from ragbot_fastapi.core.text_chunker import TextChunker
from ragbot_fastapi.core.embedding_service import EmbeddingService
from ragbot_fastapi.core.vector_store import VectorStore
import os
import PyPDF2

app = FastAPI(title="RAG Bot (FastAPI)")

qa_engine = QAEngine()
chunker = TextChunker()
embedder = EmbeddingService()
vector_store = VectorStore(db_path="ragbot_fastapi/vector_db")

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

class AskRequest(BaseModel):
    question: str
    model_name: str = None

class AskResponse(BaseModel):
    answer: str
    sources: list[str]
    processing_time: float
    context_used: str = None
    metadata: dict = None

@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI RAG Bot!"}

@app.post("/upload")
def upload_document(file: UploadFile = File(...)):
    os.makedirs("ragbot_fastapi/data", exist_ok=True)
    file_path = os.path.join("ragbot_fastapi/data", file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    # Extract text
    if file.filename.lower().endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    else:
        with open(file_path, "r", encoding="utf-8") as ftxt:
            text = ftxt.read()
    # Chunk, embed, and store
    doc = {"content": text, "file_name": file.filename, "file_path": file_path, "file_extension": file.filename.split('.')[-1]}
    chunks = chunker.chunk_by_section(doc)
    embeddings = embedder.generate_embeddings([c["content"] for c in chunks])
    vector_store.store_documents(chunks, embeddings)
    return {"filename": file.filename, "status": "uploaded and ingested"}

@app.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    result = qa_engine.ask_question(request.question, model_name=request.model_name)
    return AskResponse(
        answer=result.answer,
        sources=result.sources,
        processing_time=result.processing_time,
        context_used=result.context_used,
        metadata=result.metadata
    ) 
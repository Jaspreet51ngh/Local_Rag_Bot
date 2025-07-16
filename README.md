# Local RAG AI Assistant

A modular, fully local Retrieval-Augmented Generation (RAG) system for private document Q&A using LangChain and ChromaDB. Ingest and search your own documents (PDF, TXT, DOCX, PPTX, MD) with a modern, privacy-first chat interface.

## Output Demo Video

[Watch Demo](https://drive.google.com/file/d/1FTVVvOIg88dLJOFiuzKjN6NQqh_9TtXZ/view?usp=drive_link)

---

## Features

- **Local-first:** All processing and LLM inference run on your machine.
- **Multi-format ingestion:** PDF, TXT, DOCX, PPTX, Markdown.
- **Modular architecture:** Clean separation of ingestion, retrieval, QA, and UI.
- **Modern UI:** Streamlit-based chat interface.

## Getting Started

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the backend:
   ```bash
   uvicorn rag.main:app --reload
   ```
4. Run the UI:
   ```bash
   streamlit run rag/streamlit_app.py
   ```

## Project Structure

```
rag/
    main.py
    ...
tests/
    ...
data/
    sample_document.txt
demo.mp4
requirements.txt
README.md
setup.py
```

## License

MIT 

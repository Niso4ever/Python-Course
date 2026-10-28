# Project 1: Enterprise Knowledge Assistant (RAG Pipeline)

**The 2026 context:** Every company has moved its internal documentation, policies, and product knowledge into a RAG system. Employees and customers query it in plain English instead of searching PDFs. This is that system.

---

## What It Does

1. **Ingest** — reads your documents, splits them into chunks, embeds them into a vector database
2. **Retrieve** — when a user asks a question, finds the most relevant chunks
3. **Answer** — feeds those chunks to Claude, which answers grounded in your actual documents

No hallucination about your company's policies. If it's not in the docs, it says so.

---

## Architecture

```
Your Documents (PDF, TXT, MD)
       ↓  ingest.py
  Chunk + Embed
       ↓
  ChromaDB (local vector store)
       ↓  retriever.py
  similarity_search(question, k=4)
       ↓
  Top 4 chunks + question → Claude Sonnet 5.5
       ↓
  Grounded Answer
```

---

## Files

| File | What it does |
|:-----|:-------------|
| `ingest.py` | Load docs → split → embed → save to ChromaDB |
| `retriever.py` | Query ChromaDB → format context → ask Claude |
| `main.py` | Interactive Q&A loop with the knowledge base |
| `sample_data/knowledge_base.txt` | Sample company docs (AI startup, 2026) |

---

## Setup

```bash
cd Project1_RAG_Pipeline
pip install -r requirements.txt
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env

# Step 1: Ingest documents into vector DB
python ingest.py

# Step 2: Run the assistant
python main.py
```

---

## Demo Mode (No API Key)

```bash
python main.py --demo
```

Simulates the full pipeline showing chunk retrieval and answer generation.

---

## Extending This Project

- Replace `sample_data/` with your actual company docs (PDF, Word, HTML)
- Add more document loaders: `PyPDFLoader`, `UnstructuredHTMLLoader`
- Add streaming responses for real-time output
- Deploy as a web API with FastAPI
- Add source citations to every answer

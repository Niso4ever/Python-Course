"""
ingest.py — Load, split, embed, and store documents in ChromaDB.

Run this ONCE (or whenever your documents change):
    python ingest.py

What it does:
1. Reads documents from sample_data/
2. Splits them into overlapping chunks (preserves context at boundaries)
3. Creates embeddings using Anthropic-compatible embeddings
4. Stores everything in a local ChromaDB vector database

In 2026: This runs on a schedule (every 15 minutes) to keep the
knowledge base fresh as documents are added or updated.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── Configuration ────────────────────────────────────────────────
DOCS_DIR       = Path("./sample_data")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "company_knowledge")
CHUNK_SIZE     = 800    # characters per chunk
CHUNK_OVERLAP  = 150    # overlap between chunks (preserves context at edges)


def load_documents(docs_dir: Path) -> list[dict]:
    """
    Load all .txt, .md files from a directory.
    Returns list of {text, source, filename} dicts.

    In production: add PDF, Word, HTML loaders here.
    """
    documents = []
    for filepath in docs_dir.glob("**/*.txt"):
        text = filepath.read_text(encoding="utf-8")
        documents.append({
            "text":     text,
            "source":   str(filepath),
            "filename": filepath.name
        })

    for filepath in docs_dir.glob("**/*.md"):
        text = filepath.read_text(encoding="utf-8")
        documents.append({
            "text":     text,
            "source":   str(filepath),
            "filename": filepath.name
        })

    print(f"  Loaded {len(documents)} document(s) from {docs_dir}")
    return documents


def split_into_chunks(documents: list[dict]) -> list[dict]:
    """
    Split documents into overlapping chunks.
    Overlap prevents losing context when a sentence spans chunk boundaries.

    Example: chunk_size=800, overlap=150 means:
      Chunk 1: chars 0-800
      Chunk 2: chars 650-1450  ← 150-char overlap
      Chunk 3: chars 1300-2100
    """
    chunks = []
    for doc in documents:
        text = doc["text"]
        start = 0
        chunk_idx = 0

        while start < len(text):
            end  = start + CHUNK_SIZE
            chunk_text = text[start:end]

            # Skip very short chunks (likely whitespace/headers)
            if len(chunk_text.strip()) > 50:
                chunks.append({
                    "text":      chunk_text,
                    "source":    doc["source"],
                    "filename":  doc["filename"],
                    "chunk_idx": chunk_idx,
                    "id":        f"{doc['filename']}_chunk_{chunk_idx}"
                })
                chunk_idx += 1

            start += CHUNK_SIZE - CHUNK_OVERLAP  # slide window with overlap

    print(f"  Split into {len(chunks)} chunks "
          f"(size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")
    return chunks


def store_in_chromadb(chunks: list[dict], db_path: str, collection_name: str):
    """
    Store chunks in ChromaDB.
    ChromaDB handles embedding automatically (uses sentence-transformers by default).

    In production: use OpenAI text-embedding-3-large or Voyage AI's
    voyage-3 embeddings for better retrieval quality.
    """
    import chromadb

    # Initialize ChromaDB (local persistent storage)
    client     = chromadb.PersistentClient(path=db_path)

    # Delete existing collection to rebuild fresh
    try:
        client.delete_collection(collection_name)
        print(f"  Cleared existing collection: {collection_name}")
    except Exception:
        pass

    # Create fresh collection
    collection = client.create_collection(
        name=collection_name,
        # Default embedding: all-MiniLM-L6-v2 (fast, good quality)
        # For production, configure OpenAI or voyage embeddings here
    )

    # Add all chunks to collection
    collection.add(
        ids        = [chunk["id"] for chunk in chunks],
        documents  = [chunk["text"] for chunk in chunks],
        metadatas  = [{
            "source":    chunk["source"],
            "filename":  chunk["filename"],
            "chunk_idx": chunk["chunk_idx"]
        } for chunk in chunks]
    )

    print(f"  Stored {len(chunks)} chunks in ChromaDB at: {db_path}")
    print(f"  Collection: {collection_name}")
    return collection


def ingest(docs_dir: Path = DOCS_DIR, db_path: str = CHROMA_DB_PATH,
           collection_name: str = COLLECTION_NAME) -> int:
    """
    Full ingestion pipeline: load → split → embed → store.
    Returns number of chunks stored.
    """
    print("\n=== Nexus AI Knowledge Base Ingestion ===")
    print(f"Source: {docs_dir}")
    print(f"Database: {db_path}")
    print()

    # Step 1: Load
    print("Step 1: Loading documents...")
    documents = load_documents(docs_dir)
    if not documents:
        print("  ERROR: No documents found. Add .txt or .md files to sample_data/")
        return 0

    # Step 2: Split
    print("Step 2: Splitting into chunks...")
    chunks = split_into_chunks(documents)

    # Step 3: Store (ChromaDB embeds automatically)
    print("Step 3: Embedding and storing in ChromaDB...")
    store_in_chromadb(chunks, db_path, collection_name)

    print()
    print(f"✅ Ingestion complete. {len(chunks)} chunks ready for retrieval.")
    print(f"   Run `python main.py` to start the assistant.")
    return len(chunks)


if __name__ == "__main__":
    try:
        count = ingest()
        if count == 0:
            exit(1)
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Run: pip install -r requirements.txt")
        exit(1)

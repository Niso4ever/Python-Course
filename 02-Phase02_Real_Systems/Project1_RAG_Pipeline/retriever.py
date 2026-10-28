"""
retriever.py — Search the knowledge base and generate grounded answers.

Two main functions:
  - search(question) → returns top-k relevant chunks
  - answer(question) → retrieves context + asks Claude → returns answer with sources

In 2026: This module is the heart of every enterprise AI assistant.
The same pattern scales from 100 docs to 10 million docs.
"""

import os
from dotenv import load_dotenv

load_dotenv()

CHROMA_DB_PATH  = os.getenv("CHROMA_DB_PATH", "./chroma_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "company_knowledge")
RETRIEVAL_K     = 4       # number of chunks to retrieve per query
MODEL           = "claude-sonnet-5-5"   # main answer model
MAX_TOKENS      = 1500


SYSTEM_PROMPT = """You are the Nexus AI internal knowledge assistant.
You answer employee and customer questions using only the provided context from our knowledge base.

Rules:
1. Base your answer ONLY on the provided context — do not use general knowledge
2. If the answer is not in the context, say: "I don't have information about that in the knowledge base."
3. Be concise and specific — cite which section your answer comes from
4. Use plain language — avoid unnecessary jargon
5. If a question has multiple parts, address each part clearly

This is 2026. Employees expect precise, sourced answers, not vague responses."""


def get_collection():
    """Connect to ChromaDB and return the collection."""
    import chromadb
    client     = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_collection(COLLECTION_NAME)
    return collection


def search(question: str, k: int = RETRIEVAL_K) -> list[dict]:
    """
    Semantic search: find top-k chunks most relevant to the question.

    Returns list of {text, source, filename, chunk_idx, distance} dicts.
    Lower distance = more relevant.
    """
    collection = get_collection()
    results    = collection.query(
        query_texts=[question],
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )

    chunks = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        chunks.append({
            "text":      doc,
            "source":    meta.get("source", "unknown"),
            "filename":  meta.get("filename", "unknown"),
            "chunk_idx": meta.get("chunk_idx", 0),
            "distance":  round(dist, 4)   # 0 = identical, 2 = completely unrelated
        })

    return chunks


def format_context(chunks: list[dict]) -> str:
    """
    Format retrieved chunks into a clean context block for the LLM.
    Each chunk is labeled with its source for citation.
    """
    sections = []
    for i, chunk in enumerate(chunks, 1):
        sections.append(
            f"[Source {i}: {chunk['filename']}]\n{chunk['text'].strip()}"
        )
    return "\n\n---\n\n".join(sections)


def answer(question: str, verbose: bool = False) -> dict:
    """
    Full RAG pipeline: search → format context → ask Claude → return answer.

    Returns:
    {
        "answer":   str,          ← Claude's grounded answer
        "sources":  list[str],    ← source filenames used
        "chunks":   list[dict],   ← raw retrieved chunks (for debugging)
        "question": str           ← original question
    }
    """
    import anthropic

    # Step 1: Retrieve relevant chunks
    chunks = search(question, k=RETRIEVAL_K)

    if verbose:
        print(f"\n[RAG] Retrieved {len(chunks)} chunks:")
        for i, c in enumerate(chunks, 1):
            print(f"  {i}. [{c['filename']}] distance={c['distance']} | "
                  f"{c['text'][:60].strip()}...")

    # Step 2: Format context
    context = format_context(chunks)

    # Step 3: Ask Claude (grounded in context only)
    client = anthropic.Anthropic()
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": (
                f"Context from knowledge base:\n\n{context}\n\n"
                f"---\n\nQuestion: {question}"
            )
        }]
    )

    answer_text = response.content[0].text
    sources     = list({c["filename"] for c in chunks})   # unique filenames

    return {
        "answer":   answer_text,
        "sources":  sources,
        "chunks":   chunks,
        "question": question,
        "tokens":   {
            "input":  response.usage.input_tokens,
            "output": response.usage.output_tokens
        }
    }


def answer_demo(question: str) -> dict:
    """
    Demo mode: simulates retrieval and answer without API calls.
    Shows the RAG pipeline mechanics clearly.
    """
    # Simulate retrieval from knowledge base
    demo_chunks = [
        {
            "text": "Nexus AI is a B2B artificial intelligence platform founded in 2023, "
                    "headquartered in San Francisco. As of Q1 2026, Nexus AI serves over "
                    "1,200 enterprise customers with ARR of $180M.",
            "filename": "knowledge_base.txt",
            "distance": 0.18
        },
        {
            "text": "NexusRAG is our flagship product. It allows enterprises to connect their "
                    "internal documentation to large language models. Key features include "
                    "multi-modal ingestion, hybrid search, and citation tracking.",
            "filename": "knowledge_base.txt",
            "distance": 0.24
        }
    ]

    answer_text = (
        f"[DEMO MODE — No API call made]\n\n"
        f"Based on the retrieved context, here is a simulated answer to:\n"
        f"'{question}'\n\n"
        f"The knowledge base contains relevant information from {len(demo_chunks)} chunks. "
        f"In real mode, Claude Sonnet 5.5 would synthesize these into a grounded answer "
        f"with source citations."
    )

    return {
        "answer":   answer_text,
        "sources":  ["knowledge_base.txt"],
        "chunks":   demo_chunks,
        "question": question,
        "tokens":   {"input": 0, "output": 0}
    }

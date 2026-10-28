"""
TEMPLATE: RAG Pipeline
=======================
Use: End-to-end Retrieval-Augmented Generation

COPY this when you need to:
- Build a complete RAG system
- Chain search → format → generate
- Package the full flow into one function

2026 note: All functions use type hints.
  def fn(query: str, top_k: int = 3) -> list:  — same logic, adds type labels
"""

# ═══════════════════════════════════════════════════════════
# STEP FUNCTIONS (Build each step separately)
# ═══════════════════════════════════════════════════════════

def search_knowledge(query: str, knowledge_base: list, top_k: int = 3) -> list:
    """
    Step 1: Retrieve relevant documents.
    IN:  query (str), knowledge_base (list), top_k (int)
    OUT: list of top matching dicts
    """
    # ← MODIFY: Replace with your actual vector DB search
    # Example: results = vector_db.similarity_search(query, k=top_k)

    # Simulated search (replace this)
    results = sorted(
        knowledge_base,
        key=lambda x: x.get("score", 0),
        reverse=True
    )
    return results[:top_k]


def filter_results(docs: list, threshold: float = 0.75) -> list:
    """
    Step 1b: Keep only high-quality results.
    IN:  docs (list of dicts), threshold (float)
    OUT: filtered list
    """
    return [d for d in docs if d.get("score", 0) >= threshold]


def build_context(docs: list) -> str:
    """
    Step 2: Combine documents into context string.
    IN:  docs (list of dicts with 'text' key)
    OUT: context string
    """
    parts = []
    for i, doc in enumerate(docs, 1):
        source = doc.get("source", f"Source {i}")
        text   = doc.get("text", "")
        parts.append(f"[{source}]: {text}")
    return "\n\n".join(parts)


def format_prompt(question: str, context: str) -> str:
    """
    Step 3: Build the LLM prompt.
    IN:  question (str), context (str)
    OUT: formatted prompt string
    """
    return f"""Answer based on the context below.

Context:
{context}

Question: {question}

Answer:"""


def call_llm_mock(prompt: str) -> str:
    """
    Step 4: Call the LLM (REPLACE WITH REAL LLM).
    IN:  prompt (str)
    OUT: answer (str)
    """
    # ← MODIFY: Replace with real LLM call
    # Example with Anthropic:
    # response = client.messages.create(
    #     model="claude-sonnet-5-5",
    #     max_tokens=1000,
    #     messages=[{"role": "user", "content": prompt}]
    # )
    # return response.content[0].text

    return f"[Simulated LLM response to prompt of length {len(prompt)}]"


def package_result(question: str, answer: str, docs: list) -> dict:
    """
    Step 5: Package everything into structured output.
    IN:  question, answer, docs (list of dicts)
    OUT: result dict
    """
    return {
        "question": question,
        "answer": answer,
        "sources": [d.get("source", "Unknown") for d in docs],
        "doc_count": len(docs),
        "top_score": docs[0].get("score", 0) if docs else 0
    }


# ═══════════════════════════════════════════════════════════
# MAIN PIPELINE FUNCTION (One call, full flow)
# ═══════════════════════════════════════════════════════════
def rag_pipeline(user_question: str, knowledge_base: list, top_k: int = 3, threshold: float = 0.75) -> dict:
    """
    Complete RAG: Search → Filter → Format → Generate → Package.
    IN:  user_question (str), knowledge_base (list), top_k, threshold
    OUT: result dict with answer and metadata
    """
    print(f"→ Searching for: {user_question}")
    raw_docs = search_knowledge(user_question, knowledge_base, top_k)

    print(f"→ Filtering {len(raw_docs)} results (threshold={threshold})")
    filtered_docs = filter_results(raw_docs, threshold)

    if not filtered_docs:
        return {
            "question": user_question,
            "answer": "I don't have enough reliable information to answer that.",
            "sources": [],
            "doc_count": 0,
            "top_score": 0
        }

    print(f"→ Building context from {len(filtered_docs)} docs")
    context = build_context(filtered_docs)

    print(f"→ Formatting prompt")
    prompt  = format_prompt(user_question, context)

    print(f"→ Calling LLM")
    answer  = call_llm_mock(prompt)  # ← MODIFY: use real call_llm

    print(f"→ Packaging result")
    result  = package_result(user_question, answer, filtered_docs)

    return result


# ═══════════════════════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    # Sample knowledge base (← MODIFY: use your real data)
    knowledge_base = [
        {
            "text": "RAG combines retrieval with generation to ground LLM answers.",
            "source": "Wikipedia",
            "score": 0.95
        },
        {
            "text": "Vector databases store embeddings for semantic search.",
            "source": "ArXiv",
            "score": 0.88
        },
        {
            "text": "Semantic search finds similar meaning, not just keywords.",
            "source": "Blog",
            "score": 0.72
        },
        {
            "text": "Random unrelated document about cooking.",
            "source": "Forum",
            "score": 0.45
        }
    ]

    print("="*60)
    print("RAG PIPELINE DEMO")
    print("="*60)

    result = rag_pipeline("What is RAG?", knowledge_base)

    print("\n" + "="*60)
    print("RESULT:")
    print("="*60)
    print(f"Question:  {result['question']}")
    print(f"Answer:    {result['answer']}")
    print(f"Sources:   {', '.join(result['sources'])}")
    print(f"Doc Count: {result['doc_count']}")
    print(f"Top Score: {result['top_score']:.2f}")

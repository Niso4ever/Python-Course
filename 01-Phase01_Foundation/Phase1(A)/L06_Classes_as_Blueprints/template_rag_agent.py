"""
TEMPLATE: RAG Agent
=====================
Use: Retrieval-Augmented Generation agents with state tracking

COPY this when you need to:
- Build an agent that searches a database then generates answers
- Track query history and usage counts
- Filter results by confidence score
- Include source citations in answers

2026 NOTE: Three class styles shown in AI code.
  This file = standard class (has methods + memory).
  For config containers, see @dataclass pattern in CHEATSHEET_L06.py.
  For LLM output validation, see Pydantic BaseModel in CHEATSHEET_L06.py.
"""

# ═══════════════════════════════════════════════════════════
# TEMPLATE 1: Basic RAG Agent
# ═══════════════════════════════════════════════════════════
class RAGAgent:
    """
    Core RAG pattern: Retrieve → Format → Generate → Track.

    IN:  vector_db (object), llm_client (object), top_k (int)
    USE: agent.answer(question) → response (str)
    """
    def __init__(self, vector_db, llm_client, top_k=3):
        self.db         = vector_db     # Database connection
        self.llm        = llm_client    # LLM connection
        self.top_k      = top_k         # How many docs to retrieve
        self.call_count = 0             # Total answers generated
        self.queries    = []            # Log of all questions

    def answer(self, question):
        self.queries.append(question)
        self.call_count += 1

        # Step 1: Retrieve
        docs    = self.db.search(question, top_k=self.top_k)

        # Step 2: Format context
        context = "\n".join([d["text"] for d in docs])

        # Step 3: Build prompt
        prompt  = f"Context:\n{context}\n\nQuestion: {question}"

        # Step 4: Generate
        return self.llm.invoke(prompt)

    def get_usage(self):
        return {
            "total_queries": self.call_count,
            "queries":       self.queries
        }


# ═══════════════════════════════════════════════════════════
# TEMPLATE 2: RAG Agent with Confidence Filtering
# ═══════════════════════════════════════════════════════════
class ConfidentRAGAgent:
    """
    RAG agent that only uses high-confidence documents.
    Low-score documents are filtered before context building.

    IN:  vector_db, llm_client, top_k, threshold
    USE: agent.answer(question) → response (str)
    """
    def __init__(self, vector_db, llm_client, top_k=5, threshold=0.80):
        self.db          = vector_db
        self.llm         = llm_client
        self.top_k       = top_k
        self.threshold   = threshold    # Min score to use a doc
        self.call_count  = 0
        self.low_conf_count = 0         # Tracks how often we filter

    def _filter_docs(self, docs):
        """Keep only docs above confidence threshold."""
        good = [d for d in docs if d["score"] >= self.threshold]
        self.low_conf_count += len(docs) - len(good)
        return good

    def answer(self, question):
        self.call_count += 1

        # Step 1: Retrieve
        raw_docs  = self.db.search(question, top_k=self.top_k)

        # Step 2: Filter by confidence
        good_docs = self._filter_docs(raw_docs)

        # Step 3: Handle empty results
        if not good_docs:
            return "I don't have confident information to answer this."

        # Step 4: Build context and generate
        context = "\n".join([d["text"] for d in good_docs])
        prompt  = f"Context:\n{context}\n\nQuestion: {question}"
        return self.llm.invoke(prompt)

    def get_stats(self):
        return {
            "total_calls":      self.call_count,
            "docs_filtered":    self.low_conf_count,
            "threshold_used":   self.threshold
        }


# ═══════════════════════════════════════════════════════════
# TEMPLATE 3: RAG Agent with Source Citations
# ═══════════════════════════════════════════════════════════
class CitingRAGAgent:
    """
    RAG agent that includes source documents in the response.
    Returns structured dict with answer + sources.

    IN:  vector_db, llm_client, top_k
    USE: agent.answer(question) → dict {"answer": ..., "sources": [...]}
    """
    def __init__(self, vector_db, llm_client, top_k=3):
        self.db         = vector_db
        self.llm        = llm_client
        self.top_k      = top_k
        self.call_count = 0
        self.answers    = []            # Full answer history

    def answer(self, question):
        self.call_count += 1

        # Step 1: Retrieve docs
        docs    = self.db.search(question, top_k=self.top_k)

        # Step 2: Build context
        context = "\n".join([d["text"] for d in docs])

        # Step 3: Prompt with citation instruction
        prompt  = (
            f"Context:\n{context}\n\n"
            f"Question: {question}\n\n"
            f"Answer concisely, then list your sources."
        )

        # Step 4: Generate
        raw_answer = self.llm.invoke(prompt)

        # Step 5: Package result with sources
        sources = [
            {
                "source": d.get("source", "Unknown"),
                "score":  d.get("score", 0),
                "text":   d["text"][:100] + "..."
            }
            for d in docs
        ]

        result = {
            "question": question,
            "answer":   raw_answer,
            "sources":  sources,
            "doc_count": len(docs)
        }

        self.answers.append(result)
        return result

    def get_history(self):
        return self.answers


# ═══════════════════════════════════════════════════════════
# TEMPLATE 4: RAG Agent with Cost Tracking
# ═══════════════════════════════════════════════════════════
COST_PER_TOKEN = {
    "claude-sonnet-5-5":         {"input": 0.000002, "output": 0.00001},
    "claude-haiku-5-5":          {"input": 0.0000001, "output": 0.0000005},  # Haiku 5.5 rate for prompts up to 100k tokens; higher above
    "claude-opus-5-5":           {"input": 0.000004, "output": 0.00002},
}

class CostTrackingRAGAgent:
    """
    RAG agent that estimates and tracks API costs per query.

    IN:  vector_db, llm_client, model_name, top_k
    USE: agent.answer(question) → response (str)
    """
    def __init__(self, vector_db, llm_client, model_name="claude-sonnet-5-5", top_k=3):
        self.db         = vector_db
        self.llm        = llm_client
        self.model      = model_name
        self.top_k      = top_k
        self.call_count = 0
        self.total_cost = 0.0
        self.cost_log   = []            # Cost per query

    def _estimate_cost(self, prompt, response):
        """Estimate cost from character lengths (rough: 4 chars = 1 token)."""
        rates        = COST_PER_TOKEN.get(self.model, {"input": 0.000002, "output": 0.00001})
        input_tokens  = len(prompt) / 4
        output_tokens = len(response) / 4
        return round(input_tokens * rates["input"] + output_tokens * rates["output"], 6)

    def answer(self, question):
        self.call_count += 1

        # Retrieve and build prompt
        docs    = self.db.search(question, top_k=self.top_k)
        context = "\n".join([d["text"] for d in docs])
        prompt  = f"Context:\n{context}\n\nQuestion: {question}"

        # Generate
        response = self.llm.invoke(prompt)

        # Track cost
        call_cost = self._estimate_cost(prompt, str(response))
        self.total_cost += call_cost
        self.cost_log.append({
            "query":    question[:50],
            "cost_usd": call_cost
        })

        return response

    def get_cost_report(self):
        return {
            "total_calls":     self.call_count,
            "total_cost_usd":  round(self.total_cost, 6),
            "avg_cost_usd":    round(self.total_cost / max(self.call_count, 1), 6),
            "model":           self.model,
            "cost_log":        self.cost_log
        }


# ═══════════════════════════════════════════════════════════
# SIMULATED COMPONENTS (for demo — replace with real ones)
# ═══════════════════════════════════════════════════════════
class MockVectorDB:
    """Stand-in for a real vector database like Chroma or FAISS."""
    def search(self, query, top_k=3):
        return [
            {"text": f"Document about: {query} — section 1",
             "source": "doc_1.pdf", "score": 0.92},
            {"text": f"Document about: {query} — section 2",
             "source": "doc_2.pdf", "score": 0.85},
            {"text": f"Document about: {query} — section 3",
             "source": "doc_3.pdf", "score": 0.71},
        ][:top_k]


class MockLLM:
    """Stand-in for a real LLM client."""
    def invoke(self, prompt):
        return f"[Simulated answer based on {len(prompt)} chars of context]"


# ═══════════════════════════════════════════════════════════
# DEMO (runnable!)
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    db  = MockVectorDB()
    llm = MockLLM()

    print("=" * 60)
    print("TEMPLATE 1: Basic RAG Agent")
    print("=" * 60)
    rag = RAGAgent(db, llm, top_k=3)
    print(rag.answer("What is RAG?"))
    print(rag.answer("How does vector search work?"))
    print(f"Usage: {rag.get_usage()}")

    print("\n" + "=" * 60)
    print("TEMPLATE 2: Confidence Filtering (threshold=0.85)")
    print("=" * 60)
    conf_rag = ConfidentRAGAgent(db, llm, top_k=3, threshold=0.85)
    print(conf_rag.answer("What is embeddings?"))
    print(f"Stats: {conf_rag.get_stats()}")
    print("(1 doc filtered — score 0.71 < 0.85 threshold)")

    print("\n" + "=" * 60)
    print("TEMPLATE 3: With Source Citations")
    print("=" * 60)
    cite_rag = CitingRAGAgent(db, llm, top_k=2)
    result   = cite_rag.answer("What is a transformer?")
    print(f"Answer: {result['answer']}")
    print(f"Sources ({result['doc_count']} docs):")
    for s in result["sources"]:
        print(f"  [{s['score']:.2f}] {s['source']}: {s['text']}")

    print("\n" + "=" * 60)
    print("TEMPLATE 4: Cost Tracking Agent")
    print("=" * 60)
    cost_rag = CostTrackingRAGAgent(db, llm, model_name="claude-sonnet-5-5")
    cost_rag.answer("What is a neural network?")
    cost_rag.answer("Explain attention mechanisms.")
    cost_rag.answer("What is fine-tuning?")
    report = cost_rag.get_cost_report()
    print(f"Model:       {report['model']}")
    print(f"Total calls: {report['total_calls']}")
    print(f"Total cost:  ${report['total_cost_usd']:.6f}")
    print(f"Avg/call:    ${report['avg_cost_usd']:.6f}")

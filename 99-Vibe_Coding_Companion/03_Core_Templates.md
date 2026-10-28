# Core Templates (`01-Phase01_Foundation/Templates/`, 3 templates)

These are the reusable, course-wide reference files — including
`template_rag_pipeline.py`, called out in CLAUDE.md as *"the most important
single file in the course."* Reverse-engineering the RAG pipeline is the single
most valuable vibe prompt to internalize.

---

## 34. `template_metadata_storage.py`
**Level 3 (Contract) · Mode 2 (Specification)**

#### 📝 VIBE PROMPT
```
CONSTRAINTS: Dict key-value pattern. One canonical shape reused for every operation type.
REQUEST: A metadata shape that logs LLM calls, RAG retrievals, AND agent steps with the
         same structure — id, type, payload, success, cost, timestamp.
VALIDATION: One schema covers all three uses; safe .get() access; serializes to JSON.
```
#### 💻 PRODUCES (essence)
```python
operation = {"op_id": "op_001", "type": "llm_call",
             "payload": {...}, "success": True,
             "cost_usd": 0.02, "timestamp": "..."}
```

---

## 35. `template_rag_pipeline.py` ⭐ THE keystone file
**Level 3 (Contract) · Mode 5 (Integration)** — the prompt every Architect should own.

#### 📝 VIBE PROMPT
```
CONSTRAINTS: Five named stages, each its own function. Type hints throughout. DEMO runs dry.
REQUEST: An end-to-end RAG pipeline: user query → vector search → filter by relevance →
         format prompt with context → LLM generation → answer with citations.
VALIDATION:
  - query="" raises ValueError.
  - zero retrieved docs → graceful "I don't have enough information" fallback.
  - output is {answer, sources[], confidence}; sources are the docs actually used.
  - each stage is independently testable.
```
#### 💻 PRODUCES (essence)
```python
def rag_pipeline(query: str, top_k: int = 3) -> dict:
    hits = filter_by_score(vector_search(query, top_k), threshold=0.85)
    if not hits: return {"answer": FALLBACK, "sources": [], "confidence": 0.0}
    prompt = format_rag_prompt(query, hits)
    return {"answer": generate(prompt), "sources": [h["source"] for h in hits]}
```
> This is the Level-3 + Mode-5 combination at its purest: a named contract for
> every stage, assembled into one flow. 80% of AI apps are a variation of this prompt.

---

## 36. `template_rag_pipeline_clone.py`
**Level 4 (Test Cases) · Mode 3 (Iteration)** — the *refine an existing build* prompt.

#### 📝 VIBE PROMPT (a Surgical Edit, not a rebuild)
```
CONSTRAINTS: Keep template_rag_pipeline.py's structure EXACTLY. Change one thing only.
REQUEST: Clone the RAG pipeline but make the filter use .get("score", 0.0) for
         missing-key safety, and add a second re-ranking pass. Touch nothing else.
VALIDATION: Show me only the changed functions; every original test still passes.
```
#### 💻 PRODUCES (essence)
```python
# identical to template_rag_pipeline.py EXCEPT:
hits = [h for h in raw if h.get("score", 0.0) >= 0.85]   # ← safer access
hits = rerank(hits)                                      # ← added pass
```
> Two near-identical files exist on purpose: they demonstrate **Mode 3** — you
> iterate by cloning and surgically editing, not by re-prompting from scratch.

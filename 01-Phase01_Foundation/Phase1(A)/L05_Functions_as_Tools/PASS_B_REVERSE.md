# L05 — Path B: Functions as Tools in the RAG Pipeline

**Source file:** `01-Phase01_Foundation/Templates/template_rag_pipeline.py`

> **Metaphor:** The first 200 lines of the file are a single recipe written out step by step. Line 246 is the same recipe put into a reusable machine. You feed the machine a query; it returns an answer. The machine is the function.

---

## Where to find it

### 1. The function signature — its contract with the outside world (lines 246–252)
```python
def rag_pipeline(
    query: str,
    search_results: list,
    relevance_threshold: float = 0.85,
    require_verification: bool = True,
    max_context_docs: int = 3
) -> dict:
```
Inputs are named parameters. Defaults mean "use this if not told otherwise."

### 2. The docstring — what the LLM (and you) read to understand it (lines 253–266)
```python
"""
Complete RAG pipeline as a reusable function

Args:
    query: User's question
    search_results: List of dicts from vector search
    ...
Returns:
    Dict with 'answer', 'sources', 'metadata', 'success'
"""
```
The docstring IS the tool schema. Without it, the LLM can't call this function correctly.

### 3. The return value — the structured output (lines 294–308)
```python
return {
    "answer":   response,
    "sources":  [{"source": doc["source"], "score": doc["relevance_score"]} ...],
    "metadata": {"retrieved": ..., "filtered": ..., "used": ...},
    "success":  True
}
```
Always return a dict with consistent keys. The caller depends on this shape.

---

## Architect's question
> "If I change what this function returns, what breaks? The caller at line 294 expects 'answer', 'sources', 'metadata', 'success'. Change any of those keys and the caller breaks silently."

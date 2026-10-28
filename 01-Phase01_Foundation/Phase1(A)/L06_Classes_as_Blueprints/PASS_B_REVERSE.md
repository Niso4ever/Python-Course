# L06 — Path B: Classes as Blueprints in the RAG Pipeline

**Source file:** `01-Phase01_Foundation/Templates/template_rag_pipeline.py`

> **Metaphor:** The `rag_pipeline()` function is a recipe card. A class is the kitchen that uses that recipe every day — it holds the oven temperature (threshold), the pantry stock (vector DB connection), and the recipe itself (the method). You configure it once, then call it many times.

---

## Where to find it

The RAG pipeline **does not use a class** — and that is the lesson.

The function at line 246 works fine for one call. But notice what you'd need to repeat for every call:
- Pass `relevance_threshold=0.85` every time
- Pass `require_verification=True` every time
- Recreate the `search_results` connection every time

A class solves this. Here's what the pipeline looks like **after** applying L06:

```python
class RAGAgent:
    def __init__(self, threshold: float = 0.85, verify: bool = True):
        self.threshold = threshold          # configured once at creation
        self.verify    = verify

    def run(self, query: str, search_results: list) -> dict:
        # same logic as rag_pipeline(), but uses self.threshold
        ...
```

Now compare to `rag_pipeline(query, results, 0.85, True, 3)` — the class version is:
```python
agent = RAGAgent(threshold=0.85)     # configure once
agent.run(query1, results1)          # call many times, no repeated args
agent.run(query2, results2)
```

---

## Architect's question
> "What configuration is repeated on every call? That repetition is the signal to wrap the function in a class."

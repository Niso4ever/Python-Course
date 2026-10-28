# L02 — Path B: Lists & Collections in the RAG Pipeline

**Source file:** `01-Phase01_Foundation/Templates/template_rag_pipeline.py`

> **Metaphor:** The RAG pipeline is a conveyor belt. `raw_search_results` is the full belt coming in. `filtered_results` is the belt after the quality inspector removes bad parts. `context_docs` is the final tray — only the top 3 pieces.

---

## Where to find it

### 1. A list of dicts as the input collection (line 45)
```python
raw_search_results = [
    {"content": "...", "relevance_score": 0.947, ...},
    {"content": "...", "relevance_score": 0.923, ...},
    # ... 5 docs total
]
```
This is the standard shape for search results everywhere: **list of dicts**.

### 2. Build a list incrementally with `.append()` (lines 95, 108)
```python
filtered_results = []              # start empty
for doc in raw_search_results:
    if passes_quality_check:
        filtered_results.append(doc)   # add one at a time
```

### 3. Slice a list to take the top N (line 129)
```python
context_docs = filtered_results[:MAX_CONTEXT_DOCS]   # top 3 only
```

### 4. List comprehension — transform a list in one line (line 201)
```python
sources_used = [doc["source"] for doc in context_docs]
# → ["Wikipedia", "ArXiv Paper", "Internal Docs"]
```

### 5. Join a list into a single string (line 139)
```python
combined_context = "\n\n".join(context_parts)
```

---

## Architect's question
> "At each stage of the pipeline, how many items are in this list and why? Retrieval: 5 → Filter: 3 → Context: 3. If that count is wrong, the answer will be wrong."

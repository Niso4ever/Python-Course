# L04 — Path B: Loops & Iteration in the RAG Pipeline

**Source file:** `01-Phase01_Foundation/Templates/template_rag_pipeline.py`

> **Metaphor:** The pipeline runs the same inspection on every document that comes off the conveyor belt. A loop is the conveyor belt mechanism — it applies the same set of actions to every item in the collection.

---

## Where to find it

### 1. Filter loop — process every item, keep some (lines 98–112)
```python
for doc in raw_search_results:      # visit every document
    relevance = doc["relevance_score"]
    if passes_quality_check:
        filtered_results.append(doc)
```
This is the most common loop in AI pipelines: **iterate → test → collect**.

### 2. Build loop with index — when you need a position number (lines 133–136)
```python
for i, doc in enumerate(context_docs, start=1):
    context_part = f"[{doc['source']} #{i}] {doc['content']}"
    context_parts.append(context_part)
```
`enumerate` gives you `(position, item)` pairs. Use it when the order matters.

### 3. Print loop — iterate a dict's key-value pairs (line 212)
```python
for key, value in operation_metadata.items():
    print(f"  {key}: {value}")
```

### 4. List comprehension — loop in one line (lines 278–280, refactored version)
```python
context_parts = [
    f"[{doc['source']}] {doc['content']}"
    for doc in context_docs
]
```
Same as the build loop above, compressed. Both produce identical results.

---

## Architect's question
> "What is this loop visiting? What does it produce? A loop that visits 5 docs and appends 0 means your filter is wrong, not your loop."

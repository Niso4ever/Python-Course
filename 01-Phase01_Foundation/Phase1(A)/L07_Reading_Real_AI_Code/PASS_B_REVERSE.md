# L07 — Path B: Reading the Complete RAG Pipeline

**Source file:** `01-Phase01_Foundation/Templates/template_rag_pipeline.py`

> **Metaphor:** L07 is the graduation test. Path B is the whole curriculum. This file is the exam paper. Apply the 3-pass method to the RAG pipeline and you'll find every pattern from L01–L06 hiding in one place.

---

## Pass 1 — Recognition (read without running)

Scan for these patterns. Check each off when you spot it:

| Pattern | Where in the file | L lesson |
|---------|-------------------|----------|
| `variable = value` with typed values | Lines 31, 92–93 | L01 |
| Dict with typed fields (`str`, `float`, `bool`) | Lines 45–80 | L01 |
| `list = [...]` holding dicts | Line 45 | L02 |
| `.append()` to build a list | Lines 95–108 | L02 |
| `list[:N]` to slice | Line 129 | L02 |
| `[x for x in list if condition]` | Line 201, 278–280 | L02 |
| `if condition and condition:` | Line 107 | L03 |
| `value if condition else other` | Line 105 | L03 |
| `for item in collection:` | Lines 98, 133, 212 | L04 |
| `for i, item in enumerate(...):` | Line 133 | L04 |
| `def name(params) -> return_type:` | Line 246 | L05 |
| Docstring with Args/Returns | Lines 253–266 | L05 |
| `return {structured dict}` | Lines 294–308 | L05 |
| Repeated parameters → candidate for `__init__` | Lines 246–252 | L06 |

---

## Pass 2 — Evaluate (ask architect questions)

1. **Data contracts:** What shape does `rag_pipeline()` return? If a caller expects `result["answer"]` and the function changes that key, what breaks?
2. **Quality gates:** What score qualifies a document? Where would you raise or lower that threshold?
3. **Failure modes:** The "Red Flags" section (lines 320–360) lists 4 common mistakes. Which ones exist in the step-by-step version above the function?
4. **Class candidate:** Lines 246–252 repeat 5 configuration parameters. What would `RAGAgent.__init__` look like?

---

## Pass 3 — Use

You don't rewrite the pipeline. You direct AI to clone it:

```
[CONTEXT] I need a RAG pipeline for legal documents.
[CONSTRAINT] Clone the structural pattern from template_rag_pipeline.py exactly.
[CHANGE] Replace the relevance threshold with a recency filter (documents < 2 years old).
[KEEP] Return shape: {"answer", "sources", "metadata", "success"}
```

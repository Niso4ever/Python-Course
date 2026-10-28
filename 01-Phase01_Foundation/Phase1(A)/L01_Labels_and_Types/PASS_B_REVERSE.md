# L01 — Path B: Labels & Types in the RAG Pipeline

**Source file:** `01-Phase01_Foundation/Templates/template_rag_pipeline.py`

> **Metaphor:** Every drawer in a kitchen is labelled. The label tells you what's inside and what shape it is. In the RAG pipeline, every variable is a labelled drawer — `str`, `float`, `bool`, `int`, or `dict`.

---

## Where to find it

### 1. Scalar labels (line 31, 92–93)
```python
user_query          = "What is retrieval-augmented generation?"  # str
RELEVANCE_THRESHOLD = 0.85                                        # float
REQUIRE_VERIFICATION = True                                       # bool
MAX_CONTEXT_DOCS    = 3                                           # int
```
These four lines show all four basic types used as configuration knobs.

### 2. A dict as a structured label (lines 45–52, one document)
```python
{
    "content":         "RAG combines retrieval systems...",  # str
    "source":          "Wikipedia",                          # str
    "relevance_score": 0.947,                                # float
    "verified":        True,                                 # bool
    "doc_id":          "wiki_rag_001"                        # str
}
```
Each key is a label. Each value has a type. This is your data contract.

### 3. A nested dict (lines 188–214)
```python
operation_metadata = {
    "retrieval": {
        "total_retrieved": 5,       # int
        "relevance_threshold": 0.85 # float
    },
    "success": True                 # bool
}
```
Dicts can nest. The outer keys are category labels; the inner keys are detail labels.

---

## Architect's question
> "What type should this field be? If I get a `str` where I expected a `float`, where does the system break?"

# L03 — Path B: Logic Gates in the RAG Pipeline

**Source file:** `01-Phase01_Foundation/Templates/template_rag_pipeline.py`

> **Metaphor:** A bouncer at a club checks two things: "Is your score high enough? Are you on the verified list?" Only if BOTH are true do you get in. That's exactly the quality gate at the heart of the RAG pipeline.

---

## Where to find it

### 1. The core quality gate (lines 104–112)
```python
passes_relevance     = relevance >= RELEVANCE_THRESHOLD       # float comparison
passes_verification  = verified if REQUIRE_VERIFICATION else True

if passes_relevance and passes_verification:
    filtered_results.append(doc)          # let it through
else:
    reason = "low score" if not passes_relevance else "unverified"
```
Two conditions. Both must pass. This is a classic **confidence threshold + safety guard** combo.

### 2. Ternary gate — one-line if/else (line 105)
```python
passes_verification = verified if REQUIRE_VERIFICATION else True
#                     ↑ value if true    ↑ condition       ↑ value if false
```

### 3. Guardrail pattern from the Red Flags section (lines 332–337)
```python
# ❌ no guard:
context = results[0]["content"]    # crashes if results is empty

# ✅ with guard:
if not results:
    return "No relevant documents found"
```
Every potential failure point needs a gate before it.

---

## Architect's question
> "What happens when a document fails this gate? Is there a fallback, or does the pipeline silently get worse? Silence is the danger."

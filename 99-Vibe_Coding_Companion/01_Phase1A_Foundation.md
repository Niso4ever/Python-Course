# Phase 1A — Foundation Syntax (L01–L06, 21 templates)

These are the building blocks. Notice the pattern: **data shapes** (L01–L02)
are summoned at low Spec Levels, but the moment **logic** appears (L03+) you
climb to Level 3–4. Vague prompts make vague configs; precise prompts make
correct logic.

---

## L01 — Labels & Types (4 templates)

### 1. `template_agent_config.py`
**L01 · Level 3 (Contract) · Mode 2 (Specification)**

#### 📝 VIBE PROMPT
```
CONSTRAINTS: Plain dicts, no classes. Every key gets an inline comment with its unit/range.
REQUEST: Give me a RAG config dict (relevance threshold, max docs, model, temperature,
         fallback message) plus an agent-state dict that tracks current task + history.
VALIDATION: Thresholds are floats 0.0–1.0; appending a step to history must work.
```
#### 💻 PRODUCES (essence)
```python
rag_config = {"relevance_threshold": 0.85, "max_context_docs": 3,
              "model": "claude-opus-5-5", "temperature": 0.7,
              "enable_fallback": True,
              "fallback_message": "I don't have enough information to answer."}
```

### 2. `template_document_metadata.py`
**L01 · Level 3 (Contract) · Mode 2**

#### 📝 VIBE PROMPT
```
CONSTRAINTS: One dict per retrieved doc. Use a list-of-dicts for multiple results.
REQUEST: Metadata shape for one RAG search hit (doc_id, source, relevance_score,
         content, verified) and a filter that keeps only verified docs above 0.85.
VALIDATION: Filter must use .get() safety; empty results return [].
```
#### 💻 PRODUCES (essence)
```python
doc = {"doc_id": "doc_001", "source": "Wikipedia",
       "relevance_score": 0.95, "content": "...", "verified": True}
keep = [d for d in results if d["relevance_score"] >= 0.85 and d["verified"]]
```

### 3. `template_llm_metadata.py`
**L01 · Level 3 (Contract) · Mode 2**

#### 📝 VIBE PROMPT
```
CONSTRAINTS: One flat dict + one logging function with type hints.
REQUEST: A shape to log every LLM call — model, input/output tokens, latency_ms,
         cost_usd, success, timestamp — and a log_llm_call(prompt, response) helper.
VALIDATION: success is bool; error_message is None on success; function returns the dict.
```
#### 💻 PRODUCES (essence)
```python
def log_llm_call(prompt: str, response: str, model: str = "claude-opus-5-5") -> dict:
    return {"model": model, "tokens_total": len(prompt) + len(response),
            "success": True, "timestamp": "..."}
```

### 4. `template_structured_output.py`
**L01 · Level 4 (Test Cases) · Mode 2**

#### 📝 VIBE PROMPT
```
CONSTRAINTS: Prompt must say "Return ONLY valid JSON." Parse with json.loads + try/except.
REQUEST: A prompt template that forces the LLM into {abstract, bullet_points[]} JSON,
         plus a safe_parse() that validates required fields exist.
VALIDATION: Bad JSON returns None (not a crash); missing 'abstract' key returns None.
```
#### 💻 PRODUCES (essence)
```python
def safe_parse_llm_output(raw: str) -> dict | None:
    try:    p = json.loads(raw)
    except json.JSONDecodeError: return None
    return p if "abstract" in p and "bullet_points" in p else None
```

---

## L02 — Lists & Collections (2 templates)

### 5. `template_conversation_history.py`
**L02 · Level 2 (Behavior) · Mode 2**

#### 📝 VIBE PROMPT
```
CONSTRAINTS: Messages are {role, content} dicts in a growing list. No DB.
REQUEST: Helpers to add user/assistant turns and return the full list (optionally
         prefixed with a system prompt) to send to the LLM each turn.
VALIDATION: The whole list is re-sent every turn (that's "memory"); add a last-N trimmer.
```
#### 💻 PRODUCES (essence)
```python
def add_user_message(conv, text):
    conv.append({"role": "user", "content": text}); return conv
def get_recent_messages(conv, max_messages=10):
    return conv[-max_messages:] if len(conv) > max_messages else conv
```

### 6. `template_list_operations.py`
**L02 · Level 1 (Features) · Mode 1 (Exploration)**

#### 📝 VIBE PROMPT
```
CONSTRAINTS: Pure standard library. One short, labeled block per pattern.
REQUEST: Show me the 10 list patterns an AI system actually uses — results storage,
         filtering by score, token sums, ranking top-N, error collection.
VALIDATION: Each block runs standalone; include the common-mistakes anti-patterns.
```
#### 💻 PRODUCES (essence)
```python
results.sort(key=lambda x: x["score"], reverse=True)   # rank
top3 = results[:3]                                      # top-N
total = sum(token_log)                                  # usage
keep = [r for r in all_results if r["score"] >= 0.85]   # filter
```

---

## L03 — Logic Gates (5 templates)

> All five are **Level 4 (Test Cases)** — logic is where you specify edge cases
> or pay for them later. Mode 2 (Specification).

### 7. `template_confidence_threshold.py`
#### 📝 VIBE PROMPT
```
CONSTRAINTS: if/elif/else (numeric comparison — NOT match/case).
REQUEST: A quality gate: score ≥ 0.85 → return; 0.6–0.85 → return with disclaimer;
         below → fall back to "not confident enough."
VALIDATION: score=0.85 passes (inclusive); score=0.0 hits fallback; no score crashes.
```
#### 💻 PRODUCES (essence)
```python
if confidence >= 0.85:   return answer
elif confidence >= 0.6:  return answer + " (low confidence)"
else:                    return FALLBACK_MESSAGE
```

### 8. `template_fallback_chains.py`
#### 📝 VIBE PROMPT
```
CONSTRAINTS: if/elif on boolean availability. Always end with a guaranteed default.
REQUEST: Try primary source → backup source → cached → hardcoded default, in order.
VALIDATION: If all upstreams are down, the default still returns (never raises).
```
#### 💻 PRODUCES (essence)
```python
if primary_available:   data = get_primary()
elif backup_available:  data = get_backup()
else:                   data = DEFAULT_RESPONSE
```

### 9. `template_intent_routing.py`
#### 📝 VIBE PROMPT
```
CONSTRAINTS: Show BOTH if/elif AND match/case. match/case is the 2026-preferred
             form for routing by NAME.
REQUEST: Route a classified intent ("search"/"summarize"/"calculate") to its handler.
VALIDATION: An unknown intent hits the default branch, not a KeyError.
```
#### 💻 PRODUCES (essence)
```python
match intent:
    case "search":    return search_tool(query)
    case "summarize": return summarize_tool(query)
    case _:           return "I can't handle that request."
```

### 10. `template_safety_guards.py`
#### 📝 VIBE PROMPT
```
CONSTRAINTS: if/elif on thresholds + boolean flags. Guards run BEFORE any LLM call.
REQUEST: Block content that fails moderation, exceeds rate limit, or lacks authorization.
VALIDATION: A blocked request returns a refusal + reason; never reaches the model.
```
#### 💻 PRODUCES (essence)
```python
if toxicity_score > 0.7:        return block("unsafe content")
elif calls_this_minute > 60:    return block("rate limit")
elif not user_authorized:       return block("unauthorized")
```

### 11. `template_source_validation.py`
#### 📝 VIBE PROMPT
```
CONSTRAINTS: Show if/elif AND match/case (routing by source NAME). Assign trust levels.
REQUEST: Map each RAG source to a trust tier and attach a disclaimer for low-trust ones.
VALIDATION: Unknown source defaults to lowest trust + strongest disclaimer.
```
#### 💻 PRODUCES (essence)
```python
match source:
    case "internal_kb" | "official_docs": trust = "high"
    case "wikipedia" | "arxiv":           trust = "medium"
    case _:                               trust = "low"
```

---

## L04 — Loops & Iteration (3 templates)

> All **Level 3 (Contract) · Mode 2** — name the input list, the key, and the output.

### 12. `template_count_sum.py`
#### 📝 VIBE PROMPT
```
CONSTRAINTS: One for-loop accumulator. Handle the empty-list case (avg → 0.0).
REQUEST: Sum tokens and compute average cost across a list of call dicts.
VALIDATION: Empty list returns total=0, avg=0.0 (no ZeroDivisionError).
```
#### 💻 PRODUCES (essence)
```python
total = 0
for call in calls: total += call["tokens"]
avg = total / len(calls) if calls else 0.0
```

### 13. `template_filter_collection.py`
#### 📝 VIBE PROMPT
```
CONSTRAINTS: Build a NEW list (never mutate while looping). Configurable threshold.
REQUEST: Keep only RAG results whose score ≥ threshold AND are verified.
VALIDATION: Original list is untouched; below-threshold items are excluded.
```
#### 💻 PRODUCES (essence)
```python
kept = []
for r in results:
    if r["score"] >= THRESHOLD and r["verified"]:
        kept.append(r)
```

### 14. `template_find_first.py`
#### 📝 VIBE PROMPT
```
CONSTRAINTS: Early-exit loop (break/return on first hit). Return None if no match.
REQUEST: Return the first result above the confidence bar, then stop scanning.
VALIDATION: No match → None; first qualifying item short-circuits the rest.
```
#### 💻 PRODUCES (essence)
```python
for r in results:
    if r["score"] >= 0.9:
        return r          # stop immediately
return None
```

---

## L05 — Functions as Tools (3 templates)

> **Level 3 (Contract) · Mode 2** — the Architect's sweet spot. Specify signatures.

### 15. `template_llm_caller.py`
#### 📝 VIBE PROMPT
```
CONSTRAINTS: Type hints on every function. DEMO_MODE returns canned text, no key needed.
REQUEST: Reusable call_llm(prompt, model) -> str, plus a token cost estimator.
VALIDATION: Demo path makes zero network calls; signature is JSON-compatible types.
```
#### 💻 PRODUCES (essence)
```python
def call_llm(prompt: str, model: str = "claude-opus-5-5") -> str:
    if DEMO_MODE: return f"[demo reply to: {prompt[:30]}]"
    ...  # real Anthropic call
```

### 16. `template_prompt_formatter.py`
#### 📝 VIBE PROMPT
```
CONSTRAINTS: Pure string assembly. No LLM call inside. Type-hinted.
REQUEST: format_rag_prompt(question, context_docs) that stitches system + context + Q.
VALIDATION: Empty context still produces a valid prompt; sources are clearly delimited.
```
#### 💻 PRODUCES (essence)
```python
def format_rag_prompt(question: str, docs: list) -> str:
    context = "\n".join(d["content"] for d in docs)
    return f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
```

### 17. `template_rag_pipeline.py` (L05 version)
**Mode 5 (Integration)** — wires the three functions above into one flow.
#### 📝 VIBE PROMPT
```
CONSTRAINTS: Reuse search + format_rag_prompt + call_llm. One orchestration function.
REQUEST: rag_pipeline(query, top_k) that searches → filters → formats → generates.
VALIDATION: Each stage is a named function; the pipeline returns answer + sources used.
```
#### 💻 PRODUCES (essence)
```python
def rag_pipeline(query: str, top_k: int = 3) -> dict:
    hits = search(query, top_k)
    prompt = format_rag_prompt(query, hits)
    return {"answer": call_llm(prompt), "sources": [h["source"] for h in hits]}
```

---

## L06 — Classes as Blueprints (4 templates)

> **Level 3 (Contract) · Mode 2** — now state lives inside an object.

### 0. `template_ai_agent_anatomy.py` (L06 Part 0)
**Pattern:** L06 Part 0 · **Level 2 (Behavior)** · **Mode 1 (Exploration)**

Source: `01-Phase01_Foundation/Phase1(A)/L06_Classes_as_Blueprints/template_ai_agent_anatomy.py`

#### 📝 THE VIBE PROMPT
```
CONSTRAINTS:
  Standard library only. One single class. Add a comment label on EVERY
  OOP concept as it appears (class, __init__, attribute, method, self, instance).

REQUEST:
  Build one teaching Agent class where I can watch its state change as I call
  methods. It should hold a name + history, have a method that does work and
  appends to history, and a method that prints its current state.

VALIDATION:
  - Creating two agents proves they are independent (separate state).
  - Calling a method visibly mutates that instance's history.
  - Running the file top-to-bottom narrates what each concept is.
```

#### 💻 THE CODE IT PRODUCES (essence)
```python
class Agent:                       # ← class (the blueprint)
    def __init__(self, name):      # ← constructor
        self.name = name           # ← attribute (state)
        self.history = []          # ← state that will grow
    def act(self, task):           # ← method (behavior)
        self.history.append(task)  # ← self mutates THIS instance
```
> Two `Agent(...)` instances never share `history` — that's the whole lesson.

---

### 18. `template_conversation_agent.py`
#### 📝 VIBE PROMPT
```
CONSTRAINTS: Standard class with __init__ holding history + system prompt. Type hints.
REQUEST: A ConversationAgent with .chat(message) that appends turns and returns a reply.
VALIDATION: Two agents keep separate history; turn count increments per .chat().
```
#### 💻 PRODUCES (essence)
```python
class ConversationAgent:
    def __init__(self, persona: str):
        self.history, self.persona = [], persona
    def chat(self, msg: str) -> str:
        self.history.append({"role": "user", "content": msg}); ...
```

### 19. `template_multi_tool_agent.py`
#### 📝 VIBE PROMPT
```
CONSTRAINTS: A tool registry (dict name→callable). Model tier selectable. Type hints.
REQUEST: An agent that routes a request to one of several registered tools, with a
         fallback chain (try A → B → C).
VALIDATION: Unknown tool name → graceful fallback, not KeyError; tools are pluggable.
```
#### 💻 PRODUCES (essence)
```python
class MultiToolAgent:
    def __init__(self): self.tools = {"search": search, "summarize": summarize}
    def run(self, name: str, arg: str) -> str:
        return self.tools.get(name, self._fallback)(arg)
```

### 20. `template_rag_agent.py`
#### 📝 VIBE PROMPT
```
CONSTRAINTS: Class holds a vector store handle + query history. Confidence filter built in.
REQUEST: A RAGAgent.ask(question) that searches, filters by score, generates, and
         returns the answer WITH source citations.
VALIDATION: Below-threshold hits are dropped; answer always lists which sources it used.
```
#### 💻 PRODUCES (essence)
```python
class RAGAgent:
    def ask(self, question: str) -> dict:
        hits = [h for h in self.search(question) if h["score"] >= self.min_score]
        return {"answer": self.generate(question, hits),
                "sources": [h["source"] for h in hits]}
```

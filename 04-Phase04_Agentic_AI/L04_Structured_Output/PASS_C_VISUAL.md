# Lesson 20 — Pass C: VISUAL PATTERNS
## See How Schemas Become Typed Objects

**Goal:** Visualize the flow from Pydantic model definition → tool schema → forced LLM response → typed Python object.


> **Update (2026-10-28): native structured outputs replaced the `tool_choice` trick.**
> `client.messages.parse(model=..., max_tokens=..., messages=..., output_format=MyModel)` returns
> `response.parsed_output`, already a validated `MyModel` instance. It is GA (no beta header) on every current model.
> The forced-tool pattern taught below (`tool_choice={"type": "tool", "name": ...}` or `{"type": "any"}`)
> **returns a 400 error on claude-opus-5-5, claude-sonnet-5-5 and claude-fable-5-1**. Keep recognising it, because
> older code is full of it, but write new code with `messages.parse`. If you need a tool call with schema-exact
> arguments, use `tool_choice={"type": "auto"}` plus `"strict": True` on the tool.
> Sources: platform.claude.com/docs/en/build-with-claude/structured-outputs and
> platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools#forcing-tool-use.

---

## Visual 1: From Python Class to JSON Schema

### Code:
```python
from pydantic import BaseModel

class SearchResult(BaseModel):
    query: str
    results: list[str]
    confidence: float
    found: bool
```

**Example call:**
```python
print(SearchResult.model_json_schema())
# {
#   "title": "SearchResult",
#   "type": "object",
#   "properties": {
#     "query":      {"type": "string"},
#     "results":    {"type": "array", "items": {"type": "string"}},
#     "confidence": {"type": "number"},
#     "found":      {"type": "boolean"}
#   },
#   "required": ["query", "results", "confidence", "found"]
# }
```

### Visual — Pydantic field → JSON schema field:
```
Python class:              JSON schema:
─────────────────────────────────────────────────
query: str         →    "query": {"type": "string"}
results: list[str] →    "results": {"type": "array", "items": {"type": "string"}}
confidence: float  →    "confidence": {"type": "number"}
found: bool        →    "found": {"type": "boolean"}
= []  (default)    →    not in "required" list
```

**Pattern:** Pydantic reads your type hints and generates the JSON schema automatically.

---

## Visual 2: The Full Structured Output Flow

### Code:
```python
class PersonInfo(BaseModel):
    name: str
    age: int

tool = {"name": "PersonInfo", "description": "Extract.", "input_schema": PersonInfo.model_json_schema()}
response = client.messages.create(tools=[tool], tool_choice={"type": "tool", "name": "PersonInfo"}, messages=messages)
person = PersonInfo(**response.content[0].input)
```

**Example call:**
```python
messages = [{"role": "user", "content": "Extract info: Jane Doe is 28 years old."}]
person = PersonInfo(**response.content[0].input)
print(person.name)  # "Jane Doe"
print(person.age)   # 28
```

### Visual — End to end:
```
YOU DEFINE:
  class PersonInfo(BaseModel):
      name: str
      age: int
              │
              ▼ .model_json_schema()
              │
TOOL SCHEMA:
  {"name": "PersonInfo",
   "input_schema": {"properties": {"name": {..}, "age": {..}}}}
              │
              ▼ tools=[tool], tool_choice={"type":"tool","name":"PersonInfo"}
              │
LLM FILLS IN:
  ToolUseBlock(
    name="PersonInfo",
    input={"name": "Jane Doe", "age": 28}
  )
              │
              ▼ PersonInfo(**response.content[0].input)
              │
TYPED OBJECT:
  person.name  = "Jane Doe"   ← str
  person.age   = 28           ← int (not "28"!)
```

**Pattern:** Define → Schema → Force → Parse → Typed Object.

---

## Visual 3: The Evaluator Pattern (Quality Gate)

### Code:
```python
class QualityGate(BaseModel):
    passes: bool
    score: float
    action: str   # "accept" | "retry" | "escalate"
```

**Example call:**
```python
gate = evaluate_response("What is RAG?", "RAG is a thing.")
print(gate.passes)  # False
print(gate.action)  # "retry"
# → triggers regenerate_answer() automatically
```

### Visual — Pipeline with quality gate:
```
User Question
      │
      ▼
┌─────────────┐
│  Generate   │ ← agent produces an answer
│  Answer     │
└─────────────┘
      │
      ▼  answer
┌─────────────────────┐
│  QUALITY GATE       │ ← second LLM call, structured output forced
│  (Structured Output)│
│                     │
│  passes: bool       │
│  score: 0.0–1.0     │
│  action: str        │
└─────────────────────┘
      │
  ┌───┴───────────┐
  │               │
passes?          fails?
  │               │
  ▼               ▼
Return        action?
answer          │
            ┌───┴───┐
            │       │
         "retry" "escalate"
            │       │
         Regenerate  Human
```

**Pattern:** First LLM generates, second LLM evaluates → structured gate controls routing.

---

## Visual 4: Optional vs Required Fields

```python
from pydantic import BaseModel
from typing import Optional

class RAGResponse(BaseModel):
    answer: str                    # REQUIRED — must always be provided
    confidence: float              # REQUIRED — must always be provided
    sources: list[str] = []        # OPTIONAL — default empty list
    follow_up: Optional[str] = None   # OPTIONAL — default None
    needs_human: bool = False      # OPTIONAL — default False
```

**Example calls:**
```python
# LLM provides only required fields:
r = RAGResponse(answer="RAG combines...", confidence=0.9)
print(r.sources)      # []     (default)
print(r.follow_up)    # None   (default)
print(r.needs_human)  # False  (default)

# LLM provides all fields:
r = RAGResponse(answer="RAG combines...", confidence=0.9,
                sources=["wiki", "arxiv"], follow_up="Want examples?", needs_human=False)
print(r.follow_up)    # "Want examples?"
```

### Visual:
```
field: str              → in "required" list  → LLM MUST fill in
field: str = "default"  → NOT in "required"   → LLM can skip
field: Optional[str]    → NOT in "required"   → LLM can return null
```

---

## Visual 5: Nested Models

```python
class Source(BaseModel):
    title: str
    score: float

class Report(BaseModel):
    summary: str
    sources: list[Source]    # ← nested model
```

**Example call:**
```python
report = Report(
    summary="AI in healthcare is growing.",
    sources=[
        Source(title="NEJM Study", score=0.95),
        Source(title="ArXiv Paper", score=0.88)
    ]
)
print(report.sources[0].title)  # "NEJM Study"
print(report.sources[1].score)  # 0.88
```

### Visual — Schema nesting:
```
Report
├── summary: str
└── sources: list[Source]
              └── Source
                  ├── title: str
                  └── score: float

JSON schema:
{
  "properties": {
    "summary": {"type": "string"},
    "sources": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/Source"      ← nested schema reference
      }
    }
  },
  "$defs": {
    "Source": {
      "properties": {"title": {...}, "score": {...}}
    }
  }
}
```

**Pattern:** Pydantic handles nested schemas automatically. You just write Python classes.

---

## Visual 6: tool_choice vs No tool_choice

```
WITH tool_choice={"type":"tool","name":"X"}:
  response.stop_reason = "tool_use"   (always)
  response.content[0].type = "tool_use"
  response.content[0].input = {"field1": "...", "field2": 42}  ← the structured data

WITHOUT tool_choice:
  response.stop_reason = "end_turn"   (usually)
  response.content[0].type = "text"
  response.content[0].text = "Here are the results:\n..."  ← free text (unpredictable)
```

**Visual:**
```
tool_choice forced:           No tool_choice:
┌───────────────────┐         ┌───────────────────┐
│  PREDICTABLE      │         │  UNPREDICTABLE    │
│  Always tool_use  │         │  May be text      │
│  Always all fields│         │  May skip fields  │
│  Typed values     │         │  All strings      │
└───────────────────┘         └───────────────────┘
         ↓                              ↓
   Pydantic object              json.loads() or regex
   (reliable)                   (fragile)
```

**Pattern:** a schema the API enforces beats prompting for JSON. Today that is `messages.parse(output_format=...)`; on older models it was forced `tool_choice` (now a 400 on Opus 5.5 / Sonnet 5.5 / Fable 5.1).

---

## You've Completed Pass C!

You can now:
✓ **Visualize** Pydantic fields → JSON schema fields
✓ **See** the full flow: define → schema → force → parse → typed object
✓ **Understand** the evaluator-as-gate pattern
✓ **Map** required vs optional to the "required" array
✓ **See** why an enforced schema (`messages.parse`, or forced `tool_choice` on older models) beats prompting for JSON
✓ **Read** nested Pydantic models as nested schemas

**Next:** Pass 3 — Copy structured output templates for extractors, evaluators, and result packagers.

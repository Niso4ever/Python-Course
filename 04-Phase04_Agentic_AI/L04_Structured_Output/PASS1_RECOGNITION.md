# Lesson 20 — Pass 1: RECOGNITION
## Learn to SEE Structured Output Patterns

**Goal:** Recognize how LLM responses are forced into typed Python objects — using Pydantic and direct API features — without any output parser framework.

> **2026 Note:** LangChain's `PydanticOutputParser` and similar tools parse LLM text after the fact and often break. The 2026 pattern has the API fill in a schema directly — using `client.messages.parse(output_format=...)`; older code used forced `tool_choice`. The result is a Python object, not text to parse. No regex, no retry logic.


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

## The Three Shapes of Structured Output

### Shape 1: Pydantic Model (the schema)
```python
from pydantic import BaseModel

class SearchResult(BaseModel):
    query: str
    results: list[str]
    confidence: float
    found: bool
```
**Recognize:** Class inherits from `BaseModel`. Fields with type annotations. No `__init__`, no methods needed.

---

### Shape 2: Schema as a Tool (the trick)
```python
# Convert Pydantic model to tool schema
extract_tool = {
    "name": "SearchResult",
    "description": "Extract search results in structured format.",
    "input_schema": SearchResult.model_json_schema()   # ← Pydantic generates the JSON schema
}

# Force LLM to fill it in
response = client.messages.create(
    tools=[extract_tool],
    tool_choice={"type": "tool", "name": "SearchResult"},  # ← forced
    messages=messages
)
```
**Recognize:** `model_json_schema()` + `tool_choice={"type": "tool", ...}`.

---

### Shape 3: Parsing the Result
```python
# The LLM fills in the schema as a tool_use block
tool_block = response.content[0]    # first block (always tool_use when forced)
data = tool_block.input             # ← dict with all the fields filled in

# Convert to typed Pydantic object
result = SearchResult(**data)       # or SearchResult.model_validate(data)
print(result.confidence)            # 0.92 — typed float, not a string
print(result.found)                 # True — typed bool
```
**Recognize:** `tool_block.input` → `MyModel(**data)` or `MyModel.model_validate(data)`.

---

## Real Examples to RECOGNIZE (Don't Write, Just Read)

### Example 1: Simple Data Extraction

```python
from pydantic import BaseModel
import anthropic

client = anthropic.Anthropic()

class PersonInfo(BaseModel):
    name: str
    age: int
    occupation: str
    city: str

# Build the tool from the Pydantic model
extract_person = {
    "name": "PersonInfo",
    "description": "Extract person information from text.",
    "input_schema": PersonInfo.model_json_schema()
}

text = "John Smith is a 34-year-old software engineer living in San Francisco."

response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=[extract_person],
    tool_choice={"type": "tool", "name": "PersonInfo"},   # ← force extraction
    messages=[{"role": "user", "content": f"Extract person info from: {text}"}]
)

person = PersonInfo(**response.content[0].input)
print(person.name)        # "John Smith"
print(person.age)         # 34            ← typed int, not "34"
print(person.occupation)  # "software engineer"
print(person.city)        # "San Francisco"
```

**RECOGNIZE THIS:**
- `PersonInfo(BaseModel)` ← Pydantic schema
- `PersonInfo.model_json_schema()` ← converts to JSON schema automatically
- `tool_choice={"type": "tool", "name": "PersonInfo"}` ← LLM MUST fill this schema
- `PersonInfo(**response.content[0].input)` ← typed object from the raw dict

**What it does:** "Force LLM to fill in every field of a typed schema — no text parsing needed."

---

### Example 2: LLM Evaluation / Judge

```python
from pydantic import BaseModel

class EvaluationResult(BaseModel):
    score: int           # 1-10
    reasoning: str       # why this score
    passed: bool         # True if score >= 7
    suggestions: list[str]   # improvement suggestions

eval_tool = {
    "name": "EvaluationResult",
    "description": "Evaluate the quality of an LLM response.",
    "input_schema": EvaluationResult.model_json_schema()
}

def evaluate_response(question: str, answer: str) -> EvaluationResult:
    prompt = f"""Evaluate this AI response:
Question: {question}
Answer: {answer}

Score from 1-10 and explain your reasoning."""

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        tools=[eval_tool],
        tool_choice={"type": "tool", "name": "EvaluationResult"},
        messages=[{"role": "user", "content": prompt}]
    )
    return EvaluationResult(**response.content[0].input)

# Example call:
result = evaluate_response("What is RAG?", "RAG stands for Random Access Generation.")
print(result.score)         # 2
print(result.passed)        # False
print(result.reasoning)     # "The definition is completely wrong. RAG stands for..."
print(result.suggestions)   # ["Correct the acronym", "Explain retrieval step"]
```

**RECOGNIZE THIS:**
- `passed: bool` ← gate: True if score >= 7 (LLM fills this in based on the score)
- `suggestions: list[str]` ← list field — Pydantic handles the array automatically
- `evaluate_response(...)` returns a `EvaluationResult` object, not a string

**What it does:** "LLM as judge — returns a structured verdict with score, pass/fail, and feedback."

---

### Example 3: Optional Fields with Defaults

```python
from pydantic import BaseModel, Field
from typing import Optional

class RAGResult(BaseModel):
    answer: str
    confidence: float = Field(ge=0.0, le=1.0, description="0.0 to 1.0")
    sources: list[str] = []           # ← default empty list
    follow_up: Optional[str] = None   # ← optional, may be None
    needs_human: bool = False         # ← default False

rag_tool = {
    "name": "RAGResult",
    "description": "Return a structured RAG system answer.",
    "input_schema": RAGResult.model_json_schema()
}

# Example call:
response = client.messages.create(
    model="claude-opus-4-6", max_tokens=1024,
    tools=[rag_tool],
    tool_choice={"type": "tool", "name": "RAGResult"},
    messages=[{"role": "user", "content": "What is quantum computing? (Be concise)"}]
)

result = RAGResult(**response.content[0].input)
print(result.answer)        # "Quantum computing uses quantum mechanics to..."
print(result.confidence)    # 0.88
print(result.sources)       # []   (LLM returned default — no sources in this context)
print(result.follow_up)     # None or "Would you like more detail on qubits?"
print(result.needs_human)   # False
```

**RECOGNIZE THIS:**
- `= []` and `= None` and `= False` ← Pydantic defaults (LLM can omit these)
- `Optional[str]` ← Python type hint: str or None
- `Field(ge=0.0, le=1.0)` ← validation constraint: must be between 0 and 1
- `description=` inside Field ← the LLM reads this too

**What it does:** "Structured response with validation constraints and sensible defaults."

---

### Example 4: Nested Pydantic Models

```python
from pydantic import BaseModel

class Source(BaseModel):
    title: str
    url: str
    relevance_score: float

class ResearchReport(BaseModel):
    topic: str
    summary: str
    key_findings: list[str]
    sources: list[Source]         # ← nested model inside a list
    confidence: float
    limitations: str

report_tool = {
    "name": "ResearchReport",
    "description": "Structure a research report on any topic.",
    "input_schema": ResearchReport.model_json_schema()  # ← handles nested models
}

# Example call:
response = client.messages.create(
    model="claude-opus-4-6", max_tokens=4096,
    tools=[report_tool],
    tool_choice={"type": "tool", "name": "ResearchReport"},
    messages=[{"role": "user", "content": "Research report on LLMs in healthcare 2026."}]
)

report = ResearchReport(**response.content[0].input)
print(report.topic)                        # "LLMs in Healthcare 2026"
print(report.key_findings[0])              # "LLMs reduced diagnostic time by 40%..."
print(report.sources[0].title)             # "NEJM 2026 Study"
print(report.sources[0].relevance_score)   # 0.95  ← typed float
```

**RECOGNIZE THIS:**
- `list[Source]` ← list of Pydantic objects (nested schema)
- `model_json_schema()` handles the nesting automatically
- `report.sources[0].title` ← deeply typed access

**What it does:** "Complex structured output — report with nested source objects, all typed."

---

### Example 5: Validation and Error Handling

```python
from pydantic import BaseModel, ValidationError

class SafeScore(BaseModel):
    score: int        # will validate it's an int
    label: str

def get_structured_score(text: str) -> SafeScore | None:
    response = client.messages.create(
        model="claude-opus-4-6", max_tokens=512,
        tools=[score_tool],
        tool_choice={"type": "tool", "name": "SafeScore"},
        messages=[{"role": "user", "content": text}]
    )
    try:
        return SafeScore(**response.content[0].input)
    except ValidationError as e:
        print(f"Validation failed: {e}")
        return None

# Example calls:
result = get_structured_score("Rate this: 'The answer was very clear.'")
print(result.score)   # 8 (int)
print(result.label)   # "Good"

result = get_structured_score("Rate this: [garbled input]")
# If LLM returns wrong types → ValidationError caught → returns None safely
print(result)         # None
```

**RECOGNIZE THIS:**
- `except ValidationError` ← Pydantic raises this if the LLM returns wrong types
- Return type `SafeScore | None` ← function handles failure gracefully
- No crash — validation failure is caught and handled

**What it does:** "Safe structured output — always returns typed object or None, never crashes."

---

### Example 6: The Evaluator Pattern (Production Standard)

```python
from pydantic import BaseModel

class QualityGate(BaseModel):
    passes: bool
    score: float          # 0.0–1.0
    reason: str
    action: str           # "accept", "retry", "escalate"

gate_tool = {
    "name": "QualityGate",
    "description": "Evaluate whether an AI response meets quality standards.",
    "input_schema": QualityGate.model_json_schema()
}

def quality_gate(question: str, answer: str, threshold: float = 0.8) -> str:
    prompt = f"Q: {question}\nA: {answer}\n\nEvaluate quality. Score 0-1. Action: accept/retry/escalate."

    response = client.messages.create(
        model="claude-opus-4-6", max_tokens=512,
        tools=[gate_tool],
        tool_choice={"type": "tool", "name": "QualityGate"},
        messages=[{"role": "user", "content": prompt}]
    )
    gate = QualityGate(**response.content[0].input)

    if gate.passes and gate.score >= threshold:
        return answer                                      # ← accept
    elif gate.action == "retry":
        return regenerate_answer(question)                 # ← retry
    else:
        return escalate_to_human(question, answer, gate)   # ← escalate

# Example call:
final = quality_gate("What is RAG?", "RAG is a thing in AI.")
# gate.passes = False, gate.score = 0.2, gate.action = "retry"
# → triggers regenerate_answer("What is RAG?") automatically
```

**RECOGNIZE THIS:**
- `action: str` with values like "accept"/"retry"/"escalate" ← routing decision
- The function uses `gate.action` to branch — structured output drives control flow
- This is the **evaluator-as-router** pattern common in production AI pipelines

**What it does:** "LLM evaluates its own output → structured verdict → routes to accept/retry/escalate."

---

### Example 7: JSON Mode (Alternative to tool_choice)

```python
import json
from pydantic import BaseModel

class Intent(BaseModel):
    category: str
    confidence: float
    entities: list[str]

def extract_intent(text: str) -> Intent:
    prompt = f"""Analyze the intent of this user message and return JSON.

Message: {text}

Return ONLY valid JSON with this exact structure:
{{
    "category": "question|command|complaint|other",
    "confidence": 0.0_to_1.0,
    "entities": ["list", "of", "key", "entities"]
}}"""

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}]
        # No tools — ask for JSON in the prompt
    )

    raw_text = response.content[0].text
    # Parse the JSON text manually
    data = json.loads(raw_text)
    return Intent(**data)

# Example call:
intent = extract_intent("Can you help me find the nearest coffee shop?")
print(intent.category)    # "question"
print(intent.confidence)  # 0.95
print(intent.entities)    # ["coffee shop", "location"]
```

**RECOGNIZE THIS:**
- No `tools=` parameter ← different approach: ask for JSON in the prompt
- `json.loads(raw_text)` ← parse the text response
- Less reliable than `tool_choice` (LLM might add extra text) but simpler

**What it does:** "Prompt-based JSON extraction — less reliable than tool_choice but works without tool schemas."

---

### Example 8: Reading Structured Output in Framework Code

```python
# From agents/1_foundations/3_lab3.py — the evaluator pattern:
from pydantic import BaseModel

class Evaluation(BaseModel):
    is_acceptable: bool
    score: int              # 1-10
    critique: str

evaluator_tool = {
    "name": "Evaluation",
    "description": "Evaluate the quality of an AI response to a user's question.",
    "input_schema": Evaluation.model_json_schema()
}

def evaluate(reply: str, message: str) -> Evaluation:
    response = openai.beta.chat.completions.parse(   # ← OpenAI's built-in structured output
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": f"Evaluate: Q={message}, A={reply}"
        }],
        response_format=Evaluation                   # ← OpenAI's version of tool_choice trick
    )
    return response.choices[0].message.parsed        # ← already typed Pydantic object
```

**RECOGNIZE THIS:**
- `response_format=Evaluation` ← OpenAI's native structured output (same concept, different API)
- `.parsed` ← OpenAI returns a typed object directly
- Anthropic: use `tool_choice` + `response.content[0].input`
- OpenAI: use `response_format=` + `.message.parsed`

**What it does:** "OpenAI's equivalent of the Anthropic tool_choice trick. Same concept, different syntax."

---

## Structured Output Anatomy Reference

| Pattern | Syntax | Role |
|:--------|:-------|:-----|
| Define schema | `class X(BaseModel): field: type` | The typed contract |
| Generate tool | `X.model_json_schema()` | Convert schema to JSON |
| Force output | `tool_choice={"type":"tool","name":"X"}` | LLM must fill the schema |
| Parse result | `X(**response.content[0].input)` | Typed Python object |
| Validate | `X.model_validate(data)` | Validate a raw dict |
| Handle failure | `except ValidationError` | Catch type mismatches |

---

## You've Completed Pass 1!

You can now:
✓ **Read** Pydantic BaseModel definitions and understand the field types
✓ **Spot** `tool_choice={"type":"tool"}` as the structured output trigger
✓ **Trace** from `response.content[0].input` → typed Pydantic object
✓ **Recognize** the evaluator pattern (judge → pass/fail/retry)
✓ **Distinguish** tool_choice approach vs JSON prompt approach
✓ **Read** OpenAI's `response_format=` as the equivalent pattern

**Next:**
- **Pass C (Visual):** See the schema → response → typed object flow
- **Pass 3 (Templates):** Copy structured output patterns for extractors and judges

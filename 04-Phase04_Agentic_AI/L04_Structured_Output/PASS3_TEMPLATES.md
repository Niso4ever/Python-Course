# Lesson 20 — Pass 3: TEMPLATES
## Your Structured Output Copy-Paste Library

**Goal:** Ready-to-use Pydantic models and structured output patterns. Define your schema, copy the extractor, get typed objects.


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

## Template 1: Basic Extractor
**Use when:** Extract structured data from unstructured text

```python
from pydantic import BaseModel
import anthropic

client = anthropic.Anthropic()

class ExtractedData(BaseModel):         # ← MODIFY: your fields here
    field_one: str
    field_two: int
    field_three: float
    field_four: bool

def extract(text: str) -> ExtractedData:
    tool = {
        "name": "ExtractedData",
        "description": "Extract structured information from text.",
        "input_schema": ExtractedData.model_json_schema()
    }
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        tools=[tool],
        tool_choice={"type": "tool", "name": "ExtractedData"},
        messages=[{"role": "user", "content": f"Extract structured data from:\n{text}"}]
    )
    return ExtractedData(**response.content[0].input)
```

**Example call:**
```python
class ProductInfo(BaseModel):
    name: str
    price: float
    in_stock: bool
    rating: float

# Use extract() with ProductInfo substituted in
result = extract("The Pro Widget costs $29.99, is currently available, and has a 4.7 star rating.")
print(result.name)      # "Pro Widget"
print(result.price)     # 29.99
print(result.in_stock)  # True
print(result.rating)    # 4.7
```

---

## Template 2: LLM Evaluator / Quality Gate
**Use when:** Need a second LLM to judge, score, or validate output

```python
from pydantic import BaseModel
from typing import Literal

class EvaluationResult(BaseModel):
    score: int                                       # 1–10
    passes: bool                                     # True if quality is acceptable
    reasoning: str                                   # why this score
    action: Literal["accept", "retry", "escalate"]  # what to do next
    suggestions: list[str]                           # how to improve

eval_tool = {
    "name": "EvaluationResult",
    "description": "Evaluate quality of an AI-generated response.",
    "input_schema": EvaluationResult.model_json_schema()
}

def evaluate(question: str, answer: str, threshold: int = 7) -> EvaluationResult:
    prompt = f"""Evaluate this AI response:
Question: {question}
Answer: {answer}

Score from 1-10. If score < {threshold}, action = 'retry'. If harmful, action = 'escalate'. Else 'accept'."""

    response = client.messages.create(
        model="claude-opus-4-6", max_tokens=1024,
        tools=[eval_tool],
        tool_choice={"type": "tool", "name": "EvaluationResult"},
        messages=[{"role": "user", "content": prompt}]
    )
    return EvaluationResult(**response.content[0].input)
```

**Example calls:**
```python
result = evaluate("What is RAG?", "RAG stands for Random Access Generation.")
print(result.score)      # 1
print(result.passes)     # False
print(result.action)     # "retry"
print(result.suggestions)# ["Correct the acronym: RAG = Retrieval-Augmented Generation"]

result = evaluate("What is RAG?", "RAG combines document retrieval with LLM generation.")
print(result.score)      # 9
print(result.passes)     # True
print(result.action)     # "accept"
```

---

## Template 3: Structured RAG Response
**Use when:** RAG pipeline needs to return typed output instead of raw text

```python
from pydantic import BaseModel, Field
from typing import Optional

class RAGResponse(BaseModel):
    answer: str
    confidence: float = Field(ge=0.0, le=1.0)     # must be 0.0–1.0
    sources: list[str] = []
    follow_up_question: Optional[str] = None
    needs_human_review: bool = False

rag_response_tool = {
    "name": "RAGResponse",
    "description": "Return a structured answer from the RAG system.",
    "input_schema": RAGResponse.model_json_schema()
}

def structured_rag_answer(question: str, context: str) -> RAGResponse:
    prompt = f"""Answer this question using ONLY the provided context.

Context: {context}

Question: {question}

If the context doesn't fully answer the question, set needs_human_review=True and confidence accordingly."""

    response = client.messages.create(
        model="claude-opus-4-6", max_tokens=1024,
        tools=[rag_response_tool],
        tool_choice={"type": "tool", "name": "RAGResponse"},
        messages=[{"role": "user", "content": prompt}]
    )
    return RAGResponse(**response.content[0].input)
```

**Example calls:**
```python
result = structured_rag_answer(
    question="What is RAG?",
    context="RAG (Retrieval-Augmented Generation) combines a retrieval system with an LLM."
)
print(result.answer)              # "RAG combines a retrieval system with an LLM..."
print(result.confidence)          # 0.95
print(result.needs_human_review)  # False

# When context is insufficient:
result = structured_rag_answer("What is the stock price?", context="RAG is an AI technique.")
print(result.confidence)          # 0.1
print(result.needs_human_review)  # True
```

---

## Template 4: Intent Classifier
**Use when:** Need to route user input to the right agent or tool

```python
from pydantic import BaseModel
from typing import Literal

class UserIntent(BaseModel):
    category: Literal["question", "command", "complaint", "other"]
    topic: str                              # what it's about
    urgency: Literal["low", "medium", "high"]
    entities: list[str]                     # key things mentioned
    confidence: float                       # 0.0–1.0

intent_tool = {
    "name": "UserIntent",
    "description": "Classify the intent and content of a user message.",
    "input_schema": UserIntent.model_json_schema()
}

def classify_intent(user_message: str) -> UserIntent:
    response = client.messages.create(
        model="claude-opus-4-6", max_tokens=512,
        tools=[intent_tool],
        tool_choice={"type": "tool", "name": "UserIntent"},
        messages=[{"role": "user", "content": f"Classify this message: {user_message}"}]
    )
    return UserIntent(**response.content[0].input)
```

**Example calls:**
```python
intent = classify_intent("My order hasn't arrived and I need it urgently!")
print(intent.category)   # "complaint"
print(intent.urgency)    # "high"
print(intent.entities)   # ["order", "delivery"]

intent = classify_intent("What time does the store close?")
print(intent.category)   # "question"
print(intent.urgency)    # "low"
print(intent.topic)      # "store hours"
```

---

## Template 5: Safe Extractor (with validation)
**Use when:** Critical data that must be validated before use

```python
from pydantic import BaseModel, ValidationError
from typing import Optional

class CriticalData(BaseModel):
    value: float
    unit: str
    verified: bool

extract_tool = {
    "name": "CriticalData",
    "description": "Extract a critical measurement value from text.",
    "input_schema": CriticalData.model_json_schema()
}

def safe_extract(text: str) -> Optional[CriticalData]:
    """Returns typed CriticalData or None if extraction fails."""
    try:
        response = client.messages.create(
            model="claude-opus-4-6", max_tokens=512,
            tools=[extract_tool],
            tool_choice={"type": "tool", "name": "CriticalData"},
            messages=[{"role": "user", "content": f"Extract critical data from: {text}"}]
        )
        return CriticalData(**response.content[0].input)
    except ValidationError as e:
        print(f"Validation error: {e}")
        return None
    except Exception as e:
        print(f"Extraction error: {e}")
        return None
```

**Example calls:**
```python
data = safe_extract("Temperature reading: 98.6 degrees Fahrenheit, verified by sensor.")
if data:
    print(data.value)     # 98.6
    print(data.unit)      # "Fahrenheit"
    print(data.verified)  # True

data = safe_extract("The thing was really hot.")
if data is None:
    print("Extraction failed — no structured data found")  # graceful failure
```

---

## Quick Selection Guide

| Need | Template |
|:-----|:---------|
| Extract any fields from text | Template 1: Basic Extractor |
| Judge / score LLM output | Template 2: Evaluator |
| Typed RAG answer | Template 3: Structured RAG Response |
| Route user to right handler | Template 4: Intent Classifier |
| Critical validated extraction | Template 5: Safe Extractor |

---

## The Pydantic ↔ JSON Schema Cheat Map

| Pydantic type | JSON schema type |
|:-------------|:----------------|
| `str` | `"type": "string"` |
| `int` | `"type": "integer"` |
| `float` | `"type": "number"` |
| `bool` | `"type": "boolean"` |
| `list[str]` | `"type": "array", "items": {"type": "string"}` |
| `Optional[str]` | not in `"required"`, can be null |
| `= default_value` | not in `"required"` list |
| `Literal["a","b"]` | `"enum": ["a", "b"]` |
| `Field(ge=0, le=1)` | `"minimum": 0, "maximum": 1` |

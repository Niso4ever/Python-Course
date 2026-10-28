# Lesson 19: Structured Outputs & JSON Mode
## The Contract Theory

> **2026 Reality:** Every production AI system returns structured data — not raw text.
> JSON mode, Pydantic output parsing, and response_format are how you get
> reliable, typed data from LLMs. This is the bridge between "chatbot" and "system component."

---

## Why Structured Outputs Matter

An LLM that returns free text:
```
"The sentiment is positive with a score of about 85%"
```

An LLM that returns structured output:
```json
{"sentiment": "positive", "score": 0.85, "confidence": "high"}
```

The first is a chatbot. The second is a **system component** you can plug into a pipeline.

---

## 1. The Problem: Parsing Free Text is Fragile

```python
# ❌ BAD: Parsing free text (every production team has been burned by this)
response = "The answer is 42, with high confidence"
# How do you extract 42? What if the LLM says "forty-two"? "approximately 42"?
# Regex? split()? Hope and prayer?
```

```python
# ✅ GOOD: Structured output (guaranteed format)
response = {"answer": 42, "confidence": "high"}
# response["answer"] is ALWAYS an int. No parsing. No guessing.
```

---

## 2. Method 1: OpenAI JSON Mode (response_format)

```python
from openai import OpenAI
import json

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    response_format={"type": "json_object"},   # ← Force JSON output
    messages=[
        {"role": "system", "content": "Return analysis as JSON with keys: sentiment, score, reasoning"},
        {"role": "user", "content": "Analyze: The RAG pipeline exceeded expectations"}
    ]
)

data = json.loads(response.choices[0].message.content)
print(data["sentiment"])   # "positive"
print(data["score"])       # 0.92
```

**Limitation:** You get JSON, but no TYPE validation. The LLM might return `"score": "high"` instead of `"score": 0.92`.

---

## 3. Method 2: Pydantic Output Parsing (The 2026 Standard)

```python
from pydantic import BaseModel, Field
from openai import OpenAI

class SentimentAnalysis(BaseModel):
    sentiment: str = Field(description="positive, negative, or neutral")
    score: float = Field(ge=0, le=1, description="Confidence score 0-1")
    key_phrases: list[str] = Field(description="Important phrases detected")
    reasoning: str = Field(description="Why this sentiment was chosen")

client = OpenAI()

response = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    response_format=SentimentAnalysis,   # ← Pydantic model as format!
    messages=[
        {"role": "user", "content": "Analyze: The multi-agent system failed to coordinate properly"}
    ]
)

result = response.choices[0].message.parsed   # ← Already a Pydantic object!
print(result.sentiment)     # "negative"
print(result.score)         # 0.78 (guaranteed float between 0 and 1)
print(result.key_phrases)   # ["failed", "coordinate properly"]
```

**The power:** If the LLM returns `score: "high"`, Pydantic rejects it. The model retries.
Your code NEVER receives invalid data.

---

## 4. Method 3: DSPy Typed Signatures

```python
import dspy
from pydantic import BaseModel

class AgentPlan(BaseModel):
    goal: str
    steps: list[str]
    tools_needed: list[str]
    estimated_calls: int

class PlanAgent(dspy.Signature):
    """Plan the steps to answer a user's question."""
    question: str = dspy.InputField()
    plan: AgentPlan = dspy.OutputField()   # ← Pydantic model as output type

planner = dspy.Predict(PlanAgent)   # DSPy 3.x: Predict reads the types; TypedPredictor was removed
result = planner(question="What is the latest AI market size?")
print(result.plan.steps)          # ["Search web", "Extract data", "Calculate"]
print(result.plan.tools_needed)   # ["web_search", "calculator"]
```

---

## 5. Real-World Patterns

### Pattern 1: RAG with Structured Answers
```python
class RAGAnswer(BaseModel):
    answer: str
    sources: list[str]
    confidence: float
    needs_human_review: bool

# Your RAG returns a RAGAnswer, not raw text
# Downstream systems check needs_human_review automatically
```

### Pattern 2: Agent Tool Selection
```python
class ToolDecision(BaseModel):
    tool_name: str
    tool_input: dict
    reasoning: str

# Agent returns which tool to use as a typed object
# No regex parsing of "I think I should use the calculator..."
```

### Pattern 3: Multi-Agent Communication
```python
class AgentMessage(BaseModel):
    from_agent: str
    to_agent: str
    task: str
    data: dict
    priority: int = Field(ge=1, le=5)

# Agents communicate via typed messages, not free text
```

---

## 6. Token Economics Note

Structured outputs typically use **10-30% more tokens** than free text because the model
must adhere to a schema. However, they **save 100% of post-processing code** and
**eliminate 100% of parsing failures**. The ROI is always positive.

---

## 7. Key Takeaways

✓ **Structured outputs = system components** — not chatbots
✓ **JSON mode** is the minimum — forces JSON but no type validation
✓ **Pydantic parsing** is the 2026 standard — typed, validated, automatic retry
✓ **DSPy typed signatures** (`dspy.Predict` with a Pydantic output field) combine optimization with typed outputs
✓ **Every production agent** should return Pydantic objects, not strings
✓ **Costs 10-30% more tokens** but saves 100% of parsing bugs

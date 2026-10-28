# The Decoder Ring: Translating Fancy AI Code

When you see professional AI frameworks (LangChain, CrewAI, DSPy), use this guide to decode what's really happening.

---

## Quick Translation Table

| You See in the Wild | What It Really Is | Lesson |
|:-------------------|:------------------|:-------|
| `config = {...}` | Dictionary with settings | **L01** |
| `metadata = {"key": "value"}` | Dictionary storing labeled data | **L01** |
| `model: str = "claude-sonnet-5-5"` | Variable with type hint | **L01** |
| `results = []` | Empty list | **L02** |
| `docs = [...]` | List with items | **L02** |
| `[{"id": 1}, {"id": 2}]` | **List of dicts** (THE CORE PATTERN) | **L02** |
| `.append(item)` | Add to end of list | **L02** |
| `data["key"]` | Access dictionary value | **L01** |
| `list[0]` | Access first item in list | **L02** |
| `list[-1]` | Access last item in list | **L02** |
| `if score > 0.8:` | Threshold check (logic gate) | **L03** |
| `if x: ... else: ...` | Branch based on condition | **L03** |
| `match intent: case "search":` | Route by name — not a score | **L03** |
| `match stop_reason: case "tool_use":` | Route by API status | **L03** |
| `for item in list:` | Loop through list | **L04** |
| `while condition:` | Repeat while true | **L04** |
| `[x["score"] for x in results]` | List comprehension (compact loop) | **L04** |
| `def process(q: str) -> dict:` | Function with type hints | **L01 + L05** |
| `result = function(arg)` | Function call | **L05** |
| `model.invoke(...)` | Method call (function on class) | **L05 + L06** |
| `class Agent:` | Standard class — does things, holds memory | **L06** |
| `agent = Agent(...)` | Create instance from class | **L06** |
| `@dataclass class Config:` | Config container — holds settings | **L06** |
| `class Output(BaseModel):` | Pydantic model — validates data | **L06** |

---

## Framework-Specific Decodings

### LangChain

```python
# What you see:
from langchain_anthropic import ChatAnthropic
model = ChatAnthropic(model="claude-sonnet-5-5")
response = model.invoke([HumanMessage(content="Hello")])

# What it really is:
# L06: Create instance from blueprint (standard class)
# L05: Call method with list of dicts
# L02: [{"role": "user", "content": "Hello"}]
```

### CrewAI

```python
# What you see:
agent = Agent(
    role="Researcher",
    goal="Find information",
    tools=[search_tool, calculator]
)

# What it really is:
# L06: Create agent instance (standard class)
# L01: Dictionary of settings (role, goal)
# L02: List of available tools
```

### DSPy

```python
# What you see:
class RAG(dspy.Module):
    def forward(self, question: str) -> str:
        context = self.retrieve(question)
        return self.generate(question, context)

# What it really is:
# L06: Class definition (blueprint)
# L05: Methods with type hints (functions in a class)
# L05: Function calls chained together
```

### Anthropic SDK (direct)

```python
# What you see:
client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-sonnet-5-5",
    messages=[{"role": "user", "content": "Hello"}]
)
match response.stop_reason:
    case "end_turn":  ...
    case "tool_use":  ...

# What it really is:
# L06: Create client instance
# L02: List of dicts (messages)
# L03: match/case routing by stop_reason name
```

---

## The Pattern Recognition Shortcuts

### When you see `[]`
- Empty list: `results = []`
- List with items: `[1, 2, 3]`
- List of dicts: `[{"key": "value"}, {"key": "value"}]` ← **80% of AI code**
- Accessing list: `items[0]`, `items[-1]`

### When you see `{}`
- Empty dict: `config = {}`
- Dict with data: `{"model": "claude-sonnet-5-5", "temp": 0.7}`
- Accessing dict: `config["model"]`
- Dict in a list: `[{"id": 1}, {"id": 2}]` ← **THE PATTERN**

### When you see `def`
- Function with type hints: `def search(query: str) -> list:`
- Method in class: Inside `class Agent:` block
- Lambda (anonymous): `lambda x: x["score"]`

### When you see `class`
- Standard class: `class Agent:` — has `__init__`, `self`, methods
- Dataclass: `@dataclass class Config:` — Python writes `__init__` for you
- Pydantic model: `class Output(BaseModel):` — validates types automatically

### When you see `match`
- Routing by name: `match tool_name: case "search":`
- Routing by API status: `match stop_reason: case "tool_use":`
- Rule: if you're checking a **name or label**, use `match/case`
- Rule: if you're checking a **score or number**, use `if/elif`

### When you see `.`
- Access dict value: `config["key"]` or `config.get("key")`
- Call method: `model.invoke(...)` — function in a class
- Access attribute: `agent.name` — variable stored in instance

---

## Common "Scary" Patterns Decoded

### Pattern: List Comprehension

```python
# What you see:
scores = [doc["score"] for doc in results]

# What it means (L04 + L02):
scores = []
for doc in results:       # L04: loop
    scores.append(doc["score"])   # L02: extract from dict

# Translation: "Loop through results, extract score from each dict"
```

### Pattern: Method Chaining

```python
# What you see:
result = agent.search("query").filter(threshold=0.8).format()

# What it means (L05):
temp1 = agent.search("query")
temp2 = temp1.filter(threshold=0.8)
result = temp2.format()

# Translation: "Call search, then filter, then format (each returns object)"
```

### Pattern: Nested Dicts/Lists

```python
# What you see:
data = {
    "results": [
        {"id": 1, "scores": [0.9, 0.8]},
        {"id": 2, "scores": [0.7, 0.6]}
    ]
}

# How to access:
data["results"]                  # The list (L02)
data["results"][0]               # First dict in list (L02)
data["results"][0]["id"]         # Value from dict (L01)
data["results"][0]["scores"][0]  # First score (L02)

# Translation: "Dict contains list of dicts, each with nested list"
```

### Pattern: stop_reason routing (Anthropic SDK)

```python
# What you see:
match response.stop_reason:
    case "end_turn":
        return response.content[0].text
    case "tool_use":
        ...
    case _:
        return "[Unexpected]"

# What it really is (L03):
# match/case routing by the NAME of stop_reason
# NOT a score check — that's why match/case is used, not if/elif
```

---

## The Three Questions to Decode Any Line

When you see unfamiliar code, ask:

### 1. Is it data or action?
- **Data:** Dictionary `{}`, List `[]`, String `"text"`, Number `42`
- **Action:** Function call `function()`, Method `.invoke()`, Loop `for`

### 2. What lesson pattern is it?
- Curly braces `{}` → **L01** (Dictionary)
- Square brackets `[]` → **L02** (List)
- `if/elif/else` → **L03** (Logic gate — threshold/boolean)
- `match/case` → **L03** (Logic gate — name routing)
- `for/while` → **L04** (Loop)
- `def fn(x: str) -> dict:` → **L01 + L05** (Function with type hints)
- `class Agent:` → **L06** (Standard class)
- `@dataclass` → **L06** (Config container)
- `BaseModel` → **L06** (Validated data)

### 3. What's the input and output?
- If it's a function: What type goes in? What type comes out?
- If it's a list: List of what? (strings, numbers, **dicts**?)
- If it's a dict: What labels does it have?

---

## Practice Test

Decode this real Anthropic SDK code:

```python
import anthropic
from dataclasses import dataclass
from pydantic import BaseModel

@dataclass
class AgentConfig:
    model: str = "claude-sonnet-5-5"
    max_tokens: int = 1000

class ToolResult(BaseModel):
    tool_name: str
    output: str

client = anthropic.Anthropic()
config = AgentConfig()

messages = [{"role": "user", "content": "What is RAG?"}]
response = client.messages.create(
    model=config.model,
    max_tokens=config.max_tokens,
    messages=messages
)

match response.stop_reason:
    case "end_turn":
        print(response.content[0].text)
    case "tool_use":
        print("Tool call needed")
```

**Answers:**
1. `@dataclass class AgentConfig:` → **L06**: Config container, Python writes `__init__`
2. `class ToolResult(BaseModel):` → **L06**: Pydantic — validates output types
3. `client = anthropic.Anthropic()` → **L06**: Create instance from Anthropic's class
4. `messages = [{"role": "user", ...}]` → **L02**: List of dicts (THE PATTERN)
5. `config.model` → **L06 + L01**: Access attribute on dataclass instance
6. `match response.stop_reason:` → **L03**: Route by name, not score

---

## The Ultimate Truth

**Every** AI framework does the same thing:
1. Store configuration in **dicts** (L01) — often with type hints
2. Store collections in **lists** (L02) — usually list of dicts
3. Route with **if/elif** for scores, **match/case** for names (L03)
4. Process collections with **loops** (L04)
5. Encapsulate logic in **functions** with type hints (L05)
6. Build modules with **classes** — standard, @dataclass, or Pydantic (L06)

When you see fancy names like "Chain", "Agent", "Module", "Pipeline" — they're all just classes (L06) that manipulate lists of dicts (L02) using functions (L05).

**You already know this.** Now you just recognize it in the wild.

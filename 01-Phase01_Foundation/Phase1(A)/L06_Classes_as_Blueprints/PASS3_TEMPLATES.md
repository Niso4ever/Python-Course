# Pass 3: Templates Overview — Classes as Blueprints
## Your Lesson 06 Template Library

All templates are in the L06 folder.
**Your workflow:** Find the agent type you need → copy → modify `__init__` → use.

> **2026 Note:** Three class styles you'll see in real AI code:
> - Standard `class` → agent with methods + memory (Templates 1-3)
> - `@dataclass` → config container (Template 4)
> - Pydantic `BaseModel` → validated LLM output (Template 5)

---

## Template Files at a Glance

| File | What it builds | Key attributes |
|:-----|:---------------|:---------------|
| `template_conversation_agent.py` | Chat agent with memory | `history`, `model`, `system` |
| `template_rag_agent.py` | RAG agent with usage tracking | `db`, `llm`, `top_k`, `call_count` |
| `template_multi_tool_agent.py` | Multi-model + tool registry | `tools`, `models`, `usage` |
| `CHEATSHEET_L06.py` | All class patterns quick reference | — |

---

## Template 1: Conversation Agent

**File:** `template_conversation_agent.py`
**Use when:** You need an agent that remembers conversation history across turns.

```python
class ConversationAgent:
    def __init__(self, model_name, system_prompt):
        self.model   = model_name
        self.system  = system_prompt
        self.history = []
        self.turns   = 0

    def chat(self, user_input):      # Main tool
        ...
    def reset(self):                 # Wipe memory
        ...
    def get_stats(self):             # Read state
        ...
```

**Variations included:**
1. Basic conversation agent (history list)
2. Agent with token counting
3. Agent with system prompt injection
4. Agent with turn limit enforcement

---

## Template 2: RAG Agent

**File:** `template_rag_agent.py`
**Use when:** You need retrieval-augmented generation with logging and tracking.

```python
class RAGAgent:
    def __init__(self, vector_db, llm_client, top_k=3):
        self.db         = vector_db
        self.llm        = llm_client
        self.top_k      = top_k
        self.call_count = 0
        self.queries    = []

    def answer(self, question):      # Core retrieval + generation
        ...
    def search_only(self, question): # Just retrieval, no generation
        ...
    def get_usage(self):             # Usage report
        ...
```

**Variations included:**
1. Basic RAG agent (search + generate)
2. RAG agent with confidence filtering
3. RAG agent with source citations
4. RAG agent with cost tracking

---

## Template 3: Multi-Tool Agent

**File:** `template_multi_tool_agent.py`
**Use when:** You need an agent that selects between multiple models or tools.

```python
class MultiModelAgent:
    def __init__(self):
        self.models = {"fast": ..., "balanced": ..., "powerful": ...}
        self.usage  = {"fast": 0, "balanced": 0, "powerful": 0}

    def answer(self, question, mode="balanced"):   # Route to model
        ...
    def usage_report(self):                        # Track costs
        ...


class ToolAgent:
    def __init__(self, tools):
        self.tools   = tools
        self.results = []

    def run(self, task):             # Auto-select tool
        ...
    def get_history(self):           # View past results
        ...
```

**Variations included:**
1. Multi-model router (fast/balanced/powerful)
2. Tool registry agent (auto-selects tool)
3. Fallback chain agent (tries next if first fails)
4. Config manager class (singleton settings)

---

## Template 4: @dataclass (Config Container)

**Use when:** Passing configuration or dependencies cleanly between components.

```python
from dataclasses import dataclass

@dataclass
class AgentConfig:
    model: str                       # Required — no default
    temperature: float = 0.7         # Optional — has default
    max_tokens: int    = 1000        # Optional — has default
    top_k: int         = 3           # Optional — has default

# Python writes __init__ automatically:
config = AgentConfig(model="claude-sonnet-5-5")
config.model         # "claude-sonnet-5-5"
config.temperature   # 0.7

# Pass into an agent:
agent = RAGAgent(db=my_db, llm=my_llm, config=config)
```

**Modification Guide:**
- Add fields with `: type` (required) or `: type = default` (optional)
- No `def __init__` needed — Python generates it
- No methods needed — this is a data holder, not a doer

---

## Template 5: Pydantic BaseModel (LLM Output Validator)

**Use when:** Parsing and validating structured output from an LLM or API.

```python
from pydantic import BaseModel

class AgentResponse(BaseModel):
    answer: str
    confidence: float
    sources: list[str]
    reasoning: str | None = None    # Optional — can be None

# Usage — types validated at creation:
response = AgentResponse(
    answer="RAG stands for Retrieval-Augmented Generation.",
    confidence=0.92,
    sources=["internal_kb", "wikipedia"]
)

# Access fields like attributes:
print(response.answer)       # "RAG stands for..."
print(response.confidence)   # 0.92

# Wrong type → immediate ValidationError (safer than silent bugs):
# AgentResponse(answer="x", confidence="not-a-number", sources=[])  ← ERROR
```

**Modification Guide:**
- Add fields: `field_name: type` for required, `field_name: type = default` for optional
- Use `field: SomeType | None = None` for nullable optional fields
- Install with: `pip install pydantic` (v2 is current in 2026)

---

## CHEATSHEET: Quick Class Pattern Reference

**File:** `CHEATSHEET_L06.py`
**Use:** Keep this open while reading AI code. Instant pattern lookup.

Covers:
- Define a class (standard, @dataclass, Pydantic)
- Create an instance
- Call a method
- Read an attribute
- Update state
- Common AI class patterns
- Class vs Function decision table
- `self` explained in plain terms

---

## Quick Decision Guide

**Which template do I need?**

```
Does it need to REMEMBER a conversation?
  YES → template_conversation_agent.py

Does it SEARCH a database and call an LLM?
  YES → template_rag_agent.py

Does it CHOOSE between models or tools?
  YES → template_multi_tool_agent.py

Do I need to PASS CONFIG around cleanly?
  YES → Template 4: @dataclass

Do I need to VALIDATE data from an LLM or API?
  YES → Template 5: Pydantic BaseModel

Do I just need SETTINGS in one place?
  YES → Config class in CHEATSHEET_L06.py (Pattern 3)

Is it a ONE-TIME operation with no memory?
  → Use a function (def) from L05 instead
```

---

## Copy-Modify-Use Workflow

**Step 1:** Identify what kind of agent you're building
**Step 2:** Open the matching template file
**Step 3:** Modify `__init__` — change attribute names and values
**Step 4:** Add/remove methods as needed
**Step 5:** Create an instance: `my_agent = MyClass(args)`
**Step 6:** Call methods: `my_agent.method(input)`

---

## Patterns Combined Reference

All class templates use earlier lesson patterns internally:

| Inside the class | Pattern from |
|:----------------|:-------------|
| `self.data = {}` | L01: Dict storage |
| `self.history = []` | L02: List storage |
| `if score >= threshold:` | L03: Condition check |
| `match intent: case "search":` | L03: match/case routing |
| `for doc in docs:` | L04: Loop |
| `def format_prompt(q, ctx):` | L05: Function inside class |
| `self.x = param` | L06: State stored as attribute |
| `@dataclass class Config:` | L06: Config container (2026) |
| `class Output(BaseModel):` | L06: Pydantic validator (2026) |

**Learning milestone:** When you can read any of these templates and say "I see an L04 loop inside an L06 class" — you're reading AI code fluently.

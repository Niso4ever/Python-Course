# Lesson 06 Templates: Classes as Blueprints

Reusable class patterns for building stateful AI agents.

---

## Learning Materials
0. **PASS0_OOP_FUNDAMENTALS.md** - Why classes exist: the mental model (READ FIRST if OOP is new). With it: **CHEATSHEET_OOP.py** and **template_ai_agent_anatomy.py**
1. **PASS1_RECOGNITION.md** - Learn to recognize classes in real AI code (START HERE)
2. **PASS_C_VISUAL.md** - See how blueprints, instances, and `self` work visually
3. **PASS3_TEMPLATES.md** - Overview of all templates and when to use each

## Templates
4. **CHEATSHEET_L06.py** - Quick reference (KEEP OPEN!)
5. **template_conversation_agent.py** - Chat agents with memory (4 variations)
6. **template_rag_agent.py** - RAG agents with usage tracking (4 variations)
7. **template_multi_tool_agent.py** - Model router + tool selector (4 variations)

---

## Quick Selection

| Need | File |
|:-----|:-----|
| Chat agent with memory | template_conversation_agent.py |
| RAG system with tracking | template_rag_agent.py |
| Route between models/tools | template_multi_tool_agent.py |
| All class patterns | CHEATSHEET_L06.py |

---

## Three Class Styles in AI Code (2026)

You will see **three ways** to define a class in real AI code. Recognize all three.

### Style 1: Standard Class (what you learned)
Use for complex agents with methods and full behavior.
```python
class RAGAgent:
    def __init__(self, db, model):
        self.db = db
        self.model = model
        self.history = []

    def query(self, question):
        results = self.db.search(question)
        return self.model.generate(results, question)
```

### Style 2: @dataclass (Python built-in, cleaner syntax)
Use for **passing data around** — config, dependencies, settings.
No need to write `__init__` manually. Python writes it for you.
```python
from dataclasses import dataclass

@dataclass
class AgentConfig:
    model: str
    temperature: float = 0.7
    max_tokens: int = 1000

# Same as writing __init__ yourself — but shorter
config = AgentConfig(model="claude-opus-5-5")
print(config.model)        # "claude-opus-5-5"
print(config.temperature)  # 0.7
```

### Style 3: Pydantic BaseModel (type-safe, validates data)
Use for **LLM outputs and API inputs** — when data comes from outside and must be validated.
```python
from pydantic import BaseModel

class AgentResponse(BaseModel):
    answer: str
    confidence: float
    sources: list[str]

# Pydantic validates types automatically — wrong type raises an error immediately
response = AgentResponse(answer="RAG stands for...", confidence=0.92, sources=["wiki"])
```

---

## When to Use Each Style

| Style | Use when | Common in |
|:------|:---------|:----------|
| Standard `class` | Agent needs methods + behavior + memory | LangChain agents, CrewAI agents |
| `@dataclass` | Passing config or dependencies around | PydanticAI, dependency injection |
| Pydantic `BaseModel` | Validating LLM output or API input | Tool outputs, structured responses |

**The rule:**
- Agent that DOES things → standard class
- Container that HOLDS data internally → @dataclass
- Data arriving from OUTSIDE (LLM/API) → Pydantic BaseModel

---

## Learning Path

**Step 1:** Read `PASS1_RECOGNITION.md` (30 min) — 8 examples, just reading
**Step 2:** Study `PASS_C_VISUAL.md` (15 min) — 9 diagrams
**Step 3:** Browse `PASS3_TEMPLATES.md` (10 min) — overview
**Step 4:** Run any template file to see it work!

---

## 3-Second Class Read (works for all three styles)
1. **Class name** → What kind of agent or data is this?
2. **Attributes / fields** → What does it remember or hold?
3. **Method names** → What can it do? (only standard class has these)

## Key Insight (Coffee Machine Version)
- Standard class = the full coffee machine with buttons and memory
- @dataclass = the spec sheet for the machine (model, voltage, capacity)
- Pydantic BaseModel = the quality inspector at the door checking every latte meets standard before it goes out

> **Python version note:** `@dataclass` is built into Python 3.7+. Pydantic requires `pip install pydantic` (v2 is current in 2026).

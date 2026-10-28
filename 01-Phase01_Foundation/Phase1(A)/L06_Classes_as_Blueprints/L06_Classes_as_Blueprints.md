# Lesson 06: Classes (class) as Blueprints
## The Toolbox Theory

Architect, you know how to store data (L01, L02), route it (L03), process collections (L04), and package logic into functions (L05). Now you need to **combine all of that into a module** — something that remembers its own state.

If a **Function** is a single tool (a hammer), a **Class** is a **Toolbox** that:
- Holds multiple tools (methods)
- Remembers its own state (attributes)
- Can be created many times from one blueprint (instances)

In AI systems, classes build **Agents** — modules that remember API keys, conversation history, usage counts, and configurations across multiple calls.

---

## 1. The Blueprint (class + __init__)

```python
class SearchAgent:
    def __init__(self, engine_name):   # Setup (runs once at creation)
        self.engine = engine_name       # Remember the engine
        self.history = []               # Remember all searches

    def search(self, query):            # A tool in the toolbox
        self.history.append(query)
        return f"Searching {self.engine} for: {query}"
```

| Symbol | Role |
|:-------|:-----|
| `class` | "I am defining a blueprint" |
| `__init__` | Setup method — runs once when created |
| `self` | "This specific instance" — access its own data |
| `self.engine` | Instance attribute — stored in THIS toolbox |
| `def search(self, ...)` | Method — a function that belongs to this class |

**Pattern:** `class Name:` → `def __init__(self, ...)` → `self.x = value` → `def method(self, ...)`

---

## 2. Creating Instances (Birthing the Toolbox)

The class is just a blueprint. Create real instances from it:

```python
# Two agents from the same blueprint
google_agent = SearchAgent("Google")
arxiv_agent  = SearchAgent("ArXiv")

# Each has its OWN memory
google_agent.search("Python tutorials")
arxiv_agent.search("LLM research papers")

print(google_agent.history)  # ["Python tutorials"]
print(arxiv_agent.history)   # ["LLM research papers"]
```

**Key insight:** Each instance is independent. `google_agent` and `arxiv_agent` don't share history.

---

## 3. Accessing State (self.attribute)

```python
class RAGAgent:
    def __init__(self, model, db):
        self.model        = model   # Stores config
        self.db           = db      # Stores reference
        self.search_count = 0       # Tracks usage
        self.total_cost   = 0.0     # Tracks cost

    def search_and_answer(self, query):
        docs = self.db.search(query)
        self.search_count += 1           # Update counter
        answer = self.model.invoke(docs)
        self.total_cost += 0.002         # Track cost
        return answer

    def get_stats(self):
        return {
            "searches": self.search_count,
            "total_cost": self.total_cost
        }
```

**What `self` does:** Lets any method access the data stored in `__init__`.

---

## 4. Real-World AI Examples

### Conversation Agent
```python
class ConversationAgent:
    def __init__(self, model_name, system_prompt):
        self.model   = model_name
        self.system  = system_prompt
        self.history = []           # Grows with each turn

    def chat(self, user_input):
        self.history.append({"role": "user", "content": user_input})
        # call LLM with full self.history
        response = call_llm(self.history, model=self.model)
        self.history.append({"role": "assistant", "content": response})
        return response

    def reset(self):
        self.history = []           # Start fresh conversation

# Create and use
agent = ConversationAgent("claude-sonnet-5-5", "You are helpful.")
agent.chat("What is RAG?")
agent.chat("Give me an example")  # Remembers previous message!
print(len(agent.history))         # 4 messages stored
```

### RAG Agent
```python
class RAGAgent:
    def __init__(self, vector_db, llm_client, top_k=3):
        self.db       = vector_db
        self.llm      = llm_client
        self.top_k    = top_k
        self.queries  = []      # Log all queries
        self.call_count = 0

    def answer(self, question):
        self.queries.append(question)
        self.call_count += 1
        docs    = self.db.search(question, top_k=self.top_k)
        context = "\n".join([d["text"] for d in docs])
        prompt  = f"Context: {context}\nQ: {question}"
        return self.llm.invoke(prompt)

    def get_usage(self):
        return {"total_queries": self.call_count, "queries": self.queries}

# Create and use
rag = RAGAgent(my_vectorstore, anthropic_client)
rag.answer("What is RAG?")
rag.answer("How does vector search work?")
print(rag.get_usage())  # {'total_queries': 2, 'queries': [...]}
```

### Multi-Model Agent
```python
class MultiModelAgent:
    def __init__(self):
        self.models = {
            "fast":     "claude-haiku-5-5",
            "balanced": "claude-sonnet-5-5",
            "powerful": "claude-opus-5-5"
        }
        self.usage = {"fast": 0, "balanced": 0, "powerful": 0}

    def answer(self, question, mode="balanced"):
        model = self.models[mode]       # L01: access dict
        self.usage[mode] += 1           # L01: update counter
        return call_llm(question, model=model)

    def usage_report(self):
        return self.usage

agent = MultiModelAgent()
agent.answer("Quick question", mode="fast")
agent.answer("Complex analysis", mode="powerful")
print(agent.usage_report())  # {'fast': 1, 'balanced': 0, 'powerful': 1}
```

---

## 4B. Two More Class Styles (2026 Standard)

In real AI code you will see **three class styles**. Recognize all three.

### Style 2: @dataclass (Config Container)
Use for **data holders** — config, settings, dependency bundles. Python writes `__init__` automatically.

```python
from dataclasses import dataclass

@dataclass
class AgentConfig:
    model: str                   # Required (no default)
    temperature: float = 0.7     # Optional (has default)
    max_tokens: int    = 1000    # Optional (has default)

config = AgentConfig(model="claude-sonnet-5-5")
config.model        # "claude-sonnet-5-5"
config.temperature  # 0.7
```

**Recognize it by:** `@dataclass` decorator above the class + field-style lines (no `self.x =`)

### Style 3: Pydantic BaseModel (Type Validator)
Use for **validating data from LLMs or APIs**. Raises an error immediately if wrong type.

```python
from pydantic import BaseModel

class AgentResponse(BaseModel):
    answer: str
    confidence: float
    sources: list[str]

response = AgentResponse(answer="RAG is...", confidence=0.92, sources=["kb"])
response.answer  # "RAG is..."
```

**Recognize it by:** `class Name(BaseModel):` — the `(BaseModel)` in the class definition

### The Rule
| Style | Use for | Tell |
|:------|:--------|:-----|
| Standard `class` | Agent that **does things** | Has methods (`def x(self, ...)`) |
| `@dataclass` | Container that **holds config** | `@dataclass` decorator |
| Pydantic `BaseModel` | Data **arriving from outside** | `(BaseModel)` in class signature |

---

## 5. Pattern Recognition Guide

**When you see:**
```python
class AgentName:
    def __init__(self, param):
        self.attribute = param
```
**Translation:** "Blueprint being defined. `__init__` sets up initial state."

**When you see:**
```python
agent = AgentName("value")
```
**Translation:** "Creating an instance from the blueprint."

**When you see:**
```python
agent.method_name(argument)
```
**Translation:** "Calling a tool that belongs to this instance."

**When you see:**
```python
self.history.append(item)
```
**Translation:** "This instance is updating its own stored list."

---

## 6. Class vs Function — When to Use What

| Use `def` (Function) when... | Use `class` (Class) when... |
|:-----------------------------|:----------------------------|
| Single operation | Multiple related operations |
| No memory needed | Must remember state |
| One-time logic | Reusable module |
| Simple input → output | Agent with config + methods |

---

## 7. Common AI Class Patterns

### Pattern 1: Agent with Memory
```python
class Agent:
    def __init__(self, config):
        self.config  = config
        self.history = []
        self.stats   = {"calls": 0, "cost": 0.0}
```

### Pattern 2: Agent with Tools
```python
class ToolAgent:
    def __init__(self, tools):
        self.tools = tools         # List of available tools
        self.results = []          # Store all results

    def run(self, task):
        for tool in self.tools:    # L04: loop through tools
            if tool.can_handle(task):  # L03: check condition
                result = tool.execute(task)
                self.results.append(result)
                return result
```

### Pattern 3: Singleton Config
```python
class Config:
    def __init__(self):
        self.model = "claude-sonnet-5-5"
        self.temperature = 0.7
        self.max_tokens = 1000
        self.thresholds = {"confidence": 0.85, "toxicity": 0.20}
```

---

## 8. Key Takeaways

✓ **`class`** defines a blueprint for a reusable module
✓ **`__init__`** runs once at creation — sets up state
✓ **`self`** means "this specific instance"
✓ **`self.x`** stores data that persists across method calls
✓ **Methods** are functions that belong to the class
✓ **Instances** are independent copies from the same blueprint
✓ **`@dataclass`** — Python writes `__init__` for you (2026 standard for config)
✓ **Pydantic `BaseModel`** — validates types at runtime (2026 standard for LLM output)

**Most common AI use:**
- Conversation agents → standard class (remember history)
- RAG agents → standard class (remember db + track usage)
- Config bundles → `@dataclass` (clean, no boilerplate)
- LLM output parsing → Pydantic `BaseModel` (validated, fail-fast)

---

## 9. Templates Available

See this lesson folder ([./](./)) for ready-to-use class templates: `template_conversation_agent.py`, `template_multi_tool_agent.py`, `template_rag_agent.py`.

**Your workflow:**
1. Find the agent template matching your need
2. Copy and modify `__init__` attributes
3. Add/remove methods
4. Create instances and use them

---

**Remember:** You're not memorizing class syntax. You're recognizing: "Oh, this is an agent that remembers its history" or "This tracks API usage." The template handles the structure.

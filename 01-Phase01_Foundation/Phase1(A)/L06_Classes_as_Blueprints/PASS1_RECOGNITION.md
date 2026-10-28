# Pass 1: Recognition — Classes (class) as Blueprints
## Read These 10 Examples — Don't Write Them

**Goal:** When you see a class in real AI code, instantly recognize what it does.

**Your 3-Second Class Read:**
1. **Class name** → What kind of agent is this?
2. **`__init__` attributes** → What does it remember?
3. **Methods** → What tools does it have?

> **2026 Note:** Three class styles in real AI code — recognize all three.
> - Standard `class` → agent with methods + memory (the coffee machine)
> - `@dataclass` → config/dependency container (the spec sheet)
> - Pydantic `BaseModel` → validated data from LLM/API (the quality inspector)

---

## Example 1: Conversation Agent (The Most Common Pattern)

```python
class ConversationAgent:
    def __init__(self, model_name, system_prompt):
        self.model   = model_name        # Which LLM to use
        self.system  = system_prompt     # Personality/role
        self.history = []                # Growing conversation

    def chat(self, user_input):
        self.history.append({"role": "user", "content": user_input})
        response = call_llm(self.history, model=self.model)
        self.history.append({"role": "assistant", "content": response})
        return response

    def reset(self):
        self.history = []               # Wipe memory, start fresh
```

**What to notice:**
- `self.history = []` → empty list in `__init__`, grows with every `.chat()` call
- `self.history.append(...)` → updating its OWN memory
- `self.model` used inside `chat()` — set once in `__init__`, used everywhere

---

## Example 2: RAG Agent (Retrieval + Tracking)

```python
class RAGAgent:
    def __init__(self, vector_db, llm_client, top_k=3):
        self.db         = vector_db      # Holds the database connection
        self.llm        = llm_client     # Holds the LLM connection
        self.top_k      = top_k          # Config remembered forever
        self.call_count = 0              # Tracks usage
        self.queries    = []             # Logs all questions

    def answer(self, question):
        self.queries.append(question)    # Log it
        self.call_count += 1             # Count it
        docs    = self.db.search(question, top_k=self.top_k)
        context = "\n".join([d["text"] for d in docs])
        prompt  = f"Context: {context}\nQ: {question}"
        return self.llm.invoke(prompt)

    def get_usage(self):
        return {"total": self.call_count, "queries": self.queries}
```

**What to notice:**
- `self.call_count = 0` → starts at zero, `+= 1` on every call — pure state tracking
- `self.top_k` → config set once in `__init__`, used silently in `answer()`
- `get_usage()` → reads state without changing it

---

## Example 3: Config Manager (Singleton Pattern)

```python
class AgentConfig:
    def __init__(self):
        self.model       = "claude-sonnet-5-5"
        self.temperature = 0.7
        self.max_tokens  = 1000
        self.thresholds  = {
            "confidence": 0.85,
            "toxicity":   0.20
        }

    def is_confident(self, score):
        return score >= self.thresholds["confidence"]

    def is_safe(self, toxicity_score):
        return toxicity_score < self.thresholds["toxicity"]
```

**What to notice:**
- No parameters in `__init__` — this class always starts with the same defaults
- `self.thresholds` is a dict stored on the instance (L1 inside L4!)
- Methods `is_confident()` and `is_safe()` use `self.thresholds` — state shared across methods

---

## Example 4: Multi-Model Agent (Router Pattern)

```python
class MultiModelAgent:
    def __init__(self):
        self.models = {
            "fast":      "claude-haiku-5-5",
            "balanced":  "claude-sonnet-5-5",
            "powerful":  "claude-opus-5-5"
        }
        self.usage = {"fast": 0, "balanced": 0, "powerful": 0}

    def answer(self, question, mode="balanced"):
        model = self.models[mode]      # L1: dict lookup
        self.usage[mode] += 1          # L1: update counter
        return call_llm(question, model=model)

    def usage_report(self):
        return self.usage              # Return the tracking dict
```

**What to notice:**
- `self.models` is a dict of model names — config stored as L1 pattern inside class
- `self.usage` tracks per-model call counts
- `mode="balanced"` → default parameter inside a method (L3 pattern inside L4!)

---

## Example 5: Tool Agent (Registry Pattern)

```python
class ToolAgent:
    def __init__(self, tools):
        self.tools   = tools           # List of tool objects
        self.results = []              # Log of all results
        self.calls   = 0               # Total tool calls made

    def run(self, task):
        self.calls += 1
        for tool in self.tools:        # L2.5: loop through tools
            if tool.can_handle(task):  # L2: check condition
                result = tool.execute(task)
                self.results.append(result)
                return result
        return "No tool available for this task"

    def get_history(self):
        return self.results
```

**What to notice:**
- `self.tools` is a list passed in — the agent holds its tools in memory
- Inside `run()`: for loop (L04) + if/else (L03) + self.results.append (L02) — all patterns combined
- The agent doesn't know which tool will handle it — it loops and checks

---

## Example 6: Search Agent (External API Wrapper)

```python
class SearchAgent:
    def __init__(self, engine_name, api_key):
        self.engine  = engine_name    # "Google", "ArXiv", etc.
        self.api_key = api_key        # Stored once, used on every search
        self.history = []             # All past queries
        self.count   = 0              # Number of searches done

    def search(self, query, max_results=5):
        self.history.append(query)
        self.count += 1
        # ... real search API call here ...
        return f"Results from {self.engine} for: {query}"

    def get_history(self):
        return {
            "engine":  self.engine,
            "count":   self.count,
            "queries": self.history
        }
```

**What to notice:**
- `self.api_key` — sensitive credentials stored once in `__init__`, reused silently
- `max_results=5` → optional parameter in a method (same as L3 defaults)
- `get_history()` returns a dict with multiple pieces of state — L1 pattern

---

## Example 7: Pipeline Agent (Multi-Step Processing)

```python
class PipelineAgent:
    def __init__(self, retriever, ranker, generator):
        self.retriever = retriever     # Step 1 component
        self.ranker    = ranker        # Step 2 component
        self.generator = generator    # Step 3 component
        self.log       = []            # Full process log

    def process(self, query):
        # Step 1
        raw_docs = self.retriever.get(query)
        # Step 2
        ranked   = self.ranker.rank(raw_docs)
        # Step 3
        answer   = self.generator.generate(query, ranked)

        self.log.append({
            "query":   query,
            "docs":    len(raw_docs),
            "answer":  answer
        })
        return answer

    def get_log(self):
        return self.log
```

**What to notice:**
- Three external components injected at creation — "dependency injection" pattern
- `process()` chains three steps in sequence — L05 pipeline inside L06 class
- Every call logs a dict to `self.log` — building a history of dicts (L01 + L02 inside L06)

---

## Example 8: LangChain-Style Agent (Real Framework Code)

```python
# This is how LangChain structures agents — same patterns you know
class AgentExecutor:
    def __init__(self, agent, tools, verbose=False):
        self.agent   = agent           # The LLM-powered brain
        self.tools   = tools           # Available tools (list)
        self.verbose = verbose         # Debug flag
        self.history = []

    def invoke(self, inputs):
        query = inputs["input"]
        self.history.append(query)

        # Agent decides what tool to use
        action = self.agent.plan(query, self.tools)

        # Execute that tool
        for tool in self.tools:
            if tool.name == action.tool:
                result = tool.run(action.tool_input)
                return {"output": result}

        return {"output": "No tool matched"}
```

**What to notice:**
- Same patterns: `__init__` stores things, methods use `self.x`
- `verbose=False` — optional config parameter in `__init__` (L3 defaults inside L4!)
- The LangChain `AgentExecutor` you've seen in real code — now you can decode it

---

---

## Example 9: @dataclass — Config Container (2026 standard)

```python
from dataclasses import dataclass

@dataclass
class AgentConfig:
    model: str                        # Required — no default
    temperature: float = 0.7          # Optional — has default
    max_tokens: int    = 1000         # Optional — has default
    top_k: int         = 3            # Optional — has default

# Usage — Python writes __init__ for you automatically
config = AgentConfig(model="claude-sonnet-5-5")
print(config.model)        # "claude-sonnet-5-5"
print(config.temperature)  # 0.7

# Pass config into an agent
agent = RAGAgent(config=config)
```

**What to notice:**
- No `def __init__(self, ...)` — the `@dataclass` decorator writes it automatically
- Fields with `: type` and `= default` → optional parameters (same logic as L05 function defaults)
- Fields with `: type` only → required parameters (must be passed in)
- Used for **passing data around**, not for doing work

**The tell:** `@dataclass` decorator above the class name + field-style attributes (no `self.x =`)

---

## Example 10: Pydantic BaseModel — LLM Output Validator (2026 standard)

```python
from pydantic import BaseModel

class AgentResponse(BaseModel):
    answer: str
    confidence: float
    sources: list[str]
    reasoning: str | None = None      # Optional field (can be None)

# Usage — Pydantic validates types at creation time
response = AgentResponse(
    answer="RAG stands for Retrieval-Augmented Generation.",
    confidence=0.92,
    sources=["internal_kb", "wikipedia"]
)

# If types are wrong, Pydantic raises ValidationError immediately
# response = AgentResponse(answer="x", confidence="not-a-number", sources=[])
# ↑ This raises an error — "not-a-number" can't be float
```

**What to notice:**
- Inherits from `BaseModel` instead of writing `__init__`
- Every field has a `: type` annotation — Pydantic enforces these at runtime
- `str | None = None` → optional field that can be a string or missing
- Used for **validating data coming from outside** (LLM outputs, API responses, user input)

**The tell:** `class MyClass(BaseModel):` — the `(BaseModel)` in parentheses is the giveaway

---

## Style Comparison (at a glance)

```
Standard class:             @dataclass:                 Pydantic BaseModel:
────────────────────        ────────────────────        ────────────────────
class RAGAgent:             @dataclass                  class Response(BaseModel):
    def __init__(self,      class AgentConfig:              answer: str
        db, llm):               model: str                  confidence: float
        self.db = db            temperature: float=0.7      sources: list[str]
        self.llm = llm          max_tokens: int=1000
        self.history = []
    def answer(self, q):    config = AgentConfig(       resp = Response(
        ...                     model="claude-...")         answer="...",
                                                            confidence=0.9,
                                                            sources=["kb"])

↓ Does things             ↓ Holds config             ↓ Validates input
  Has methods               No methods                 Raises error if wrong type
  Has memory                Clean syntax               Used for LLM outputs
```

**Rule:**
- Agent that **DOES** things → standard class
- Container that **HOLDS** config/dependencies → `@dataclass`
- Data **ARRIVING FROM OUTSIDE** (LLM/API) → Pydantic `BaseModel`

---

## Pattern Summary

| Pattern | What it looks like | What it means |
|:--------|:-------------------|:--------------|
| `self.x = value` in `__init__` | Setup — stored forever |
| `self.x += 1` | Counter — updates on every call |
| `self.history = []` | Empty list — will grow with `.append()` |
| `self.config = {...}` | Dict of settings stored on the agent |
| `self.component = component` | External dependency stored for later use |
| `def method(self, ...)` | Tool — a function belonging to this agent |
| `agent = MyClass(args)` | Instance created from blueprint |
| `agent.method(input)` | Using a tool from the toolbox |

---

**Next:** See [PASS_C_VISUAL.md](PASS_C_VISUAL.md) for diagrams showing how classes are built and how `self` flows through methods.

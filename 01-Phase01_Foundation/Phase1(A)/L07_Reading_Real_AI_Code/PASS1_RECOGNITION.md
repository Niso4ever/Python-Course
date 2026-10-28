# Lesson 07 - Pass 1: RECOGNITION
## Learn to SEE Your L01–L06 Patterns Inside Real AI Frameworks

**Goal:** By the end of this pass, you'll look at professional LangChain, CrewAI, or Anthropic code and immediately recognize the L01–L06 building blocks hiding inside — WITHOUT writing any code.

---

## The Decoder Ring Method

Real AI framework code looks scary. It isn't. Every line maps back to a pattern you already know.

> **The secret:** Professional AI code is 80% list manipulation (L01+L02) dressed up with framework class names. Once you see the patterns, the "complexity" disappears.

### The Master Decoder Table

When you see this in real code → it's really this from your lessons:

| You See | It's Really | Lesson |
|:--------|:-----------|:-------|
| `config = {"model": "claude-sonnet-5-5"}` | Dictionary | **L01** |
| `name: str = "value"` | Type-hinted variable | **L01** |
| `results = [...]` | List | **L02** |
| `[{...}, {...}]` | List of dicts (THE pattern) | **L02** |
| `if score > 0.8:` | Logic gate — threshold check | **L03** |
| `match intent: case "search":` | Route by name | **L03** |
| `for item in list:` | Loop | **L04** |
| `[x for x in list]` | List comprehension | **L04** |
| `def process(q: str) -> dict:` | Function with type hints | **L01+L05** |
| `model.invoke(...)` | Method call | **L05+L06** |
| `class Agent:` | Standard class | **L06** |
| `@dataclass class Config:` | Config container | **L06** |
| `class Output(BaseModel):` | Validated LLM output | **L06** |

---

## Real Examples to RECOGNIZE (Don't Write, Just Read)

### Example 1: LangChain Chatbot — Fully Decoded

```python
from langchain_anthropic import ChatAnthropic     # ← import (L08 territory)
from langchain.schema import HumanMessage, AIMessage

# ── L01: DICTIONARY — config
config = {
    "model":       "claude-sonnet-5-5",
    "temperature": 0.7,
    "max_tokens":  1000
}

# ── L06: CLASS — create agent instance
model = ChatAnthropic(
    model=config["model"],           # ← L01: dict access
    temperature=config["temperature"]  # ← older code: Claude API rejects this since API version 2026-10-21
)

# ── L02: LIST OF DICTS — conversation
conversation = [
    HumanMessage(content="What is RAG?"),
    # HumanMessage = fancy dict: {"role": "user", "content": "..."}
]

# ── L05: FUNCTION CALL — invoke = juicer from L05
response = model.invoke(conversation)

# ── L02: APPEND — add to list
conversation.append(AIMessage(content=response.content))
```

**RECOGNIZE THIS:**
- `config = {...}` ← L01 dictionary
- `ChatAnthropic(...)` ← L06 class instantiation
- `conversation = [...]` ← L02 list
- `model.invoke(...)` ← L05 method call
- `.append(...)` ← L02 list append

**What it does:** "A complete professional chatbot — built entirely from L01–L06 patterns."

---

### Example 2: RAG System — Fully Decoded

```python
# ── L02: LIST OF DICTS — knowledge base
documents = [
    {"text": "RAG combines retrieval...", "source": "Wikipedia"},
    {"text": "Vector databases store...", "source": "ArXiv"},
    {"text": "Semantic search finds...",  "source": "Blog"}
]

# ── L05: FUNCTION with TYPE HINTS — search function
def search_knowledge(query: str) -> list:    # ← L01 type hints + L05 function
    results = vectorstore.similarity_search(query, k=3)
    return results                           # ← returns a list of dicts (L02!)

# ── L01: DICTIONARY — user request
user_query = {
    "question":  "What is RAG?",
    "user_id":   "user_123",
    "timestamp": "2026-03-18"
}

# ── L05: FUNCTION CALL — retrieve docs
retrieved_docs = search_knowledge(user_query["question"])

# ── L05: FUNCTION with type hints — format prompt
def format_rag_prompt(question: str, docs: list) -> str:
    context = "\n".join([doc["text"] for doc in docs])  # ← L04: loop!
    return f"Context:\n{context}\n\nQuestion: {question}"

# ── L01: DICTIONARY — store final result
result = {
    "question":   user_query["question"],
    "answer":     answer.content,
    "sources":    [doc["source"] for doc in retrieved_docs],  # ← L04: loop!
    "confidence": 0.94
}
```

**RECOGNIZE THIS:**
- `documents = [{...}]` ← L02 list of dicts
- `def search_knowledge(query: str) -> list:` ← L05 + L01 type hints
- `[doc["text"] for doc in docs]` ← L04 list comprehension (compact loop)
- `result = {...}` ← L01 dictionary

**What it does:** "Professional RAG pipeline — all L01–L06, just orchestrated together."

---

### Example 3: Function-Calling Agent — Fully Decoded

```python
# ── L02: LIST OF DICTS — tool catalog
available_tools = [
    {
        "name":        "search_database",
        "description": "Search internal knowledge base",
        "function":    search_knowledge    # ← reference to L05 function!
    },
    {
        "name":        "calculator",
        "description": "Perform math calculations",
        "function":    do_math
    }
]

# ── L05: FUNCTION — agent decision
def agent_decide(user_input: str, tools: list) -> dict:
    decision = {
        "tool_name": "search_database",
        "reasoning": "User asked a knowledge question"
    }
    return decision

# ── L03: match/case — route by TOOL NAME
def execute_tool(tool_name: str, user_input: str) -> str:
    match tool_name:
        case "search_database":
            return search_knowledge(user_input)
        case "calculator":
            return do_math(user_input)
        case _:
            return "Tool not found"

# ── EXECUTION
decision = agent_decide(user_input, available_tools)     # L05
result   = execute_tool(decision["tool_name"], user_input)  # L03 + L01

# ── L01: DICTIONARY — log the interaction
log = {
    "input":      user_input,
    "tool_used":  decision["tool_name"],
    "result":     result,
    "timestamp":  "2026-03-18"
}
```

**RECOGNIZE THIS:**
- `available_tools = [{...}]` ← L02 list of dicts (tool catalog)
- `def agent_decide(...) -> dict:` ← L05 function returning L01 dict
- `match tool_name: case "search_database":` ← L03 match/case routing
- `log = {...}` ← L01 dictionary

**What it does:** "A complete function-calling agent — still just L01–L06."

---

### Example 4: The Three Class Styles in Real Code

```python
# STYLE 1: Standard class — agent with memory (L06 standard)
class ResearchAgent:
    def __init__(self, model: str):
        self.model   = model         # ← L01: stored attribute
        self.history: list = []      # ← L02: empty list

    def ask(self, question: str) -> str:   # ← L05: method with hints
        self.history.append(question)
        return call_llm(question)

# STYLE 2: @dataclass — config container (L06 dataclass)
from dataclasses import dataclass

@dataclass
class PipelineConfig:
    model:       str   = "claude-sonnet-5-5"   # ← L01: type hint + default
    max_tokens:  int   = 1000
    temperature: float = 0.7

config = PipelineConfig()          # Python writes __init__ for you
# config.model → "claude-sonnet-5-5"

# STYLE 3: Pydantic BaseModel — validates LLM output (L06 Pydantic)
from pydantic import BaseModel

class SearchResult(BaseModel):
    answer:     str    # ← L01: required field, must be text
    confidence: float  # ← L01: must be a decimal
    sources:    list   # ← L02: must be a list

result = SearchResult(answer="RAG is...", confidence=0.94, sources=["wiki"])
# Pydantic checks types automatically — if confidence="high", it raises an error
```

**RECOGNIZE THIS — The 3-style rule:**

| You see | Means | Lesson |
|:--------|:------|:-------|
| `class Agent:` with methods | Does things, holds memory | L06 standard |
| `@dataclass class Config:` | Holds settings, no real methods | L06 @dataclass |
| `class Output(BaseModel):` | Validates data shape | L06 Pydantic |

**What it does:** "Three different use cases for classes — recognize which style by looking at the decorator and parent class."

---

### Example 5: Mystery Code — Pattern Test

```python
# Real code from a production system
conversation_history = []

system_prompt = {
    "role":    "system",
    "content": "You are a helpful AI assistant"
}
conversation_history.append(system_prompt)

user_message = {"role": "user", "content": "Hello!"}
conversation_history.append(user_message)

if len(conversation_history) > 10:
    conversation_history = conversation_history[-10:]
```

**RECOGNIZE EACH LINE:**
- `conversation_history = []` ← L02: empty list
- `system_prompt = {...}` ← L01: dictionary
- `.append(system_prompt)` ← L02: add to list
- `if len(...) > 10:` ← L03: logic gate (threshold check)
- `[-10:]` ← L02: list slicing (keep last 10)

**What it does:** "Start a conversation, add messages, trim to last 10 to save tokens."

---

### Example 6: Recognizing Type Hints in Framework Code

```python
# You will see these signatures in LangChain, CrewAI, DSPy:
def process(query: str,
            docs:  list[dict],
            config: dict,
            max_results: int = 3) -> dict:
    ...

# And these on class attributes:
class RAGAgent:
    model:       str       = "claude-sonnet-5-5"
    temperature: float     = 0.7
    history:     list[dict] = []
```

**RECOGNIZE THIS:**
- `query: str` ← parameter is text
- `docs: list[dict]` ← parameter is a list of dicts (L02 pattern!)
- `-> dict` ← function returns a dictionary (L01)
- `list[dict]` = the L02 list-of-dicts pattern with explicit type

**What it does:** "Type hints document what goes in and comes out — same L01/L02 patterns, just labeled."

---

### Example 7: The List Comprehension Inside Frameworks

```python
# You'll see these "one-liner loops" everywhere:
sources   = [doc["source"] for doc in retrieved_docs]
scores    = [doc["score"]  for doc in retrieved_docs]
top_docs  = [doc for doc in docs if doc["score"] > 0.85]

# These are just loops compressed into one line (L04!):
# sources = []
# for doc in retrieved_docs:
#     sources.append(doc["source"])
```

**RECOGNIZE THIS:**
- `[expression for item in list]` ← list comprehension = compact L04 loop
- `[expression for item in list if condition]` ← loop with a L03 filter

**What it does:** "Extract one field from every item in a list — in one line."

---

### Example 8: Complete Real-World Agent Anatomy

```python
# Full anatomy of a real agent — find all the lessons:
class TravelAgent:                                    # L06: class blueprint
    def __init__(self):
        self.client  = anthropic.Anthropic()          # L06: create instance
        self.model   = "claude-sonnet-5-5"            # L01: string variable
        self.history: list = []                       # L02: empty list

    def search(self, destination: str) -> list:       # L05: function
        results = [                                   # L02: list of dicts
            {"city": destination, "rating": 4.8},
            {"city": destination, "rating": 4.5}
        ]
        return results

    def book(self, destination: str, budget: float) -> dict:   # L05+L01
        results = self.search(destination)            # L05: method call

        if results[0]["rating"] > 4.5:                # L03: logic gate
            status = "auto-approved"
        else:
            status = "needs-review"

        self.history.append(destination)              # L02: append

        return {                                      # L01: dict result
            "destination": destination,
            "status":      status,
            "budget":      budget
        }
```

**RECOGNIZE ALL LESSONS:** L01 variables, L02 lists, L03 logic gate, L05 functions, L06 class — inside one real agent.

---

## You've Completed Pass 1!

You can now:
✓ **Decode** any LangChain / CrewAI / Anthropic code into L01–L06 patterns
✓ **Recognize** all 3 class styles (@dataclass, standard, Pydantic) on sight
✓ **Identify** list comprehensions as compact L04 loops
✓ **Read** type hints as L01 pattern extensions
✓ **Understand** why frameworks look complex (they're just fancy names over simple patterns)

**Next:**
- **Pass C (Visual):** See real AI code as labeled building blocks
- **Pass 3 (Templates):** Use the decoder ring on any framework

**Remember:** You're not memorizing. You're training your eyes to SEE patterns.

---

## Pro Tip: The 3-Second Rule

When you see unfamiliar framework code:
1. **Second 1:** Strip the import and class names — what shape is left? (dict? list? function?)
2. **Second 2:** Which lesson does that shape come from?
3. **Second 3:** What is it storing or doing? (config? results? routing?)

That's it. Frameworks are just vocabulary. The grammar is L01–L06.

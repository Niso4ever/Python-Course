# Pass C: Visual — Classes as Blueprints

**Goal:** See the structure of a class before reading the code.

> **2026 Note:** Three class styles in real AI code. All shown below.
> - Standard `class` → full agent with methods + memory (Diagrams 1-9)
> - `@dataclass` → config container, no methods (Diagram 10A)
> - Pydantic `BaseModel` → validated data from LLM/API (Diagram 10B)

---

## Diagram 1: Blueprint vs Instance

```
THE BLUEPRINT (class definition — lives in your code once)
┌─────────────────────────────────────────────────┐
│  class ConversationAgent:                        │
│                                                  │
│  __init__          ← SETUP (runs at birth)       │
│  ┌──────────────────────────────────────┐        │
│  │  self.model   = ?  (fill in later)  │        │
│  │  self.history = []  (empty at start) │        │
│  └──────────────────────────────────────┘        │
│                                                  │
│  chat()            ← TOOL 1                      │
│  reset()           ← TOOL 2                      │
└─────────────────────────────────────────────────┘
          │
          │  agent = ConversationAgent("claude-sonnet-5-5", "You are helpful")
          │
          ▼
THE INSTANCE (a real agent — created from the blueprint)
┌─────────────────────────────────────────────────┐
│  agent                                           │
│  ┌──────────────────────────────────────┐        │
│  │  self.model   = "claude-sonnet-5-5" │        │
│  │  self.history = []                   │        │
│  └──────────────────────────────────────┘        │
│                                                  │
│  agent.chat("Hello")   → Tool 1 runs             │
│  agent.reset()         → Tool 2 runs             │
└─────────────────────────────────────────────────┘
```

---

## Diagram 2: The Toolbox (What `self` Does)

```
┌─────────────────── TOOLBOX (Instance) ──────────────────┐
│                                                          │
│  STORAGE COMPARTMENT (self.x attributes)                 │
│  ┌────────────────────────────────────────────────────┐  │
│  │  self.model   = "claude-sonnet-5-5"               │  │
│  │  self.system  = "You are helpful."                │  │
│  │  self.history = [msg1, msg2, msg3, ...]           │  │
│  └────────────────────────────────────────────────────┘  │
│                          ↑                               │
│                     self connects                        │
│                     methods to storage                   │
│                          ↓                               │
│  TOOLS (methods — functions that access storage)         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  chat()      │  │  reset()     │  │  get_stats() │   │
│  │              │  │              │  │              │   │
│  │ reads:       │  │ writes:      │  │ reads:       │   │
│  │ self.model   │  │ self.history │  │ self.history │   │
│  │ self.history │  │   = []       │  │              │   │
│  │ writes:      │  │              │  │              │   │
│  │ self.history │  │              │  │              │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────┘
```

**Key insight:** `self` is the bridge. Without it, methods can't reach storage.

---

## Diagram 3: `__init__` — The Setup Factory

```
CREATION MOMENT:
agent = ConversationAgent("claude-sonnet-5-5", "You are helpful.")
                                │                     │
                                ▼                     ▼
               __init__(self, model_name,    system_prompt)
                               │                     │
                     self.model = model_name          │
                     self.system = ─────────────────▶ system_prompt
                     self.history = []    ← ALWAYS starts empty

WHAT HAPPENS:
  Input values  ──→  stored as self.x  ──→  available in ALL methods forever
```

---

## Diagram 4: How State Grows Over Time

```
TIME →

agent created:
  self.history = []
  self.call_count = 0

agent.chat("What is RAG?")
  self.history = [{"role": "user", "content": "What is RAG?"}]
  self.history = [{"role": "user", "content": "What is RAG?"},
                  {"role": "assistant", "content": "RAG is..."}]
  self.call_count = 1

agent.chat("Give me an example")
  self.history = [msg1, msg2,
                  {"role": "user", "content": "Give me an example"}]
  self.history = [msg1, msg2, msg3,
                  {"role": "assistant", "content": "Sure, here..."}]
  self.call_count = 2

print(len(agent.history))    → 4
print(agent.call_count)      → 2
```

---

## Diagram 5: Two Instances — Independent Memory

```
BLUEPRINT:  class SearchAgent
                 │
         ┌───────┴────────┐
         │                │
         ▼                ▼
  google_agent         arxiv_agent
  ┌─────────────┐      ┌─────────────┐
  │ self.engine │      │ self.engine │
  │  = "Google" │      │  = "ArXiv"  │
  │             │      │             │
  │ self.history│      │ self.history│
  │  = ["Python"]│     │  = ["LLM"]  │
  └─────────────┘      └─────────────┘
       ↑                     ↑
       │                     │
    DIFFERENT              DIFFERENT
    memory                 memory

google_agent.history   ≠   arxiv_agent.history
```

---

## Diagram 6: Class vs Function — When to Choose

```
FUNCTION (def)                     CLASS (class)
───────────────                    ────────────
Single action                      Multiple related actions
No memory needed                   Must remember state

Input → Output → done              Created once, used many times

def format_prompt(q, ctx):         class ConversationAgent:
    return f"Q: {q}\n{ctx}"            def __init__(self, model):
                                           self.history = []
Use once, forget it.                   def chat(self, msg):
                                           ...
                                   Use it for hours, remembers everything.

RULE: If you need it to REMEMBER between calls → use class
      If it's a one-shot operation → use function
```

---

## Diagram 7: RAG Agent State Machine

```
RAG AGENT STATE FLOW

Creation:
  rag = RAGAgent(my_db, my_llm, top_k=5)
  │
  │ State at birth:
  │ self.db         = my_db      (connected)
  │ self.llm        = my_llm     (connected)
  │ self.top_k      = 5          (config)
  │ self.call_count = 0          (counter)
  │ self.queries    = []         (log)
  │
  ▼
First call: rag.answer("What is RAG?")
  │
  │ State changes:
  │ self.call_count = 1
  │ self.queries    = ["What is RAG?"]
  │
  ▼
Second call: rag.answer("How does it work?")
  │
  │ State changes:
  │ self.call_count = 2
  │ self.queries    = ["What is RAG?", "How does it work?"]
  │
  ▼
Check state: rag.get_usage()
  → {"total": 2, "queries": ["What is RAG?", "How does it work?"]}
```

---

## Diagram 8: The 4-Part Class Anatomy

```
class ClassName:                      ← PART 1: Blueprint declaration

    def __init__(self, param1):       ← PART 2: Setup (runs at creation)
        self.stored = param1          ← Attribute: persists forever
        self.counter = 0              ← Attribute: initialized state
        self.log = []                 ← Attribute: empty collection

    def action(self, input):          ← PART 3: Method (a tool)
        self.counter += 1             ←   Updates state
        return process(input)         ←   Returns result

    def report(self):                 ← PART 4: Reader method
        return self.log               ←   Reads state, no changes


WHERE TO LOOK FIRST when you see a class:
  1. Class name    → tells you the role (ConversationAgent, RAGAgent, etc.)
  2. __init__      → what it stores (what it "remembers")
  3. Method names  → what it can DO (chat, search, reset, report)
  4. self.x usage  → what it reads and updates inside each method
```

---

## Diagram 9: Patterns Combined (L01–L06 Together)

```
class RAGAgent:                            ← L06: Class blueprint
    def __init__(self, db, llm):
        self.db      = db                  ← L06: Stored dependency
        self.llm     = llm                 ← L06: Stored dependency
        self.results = []                  ← L02: List initialized

    def answer(self, question):
        docs = self.db.search(question)    ← L05: Function call

        filtered = []
        for doc in docs:                   ← L04: Loop
            if doc["score"] >= 0.8:        ← L03: Condition
                filtered.append(doc)       ← L02: List append

        context = "\n".join(               ← L04: List processing
            [d["text"] for d in filtered]
        )

        answer = self.llm.invoke(context)

        self.results.append({              ← L01: Dict, L02: append
            "question": question,
            "answer":   answer,
            "sources":  len(filtered)
        })

        return answer                      ← L05: Return value
```

Every lesson builds on the previous ones. A class is the container that holds them all.

---

## Diagram 10: Three Class Styles — The Visual Difference

### 10A: @dataclass (Config Container)

```
WITHOUT @dataclass (verbose):       WITH @dataclass (clean):
──────────────────────────────      ──────────────────────────────
class AgentConfig:                  from dataclasses import dataclass
    def __init__(self,
        model,                      @dataclass
        temperature=0.7,            class AgentConfig:
        max_tokens=1000             │   model: str           ← required
    ):                              │   temperature: float = 0.7
        self.model = model          │   max_tokens: int = 1000
        self.temperature = temp     │
        self.max_tokens = tokens    └── Python writes __init__ for you

Both create the same object:
  config = AgentConfig(model="claude-sonnet-5-5")
  config.model         → "claude-sonnet-5-5"
  config.temperature   → 0.7

Shape rule: @dataclass = fields only (no def methods, no self.x = ...)
```

### 10B: Pydantic BaseModel (Type Validator)

```
SHAPE:
class SomeName(BaseModel):       ← (BaseModel) is the tell
    field1: type                 ← required field
    field2: type = default       ← optional field
    field3: type | None = None   ← nullable optional

WHAT IT DOES (at creation time):
  Input → Pydantic checks types → ✓ creates object / ✗ raises error

COMPARE:
  Regular class: wrong type → silently stored (bug later)
  Pydantic:      wrong type → error immediately (fail fast)

VISUAL FLOW:
  LLM output (raw string)
        │
        ▼
  AgentResponse(answer=..., confidence=..., sources=[...])
        │
        ▼ Pydantic validates types
        │
   ┌────┴──────────────────────────────┐
   │ ✓ Valid → structured object       │
   │ ✗ Invalid type → ValidationError  │
   └───────────────────────────────────┘
```

### 10C: Side-by-Side Comparison

```
Standard class:          @dataclass:              Pydantic BaseModel:
─────────────────        ─────────────────        ─────────────────────
class Agent:             @dataclass               class Output(BaseModel):
  def __init__(self,     class Config:                answer: str
      db, llm):              model: str               confidence: float
    self.db = db             temp: float=0.7          sources: list[str]
    self.llm = llm           tokens: int=1000
    self.hist = []
  def chat(self, msg):
    ...

Has methods?     YES          NO                       NO
Validates types? NO           NO (just labels)         YES (runtime)
Writes __init__? MANUAL       AUTO                     AUTO
Use for:         Doing things Holding config           Validating data
```

---

**Next:** See [PASS3_TEMPLATES.md](PASS3_TEMPLATES.md) for all available class templates.

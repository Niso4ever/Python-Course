"""
═══════════════════════════════════════════════════════════════════
LESSON 06 CHEATSHEET: Classes as Blueprints
═══════════════════════════════════════════════════════════════════

Quick reference for class patterns in AI systems.
Keep this open while reading code!

Python 3.13 / 2026 — Three class styles in real AI code:
  1. Standard class     → agent with methods + memory (coffee machine)
  2. @dataclass         → config/dependency container (spec sheet)
  3. Pydantic BaseModel → validated data from LLM/API (quality inspector)

═══════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════
# 1. DEFINE A CLASS
# ═══════════════════════════════════════════════════════════

class MyAgent:
    def __init__(self, param):          # Setup — runs at creation
        self.stored = param             # Attribute — persists forever
        self.counter = 0                # Counter — starts at zero
        self.log = []                   # List — grows over time

    def action(self, input):            # Method — a tool
        self.counter += 1               # Update state
        return f"Result: {input}"       # Return output

    def report(self):                   # Reader method
        return {"count": self.counter, "log": self.log}


# ═══════════════════════════════════════════════════════════
# 2. CREATE AN INSTANCE
# ═══════════════════════════════════════════════════════════

agent = MyAgent("config_value")         # Instance from blueprint

# Two instances — independent memory:
agent_a = MyAgent("A")
agent_b = MyAgent("B")
# agent_a and agent_b do NOT share data


# ═══════════════════════════════════════════════════════════
# 3. CALL A METHOD
# ═══════════════════════════════════════════════════════════

result = agent.action("hello")          # instance.method(args)
stats  = agent.report()                 # Read state with no args


# ═══════════════════════════════════════════════════════════
# 4. READ AN ATTRIBUTE
# ═══════════════════════════════════════════════════════════

print(agent.counter)                    # Direct attribute access
print(agent.log)                        # Read the stored list
print(agent.stored)                     # Read stored config


# ═══════════════════════════════════════════════════════════
# 5. COMMON AI CLASS PATTERNS
# ═══════════════════════════════════════════════════════════

# Pattern 1: Agent with Memory
class AgentWithMemory:
    def __init__(self, config):
        self.config  = config
        self.history = []               # Conversation or query log
        self.stats   = {"calls": 0, "cost": 0.0}

    def run(self, input):
        self.history.append(input)
        self.stats["calls"] += 1
        return f"Processed: {input}"


# Pattern 2: Agent with External Components
class AgentWithComponents:
    def __init__(self, db, llm, top_k=3):
        self.db    = db                 # Database connection
        self.llm   = llm               # LLM client
        self.top_k = top_k             # Config remembered forever

    def answer(self, question):
        docs   = self.db.search(question, top_k=self.top_k)
        return self.llm.invoke(docs)


# Pattern 3: Config Manager (Singleton)
class Config:
    def __init__(self):
        self.model       = "claude-sonnet-5-5"
        self.temperature = 0.7
        self.max_tokens  = 1000
        self.thresholds  = {"confidence": 0.85, "toxicity": 0.20}

    def is_confident(self, score):
        return score >= self.thresholds["confidence"]


# Pattern 4: Multi-Model Router
class ModelRouter:
    def __init__(self):
        self.models = {
            "fast":     "claude-haiku-5-5",
            "balanced": "claude-sonnet-5-5",
            "powerful": "claude-opus-5-5"
        }
        self.usage = {"fast": 0, "balanced": 0, "powerful": 0}

    def call(self, prompt, mode="balanced"):
        self.usage[mode] += 1
        model = self.models[mode]
        return call_llm(prompt, model=model)   # noqa (placeholder)


# Pattern 5: Tool Registry
class ToolAgent:
    def __init__(self, tools):
        self.tools   = tools            # List of tool objects
        self.results = []

    def run(self, task):
        for tool in self.tools:         # L04: loop
            if tool.can_handle(task):   # L03: condition
                result = tool.execute(task)
                self.results.append(result)
                return result
        return "No tool matched"


# ═══════════════════════════════════════════════════════════
# 6. SELF — PLAIN ENGLISH EXPLANATION
# ═══════════════════════════════════════════════════════════

"""
`self` = "this specific instance"

When you write:   self.history = []
You mean:         "MY history list (not any other agent's)"

When you write:   self.history.append(item)
You mean:         "Add to MY history list"

When you write:   def chat(self, input):
You mean:         "This method belongs to this instance"

WITHOUT self → methods can't reach the stored data.
WITH self    → every method can read and update any attribute.
"""


# ═══════════════════════════════════════════════════════════
# 7. CLASS vs FUNCTION DECISION TABLE
# ═══════════════════════════════════════════════════════════

"""
Use def (Function) when:          Use class (Class) when:
─────────────────────────────     ─────────────────────────────
Single operation                  Multiple related operations
No memory between calls           Must remember state
Simple input → output             Agent with config + tools
One-time use                      Reusable module

EXAMPLES:
def format_prompt(q, ctx):        class ConversationAgent:
    return f"Q: {q}\n{ctx}"           def __init__(self, model):
                                          self.history = []
                                      def chat(self, msg):
                                          ...

→ Function: formats once, done    → Class: remembers everything

─────────────────────────────────────────────────────────────
2026 ADDITION: @dataclass vs Pydantic vs standard class
─────────────────────────────────────────────────────────────
from dataclasses import dataclass
from pydantic import BaseModel

@dataclass                        class AgentConfig:
class AgentConfig:                    standard = verbose, full control
    model: str                        @dataclass = clean, for internal data
    temperature: float = 0.7          Pydantic = validates type at runtime
    max_tokens: int = 1000

class AgentOutput(BaseModel):     # Pydantic — validates LLM output
    answer: str
    confidence: float
    sources: list[str]

RULE:
  Agent that DOES things         → standard class
  Container that HOLDS config    → @dataclass
  Data arriving from OUTSIDE     → Pydantic BaseModel
"""


# ═══════════════════════════════════════════════════════════
# 8. 3-SECOND CLASS READ
# ═══════════════════════════════════════════════════════════

"""
When you see a class:
1. READ the class name       → tells you WHAT kind of agent
2. CHECK __init__ attributes → tells you WHAT it stores/remembers
3. SCAN method names         → tells you WHAT tools it has

Example:
    class RAGAgent:                      ← "Retrieval agent"
        def __init__(self, db, llm):
            self.db    = db              ← holds a database
            self.llm   = llm            ← holds an LLM
            self.count = 0              ← tracks call count
        def answer(self, q):            ← can answer questions
        def get_usage(self):            ← can report usage

Read: 3 seconds. Done.
"""


# ═══════════════════════════════════════════════════════════
# 9. ATTRIBUTE PATTERNS AT A GLANCE
# ═══════════════════════════════════════════════════════════

"""
self.name = "value"           → String config (model name, API key)
self.count = 0                → Counter (starts at 0, += 1 later)
self.history = []             → Growing list (append on each call)
self.config = {}              → Settings dict
self.db = db_param            → Dependency (passed in, stored)
self.llm = llm_param          → Dependency (passed in, stored)
self.flag = False             → Boolean state (True/False toggle)
self.threshold = 0.85         → Numeric config (used in conditions)
"""


# ═══════════════════════════════════════════════════════════
# 10. NOVEL PATTERNS — What you'll see in real 2026 AI code
# ═══════════════════════════════════════════════════════════

# ── A. @dataclass with __post_init__ ─────────────────────────────────────────
# Use when: you need to compute or validate AFTER fields are set
from dataclasses import dataclass, field

@dataclass
class AgentConfig:
    model: str
    temperature: float = 0.7
    max_tokens: int = 1024
    model_family: str = field(init=False)   # ← computed, NOT passed in

    def __post_init__(self) -> None:
        # Runs automatically after __init__ sets the fields
        if "haiku" in self.model:
            self.model_family = "haiku"
        elif "sonnet" in self.model:
            self.model_family = "sonnet"
        else:
            self.model_family = "opus"

cfg = AgentConfig(model="claude-sonnet-5-5")
print(cfg.model_family)   # → "sonnet"  (computed, not passed)


# ── B. Frozen models (immutable config) ──────────────────────────────────────
# Use when: config should never change after creation (prevents bugs)
from dataclasses import dataclass
from pydantic import BaseModel

@dataclass(frozen=True)      # ← dataclass: immutable
class PipelineConfig:
    model: str = "claude-sonnet-5-5"
    top_k: int = 5

# cfg.model = "gpt-4"  ← raises FrozenInstanceError

from pydantic import ConfigDict

class StrictConfig(BaseModel):
    model_config = ConfigDict(frozen=True)   # ← Pydantic v2: immutable
    model: str
    temperature: float = 0.7

# Rule: production configs are almost always frozen


# ── C. Pydantic v2 field_validator ────────────────────────────────────────────
# Use when: a single field needs custom validation logic
from pydantic import BaseModel, Field, field_validator

class SearchInput(BaseModel):
    query: str = Field(..., description="Search query")
    limit: int = Field(10, ge=1, le=100, description="Max results")

    @field_validator("query")
    @classmethod
    def query_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("query cannot be blank")
        return v.strip()   # ← also normalizes: strips whitespace

# vs model_validator (cross-field logic):
from pydantic import model_validator

class DateRange(BaseModel):
    start: str
    end: str

    @model_validator(mode="after")
    def end_after_start(self) -> "DateRange":
        if self.end < self.start:
            raise ValueError("end must be after start")
        return self

# Rule:  one field logic  → @field_validator
#        cross-field logic → @model_validator(mode="after")


# ── D. Pydantic v2 vs v1 — What you'll see in older code ─────────────────────
"""
v1 pattern (pre-2023, you'll see in older code)   v2 pattern (2023+, use this)
────────────────────────────────────────────────  ────────────────────────────
obj.schema()                                      obj.model_json_schema()
obj.parse_obj(data)                               obj.model_validate(data)
obj.dict()                                        obj.model_dump()
@validator                                        @field_validator
class Config: ...                                 model_config = ConfigDict(...)

This course uses Pydantic v2 throughout.
If you see .schema() or .dict() → that's v1, still runs but deprecated.
"""


# ═══════════════════════════════════════════════════════════
# 11. TEMPLATE QUICK LINKS
# ═══════════════════════════════════════════════════════════

"""
Available templates in this folder:
- template_conversation_agent.py  → Chat with memory (4 variations)
- template_rag_agent.py           → RAG with tracking (4 variations)
- template_multi_tool_agent.py    → Model router + tool selector (4 variations)
"""


# ═══════════════════════════════════════════════════════════
# END OF CHEATSHEET
# ═══════════════════════════════════════════════════════════

print("Keep this cheatsheet open while reading AI code!")
print("When you see class + self → it's a stateful agent.")

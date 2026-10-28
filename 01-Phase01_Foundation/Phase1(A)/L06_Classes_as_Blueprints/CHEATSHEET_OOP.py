"""
═══════════════════════════════════════════════════════════════════
L06 PART 0 CHEATSHEET: Object-Oriented Programming for AI
═══════════════════════════════════════════════════════════════════

Quick reference for OOP concepts.
Keep this open while reading L06 and real AI code!

One-sentence summary:
  Class = Factory blueprint.  Instance = Product.
  Attributes = What it stores.  Methods = What it can do.
  self = This specific product.

External refs:
  https://docs.python.org/3/tutorial/classes.html
  https://realpython.com/python3-object-oriented-programming/

═══════════════════════════════════════════════════════════════════
"""


# ═══════════════════════════════════════════════════════════
# 1. CLASS ANATOMY — Complete labeled diagram
# ═══════════════════════════════════════════════════════════

class ConversationAgent:                   # ← BLOCK 1: Factory declaration
                                           #   "I define a factory for ConversationAgent objects"

    def __init__(self, model_name):        # ← BLOCK 2: Constructor (runs at birth)
        self.model   = model_name          # ← ATTRIBUTE: stored characteristic
        self.history = []                  # ← ATTRIBUTE: starts empty, grows with use
        self.turns   = 0                   # ← ATTRIBUTE: counter starting at zero

    def chat(self, user_input):            # ← BLOCK 4: Method (an action)
        self.history.append(user_input)    #   reads + updates own attribute
        self.turns += 1                    #   updates own counter
        return f"Response to: {user_input}"  # returns result


# ─────────────────────────────────────────
# CREATING INSTANCES (running the factory)
# ─────────────────────────────────────────

agent = ConversationAgent("claude-sonnet-5-5")
#  ↑    ← variable name    ↑
#  │                       └── argument → goes to model_name in __init__
#  └── agent is the INSTANCE (the product)


# ─────────────────────────────────────────
# CALLING METHODS (using the product)
# ─────────────────────────────────────────

response = agent.chat("What is RAG?")
#                ↑     ↑
#            method    argument
# → response = "Response to: What is RAG?"


# ─────────────────────────────────────────
# READING ATTRIBUTES (inspecting the product)
# ─────────────────────────────────────────

print(agent.model)    # → "claude-sonnet-5-5"
print(agent.history)  # → ["What is RAG?"]
print(agent.turns)    # → 1


# ═══════════════════════════════════════════════════════════
# 2. THE 4 BUILDING BLOCKS
# ═══════════════════════════════════════════════════════════

# BLOCK 1: Factory Declaration
class AgentName:          # defines a factory
    pass                  # (empty for now)

# BLOCK 2: Constructor (__init__)
class AgentName:
    def __init__(self, param):   # runs ONCE at creation
        pass                     # param comes from: AgentName("value")

# BLOCK 3: Attributes (self.x)
class AgentName:
    def __init__(self, model):
        self.model   = model   # config from input
        self.history = []      # starts empty
        self.count   = 0       # starts at zero
        self.client  = None    # will be set later

# BLOCK 4: Methods (def action(self, ...))
class AgentName:
    def do_something(self, input):   # has self as first param
        self.count += 1              # can update own state
        return process(input)        # returns result


# ═══════════════════════════════════════════════════════════
# 3. SELF — PLAIN ENGLISH
# ═══════════════════════════════════════════════════════════

"""
self = "this specific instance"

When you call:   agent.chat("hello")
Python does:     ConversationAgent.chat(agent, "hello")
                                        ↑
                                        this is self

self.history   = "MY history list"   (not anyone else's)
self.model     = "MY model name"
self.count     = "MY call counter"

Without self → methods can't reach the stored attributes.
With self    → every method can read and update any attribute.
"""


# ═══════════════════════════════════════════════════════════
# 4. MULTIPLE INSTANCES — INDEPENDENT MEMORY
# ═══════════════════════════════════════════════════════════

support  = ConversationAgent("claude-sonnet-5-5")
research = ConversationAgent("claude-opus-5-5")

support.chat("My order is missing")
research.chat("What is transformer architecture?")

print(support.history)   # → ["My order is missing"]
print(research.history)  # → ["What is transformer architecture?"]
# These NEVER share data — completely independent


# ═══════════════════════════════════════════════════════════
# 5. COMMON ATTRIBUTE PATTERNS (what you'll see in AI code)
# ═══════════════════════════════════════════════════════════

"""
self.model = "claude-sonnet-5-5"   → String config (LLM name)
self.history = []                   → Growing list (conversation)
self.count = 0                      → Counter (API calls made)
self.config = {"temp": 0.7}         → Settings dict
self.db = db_param                  → Dependency (passed in)
self.llm = llm_client               → Dependency (passed in)
self.flag = False                   → Boolean state
self.threshold = 0.85               → Numeric config
"""


# ═══════════════════════════════════════════════════════════
# 6. COMMON METHOD PATTERNS (what methods do)
# ═══════════════════════════════════════════════════════════

"""
def chat(self, msg):            → ACTION: takes input, returns output
    self.history.append(msg)    → UPDATES own attribute
    return call_llm(...)        → RETURNS result

def reset(self):                → ACTION: no input, modifies state
    self.history = []           → CLEARS own attribute

def get_stats(self):            → READER: returns attribute values
    return {"count": self.count, "history": self.history}

def is_ready(self):             → CHECKER: returns bool
    return self.count > 0
"""


# ═══════════════════════════════════════════════════════════
# 7. CLASS vs FUNCTION — DECISION TABLE
# ═══════════════════════════════════════════════════════════

"""
Use def (Function) when:              Use class (Class) when:
────────────────────────────          ────────────────────────────
Single operation, one-time            Multiple related operations
No memory needed                      Must remember state
Input → Output → done                 Agent reused across many calls
Simple transformation                 Holds config + external deps

Examples:
  def format_prompt(q, ctx):          class ConversationAgent:
      return f"Q: {q}\n{ctx}"             def __init__(self, model):
                                              self.history = []
  def count_tokens(text: str) -> int:      def chat(self, msg):
      return len(text) // 4                    self.history.append(msg)
                                               return call_llm(...)

ONE QUESTION TO DECIDE:
  Does it need to REMEMBER between calls?
  YES → class
  NO  → function (def)
"""


# ═══════════════════════════════════════════════════════════
# 8. 2026 ADDITION: THREE CLASS STYLES
# ═══════════════════════════════════════════════════════════

# Style 1: Standard class (full agent with methods + memory)
class RAGAgent:
    def __init__(self, db, llm):
        self.db  = db
        self.llm = llm
    def answer(self, question):
        docs = self.db.search(question)
        return self.llm.invoke(docs)

# Style 2: @dataclass (config container — no methods needed)
from dataclasses import dataclass

@dataclass
class AgentConfig:
    model: str
    temperature: float = 0.7
    max_tokens: int    = 1000

config = AgentConfig(model="claude-sonnet-5-5")
print(config.model)        # → "claude-sonnet-5-5"
print(config.temperature)  # → 0.7

# Style 3: Pydantic BaseModel (validates data from LLM/API)
from pydantic import BaseModel

class AgentResponse(BaseModel):
    answer: str
    confidence: float
    sources: list[str]

response = AgentResponse(answer="RAG is...", confidence=0.92, sources=["kb"])
print(response.answer)     # → "RAG is..."

"""
RULE:
  Agent that DOES things         → standard class
  Container that HOLDS config    → @dataclass
  Data arriving from OUTSIDE     → Pydantic BaseModel
"""


# ═══════════════════════════════════════════════════════════
# 9. TYPE HINTS ON __init__ — 2026 STANDARD
# ═══════════════════════════════════════════════════════════

# You will see THIS in all real AI code:
class ConversationAgent:
    def __init__(self, model: str, max_tokens: int = 1024) -> None:
        self.model      = model
        self.max_tokens = max_tokens
        self.history: list[dict] = []   # ← typed attribute hint

# NOT this (no hints = older code or sloppy code):
class ConversationAgent:
    def __init__(self, model, max_tokens=1024):   # ← no hints
        ...

# Rule: every __init__ in 2026 code has:
#   params typed  → def __init__(self, model: str, k: int = 5) -> None:
#   return None   → __init__ always returns None, always annotate it
#   attributes    → self.history: list[dict] = []  (optional but clean)


# ═══════════════════════════════════════════════════════════
# 10. INHERITANCE — THE PATTERN BEHIND EVERY AI FRAMEWORK
# ═══════════════════════════════════════════════════════════

"""
INHERITANCE: "A class built on top of another class"

Syntax:  class Child(Parent):
Meaning: Child gets ALL of Parent's methods and attributes,
         plus its own additions or overrides.

YOU SEE THIS EVERYWHERE in AI code:
"""

# Pydantic BaseModel (L06, Phase 3)
from pydantic import BaseModel

class AgentResponse(BaseModel):        # ← AgentResponse inherits BaseModel
    answer: str                        #   BaseModel provides: .model_dump(),
    confidence: float                  #   .model_json_schema(), type validation
    sources: list[str]                 #   YOU provide: the field definitions

# DSPy Signature (L16, Phase 4)
# import dspy
# class Summarize(dspy.Signature):     # ← Summarize inherits dspy.Signature
#     document: str = dspy.InputField()  #   dspy.Signature provides: optimizer hooks
#     summary: str = dspy.OutputField()  #   YOU provide: the field declarations

# Agent SDK pattern
# class MyAgent(BaseAgent):            # ← MyAgent inherits BaseAgent
#     def run(self, task): ...         #   override parent method

"""
3-STEP INHERITANCE READ:

1. class X(Parent)  → X inherits everything from Parent
2. def __init__:    → if present, sets up additional attributes
3. def method:      → if present, extends or overrides Parent behavior

Example: class SearchInput(BaseModel)
  → BaseModel provides validation and .model_json_schema()
  → SearchInput adds: query: str, limit: int
  → Result: SearchInput validates its fields automatically

YOU DON'T NEED TO WRITE INHERITANCE — you need to RECOGNIZE it.
When you see class X(Y): → ask "what does Y provide that X uses?"
"""


# ═══════════════════════════════════════════════════════════
# 11. 3-SECOND CLASS READ — Use this every time you see a class
# ═══════════════════════════════════════════════════════════

"""
When you see any class in AI code:

1. READ THE CLASS NAME       → What kind of agent/object is this?
2. CHECK __init__ ATTRIBUTES → What does it store? (its memory)
3. SCAN METHOD NAMES         → What can it do? (its tools)

That's it. 3 seconds.

Example:
  class RAGAgent:                       ← "Retrieval agent"
      def __init__(self, db, llm):
          self.db         = db          ← holds a database
          self.llm        = llm         ← holds an LLM
          self.call_count = 0           ← tracks usage
      def answer(self, question):       ← can answer questions
      def get_usage(self):              ← can report usage

Read: "RAG agent. Holds db + LLM. Tracks calls. Can answer and report."
Time: 3 seconds.
"""


# ═══════════════════════════════════════════════════════════
# END OF CHEATSHEET
# ═══════════════════════════════════════════════════════════

print("OOP Cheatsheet loaded. Keep this open while reading AI code.")
print("Remember: class = factory, instance = product, self = this product.")

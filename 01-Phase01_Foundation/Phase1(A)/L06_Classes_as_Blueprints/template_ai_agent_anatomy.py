"""
TEMPLATE: AI Agent Anatomy — Every OOP Concept Labeled
========================================================
Purpose: See EVERY object-oriented concept in one real file.
         Run this file and watch state change in real time.

Instructions:
  1. Read each labeled section top to bottom
  2. Notice how state builds up with each method call
  3. Notice how two instances are completely independent
  4. Then go to L06 — you'll recognize everything

OOP Concepts shown here:
  ✓ Class definition (factory declaration)
  ✓ Constructor __init__ (setup at birth)
  ✓ Attributes (self.x — stored characteristics)
  ✓ Methods (def action(self, ...) — stored actions)
  ✓ Instance creation (running the factory)
  ✓ Method calls (using the product)
  ✓ Multiple instances (independent memory)
  ✓ State changes over time (memory in action)
  ✓ Reading attributes (inspecting the product)
  ✓ @dataclass pattern (2026 config container)
  ✓ Pydantic BaseModel pattern (2026 validator)
"""


# ═══════════════════════════════════════════════════════════════════════
#
#  PART A: STANDARD CLASS — Full Agent with Methods and Memory
#
#  This is the "coffee machine" pattern. The class is the blueprint.
#  Each instance is an actual machine with its own beans loaded.
#
# ═══════════════════════════════════════════════════════════════════════

# ┌─────────────────────────────────────────────────────────────────────┐
# │  BLOCK 1: Factory Declaration                                        │
# │  "I am creating a blueprint. This factory will make agents."         │
# └─────────────────────────────────────────────────────────────────────┘
class ConversationAgent:
    """
    A blueprint for conversation agents.
    Each instance remembers its own conversation history.

    OOP vocabulary for this class:
      - ConversationAgent  = the CLASS (factory blueprint)
      - agent_1, agent_2   = INSTANCES (products from the factory)
      - self.history       = ATTRIBUTE (stored characteristic)
      - chat(), reset()    = METHODS (actions the instance can take)
    """

    # ┌───────────────────────────────────────────────────────────────┐
    # │  BLOCK 2: Constructor — runs ONCE when instance is created     │
    # │  __init__ = "initialize" — set up this new product at birth    │
    # └───────────────────────────────────────────────────────────────┘
    def __init__(self, model_name: str, system_prompt: str):
        #
        # ┌───────────────────────────────────────────────────────────┐
        # │  BLOCK 3: ATTRIBUTES — stored characteristics              │
        # │  self = "this specific instance"                           │
        # │  self.x = value → stored FOREVER on this instance          │
        # └───────────────────────────────────────────────────────────┘
        self.model   = model_name     # ATTRIBUTE: which LLM to use
        self.system  = system_prompt  # ATTRIBUTE: the agent's persona
        self.history = []             # ATTRIBUTE: starts empty — grows with each turn
        self.turns   = 0              # ATTRIBUTE: counter — starts at 0
        self.total_tokens = 0         # ATTRIBUTE: tracks usage across calls


    # ┌───────────────────────────────────────────────────────────────┐
    # │  BLOCK 4: METHODS — actions the instance can perform           │
    # │  Every method receives self as first param (automatically)     │
    # │  self gives the method access to all stored attributes         │
    # └───────────────────────────────────────────────────────────────┘

    def chat(self, user_input: str) -> str:
        """
        METHOD: Send a message and get a response.
        - Reads self.model and self.history (accessing own attributes)
        - Updates self.history and self.turns (changing own state)
        - Returns a string response
        """
        # Build the message (using self.system for context)
        message = {"role": "user", "content": user_input}
        self.history.append(message)     # ← UPDATING own attribute

        # Simulate LLM call (replace with real API in production)
        llm_response = f"[{self.model}] Responding to: {user_input}"

        # Store the assistant response
        self.history.append({"role": "assistant", "content": llm_response})
        self.turns += 1                  # ← UPDATING own counter

        # Estimate tokens (simplified)
        self.total_tokens += len(user_input.split()) * 2
        return llm_response

    def reset(self) -> None:
        """
        METHOD: Clear memory and start fresh.
        - No input needed (just self)
        - Modifies self.history and self.turns
        """
        self.history = []               # ← RESETTING own attribute
        self.turns   = 0                # ← RESETTING own counter
        # Note: self.model and self.system are kept (config, not state)

    def get_stats(self) -> dict:
        """
        METHOD: Reader — returns info WITHOUT changing state.
        - Only reads attributes, does not modify them
        """
        return {
            "model":        self.model,
            "turns":        self.turns,
            "total_tokens": self.total_tokens,
            "history_len":  len(self.history)
        }

    def summarize_history(self) -> str:
        """
        METHOD: Returns a human-readable conversation summary.
        """
        if not self.history:
            return "No conversation yet."
        lines = []
        for msg in self.history:
            role    = msg["role"].upper()
            content = msg["content"][:50]
            lines.append(f"  [{role}] {content}...")
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════
#
#  PART B: CREATING INSTANCES (Running the Factory)
#
#  Syntax: variable = ClassName(arguments)
#  Each instance is INDEPENDENT — they never share attributes
#
# ═══════════════════════════════════════════════════════════════════════

# Create INSTANCE 1 — a customer support agent
support_agent = ConversationAgent(
    model_name    = "claude-sonnet-5-5",
    system_prompt = "You handle customer support for an e-commerce company."
)
#  support_agent is now an OBJECT (instance)
#  support_agent.model   = "claude-sonnet-5-5"
#  support_agent.history = []        ← empty at birth
#  support_agent.turns   = 0         ← zero at birth

# Create INSTANCE 2 — a research agent
research_agent = ConversationAgent(
    model_name    = "claude-opus-5-5",
    system_prompt = "You are a research analyst specializing in AI papers."
)
#  research_agent is a COMPLETELY DIFFERENT object
#  Same blueprint — different product, different memory


# ═══════════════════════════════════════════════════════════════════════
#
#  PART C: CALLING METHODS (Using the Products)
#
#  Syntax: instance.method_name(arguments)
#  Each call can update the instance's attributes
#
# ═══════════════════════════════════════════════════════════════════════

print("=" * 60)
print("DEMO: Two independent agents from the same blueprint")
print("=" * 60)

# ── AGENT 1: Support conversation
print("\n--- Support Agent ---")
r1 = support_agent.chat("My order #12345 hasn't arrived yet.")
print(f"Turn 1: {r1}")

r2 = support_agent.chat("It's been 10 days. Can you check?")
print(f"Turn 2: {r2}")

# ── AGENT 2: Research conversation
print("\n--- Research Agent ---")
r3 = research_agent.chat("What is Retrieval-Augmented Generation?")
print(f"Turn 1: {r3}")

# ── Show that attributes changed
print("\n--- State After Use ---")
print(f"Support agent turns:   {support_agent.turns}")   # → 2
print(f"Research agent turns:  {research_agent.turns}")  # → 1
print(f"Support history length: {len(support_agent.history)}")  # → 4
print(f"Research history length: {len(research_agent.history)}") # → 2

# ── KEY DEMO: Independent memory
print("\n--- PROOF: Independent Memory ---")
print("support_agent.history:", [m["role"] for m in support_agent.history])
print("research_agent.history:", [m["role"] for m in research_agent.history])
print("These lists are DIFFERENT objects — they never share data.")

# ── Read stats
print("\n--- Support Agent Stats ---")
stats = support_agent.get_stats()
for key, val in stats.items():
    print(f"  {key}: {val}")

# ── Reset one agent (the other is unaffected)
print("\n--- Reset Support Agent ---")
support_agent.reset()
print(f"Support turns after reset: {support_agent.turns}")    # → 0
print(f"Research turns unchanged:  {research_agent.turns}")   # → 1
print("Reset only affects the instance it was called on.")

# ── Show conversation history
print("\n--- Research Agent History ---")
print(research_agent.summarize_history())


# ═══════════════════════════════════════════════════════════════════════
#
#  PART D: @dataclass — Config Container (2026 Pattern)
#
#  Use when: passing configuration between components cleanly
#  Python writes __init__ automatically — no need to write self.x = ...
#
# ═══════════════════════════════════════════════════════════════════════

from dataclasses import dataclass

@dataclass                           # ← decorator that writes __init__ for you
class AgentConfig:
    """
    A config container using @dataclass.
    Compare to standard class — no def __init__ needed.
    Fields are defined as: field_name: type = default
    """
    model: str                       # REQUIRED — no default
    temperature: float = 0.7         # OPTIONAL — has default
    max_tokens: int    = 1000        # OPTIONAL — has default
    top_k: int         = 3           # OPTIONAL — has default

print("\n" + "=" * 60)
print("DEMO: @dataclass config container")
print("=" * 60)

# Create instance exactly the same way as a standard class:
config = AgentConfig(model="claude-sonnet-5-5")
print(f"model:       {config.model}")        # → "claude-sonnet-5-5"
print(f"temperature: {config.temperature}")  # → 0.7
print(f"max_tokens:  {config.max_tokens}")   # → 1000

# Customize specific fields:
custom_config = AgentConfig(model="claude-opus-5-5", temperature=0.3)
print(f"\ncustom model:       {custom_config.model}")       # → "claude-opus-5-5"
print(f"custom temperature: {custom_config.temperature}")  # → 0.3


# ═══════════════════════════════════════════════════════════════════════
#
#  PART E: Pydantic BaseModel — LLM Output Validator (2026 Pattern)
#
#  Use when: data comes FROM OUTSIDE (LLM response, API, user input)
#  Validates types at creation — wrong type → error immediately
#
# ═══════════════════════════════════════════════════════════════════════

from pydantic import BaseModel

class AgentResponse(BaseModel):      # ← (BaseModel) is the tell
    """
    Validates structured output from an LLM.
    If types are wrong → raises ValidationError immediately.
    """
    answer: str                      # REQUIRED field
    confidence: float                # REQUIRED field
    sources: list[str]               # REQUIRED field
    reasoning: str | None = None     # OPTIONAL — can be None or str

print("\n" + "=" * 60)
print("DEMO: Pydantic BaseModel validator")
print("=" * 60)

# Create validated response:
llm_output = AgentResponse(
    answer     = "RAG stands for Retrieval-Augmented Generation.",
    confidence = 0.92,
    sources    = ["internal_kb", "wikipedia"]
)
print(f"answer:     {llm_output.answer}")
print(f"confidence: {llm_output.confidence}")
print(f"sources:    {llm_output.sources}")
print(f"reasoning:  {llm_output.reasoning}")  # → None (not provided)

# Wrong type would raise an error:
# AgentResponse(answer="x", confidence="not-a-number", sources=[])
# ↑ ValidationError: confidence must be float, not str


# ═══════════════════════════════════════════════════════════════════════
#
#  PART F: SIDE-BY-SIDE COMPARISON
#
#  All three styles — recognize each on sight
#
# ═══════════════════════════════════════════════════════════════════════

print("\n" + "=" * 60)
print("SUMMARY: Three class styles in 2026 AI code")
print("=" * 60)
print("""
Standard class:              @dataclass:               Pydantic BaseModel:
────────────────             ─────────────             ──────────────────────
class Agent:                 @dataclass                class Response(BaseModel):
  def __init__(self, db):    class Config:                 answer: str
      self.db = db               model: str                confidence: float
      self.history = []          temp: float = 0.7         sources: list[str]
  def chat(self, msg):       ...
      ...
                             config = Config(...)      resp = Response(...)
Does things + has memory     Holds config cleanly      Validates LLM output
Has methods                  No methods needed         Raises error if wrong type
Write __init__ manually      Python writes it          Python writes it
""")

print("Run this file again after reading PASS0_OOP_FUNDAMENTALS.md")
print("Then move to L06_Classes_as_Blueprints/ for real patterns.")

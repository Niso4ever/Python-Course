# OOP Fundamentals for AI
## The Factory Model — Understanding Classes from First Principles

**Goal:** By the end of this lesson, you will have a clear mental model for every class you encounter in AI code.

---

## Part 1: The Problem — Why Functions Aren't Enough

You already know functions (L05). A function takes input, does something, returns output — then **forgets everything**.

```python
def chat(user_input):
    return call_llm(user_input)
    # → After this returns, NOTHING is remembered
    # → Next call starts from zero
```

For an AI agent, forgetting is a bug. Agents need to **remember**:
- Conversation history (every message sent and received)
- Configuration (which model, which API key)
- Stats (how many calls made, total cost)
- State (is it initialized? is it connected?)

**A function cannot do this.** A class can.

---

## Part 2: The Factory Model

The easiest way to understand OOP is the **Factory Model**.

```
FACTORY DESIGN (Class)        THE PRODUCTS (Instances)
─────────────────────         ────────────────────────
ConversationAgent             agent_1 = ConversationAgent("claude-sonnet-5-5", "You are helpful.")
  blueprint for all agents    agent_2 = ConversationAgent("claude-opus-5-5", "You are a researcher.")
  defined ONCE                Both are INDEPENDENT — agent_1 and agent_2 don't share history
  never changes               Each product has its OWN memory, its OWN config
```

**Three things to always remember:**

| Concept | Factory Analogy | Python |
|:--------|:----------------|:-------|
| **Class** | The factory's design/blueprint | `class ConversationAgent:` |
| **Instance** | One product made by the factory | `agent = ConversationAgent(...)` |
| **`self`** | Each product saying "I" / "my" | `self.history` = MY history |

---

## Part 3: The 4 Building Blocks

Every class is built from the same 4 blocks. Learn to recognize each one.

---

### Block 1 — The Factory Declaration (class name)

```python
class ConversationAgent:
```

**What it means:** "I am defining a factory. It will make `ConversationAgent` objects."

**Pattern:** `class FactoryName:` — always starts with a capital letter by convention.

**In AI code you'll see:**
- `class RAGAgent:` — factory for retrieval-augmented agents
- `class ToolAgent:` — factory for agents with tools
- `class AgentConfig:` — factory for config containers

---

### Block 2 — The Constructor: `__init__` (setup at birth)

```python
class ConversationAgent:
    def __init__(self, model_name, system_prompt):
        # ↑ runs ONCE when you create a new agent
        # ↑ model_name and system_prompt are the INPUTS to the factory
```

**What it means:** "Every time this factory makes a new product, run this setup code first."

**The name `__init__` is fixed** — Python looks for exactly this name. Double underscores on both sides.

**Reading it:**
- `self` → the product being created (see Part 4 for full explanation)
- `model_name` → input you pass in when creating the agent
- `system_prompt` → another input

**Analogy:** Like a car factory's setup line. Every car that comes off the line gets an engine, tires, and a chassis installed. `__init__` is that installation process.

---

### Block 3 — Attributes: `self.x` (characteristics stored forever)

```python
class ConversationAgent:
    def __init__(self, model_name, system_prompt):
        self.model   = model_name     # stores the model name
        self.system  = system_prompt  # stores the system prompt
        self.history = []             # starts empty, grows with use
        self.turns   = 0              # starts at zero, counts calls
```

**What it means:** Each `self.x = value` creates a **characteristic** attached to this specific product. It persists forever — until the object is deleted.

**Types of attributes you'll see in AI code:**

| Pattern | What it stores | Example |
|:--------|:---------------|:--------|
| `self.model = model_name` | Config from constructor | Which LLM to use |
| `self.history = []` | Empty list, grows over time | Conversation history |
| `self.count = 0` | Counter starting at zero | Number of API calls |
| `self.config = {...}` | Settings dict | Thresholds, limits |
| `self.db = db_param` | External dependency | Database connection |
| `self.flag = False` | Boolean state | Is agent initialized? |

**Key rule:** Once set in `__init__`, attributes are available in **every method** of the class.

---

### Block 4 — Methods: `def action(self, ...)` (what the product can do)

```python
class ConversationAgent:
    def __init__(self, model_name, system_prompt):
        self.model   = model_name
        self.history = []

    def chat(self, user_input):          # ← METHOD: an action
        self.history.append(user_input)  # ← uses the stored attribute
        return call_llm(self.history)    # ← returns result

    def reset(self):                     # ← METHOD: another action
        self.history = []                # ← resets the stored attribute
```

**What it means:** A method is a function that:
1. **Belongs to the class** — only works on this type of object
2. **Has access to all attributes** via `self`
3. **Can change attributes** — this is how the agent's state evolves

**Reading a method:**
- `def chat(self, user_input):` → defines the action, takes `user_input` as argument
- `self.history.append(...)` → reads AND updates the agent's own history
- `return call_llm(...)` → returns a result to whoever called it

---

## Part 4: Creating Instances (Running the Factory)

Once the class is defined, you create instances like this:

```python
# Syntax: variable = ClassName(arguments)
agent = ConversationAgent("claude-sonnet-5-5", "You are a helpful assistant.")
#  ↑                       ↑                   ↑
#  variable name           goes to model_name  goes to system_prompt in __init__
```

**What happens when Python runs this:**
1. Python looks up `ConversationAgent`
2. Creates a blank new object
3. Calls `__init__(self, "claude-sonnet-5-5", "You are a helpful assistant.")`
4. `self.model = "claude-sonnet-5-5"` is stored
5. `self.system = "You are a helpful assistant."` is stored
6. `self.history = []` is stored (empty)
7. `self.turns = 0` is stored
8. Returns the fully set-up object and binds it to `agent`

**After creation, you can read attributes:**
```python
print(agent.model)    # → "claude-sonnet-5-5"
print(agent.history)  # → []
print(agent.turns)    # → 0
```

---

## Part 5: Calling Methods (Using the Product)

```python
# Syntax: instance.method_name(arguments)
support = ConversationAgent("claude-sonnet-5-5", "You handle customer support.")

llm_answer = support.chat("What is RAG?")
#             ↑       ↑    ↑
#             inst    meth  argument to the method
```

**What happens:**
1. Python finds the `chat` method on `ConversationAgent`
2. Automatically passes `support` as `self`
3. Inside `chat`, `self.history.append("What is RAG?")` updates support's history
4. `return call_llm(self.history)` returns the LLM response
5. `llm_answer` now holds that string

**After calling — two things happened at once:**
```python
print(llm_answer)        # → "RAG stands for Retrieval-Augmented Generation..."
#    ↑ what came OUT of the method — Claude's answer (the return value)

print(support.history)   # → ["What is RAG?"]
#    ↑ what stayed INSIDE the object — the agent's memory

print(support.turns)     # → 1
#    ↑ the agent counted the exchange — also stored inside
```

`response` = what came **out**.
`agent.history` = what stayed **in**.

A plain function only gives you the return value and forgets everything.
A class gives you both — that's the whole point.

---

## Part 6: Multiple Instances — Independent Memory

This is the most important thing to understand about instances:

```python
# Same blueprint, two independent products
support = ConversationAgent("claude-sonnet-5-5", "You handle customer support.")
research = ConversationAgent("claude-opus-5-5",  "You research academic topics.")

support.chat("My order is delayed")
research.chat("What is transformer architecture?")

print(support.history)   # → ["My order is delayed"]
print(research.history)  # → ["What is transformer architecture?"]
```

`support.history` and `research.history` are **completely separate**. One object can never see or change another object's attributes.

**Analogy:** Two coffee machines built from the same blueprint. What's loaded in machine 1 doesn't affect machine 2.

---

## Part 7: What `self` Is (Demystified)

`self` confuses every beginner. Here's the plain English version:

**`self` is just the instance, passed automatically.**

When you write:
```python
agent.chat("hello")
```

Python actually does:
```python
ConversationAgent.chat(agent, "hello")
#                      ↑
#                      this is self
```

So when inside `chat` you write `self.history`, you're saying:
- "The history belonging to **this specific agent** that was passed in"
- NOT the history of any other agent
- NOT a global variable

**Every method must have `self` as its first parameter** — that's the rule. Python puts the instance there automatically every time you call a method.

```python
def chat(self, user_input):
    self.history.append(user_input)   # MY history (this agent's)
    self.turns += 1                    # MY turn count
    return call_llm(self.history)      # using MY full history
```

---

## Part 8: The Complete Picture

Here is the full 4-step workflow, one step at a time:

**STEP 1: DEFINE — Declare the factory**

```python
class ConversationAgent:
    pass   # ↑ "I am creating a blueprint for conversation agents"
```

**STEP 2: CONFIGURE — Set up every product at birth (`__init__`)**

```python
class ConversationAgent:
    def __init__(self, model_name, system_prompt):
        self.model   = model_name    # stored forever on this agent
        self.history = []            # starts empty
        self.turns   = 0             # starts at zero
```

**STEP 3: ADD TOOLS — Give the product actions (methods)**

```python
class ConversationAgent:
    def chat(self, msg):
        self.history.append(msg)     # updates own state
        return call_llm(...)         # returns result

    def reset(self):
        self.history = []            # clears own state
```

**STEP 4: CREATE — Run the factory to make a product (instance)**

```python
agent = ConversationAgent(
    "claude-sonnet-5-5",
    "You are helpful."
)
# agent.model   = "claude-sonnet-5-5"
# agent.history = []
# agent.turns   = 0
```

**STEP 5: USE — Call the product's methods**

```python
response = agent.chat("What is RAG?")
agent.reset()
print(agent.history)   # → []
print(agent.turns)     # → 0 (after reset)
```

---

## Part 9: OOP in Real AI Frameworks (2026)

You'll recognize this pattern everywhere:

**Anthropic SDK** (from [anthropic-sdk-python](https://github.com/anthropics/anthropic-sdk-python)):
```python
client = anthropic.Anthropic()       # instance of Anthropic class
response = client.messages.create(  # calling a method
    model="claude-sonnet-5-5", ...
)
```

**LangChain:**
```python
llm = ChatAnthropic(model="claude-sonnet-5-5")  # instance
result = llm.invoke("What is RAG?")             # method call
```

**CrewAI:**
```python
researcher = Agent(                              # instance
    role="Research Analyst",
    tools=[search_tool]
)
result = researcher.execute_task(task)           # method call
```

Every one of these follows: `instance = ClassName(args)` → `instance.method(input)`.

---

## Part 10: Class vs Function — The Decision Rule

```
ONE QUESTION: Does it need to REMEMBER between calls?

  YES → Use a class
        Agent remembers history, config, usage stats

  NO  → Use a function
        Format a prompt, count tokens, validate input
```

| Situation | Use | Why |
|:----------|:----|:----|
| Chat agent with history | `class` | Must remember all messages |
| RAG agent with tracking | `class` | Must remember db, count calls |
| Config holder | `class` (`@dataclass`) | Multiple settings, passed around |
| Format one prompt | `def` | Input in, output out, done |
| Count tokens in a string | `def` | No state needed |
| Validate a query once | `def` | One-shot operation |

---

## Summary — What You Now Know

✓ **OOP solves the memory problem** — functions forget, classes remember
✓ **Class** = factory blueprint (defined once, makes many products)
✓ **Instance** = one product from the factory (independent memory)
✓ **`__init__`** = setup that runs when a product is born
✓ **Attributes** (`self.x`) = characteristics stored forever on the product
✓ **Methods** (`def action(self, ...)`) = actions the product can perform
✓ **`self`** = the instance itself, passed automatically to every method
✓ **Multiple instances** = completely independent, never share state

---

## Next Steps

1. **CHEATSHEET_OOP.py** — quick syntax reference
2. **template_ai_agent_anatomy.py** — see every concept labeled in one file
3. **L06_Classes_as_Blueprints/** — now the code patterns will make full sense

> **External Reading:**
> - [Python Docs — Classes](https://docs.python.org/3/tutorial/classes.html)
> - [Real Python — OOP Guide](https://realpython.com/python3-object-oriented-programming/)

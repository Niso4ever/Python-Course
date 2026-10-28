# Phase 0: Object-Oriented Programming for AI
## The Missing Foundation

Before L06 teaches you to *recognize* class patterns in real AI code, this Phase 0 builds the **mental model** first.

**What this is:** A conceptual bridge. Vocabulary + mental model + the 4-step workflow.
**What this is NOT:** Another pattern reference (that's L06).

---

## Why This Exists

L06 shows you *what* classes look like in AI code.
This shows you *why* they exist and *how* to think about them.

**The gap:** The curriculum jumps from L00 (setup) to L01 (variables) without ever explaining:
- What "object-oriented programming" means
- Why AI code is built from classes instead of just functions
- The vocabulary: class, instance, attribute, method, object, constructor

---

## Reading Order

1. **This README** — orientation (2 min)
2. **OOP_FUNDAMENTALS.md** — the full mental model (20 min)
3. **CHEATSHEET_OOP.py** — keep open while reading AI code
4. **template_ai_agent_anatomy.py** — run it and see everything labeled live
5. **Then go to L06** — now the patterns will make sense

---

## Key Vocabulary (Plain English)

| OOP Term | Plain English | AI Example |
|:---------|:-------------|:-----------|
| **Class** | Blueprint / Factory design | `ConversationAgent` — the design for making agents |
| **Instance** | The product made from the blueprint | `agent = ConversationAgent(...)` — one real agent |
| **Object** | Same as instance | `agent` is an object |
| **Attribute** | A characteristic the object stores | `agent.history` — its stored conversation list |
| **Method** | An action the object can perform | `agent.chat("hello")` — one of its tools |
| **`__init__`** | Constructor — runs at creation | Sets up every new agent at birth |
| **`self`** | This specific instance | How each agent says "my history, not yours" |
| **Inheritance** | One class builds on another | `class MyAgent(BaseModel):` — extends BaseModel |

---

## The One-Sentence Version

> A **class** is a factory design. An **instance** is a product the factory makes. **Attributes** are what the product stores. **Methods** are what the product can do. **`self`** is how the product refers to itself.

---

## Why OOP for AI (in 2026)

Every major AI framework uses classes:

| Framework | Class | What it represents |
|:----------|:------|:------------------|
| **Anthropic SDK** | `Anthropic()` | Client that holds your API key |
| **LangChain** | `ChatAnthropic()` | LLM with memory and config |
| **CrewAI** | `Agent(role=..., tools=[...])` | Agent with role + toolset |
| **PydanticAI** | `Agent(model=..., deps_type=...)` | Typed agent with dependencies |
| **LangGraph** | `StateGraph()` | Graph that holds nodes + edges |

They're all classes because they all need **state** — they remember things between calls.

---

## External References

- [Python Official Docs — Classes](https://docs.python.org/3/tutorial/classes.html) — the authoritative source
- [Real Python — OOP in Python](https://realpython.com/python3-object-oriented-programming/) — the best practical guide
- [Pydantic v2 Docs](https://docs.pydantic.dev/latest/) — for `BaseModel` pattern (2026 standard)
- [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python) — real class-based AI code

---

## After This Phase

Go to **L06_Classes_as_Blueprints** — all the code patterns will make sense now.

> **Remember:** You don't need to memorize this. You need to recognize it. When you see `class X:` in AI code, you'll know: factory. When you see `agent = X(args)`, you'll know: product made from that factory.

# Phase 3: Tool Use & Function Calling
> **The Core of Agentic AI: Teaching LLMs to Execute Your Functions**

---

## THE CRITICAL INSIGHT

An AI agent is only as good as the tools you give it — and **the quality of those tool descriptions**.

Modern LLMs (GPT-4, Claude 3.5) don't magically know how to call your Python functions. They read:
1. **Type hints** (`def search(query: str, limit: int = 10) -> List[dict]`)
2. **Docstrings** (the triple-quoted descriptions)
3. **Pydantic schemas** (strict data validation models)

**If your documentation is poor, the agent WILL fail.**

This phase teaches you to write Python that LLMs can read like an API reference.

---

## WHY THIS MATTERS

### Without This Knowledge:
```python
def search(q, n):
    # LLM has NO IDEA what q or n means
    # Will guess wrong parameters
    # Your agent breaks
    return results[:n]
```

### With Phase 3 Skills:
```python
def search(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """
    Search the knowledge base for relevant documents.

    Args:
        query: The search query string
        max_results: Maximum number of results to return (default: 10)

    Returns:
        List of documents with 'title', 'content', and 'score' fields
    """
    return results[:max_results]
```

**The LLM now knows exactly:**
- What parameters to pass
- What types they should be
- What to expect back
- When to use this tool

---

## THE 4 LESSONS

### L01: Type Hints & Docstrings for LLMs
**What you'll learn:**
- How LLMs read Python function signatures
- Google-style vs NumPy-style docstrings
- Type hints that prevent agent failures
- Visual patterns: what the LLM actually "sees"

**Duration:** 1-2 hours
**Output:** Template library of LLM-readable functions

---

### L02: Pydantic Fundamentals
**What you'll learn:**
- Why Pydantic is industry-standard for AI agents
- Data validation that stops garbage input
- `BaseModel` pattern (all modern agents use this)
- Automatic JSON schema generation for LLMs

**Duration:** 2-3 hours
**Output:** Pydantic templates for tool inputs/outputs

---

### L03: Function Calling Patterns
**What you'll learn:**
- The ReAct pattern (Reason → Act → Observe)
- How LangChain/CrewAI/AutoGen format tool calls
- Common patterns: search, filter, transform, aggregate
- Error handling when LLMs call tools wrong

**Duration:** 1-2 hours
**Output:** Ready-to-use function calling templates

---

### L04: Tool Schema Design
**What you'll learn:**
- Converting Python functions to OpenAI/Anthropic tool schemas
- The JSON structure LLMs actually receive
- Multi-parameter tools with complex types
- Real examples from production agents

**Duration:** 1-2 hours
**Output:** Schema templates for any tool type

---

## YOUR LEARNING PATH

### Step 1: Foundation (L01)
Start here. Learn how to write functions that LLMs can understand.

```python
# Before Phase 3
def get_weather(loc):
    pass

# After L01
def get_weather(location: str, units: str = "celsius") -> Dict[str, Any]:
    """Fetch current weather for a location."""
    pass
```

### Step 2: Validation (L02)
Add Pydantic for bulletproof data handling.

```python
from pydantic import BaseModel, Field

class WeatherQuery(BaseModel):
    location: str = Field(..., description="City name or coordinates")
    units: str = Field("celsius", description="Temperature units")

def get_weather(query: WeatherQuery) -> WeatherResponse:
    """Fetch current weather with validated inputs."""
    pass
```

### Step 3: Integration (L03)
See how real frameworks use these patterns.

```python
# This is what LangChain, CrewAI, AutoGen all do internally
tools = [
    {
        "name": "get_weather",
        "description": "Fetch current weather",
        "input_schema": WeatherQuery.model_json_schema()
    }
]
```

### Step 4: Mastery (L04)
Design complete tool schemas for production agents.

---

## THE SKILL YOU'RE BUILDING

**Tool Architecture:** The ability to design Python functions that AI agents can reliably call.

This is NOT traditional Python programming. This is:
- Writing code optimized for LLM comprehension
- Validating inputs before they reach your logic
- Designing clear, single-purpose tools
- Creating self-documenting APIs

**In the real world:**
- LangChain agents need tools defined this way
- OpenAI function calling requires these schemas
- Claude tool use follows these patterns
- AutoGen/CrewAI/DSPy all expect this format

---

## PREREQUISITES

You should have completed:
- ✓ Phase 1A: Python fundamentals (dicts, lists, functions)
- ✓ Phase 1B: Pattern recognition (loops, conditionals)

You do NOT need:
- ✗ Advanced Python (decorators, metaclasses, etc.)
- ✗ API development experience
- ✗ Prior AI/ML knowledge

---

## THE PHASE 4 DELIVERABLE

By the end of this phase, you will have:

**1. A Tool Template Library** (`MY_TEMPLATES/Phase4_Tools/`)
```
├── search_tools.py          # Web search, RAG search, etc.
├── data_tools.py            # Filter, transform, aggregate
├── validation_schemas.py    # Pydantic models for common patterns
└── tool_registry.py         # How to register tools with agents
```

**2. The "LLM View" Mental Model**
You'll see every function through the LLM's eyes:
- "Can the LLM understand what this parameter is?"
- "Is the return type clear?"
- "Would I know when to call this tool?"

**3. Production-Ready Patterns**
Every template follows best practices from:
- OpenAI function calling docs
- Anthropic Claude tool use guide
- LangChain tool implementation
- Pydantic V2 standards

---

## HOW TO USE THIS PHASE

### If You're Following the Full Curriculum:
Complete L01 → L02 → L03 → L04 in order.

### If You're Building an Agent RIGHT NOW:
1. Read L01 (30 min) — learn the docstring pattern
2. Skim L02 (15 min) — grab the Pydantic template you need
3. Copy from L03 (10 min) — get the exact function pattern
4. Reference L04 as needed — when integrating with frameworks

### If You're Reverse-Engineering Existing Code:
Use this phase as a DECODER RING:
- See a `BaseModel` → that's L02 Pydantic validation
- See `Field(description=...)` → that's for LLM schema generation
- See detailed docstrings → that's L01 LLM-readable format

---

## THE INDUSTRY REALITY

**95% of agent failures happen at the tool-calling layer.**

Not because LLMs are bad at reasoning. Because:
- The tool had no type hints (LLM guesses wrong)
- The docstring was unclear (LLM picks wrong tool)
- No input validation (garbage data breaks your function)
- Poor error messages (LLM doesn't know what went wrong)

**Phase 3 teaches you to prevent all four.**

---

## NEXT STEPS

**Start with:** [L01_TypeHints_Docstrings](L01_TypeHints_Docstrings/)

**After Phase 3:** Move to Phase 2 (Real Systems) and see how LangChain/CrewAI/AutoGen implement everything you just learned.

---

**Remember:** You are not learning Python for its own sake. You are learning to write Python that AI agents can read, understand, and execute reliably. That is the skill that matters.

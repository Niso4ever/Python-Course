# Phase 3: Tool Use & Function Calling - Summary

## What You've Built

A complete, production-ready curriculum for teaching AI agents to use Python functions reliably.

---

## The Core Insight

**LLMs don't see your code. They see schemas.**

Your job as an AI architect is to write Python that:
1. **Documents itself** (type hints + docstrings)
2. **Validates automatically** (Pydantic)
3. **Generates perfect schemas** (for OpenAI, Anthropic, LangChain)

---

## The Three-Layer System

### Layer 1: Type Hints (Structure)
```python
def search(query: str, limit: int = 10) -> List[dict]:
    pass
```
→ **LLM knows:** "query is string, limit is int with default 10"

### Layer 2: Docstrings (Meaning)
```python
def search(query: str, limit: int = 10) -> List[dict]:
    """
    Search for documents. Use this when user asks questions.
    
    Args:
        query: The search query
        limit: Max results
    """
    pass
```
→ **LLM knows:** "Call this to search. Pass a query and optionally a limit."

### Layer 3: Pydantic (Validation + Schema)
```python
from pydantic import BaseModel, Field

class SearchInput(BaseModel):
    query: str = Field(..., description="Search query", min_length=1)
    limit: int = Field(10, description="Max results", ge=1, le=100)

def search(input: SearchInput) -> List[dict]:
    """Search for documents."""
    # Guaranteed valid input!
    pass

# Generates perfect JSON schema
schema = SearchInput.model_json_schema()
```
→ **Automatic validation + LLM-ready schema**

---

## What's Inside Phase 3

### [README.md](README.md)
- Why Pydantic is industry-standard
- The problem it solves
- Overview of all 4 lessons
- Learning path

### [QUICKSTART.md](QUICKSTART.md)
- 5-minute version (copy-paste template)
- 15-minute deep dive
- 30-minute workshop (build a real tool)
- Framework integration examples

### [CHEATSHEET.md](CHEATSHEET.md)
- One-page reference
- All patterns at a glance
- Type hints quick reference
- Pydantic field parameters
- Framework integration code

### [L01: Type Hints & Docstrings](L01_TypeHints_Docstrings/)
**Focus:** Writing functions LLMs can understand

**Files:**
- `README.md` - Complete guide to LLM-readable functions
- `VISUAL_LLM_PERSPECTIVE.md` - How LLMs "see" your code
- `template_search_tools.py` - 7 production-ready search patterns

**Key Concepts:**
- How type hints become JSON schemas
- Google-style docstrings for LLMs
- What information LLMs need
- Common mistakes and fixes

### [L02: Pydantic Fundamentals](L02_Pydantic_Fundamentals/)
**Focus:** Data validation and schema generation

**Files:**
- `README.md` - Complete Pydantic guide for agents
- `template_agent_schemas.py` - 8 production schemas

**Key Concepts:**
- `BaseModel` pattern
- `Field` with descriptions for LLMs
- Validation (types, constraints, custom validators)
- JSON schema generation
- Nested models

**Templates:**
- Search tool input/output
- LLM response with citations
- Agent configuration
- Multi-tool action schemas
- Conversation/message schemas
- RAG document schemas
- Evaluation metrics
- Error handling schemas

### [L03: Function Calling Patterns](L03_Function_Calling_Patterns/)
**Focus:** How frameworks use your tools in production

**Files:**
- `README.md` - Complete function calling guide

**Key Concepts:**
- The ReAct pattern (Reason → Act → Observe)
- Single tool call (OpenAI style)
- Multi-tool selection
- Sequential tool calls (chains)
- Parallel tool calls
- Error handling
- LangChain integration

**Patterns:**
- Simple function calling
- Tool registry
- Agent loop implementation
- Safe execution wrapper
- Complete mini RAG agent

### [L04: Tool Schemas](L04_Tool_Schemas/)
**Files (checked 2026-10-28):** `README.md`, `CHEATSHEET_L04.md`, `SUMMARY_L04.md`, `template_production_rag_tools.py`, `template_framework_adapters.py`
- Schema design for different frameworks (OpenAI, Anthropic, LangChain adapters)

---

## The Complete Workflow

### 1. Design (5 min)
```
What does my tool do?
What inputs does it need?
What will it return?
```

### 2. Define Schema (5 min)
```python
class MyToolInput(BaseModel):
    param1: str = Field(..., description="...")
    param2: int = Field(10, description="...", ge=1, le=100)
```

### 3. Implement Function (10 min)
```python
def my_tool(input: MyToolInput) -> Dict[str, Any]:
    """
    What the tool does. Use this when [when to call].
    
    Args:
        input: Validated parameters
    
    Returns:
        Description of output
    """
    # Implementation
    return {"result": "success"}
```

### 4. Generate Schema (1 min)
```python
schema = MyToolInput.model_json_schema()
```

### 5. Register with Framework (5 min)
```python
# OpenAI
tools = [{"type": "function", "function": {"name": "my_tool", "parameters": schema}}]

# Anthropic
tools = [{"name": "my_tool", "input_schema": schema}]

# LangChain
tool = Tool(name="my_tool", func=my_tool, args_schema=MyToolInput)
```

**Total time: ~25 minutes for a production-ready tool**

---

## Key Takeaways

1. **Type hints are not optional** - They become the LLM's API documentation
2. **Docstrings must be specific** - "Search for documents" < "Search the knowledge base when user asks questions requiring lookup"
3. **Pydantic is the standard** - OpenAI, Anthropic, LangChain all expect it
4. **Field descriptions are critical** - LLMs read them first
5. **Always validate inputs** - LLMs will pass garbage sometimes
6. **Always handle errors** - Wrap tools in try/except
7. **ReAct is everywhere** - Learn the pattern once, use it everywhere

---

## What This Enables

After mastering Phase 3, you can:

✓ **Read any agent codebase** - Recognize tool patterns instantly
✓ **Build production tools** - With proper validation and schemas
✓ **Integrate with any framework** - OpenAI, Anthropic, LangChain, CrewAI, AutoGen
✓ **Debug tool failures** - Understand what LLMs see and why they fail
✓ **Design better APIs** - For both humans and LLMs

---

## The Industry Reality

**95% of agent failures happen at tool-calling:**
- ❌ No type hints → LLM guesses wrong types
- ❌ Vague docstrings → LLM picks wrong tool
- ❌ No validation → Garbage input breaks your code
- ❌ Poor error messages → LLM doesn't know what went wrong

**Phase 3 teaches you to prevent all four.**

---

## Integration with Rest of Curriculum

### Before Phase 3:
- **Phase 1A:** Python fundamentals (dicts, lists, functions)
- **Phase 1B:** Pattern recognition (loops, conditionals)

### After Phase 3:
- **Phase 2:** Real Systems (see how LangChain/CrewAI use these patterns)
- **Multi-Agent:** Design systems where agents use your tools

**Phase 3 is the bridge:** From basic Python → Production-ready agent tools

---

## Next Steps for Learners

### If starting fresh:
1. Read [QUICKSTART.md](QUICKSTART.md) (15 min)
2. Complete the 30-min workshop
3. Browse templates in L01 and L02
4. Build one tool for your own use case

### If experienced with Python:
1. Skim [CHEATSHEET.md](CHEATSHEET.md) (5 min)
2. Copy a template from L01 or L02
3. Integrate with OpenAI/Anthropic
4. Done

### If building an agent now:
1. Open [template_agent_schemas.py](L02_Pydantic_Fundamentals/template_agent_schemas.py)
2. Find the pattern you need
3. Copy and modify
4. Ship

---

## Maintenance & Updates

This curriculum is designed to be:
- **Framework-agnostic** - Works with any LLM API
- **Future-proof** - Based on Pydantic V2 (current standard)
- **Template-first** - Copy-paste > memorization
- **Production-ready** - All patterns from real systems

**Version:** 1.0 (March 2025)
**Based on:** Pydantic V2, OpenAI function calling, Anthropic tool use, LangChain 0.1+

---

## The Mental Model

Think of your tools as **API endpoints for LLMs:**

```
Your Function = An API endpoint
Type Hints = API schema
Docstring = API documentation
Pydantic = Request validation
Field descriptions = Parameter documentation
```

If you'd give it to a human developer, give it to an LLM the same way.

---

## Success Metrics

You've mastered Phase 3 when:

✓ You can write an LLM-callable function in < 10 minutes
✓ You instinctively add Pydantic validation
✓ Your docstrings include "Use this when..."
✓ You can read any agent framework's tool code
✓ You debug tool failures by checking the schema first

---

**Remember:** The best code is code you don't have to write. These templates are battle-tested patterns from production systems. Copy, modify, ship.

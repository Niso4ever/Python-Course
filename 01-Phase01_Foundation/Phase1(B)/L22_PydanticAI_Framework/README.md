# Lesson 18: PydanticAI Framework
## The Typed Agent Theory

> **2026 Reality:** PydanticAI is the new standard for building typed, validated AI agents.
> It replaces hand-wired LangChain chains with a clean, Pythonic, type-safe approach.
> Think of it as: **DSPy's philosophy + Pydantic's validation + Python's simplicity**.

> **Version note (checked 2026-10-28, pydantic-ai 2.53 installed):** This lesson uses the current names `output_type=` and `result.output`. Tutorials written for PydanticAI 0.x use `result_type=` and `result.data`; both were removed in v0.6.0 and now raise an error.

---

## Why PydanticAI Exists

In 2025, building an AI agent required:
- LangChain: powerful but complex (1000+ classes)
- DSPy: elegant but academic
- Raw API calls: flexible but repetitive

PydanticAI asks: **what if building an agent was as simple as writing a Python function with type hints?**

```python
from pydantic_ai import Agent

agent = Agent(
    'openai:gpt-4o-mini',    # Model-agnostic! Works with any provider
    system_prompt='You are a helpful AI assistant for Python learners.'
)

result = agent.run_sync('What is a decorator in Python?')
print(result.output)
```

That's it. No chains. No executors. No 47-line setup.

---

## 1. The Core Concept: Agent as a Function

```python
from pydantic_ai import Agent
from pydantic import BaseModel

# Define your output TYPE (Pydantic model)
class CodeExplanation(BaseModel):
    concept: str
    explanation: str
    example_code: str
    difficulty: str  # "beginner", "intermediate", "advanced"

# Create a typed agent — output is ALWAYS a CodeExplanation
agent = Agent(
    'openai:gpt-4o-mini',
    output_type=CodeExplanation,   # ← The magic: TYPED output
    system_prompt='Explain Python concepts for AI architects.'
)

result = agent.run_sync('Explain match/case')
print(result.output.concept)       # "match/case"
print(result.output.example_code)  # actual code string
print(result.output.difficulty)    # "intermediate"
```

**The insight:** Your agent's output is a **validated Pydantic object**, not raw text.
If the LLM returns invalid data, Pydantic catches it and retries. No more parsing JSON strings.

---

## 2. Model-Agnostic Design (2026 Critical Skill)

```python
# Same agent, different models — just change the string
agent_openai  = Agent('openai:gpt-4o-mini', output_type=Answer)
agent_claude  = Agent('anthropic:claude-sonnet-5-5', output_type=Answer)
agent_gemini  = Agent('google-gla:gemini-2.0-flash', output_type=Answer)

# Same code, same types, same validation — different provider
result = agent_openai.run_sync('What is RAG?')
```

**Architect's rule:** Never hardcode a provider. Design for swapability.

---

## 3. Tools in PydanticAI

```python
from pydantic_ai import Agent, RunContext

agent = Agent('openai:gpt-4o-mini', system_prompt='Research assistant.')

@agent.tool     # ← Decorator registers a tool
async def search_web(ctx: RunContext[str], query: str) -> str:
    """Search the web for current information."""
    # Your search implementation
    return f"Results for: {query}"

@agent.tool
async def calculate(ctx: RunContext[str], expression: str) -> str:
    """Evaluate a math expression."""
    return str(eval(expression))

result = await agent.run('What is 15% of the 2024 AI market size?')
```

**Compare to LangChain:**
- LangChain: `@tool` decorator → `create_react_agent()` → `AgentExecutor()` → `.invoke()`
- PydanticAI: `@agent.tool` decorator → `agent.run()` — done.

---

## 4. Dependencies (Context Injection)

```python
from dataclasses import dataclass
from pydantic_ai import Agent, RunContext

@dataclass
class UserContext:
    user_id: str
    role: str
    preferences: dict

agent = Agent(
    'openai:gpt-4o-mini',
    deps_type=UserContext,   # ← Inject context into every tool
)

@agent.tool
async def get_user_data(ctx: RunContext[UserContext]) -> str:
    """Fetch data based on the current user."""
    return f"Data for user {ctx.deps.user_id} (role: {ctx.deps.role})"

result = await agent.run(
    'Show me my dashboard',
    deps=UserContext(user_id='arch-001', role='architect', preferences={})
)
```

---

## 5. Structured Outputs (The 2026 Standard)

Every production AI system in 2026 returns **structured data**, not raw text:

```python
from pydantic import BaseModel, Field

class ArchitectureReview(BaseModel):
    """Structured output for code architecture review."""
    components: list[str] = Field(description="List of system components")
    patterns_used: list[str] = Field(description="Design patterns identified")
    risks: list[str] = Field(description="Potential architectural risks")
    score: int = Field(ge=1, le=10, description="Architecture quality score")
    recommendation: str = Field(description="One-sentence recommendation")

agent = Agent('openai:gpt-4o-mini', output_type=ArchitectureReview)

result = agent.run_sync('Review a RAG pipeline with ChromaDB and LangChain')
print(f"Score: {result.output.score}/10")
print(f"Risks: {result.output.risks}")
# Guaranteed: score IS an int between 1-10. risks IS a list. No parsing needed.
```

---

## 6. When to Use What (Architect's Decision Matrix)

| Framework | Best For | Complexity | Type Safety |
|:----------|:---------|:-----------|:------------|
| **PydanticAI** | Typed agents, production APIs, validated outputs | Low | ✅ Full |
| **DSPy** | Optimizable pipelines, research, prompt tuning | Medium | Partial |
| **LangChain** | Complex chains, many integrations, RAG | High | ❌ None |
| **Raw API** | Simple one-shot calls, maximum control | Lowest | ❌ None |

**2026 trend:** PydanticAI for new projects. DSPy for optimization. LangChain for legacy.

---

## 7. Pattern Recognition

| You see... | It means... |
|:-----------|:------------|
| `Agent('openai:...')` | PydanticAI agent with model provider |
| `output_type=MyModel` | Typed, validated output |
| `@agent.tool` | Tool registration (like LangChain's @tool) |
| `RunContext[DepsType]` | Dependency injection into tools |
| `agent.run_sync()` | Synchronous execution |
| `await agent.run()` | Async execution |
| `result.output` | The validated output object |
| `deps_type=X` | Context available to all tools |

---

## 8. Key Takeaways

✓ **PydanticAI = typed agents** — output is always a validated Pydantic model
✓ **Model-agnostic** — swap providers by changing one string
✓ **Tools via decorators** — `@agent.tool` is simpler than LangChain
✓ **Dependency injection** — pass context to tools cleanly
✓ **Structured outputs** — the 2026 standard for production AI
✓ **No chains, no executors** — just `agent.run()`

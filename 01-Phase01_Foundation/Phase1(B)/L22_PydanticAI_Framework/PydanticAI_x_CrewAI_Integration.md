# PydanticAI × CrewAI Integration

**Core idea:** CrewAI handles *who does what* (agent roles, task delegation).
PydanticAI handles *what shape the data is* (structured outputs, type-safe tools).

They complement each other — use them together for multi-agent systems that return clean, validated, typed results.

---

## Pattern 1 — PydanticAI models as CrewAI task output schemas

The simplest integration. CrewAI has built-in `output_pydantic=` support for this.

```python
from pydantic import BaseModel
from crewai import Agent, Task, Crew

# Define the shape of what the task should return
class ResearchReport(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    confidence: float

researcher = Agent(
    role="Research Analyst",
    goal="Research topics thoroughly",
    backstory="Expert researcher with web access"
)

task = Task(
    description="Research quantum computing trends",
    agent=researcher,
    output_pydantic=ResearchReport  # <-- PydanticAI model here
)

crew = Crew(agents=[researcher], tasks=[task])
result = crew.kickoff()

# result.pydantic is now a typed ResearchReport, not raw text
print(result.pydantic.topic)       # "quantum computing"
print(result.pydantic.confidence)  # 0.92
```

**When to use:** Any time you want a CrewAI task to return structured data instead of a plain string.

---

## Pattern 2 — PydanticAI agent wrapped as a CrewAI tool

Turn a specialist PydanticAI agent into a tool that CrewAI agents can call.

```python
from pydantic_ai import Agent as PydanticAgent
from crewai.tools import BaseTool

# A PydanticAI specialist — validates and structures raw data
validator_agent = PydanticAgent(
    "openai:gpt-4o",
    output_type=dict
)

# Wrap it as a CrewAI tool
class ValidatorTool(BaseTool):
    name: str = "data_validator"
    description: str = "Validates and structures raw data"

    def _run(self, raw_data: str) -> str:
        result = validator_agent.run_sync(f"Validate this: {raw_data}")
        return str(result.output)

# Now any CrewAI agent can call PydanticAI as a tool
crew_agent = Agent(
    role="Data Processor",
    tools=[ValidatorTool()]
)
```

**When to use:** When a CrewAI agent needs a specialized sub-task handled by a PydanticAI agent (e.g. validation, classification, extraction).

---

## Pattern 3 — PydanticAI for type-safe tool definitions, CrewAI for orchestration

Define your tools with PydanticAI's structured approach, then feed results into a CrewAI pipeline.

```python
from pydantic_ai import Agent
from pydantic_ai.tools import Tool
from pydantic import BaseModel

# Structured return type for a tool
class SearchResult(BaseModel):
    query: str
    results: list[str]
    total: int

# PydanticAI tool — type-safe, validated
def search_web(query: str) -> SearchResult:
    # ... real search logic here
    return SearchResult(query=query, results=["result1", "result2"], total=2)

pydantic_agent = Agent("openai:gpt-4o", tools=[Tool(search_web)])

# Run PydanticAI first, pass structured output into CrewAI pipeline
search_output = pydantic_agent.run_sync("Find AI trends 2026")

# Hand structured data to CrewAI for further processing
```

**When to use:** When you want PydanticAI to handle data gathering/validation before CrewAI agents process and act on the results.

---

## Quick Reference — When to use which

| Need | Use |
|------|-----|
| Role-based agents (Researcher, Writer, QA) | CrewAI |
| Structured / typed outputs | PydanticAI models |
| Type-safe tool definitions | PydanticAI |
| Agent delegation & task flow | CrewAI |
| Validation of LLM responses | PydanticAI |
| Multi-agent pipelines | CrewAI |
| Guarantee output shape | PydanticAI `BaseModel` |

---

## The Simplest Starting Point

If you remember nothing else:

```python
# Step 1 — define output shape with Pydantic
class MyOutput(BaseModel):
    answer: str
    confidence: float

# Step 2 — attach it to your CrewAI task
task = Task(
    description="...",
    agent=my_agent,
    output_pydantic=MyOutput  # done
)
```

CrewAI validates the LLM output against your model automatically.
No raw text parsing. No guessing the format. Just typed data.

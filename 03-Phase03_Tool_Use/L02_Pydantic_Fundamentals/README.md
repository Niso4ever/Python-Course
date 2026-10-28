# L02: Pydantic Fundamentals for AI Agents
> **Industry-Standard Data Validation for Agentic Systems**

---

## WHY PYDANTIC IS EVERYWHERE

If you look at any modern AI agent framework, you'll see Pydantic:

- **LangChain:** All tools use Pydantic `BaseModel`
- **CrewAI:** Agent inputs/outputs are Pydantic models
- **AutoGen:** Message schemas are Pydantic models
- **DSPy:** Signatures use Pydantic for type safety
- **OpenAI/Anthropic SDKs:** Structured outputs use Pydantic

**Why?** Because Pydantic solves the #1 problem in agentic AI:

> **LLMs generate text. Your code expects structured data. Pydantic bridges the gap.**

---

## THE PROBLEM PYDANTIC SOLVES

### Without Pydantic:
```python
def search(params):
    # What if params is None?
    # What if params['query'] doesn't exist?
    # What if params['limit'] is a string "10" instead of int 10?
    # What if params has unexpected keys?

    query = params['query']  # ← Might crash
    limit = params['limit']  # ← Might be wrong type
    # ... your code breaks
```

**The LLM can return ANYTHING. Your code has no protection.**

### With Pydantic:
```python
from pydantic import BaseModel, Field

class SearchParams(BaseModel):
    query: str = Field(..., description="Search query")
    limit: int = Field(10, description="Max results", ge=1, le=100)

def search(params: SearchParams):
    # Pydantic guarantees:
    # ✓ params.query exists and is a string
    # ✓ params.limit exists and is an int between 1-100
    # ✓ No unexpected fields
    # ✓ Type conversion happened automatically ("10" → 10)

    query = params.query  # ← Always works
    limit = params.limit  # ← Always correct type
```

**Pydantic validates, converts, and documents your data automatically.**

---

## THE CORE PATTERN: BaseModel

Every Pydantic model inherits from `BaseModel`:

```python
from pydantic import BaseModel

class MyModel(BaseModel):
    field_name: field_type
```

### Example 1: Simple Model
```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    email: str

# Create an instance
user = User(name="Alice", age=30, email="alice@example.com")
print(user.name)  # "Alice"
print(user.age)   # 30

# Validation happens automatically
try:
    bad_user = User(name="Bob", age="thirty", email="bob@example.com")
except ValueError as e:
    print(e)  # "Input should be a valid integer..."
```

**Key insight:** You define the structure once, and Pydantic enforces it everywhere.

---

## FIELD DESCRIPTIONS FOR LLMS

When building agent tools, use `Field` to add descriptions:

```python
from pydantic import BaseModel, Field

class SearchRequest(BaseModel):
    query: str = Field(
        ...,  # ← Required field (no default)
        description="The search query string"
    )
    max_results: int = Field(
        10,  # ← Default value
        description="Maximum number of results to return",
        ge=1,  # ← Must be >= 1
        le=100  # ← Must be <= 100
    )
    include_metadata: bool = Field(
        False,
        description="Whether to include document metadata in results"
    )
```

### What `Field` Parameters Mean:

| Parameter | Meaning | Example |
|-----------|---------|---------|
| `...` | Required (no default) | `Field(...)` |
| `default` | Default value | `Field(10)` |
| `description` | For LLM schema | `Field(..., description="Search query")` |
| `ge` | Greater than or equal | `Field(1, ge=0)` (>= 0) |
| `le` | Less than or equal | `Field(10, le=100)` (<= 100) |
| `min_length` | Minimum string length | `Field(..., min_length=1)` |
| `max_length` | Maximum string length | `Field(..., max_length=500)` |
| `pattern` | Regex pattern | `Field(..., pattern=r"^\d{3}-\d{3}-\d{4}$")` |

---

## VISUAL: HOW PYDANTIC VALIDATES

```
USER INPUT (from LLM or elsewhere)
        |
        ↓
    ┌─────────────────────────────┐
    │  {                          │
    │    "query": "hello",        │
    │    "max_results": "25",     │  ← String "25", not int!
    │    "extra_field": "ignore"  │  ← Not in model!
    │  }                          │
    └─────────────────────────────┘
        |
        ↓ (Pydantic validation)
        |
    ┌─────────────────────────────┐
    │ 1. Check required fields    │
    │    ✓ "query" present        │
    │                             │
    │ 2. Type conversion          │
    │    "25" → 25 (int)         │
    │                             │
    │ 3. Constraint validation    │
    │    25 >= 1? ✓              │
    │    25 <= 100? ✓            │
    │                             │
    │ 4. Remove extra fields      │
    │    "extra_field" ignored    │
    └─────────────────────────────┘
        |
        ↓
    ┌─────────────────────────────┐
    │  SearchRequest(             │
    │    query="hello",           │
    │    max_results=25,          │
    │    include_metadata=False   │ ← Default added
    │  )                          │
    └─────────────────────────────┘
        |
        ↓
    YOUR FUNCTION (with guaranteed clean data)
```

---

## COMMON PATTERNS FOR AI AGENTS

### Pattern 1: Tool Input Schema
```python
from pydantic import BaseModel, Field
from typing import Optional, List

class ToolInput(BaseModel):
    """Input schema for a tool that LLMs will call."""

    # Required fields
    action: str = Field(
        ...,
        description="The action to perform: 'search', 'filter', 'summarize'"
    )
    target: str = Field(
        ...,
        description="The target to perform the action on"
    )

    # Optional fields with defaults
    parameters: Optional[dict] = Field(
        None,
        description="Additional parameters for the action"
    )
    verbose: bool = Field(
        False,
        description="Whether to return detailed output"
    )


def my_tool(input: ToolInput) -> dict:
    """A tool that uses Pydantic input validation."""
    # input.action is guaranteed to exist and be a string
    # input.target is guaranteed to exist and be a string
    # input.parameters might be None
    # input.verbose is guaranteed to be a bool (defaults to False)

    return {"status": "success", "action": input.action}
```

### Pattern 2: LLM Output Schema
```python
from pydantic import BaseModel, Field
from typing import List, Optional

class Citation(BaseModel):
    """A single citation/source."""
    source: str = Field(..., description="Source name or URL")
    quote: str = Field(..., description="Relevant quote from source")
    confidence: float = Field(..., description="Confidence in this citation (0.0-1.0)", ge=0.0, le=1.0)


class LLMResponse(BaseModel):
    """Structured output from an LLM."""

    answer: str = Field(
        ...,
        description="The main answer text"
    )
    citations: List[Citation] = Field(
        default_factory=list,
        description="Sources used to generate the answer"
    )
    confidence: float = Field(
        ...,
        description="Overall confidence in the answer (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    needs_human_review: bool = Field(
        False,
        description="Whether this answer should be reviewed by a human"
    )


# Usage: Parse LLM's JSON output into structured data
llm_json_output = {
    "answer": "Paris is the capital of France.",
    "citations": [
        {"source": "Wikipedia", "quote": "Paris is the capital...", "confidence": 0.95}
    ],
    "confidence": 0.92
}

response = LLMResponse(**llm_json_output)
# response.answer is a string
# response.citations is a list of Citation objects
# response.confidence is a validated float between 0-1
```

### Pattern 3: Agent Configuration
```python
from pydantic import BaseModel, Field
from typing import List, Optional

class AgentConfig(BaseModel):
    """Configuration for an AI agent."""

    name: str = Field(..., description="Agent name")
    role: str = Field(..., description="Agent's role/specialty")
    goal: str = Field(..., description="Agent's primary goal")

    # Model settings
    model: str = Field("gpt-4", description="LLM model to use")
    temperature: float = Field(
        0.7,
        description="Sampling temperature (0.0-2.0)",
        ge=0.0,
        le=2.0
    )
    max_tokens: int = Field(
        2000,
        description="Maximum tokens in response",
        ge=1,
        le=32000
    )

    # Tool access
    available_tools: List[str] = Field(
        default_factory=list,
        description="List of tool names this agent can use"
    )

    # Safety settings
    allow_delegation: bool = Field(
        False,
        description="Whether this agent can delegate to other agents"
    )
    requires_approval: bool = Field(
        True,
        description="Whether actions require human approval"
    )


# Create an agent
agent = AgentConfig(
    name="ResearchAgent",
    role="Research Specialist",
    goal="Find and synthesize information from multiple sources",
    available_tools=["search", "summarize", "cite"],
    temperature=0.3  # Lower for factual tasks
)
```

### Pattern 4: Nested Models
```python
from pydantic import BaseModel, Field
from typing import List

class Message(BaseModel):
    """A single message in a conversation."""
    role: str = Field(..., description="'user', 'assistant', or 'system'")
    content: str = Field(..., description="Message content")


class Conversation(BaseModel):
    """A complete conversation thread."""
    id: str = Field(..., description="Unique conversation ID")
    messages: List[Message] = Field(
        default_factory=list,
        description="List of messages in chronological order"
    )
    metadata: dict = Field(
        default_factory=dict,
        description="Additional conversation metadata"
    )


# Usage
convo = Conversation(
    id="conv_123",
    messages=[
        Message(role="user", content="Hello!"),
        Message(role="assistant", content="Hi! How can I help?")
    ],
    metadata={"user_id": "user_456", "start_time": "2024-01-01T10:00:00"}
)

# Access nested data
print(convo.messages[0].content)  # "Hello!"
print(len(convo.messages))  # 2
```

---

## THE KILLER FEATURE: JSON SCHEMA GENERATION

Pydantic can automatically generate JSON schemas for LLMs:

```python
from pydantic import BaseModel, Field

class SearchRequest(BaseModel):
    query: str = Field(..., description="Search query")
    limit: int = Field(10, description="Max results", ge=1, le=100)

# Generate schema for LLM
schema = SearchRequest.model_json_schema()
print(schema)
```

**Output:**
```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "Search query"
    },
    "limit": {
      "type": "integer",
      "description": "Max results",
      "default": 10,
      "minimum": 1,
      "maximum": 100
    }
  },
  "required": ["query"]
}
```

**This is EXACTLY what OpenAI, Anthropic, and LangChain use to tell LLMs about your tools!**

---

## VALIDATION & ERROR HANDLING

```python
from pydantic import BaseModel, Field, ValidationError

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    limit: int = Field(10, ge=1, le=100)

# Valid input
try:
    req = SearchRequest(query="hello", limit=5)
    print("✓ Valid")
except ValidationError as e:
    print(f"✗ Invalid: {e}")

# Invalid: empty query
try:
    req = SearchRequest(query="", limit=5)
except ValidationError as e:
    print(f"✗ Invalid: {e}")
    # Output: String should have at least 1 character

# Invalid: limit out of range
try:
    req = SearchRequest(query="test", limit=200)
except ValidationError as e:
    print(f"✗ Invalid: {e}")
    # Output: Input should be less than or equal to 100

# Invalid: wrong type
try:
    req = SearchRequest(query="test", limit="many")
except ValidationError as e:
    print(f"✗ Invalid: {e}")
    # Output: Input should be a valid integer
```

---

## PYDANTIC + TYPE HINTS = PERFECT TOOLS

Combine L01 (type hints) with L02 (Pydantic):

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Any

class SearchInput(BaseModel):
    """Input schema for knowledge base search."""
    query: str = Field(..., description="Search query", min_length=1)
    limit: int = Field(10, description="Max results", ge=1, le=50)


class SearchResult(BaseModel):
    """A single search result."""
    id: str
    title: str
    content: str
    score: float = Field(..., ge=0.0, le=1.0)


class SearchOutput(BaseModel):
    """Output schema for knowledge base search."""
    results: List[SearchResult]
    total_found: int
    query_time_ms: float


def search_knowledge_base(input: SearchInput) -> SearchOutput:
    """
    Search the knowledge base for relevant documents.

    Args:
        input: Validated search parameters

    Returns:
        Validated search results

    Example:
        input = SearchInput(query="RAG", limit=5)
        output = search_knowledge_base(input)
        for result in output.results:
            print(f"{result.title}: {result.score}")
    """
    # Your implementation (all inputs/outputs are validated!)
    results = [
        SearchResult(id="1", title="RAG Overview", content="...", score=0.95),
        SearchResult(id="2", title="RAG Tutorial", content="...", score=0.87),
    ]

    return SearchOutput(
        results=results,
        total_found=len(results),
        query_time_ms=45.2
    )
```

**Benefits:**
- ✓ Input is validated before function runs
- ✓ Output is validated before function returns
- ✓ LLMs get perfect schema from `.model_json_schema()`
- ✓ Your code can't receive bad data
- ✓ Type hints make IDE autocomplete work

---

## QUICK REFERENCE

### Basic Model
```python
from pydantic import BaseModel

class MyModel(BaseModel):
    field: str
```

### With Field Descriptions
```python
from pydantic import BaseModel, Field

class MyModel(BaseModel):
    field: str = Field(..., description="Description for LLM")
```

### With Defaults
```python
field: int = Field(10, description="...")
```

### With Constraints
```python
count: int = Field(10, ge=0, le=100)  # 0 <= count <= 100
name: str = Field(..., min_length=1, max_length=50)
```

### Optional Fields
```python
from typing import Optional

optional_field: Optional[str] = Field(None, description="...")
```

### Lists and Nested
```python
from typing import List

items: List[str] = Field(default_factory=list)
nested: List[NestedModel] = Field(default_factory=list)
```

### Generate Schema
```python
schema = MyModel.model_json_schema()
```

---

## NEXT STEPS

**You now know:**
✓ Why Pydantic is industry-standard for agents
✓ How to define `BaseModel` classes
✓ How to use `Field` for LLM-friendly schemas
✓ How to validate inputs/outputs automatically
✓ How to generate JSON schemas for LLMs

**Next lesson:** [L03: Function Calling Patterns](../L03_Function_Calling_Patterns/) — See how frameworks like LangChain use these patterns in production.

---

## PRACTICE EXERCISE

Create a Pydantic model for a "Calculator" tool:

**Requirements:**
- Operation: required, must be "add", "subtract", "multiply", or "divide"
- Number 1: required float
- Number 2: required float
- Precision: optional int (decimal places), default 2, range 0-10

**Solution:**
```python
from pydantic import BaseModel, Field
from typing import Literal

class CalculatorInput(BaseModel):
    operation: Literal["add", "subtract", "multiply", "divide"] = Field(
        ...,
        description="Math operation to perform"
    )
    num1: float = Field(..., description="First number")
    num2: float = Field(..., description="Second number")
    precision: int = Field(
        2,
        description="Decimal places in result",
        ge=0,
        le=10
    )

# Test it
calc = CalculatorInput(operation="add", num1=5.5, num2=3.2, precision=3)
print(calc.model_json_schema())  # See what the LLM sees!
```

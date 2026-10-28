# Phase 3 Quick Start: Tool Use & Function Calling
> **From Zero to Production-Ready Agent Tools in 30 Minutes**

---

## THE 5-MINUTE VERSION

**To make a function that AI agents can call:**

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Any

# 1. Define input schema (Pydantic)
class SearchInput(BaseModel):
    query: str = Field(..., description="Search query")
    max_results: int = Field(10, description="Max results", ge=1, le=100)

# 2. Write the function with type hints and docstring
def search_knowledge_base(
    query: str,
    max_results: int = 10
) -> List[Dict[str, Any]]:
    """
    Search the knowledge base for relevant documents.

    Use this when the user asks questions requiring information lookup.

    Args:
        query: The search query (user's question or keywords)
        max_results: Maximum number of results to return

    Returns:
        List of documents with 'title', 'content', and 'score' fields
    """
    # Your implementation
    results = vector_db.search(query, k=max_results)
    return results

# 3. Generate schema for LLM
schema = SearchInput.model_json_schema()

# 4. Register with your agent framework
# (OpenAI, Anthropic, LangChain, etc.)
```

**That's it. This works with OpenAI, Anthropic Claude, LangChain, CrewAI, and AutoGen.**

---

## THE 15-MINUTE DEEP DIVE

### Step 1: Understand What LLMs Need

LLMs don't see your code. They see a JSON schema:

```json
{
  "name": "search_knowledge_base",
  "description": "Search the knowledge base for relevant documents.",
  "parameters": {
    "type": "object",
    "properties": {
      "query": {"type": "string", "description": "Search query"},
      "max_results": {"type": "integer", "description": "Max results", "default": 10}
    },
    "required": ["query"]
  }
}
```

**Your job:** Write Python that generates this schema automatically.

---

### Step 2: The Three-Layer System

**Layer 1: Type Hints** (structure)
```python
def search(query: str, limit: int = 10) -> List[dict]:
    pass
```
→ LLM knows: "query is a string, limit is an int with default 10"

**Layer 2: Docstrings** (meaning)
```python
def search(query: str, limit: int = 10) -> List[dict]:
    """
    Search for documents.

    Args:
        query: The search query
        limit: Max results

    Returns:
        List of matching documents
    """
    pass
```
→ LLM knows: "Use this to search for documents. Pass a query and optionally a limit."

**Layer 3: Pydantic** (validation)
```python
from pydantic import BaseModel, Field

class SearchInput(BaseModel):
    query: str = Field(..., description="Search query", min_length=1)
    limit: int = Field(10, description="Max results", ge=1, le=100)

def search(input: SearchInput) -> List[dict]:
    """Search for documents."""
    # input.query is guaranteed valid!
    # input.limit is guaranteed between 1-100!
    pass
```
→ Pydantic validates + generates perfect JSON schema

---

### Step 3: Pick Your Pattern

**Pattern A: Simple Function (Good for Prototypes)**
```python
def get_weather(location: str, units: str = "celsius") -> dict:
    """
    Get current weather for a location.

    Args:
        location: City name or coordinates
        units: Temperature units (celsius/fahrenheit)

    Returns:
        Weather data with temperature and conditions
    """
    return {"temperature": 15, "conditions": "cloudy"}
```

**Pattern B: Pydantic Input (Production Standard)**
```python
from pydantic import BaseModel, Field

class WeatherInput(BaseModel):
    location: str = Field(..., description="City name or coordinates")
    units: str = Field("celsius", description="Temperature units")

def get_weather(input: WeatherInput) -> dict:
    """Get current weather for a location."""
    return {"temperature": 15, "conditions": "cloudy"}
```

**Pattern C: Full Pydantic (Maximum Safety)**
```python
from pydantic import BaseModel, Field

class WeatherInput(BaseModel):
    location: str = Field(..., description="City name")
    units: str = Field("celsius", description="Units")

class WeatherOutput(BaseModel):
    temperature: float = Field(..., description="Temperature")
    conditions: str = Field(..., description="Weather conditions")
    location: str = Field(..., description="Location name")

def get_weather(input: WeatherInput) -> WeatherOutput:
    """Get current weather for a location."""
    return WeatherOutput(
        temperature=15.0,
        conditions="cloudy",
        location=input.location
    )
```

**Recommendation:** Start with Pattern B, upgrade to Pattern C for production.

---

### Step 4: Register With Your Framework

**OpenAI Function Calling:**
```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": WeatherInput.model_json_schema()
        }
    }
]

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "What's the weather in Paris?"}],
    tools=tools
)
```

**Anthropic Claude Tool Use:**
```python
tools = [
    {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "input_schema": WeatherInput.model_json_schema()
    }
]

message = client.messages.create(
    model="claude-opus-5-5",
    messages=[{"role": "user", "content": "What's the weather in Paris?"}],
    tools=tools
)
```

**LangChain:**
```python
from langchain_core.tools import Tool   # LangChain 1.x path (0.x: from langchain.tools import Tool)

weather_tool = Tool(
    name="get_weather",
    description="Get current weather for a location",
    func=get_weather,
    args_schema=WeatherInput  # Pydantic model!
)

agent = create_openai_functions_agent(llm, tools=[weather_tool], ...)
```

---

## THE 30-MINUTE WORKSHOP: BUILD A REAL TOOL

**Goal:** Create a working search tool that validates inputs and handles errors.

### Task 1: Define the Tool (5 min)
```python
from pydantic import BaseModel, Field
from typing import List, Dict, Any

class SearchInput(BaseModel):
    query: str = Field(
        ...,
        description="The search query",
        min_length=1,
        max_length=500
    )
    max_results: int = Field(
        10,
        description="Maximum results to return",
        ge=1,
        le=50
    )
    filters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Optional filters"
    )

class SearchResult(BaseModel):
    title: str
    content: str
    score: float = Field(..., ge=0.0, le=1.0)
    url: str

class SearchOutput(BaseModel):
    results: List[SearchResult]
    total_found: int
    query_time_ms: float
```

### Task 2: Implement the Function (10 min)
```python
def search_knowledge_base(input: SearchInput) -> SearchOutput:
    """
    Search the knowledge base for relevant documents.

    Use this when the user asks questions requiring information lookup.

    Args:
        input: Validated search parameters

    Returns:
        Search results with metadata

    Example:
        input = SearchInput(query="Python best practices", max_results=5)
        output = search_knowledge_base(input)
    """
    import time
    start = time.time()

    # Fake implementation (replace with real search)
    fake_results = [
        SearchResult(
            title="Python Best Practices Guide",
            content="Use type hints, write docstrings...",
            score=0.95,
            url="https://example.com/python-guide"
        ),
        SearchResult(
            title="Python Style Guide",
            content="Follow PEP 8, use meaningful names...",
            score=0.87,
            url="https://example.com/pep8"
        )
    ]

    # Filter by query relevance (simplified)
    filtered = [r for r in fake_results if input.query.lower() in r.title.lower()]

    # Limit results
    limited = filtered[:input.max_results]

    query_time = (time.time() - start) * 1000

    return SearchOutput(
        results=limited,
        total_found=len(filtered),
        query_time_ms=query_time
    )
```

### Task 3: Add Error Handling (10 min)
```python
from pydantic import ValidationError

def execute_search_safely(query: str, max_results: int = 10) -> dict:
    """
    Safe wrapper for search function with validation and error handling.

    Returns:
        {
            "success": bool,
            "data": SearchOutput (if success),
            "error": str (if failure)
        }
    """
    try:
        # Validate input
        search_input = SearchInput(
            query=query,
            max_results=max_results
        )

        # Execute search
        output = search_knowledge_base(search_input)

        return {
            "success": True,
            "data": output.model_dump()
        }

    except ValidationError as e:
        return {
            "success": False,
            "error": f"Invalid input: {str(e)}"
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Search failed: {str(e)}"
        }
```

### Task 4: Generate Schema & Test (5 min)
```python
# Generate schema for LLM
schema = SearchInput.model_json_schema()
print("Tool Schema:")
print(json.dumps(schema, indent=2))

# Test the tool
result = execute_search_safely("Python", max_results=3)
if result["success"]:
    print(f"Found {result['data']['total_found']} results")
    for r in result['data']['results']:
        print(f"- {r['title']}: {r['score']}")
else:
    print(f"Error: {result['error']}")
```

---

## COMMON PATTERNS CHEAT SHEET

### Pattern: Search/Retrieval
```python
class SearchInput(BaseModel):
    query: str = Field(..., description="Search query")
    max_results: int = Field(10, ge=1, le=100)
    filters: Optional[Dict] = None

def search(input: SearchInput) -> List[Dict[str, Any]]:
    """Search for documents."""
    pass
```

### Pattern: Data Filtering
```python
class FilterInput(BaseModel):
    data: List[Dict[str, Any]] = Field(..., description="Data to filter")
    field: str = Field(..., description="Field to filter on")
    value: Any = Field(..., description="Value to match")

def filter_data(input: FilterInput) -> List[Dict[str, Any]]:
    """Filter data by field value."""
    pass
```

### Pattern: Aggregation/Calculation
```python
class AggregateInput(BaseModel):
    values: List[float] = Field(..., description="Values to aggregate")
    operation: Literal["sum", "avg", "min", "max"] = Field(..., description="Operation")

def aggregate(input: AggregateInput) -> float:
    """Aggregate numeric values."""
    pass
```

### Pattern: API Call
```python
class APICallInput(BaseModel):
    endpoint: str = Field(..., description="API endpoint")
    method: Literal["GET", "POST", "PUT", "DELETE"] = "GET"
    params: Dict[str, Any] = Field(default_factory=dict)

def call_api(input: APICallInput) -> Dict[str, Any]:
    """Make HTTP API call."""
    pass
```

---

## TROUBLESHOOTING

### "LLM isn't calling my tool"
**Fix:** Improve the description in the docstring and Field descriptions
```python
# BAD
"""Search."""

# GOOD
"""Search the knowledge base for relevant documents. Use this when the user asks questions that require looking up information."""
```

### "LLM is passing wrong parameters"
**Fix:** Add Field constraints and better descriptions
```python
# BAD
limit: int

# GOOD
limit: int = Field(
    10,
    description="Maximum number of results to return (recommended: 5-10)",
    ge=1,
    le=100
)
```

### "Tool is crashing on bad input"
**Fix:** Use Pydantic validation and safe execution wrapper
```python
try:
    validated_input = MyInputModel(**raw_args)
    result = my_tool(validated_input)
except ValidationError as e:
    return {"error": f"Invalid input: {e}"}
except Exception as e:
    return {"error": f"Tool failed: {e}"}
```

---

## NEXT STEPS

1. **Browse the templates:**
   - [L01/template_search_tools.py](L01_TypeHints_Docstrings/template_search_tools.py)
   - [L02/template_agent_schemas.py](L02_Pydantic_Fundamentals/template_agent_schemas.py)

2. **Read the full lessons:**
   - [L01: Type Hints & Docstrings](L01_TypeHints_Docstrings/README.md)
   - [L02: Pydantic Fundamentals](L02_Pydantic_Fundamentals/README.md)
   - [L03: Function Calling Patterns](L03_Function_Calling_Patterns/README.md)

3. **Build your first agent:**
   - Pick a simple task (weather, calculator, search)
   - Define input/output with Pydantic
   - Write the function with full documentation
   - Test with OpenAI or Anthropic

---

**Remember:** You're not memorizing syntax. You're learning patterns. Copy the templates, modify for your use case, and ship.

# Phase 3 Cheat Sheet: Tool Use & Function Calling
> **One-Page Reference for Agent Tool Development**

---

## THE MINIMAL TOOL TEMPLATE

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Any

class ToolInput(BaseModel):
    param1: str = Field(..., description="Description for LLM")
    param2: int = Field(10, description="Description", ge=1, le=100)

def my_tool(input: ToolInput) -> Dict[str, Any]:
    """
    One-sentence description of what this tool does.

    Use this when [describe when LLM should call this].

    Args:
        input: Validated input parameters

    Returns:
        Dictionary with results

    Example:
        input = ToolInput(param1="test", param2=5)
        result = my_tool(input)
    """
    # Implementation
    return {"result": "success"}

# Generate schema for LLM
schema = ToolInput.model_json_schema()
```

---

## TYPE HINTS QUICK REFERENCE

```python
from typing import List, Dict, Any, Optional, Literal, Union

# Basic types
name: str                           # String
count: int                          # Integer
score: float                        # Float
active: bool                        # Boolean

# Collections
tags: List[str]                     # List of strings
metadata: Dict[str, Any]            # Dictionary
results: List[Dict[str, Any]]       # List of dicts

# Optional (can be None)
description: Optional[str] = None   # String or None
limit: int | None = None            # Python 3.10+ syntax

# Literal (specific values only)
mode: Literal["fast", "accurate"]   # Must be one of these

# Union (multiple types)
value: Union[int, float]            # Can be int or float
```

---

## PYDANTIC FIELD PARAMETERS

```python
from pydantic import Field

# Required field (no default)
query: str = Field(..., description="Search query")

# With default value
limit: int = Field(10, description="Max results")

# Numeric constraints
age: int = Field(..., ge=0, le=120)              # 0 <= age <= 120
score: float = Field(..., gt=0.0, le=1.0)        # 0.0 < score <= 1.0

# String constraints
name: str = Field(..., min_length=1, max_length=100)
email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")

# List constraints
items: List[str] = Field(..., min_length=1, max_length=10)   # v1 called these min_items/max_items

# Default factory (for mutable defaults)
tags: List[str] = Field(default_factory=list)
metadata: Dict = Field(default_factory=dict)
```

---

## DOCSTRING TEMPLATE (Google Style)

```python
def function_name(param1: str, param2: int = 10) -> List[dict]:
    """
    One-sentence summary of what the function does.

    Optional extended description. Use this when [explain when to call].

    Args:
        param1: Description of param1
        param2: Description of param2 (default: 10)

    Returns:
        Description of return value structure

    Raises:
        ValueError: When this error occurs
        KeyError: When this error occurs

    Example:
        result = function_name("test", param2=5)
        print(result)
    """
    pass
```

---

## COMMON TOOL PATTERNS

### Search/Retrieval
```python
class SearchInput(BaseModel):
    query: str = Field(..., description="Search query", min_length=1)
    max_results: int = Field(10, ge=1, le=100)

def search(input: SearchInput) -> List[Dict[str, Any]]:
    """Search for documents."""
    pass
```

### Filtering
```python
class FilterInput(BaseModel):
    data: List[Dict] = Field(..., description="Data to filter")
    field: str = Field(..., description="Field name")
    value: Any = Field(..., description="Value to match")

def filter_data(input: FilterInput) -> List[Dict]:
    """Filter data by field value."""
    pass
```

### Calculation/Aggregation
```python
class CalcInput(BaseModel):
    values: List[float] = Field(..., description="Values")
    operation: Literal["sum", "avg", "min", "max"]

def calculate(input: CalcInput) -> float:
    """Aggregate numeric values."""
    pass
```

### API Call
```python
class APIInput(BaseModel):
    endpoint: str = Field(..., description="URL endpoint")
    method: Literal["GET", "POST"] = "GET"
    params: Dict = Field(default_factory=dict)

def call_api(input: APIInput) -> Dict:
    """Make HTTP API request."""
    pass
```

---

## ERROR HANDLING WRAPPER

```python
from pydantic import ValidationError

def execute_tool_safely(tool_func, input_model, **raw_args):
    """
    Safe tool execution with validation and error handling.

    Returns:
        {"success": True, "result": ...} or
        {"success": False, "error": "..."}
    """
    try:
        # Validate input
        validated = input_model(**raw_args)

        # Execute function
        result = tool_func(validated)

        return {"success": True, "result": result}

    except ValidationError as e:
        return {"success": False, "error": f"Validation: {e}"}

    except Exception as e:
        return {"success": False, "error": f"Execution: {e}"}
```

---

## FRAMEWORK INTEGRATION

### OpenAI Function Calling
```python
tools = [{
    "type": "function",
    "function": {
        "name": "my_tool",
        "description": "Tool description",
        "parameters": MyInputModel.model_json_schema()
    }
}]

response = client.chat.completions.create(
    model="gpt-4",
    messages=[...],
    tools=tools
)
```

### Anthropic Claude
```python
tools = [{
    "name": "my_tool",
    "description": "Tool description",
    "input_schema": MyInputModel.model_json_schema()
}]

message = client.messages.create(
    model="claude-opus-4-8",
    messages=[...],
    tools=tools
)
```

### LangChain
```python
from langchain_core.tools import Tool   # LangChain 1.x path (0.x: from langchain.tools import Tool)

tool = Tool(
    name="my_tool",
    description="Tool description",
    func=my_tool_function,
    args_schema=MyInputModel
)

agent = create_openai_functions_agent(llm, tools=[tool], ...)
```

---

## PYDANTIC QUICK METHODS

```python
# Create instance
obj = MyModel(field1="value", field2=10)

# Convert to dict
data = obj.model_dump()

# Convert to JSON string
json_str = obj.model_dump_json()

# Create from dict
obj = MyModel(**{"field1": "value", "field2": 10})

# Create from JSON
obj = MyModel.model_validate_json('{"field1": "value", "field2": 10}')

# Generate JSON schema
schema = MyModel.model_json_schema()

# Validate data (raises ValidationError if invalid)
MyModel.model_validate(data)
```

---

## VALIDATION CONSTRAINTS

```python
from pydantic import Field, field_validator, ValidationInfo

class MyModel(BaseModel):
    # Field-level constraints
    age: int = Field(..., ge=0, le=120)
    email: str = Field(..., pattern=r"^[\w\.-]+@")

    # Custom validator
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email')
        return v.lower()

    # Dependent validation
    # (info.data holds fields declared ABOVE this one)
    @field_validator('field2')
    @classmethod
    def validate_field2(cls, v, info: ValidationInfo):
        if info.data.get('field1') == 'special':
            if v < 10:
                raise ValueError('field2 must be >= 10 when field1 is special')
        return v
```

---

## THE ReAct AGENT LOOP

```python
def agent_loop(user_query: str, tools: dict, max_iterations: int = 10):
    """Standard ReAct agent loop."""

    messages = [{"role": "user", "content": user_query}]

    for i in range(max_iterations):
        # REASON: Get LLM's decision
        response = llm.chat(messages, tools=tools)

        # Check if done
        if not response.get("tool_call"):
            return response["content"]

        # ACT: Execute tool
        tool_name = response["tool_call"]["name"]
        tool_args = response["tool_call"]["arguments"]

        result = execute_tool_safely(
            tools[tool_name]["function"],
            tools[tool_name]["input_model"],
            **tool_args
        )

        # OBSERVE: Add result to context
        messages.append({
            "role": "tool",
            "name": tool_name,
            "content": json.dumps(result)
        })

    return "Max iterations reached"
```

---

## DEBUGGING CHECKLIST

**LLM not calling tool?**
- [ ] Description clear and specific?
- [ ] "Use this when..." in docstring?
- [ ] Tool name descriptive?

**LLM passing wrong types?**
- [ ] Type hints on all parameters?
- [ ] Field descriptions clear?
- [ ] Examples in docstring?

**Tool crashing?**
- [ ] Pydantic validation in place?
- [ ] Error handling wrapper used?
- [ ] Constraints on fields (min/max)?

**Schema not generating correctly?**
- [ ] Using `model_json_schema()` not `schema()`?
- [ ] All fields have descriptions?
- [ ] Imports correct (`from pydantic import BaseModel`)?

---

## MINIMAL WORKING EXAMPLE

```python
from pydantic import BaseModel, Field
from typing import Dict, Any

# 1. Define input schema
class WeatherInput(BaseModel):
    location: str = Field(..., description="City name")
    units: str = Field("celsius", description="Temperature units")

# 2. Define function
def get_weather(input: WeatherInput) -> Dict[str, Any]:
    """
    Get current weather for a location.

    Use this when the user asks about weather or temperature.

    Args:
        input: Validated weather request parameters

    Returns:
        Weather data with temperature and conditions
    """
    return {
        "location": input.location,
        "temperature": 15.0,
        "conditions": "cloudy",
        "units": input.units
    }

# 3. Generate schema
schema = WeatherInput.model_json_schema()

# 4. Test
test_input = WeatherInput(location="Paris", units="celsius")
result = get_weather(test_input)
print(result)  # {"location": "Paris", "temperature": 15.0, ...}
```

---

## TOOL USE vs STRUCTURED OUTPUT — When to Use Which

This is the most important 2026 decision point. Both extract structured data from Claude, but they're not interchangeable.

```
TOOL USE                              STRUCTURED OUTPUT (tool_choice)
───────────────────────────────────   ─────────────────────────────────────
Agent ACTS on the world               Agent EXTRACTS typed data from text
Has side effects (writes, calls APIs) Pure read — no side effects
LLM decides WHEN to call              You FORCE when it happens
Result feeds back into the loop       Result exits the agent loop
Use for: search, write file, call DB  Use for: classify, extract, parse

# Tool use — agent chooses to call
tools = [{"name": "search_web", ...}]
response = client.messages.create(tools=tools, ...)
# → LLM may or may not call search_web depending on the task

# Structured output — you force extraction
tools = [{"name": "ExtractOutput", "input_schema": MyModel.model_json_schema()}]
response = client.messages.create(
    tools=tools,
    tool_choice={"type": "tool", "name": "ExtractOutput"},  # ← FORCE it
    messages=[{"role": "user", "content": "Classify this: " + text}]
)
result = MyModel(**response.content[0].input)   # → always typed, never optional
```

**Rule:** If you need data back as a Python object with guaranteed structure → Structured Output.
If you need the agent to go do something → Tool Use.

> **Model caveat (Anthropic tool-use docs, retrieved 2026-10-28):** Claude Opus 5.5, Claude Sonnet 5.5, Claude Fable 5.1 and Claude Mythos 5.1 reject forced tool use: `tool_choice` of type `any` or `tool` returns a 400 error. On those models, use `tool_choice={"type": "auto"}` with `"strict": true` on the tool definition (schema-valid tool inputs), or structured outputs when you need a response in a fixed JSON shape. Forcing still works on models that support it; check the docs for the model you call.

---

## TOOL_CHOICE — Force Specific Behavior

```python
# Default: LLM decides whether to call any tool
# (no tool_choice param)

# Force a tool call — LLM must call at least one tool
tool_choice = {"type": "any"}

# Force a SPECIFIC tool — guaranteed structured output
tool_choice = {"type": "tool", "name": "my_tool_name"}

# Disable tools entirely in this call
tool_choice = {"type": "none"}
```

On models that support forced tool use, `tool_choice={"type": "tool", "name": "..."}` guarantees the tool is called. Without it, Claude may answer in plain text instead of calling the tool.

> **Model caveat (Anthropic tool-use docs, retrieved 2026-10-28):** Claude Opus 5.5, Claude Sonnet 5.5, Claude Fable 5.1 and Claude Mythos 5.1 reject forced tool use: `tool_choice` of type `any` or `tool` returns a 400 error. On those models, use `tool_choice={"type": "auto"}` with `"strict": true` on the tool definition (schema-valid tool inputs), or structured outputs when you need a response in a fixed JSON shape. Forcing still works on models that support it; check the docs for the model you call.

---

## PYDANTIC V2 vs V1 — What you'll see in the wild

```
v1 (pre-2023, still common in older repos)   v2 (2023+, use this)
─────────────────────────────────────────    ──────────────────────────────
obj.schema()                                 obj.model_json_schema()
obj.parse_obj(data)                          obj.model_validate(data)
obj.dict()                                   obj.model_dump()
@validator("field")                          @field_validator("field")
class Config:                                model_config = ConfigDict(...)
    orm_mode = True

This cheatsheet uses Pydantic v2 throughout.
If you see .schema() or .dict() in AI-generated code → that's v1.
Both run in Python 3.13+ but v1 methods show deprecation warnings.
```

---

## QUICK WINS

1. **Always use Pydantic** for inputs (even simple ones)
2. **Always add Field descriptions** (LLMs read them!)
3. **Always include a docstring example** (helps LLM understand)
4. **Always use error handling wrapper** (tools will fail)
5. **Always test schema generation** (`model_json_schema()`)

---

## ONE-LINER REMINDERS

- **Type hints** → LLM knows structure
- **Docstrings** → LLM knows when to call
- **Pydantic** → Validation + schema generation
- **Field descriptions** → LLM knows what to pass
- **Error handling** → Agent doesn't break
- **ReAct pattern** → Reason → Act → Observe → Repeat

---

**Need more?** See [QUICKSTART.md](QUICKSTART.md) or individual lesson READMEs.

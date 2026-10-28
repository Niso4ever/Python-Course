# L03: Function Calling Patterns
> **How AI Agents Actually Use Your Tools in Production**

---

## THE BIG PICTURE

You've learned:
- **L01:** How to write functions LLMs can understand (type hints + docstrings)
- **L02:** How to validate data with Pydantic (input/output schemas)

**Now:** See how frameworks like LangChain, OpenAI, and Anthropic actually wire these together.

---

## THE ReAct PATTERN (Reason + Act)

Almost ALL modern agents use this loop:

```
1. REASON: "What should I do next?"
2. ACT: Call a tool with parameters
3. OBSERVE: See the tool's result
4. (Repeat until task is complete)
5. RESPOND: Give final answer to user
```

### Visual Flow:
```
User: "What's the weather in Paris?"
         |
         ↓
    ┌─────────────────────┐
    │  REASON (LLM)       │
    │  "I need to get     │
    │   weather data for  │
    │   Paris"            │
    └─────────────────────┘
         |
         ↓
    ┌─────────────────────┐
    │  ACT (Tool Call)    │
    │  get_weather(       │
    │    location="Paris" │
    │  )                  │
    └─────────────────────┘
         |
         ↓
    ┌─────────────────────┐
    │  OBSERVE (Result)   │
    │  {                  │
    │    "temp": 15,      │
    │    "conditions":    │
    │      "cloudy"       │
    │  }                  │
    └─────────────────────┘
         |
         ↓
    ┌─────────────────────┐
    │  REASON (LLM)       │
    │  "I have the data,  │
    │   I can respond"    │
    └─────────────────────┘
         |
         ↓
    Assistant: "It's 15°C and cloudy in Paris."
```

---

## PATTERN 1: Single Tool Call (OpenAI Style)

### Your Function:
```python
from pydantic import BaseModel, Field

class WeatherInput(BaseModel):
    location: str = Field(..., description="City name or coordinates")
    units: str = Field("celsius", description="Temperature units")

def get_weather(location: str, units: str = "celsius") -> dict:
    """
    Get current weather for a location.

    Args:
        location: City name or coordinates
        units: Temperature units (celsius/fahrenheit)

    Returns:
        Weather data with temperature and conditions
    """
    # Implementation
    return {"temperature": 15, "conditions": "cloudy", "location": location}
```

### Tool Schema (What LLM Sees):
```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name or coordinates"
                    },
                    "units": {
                        "type": "string",
                        "description": "Temperature units (celsius/fahrenheit)",
                        "enum": ["celsius", "fahrenheit"]
                    }
                },
                "required": ["location"]
            }
        }
    }
]
```

### LLM Response (Function Call):
```json
{
  "role": "assistant",
  "content": null,
  "function_call": {
    "name": "get_weather",
    "arguments": "{\"location\": \"Paris\", \"units\": \"celsius\"}"
  }
}
```

### Your Code Executes:
```python
import json

# Parse LLM's function call
func_name = llm_response["function_call"]["name"]
func_args = json.loads(llm_response["function_call"]["arguments"])

# Execute the function
if func_name == "get_weather":
    result = get_weather(**func_args)

# Send result back to LLM
messages.append({
    "role": "function",
    "name": func_name,
    "content": json.dumps(result)
})
```

---

## PATTERN 2: Multi-Tool Selection

The LLM chooses which tool to use based on the user's request.

### Your Tools:
```python
from pydantic import BaseModel, Field
from typing import List, Dict, Any

class SearchInput(BaseModel):
    query: str = Field(..., description="Search query")
    max_results: int = Field(5, description="Max results")

class CalculatorInput(BaseModel):
    expression: str = Field(..., description="Math expression to evaluate")

class WeatherInput(BaseModel):
    location: str = Field(..., description="City name")


def search_web(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """Search the web for information."""
    pass

def calculate(expression: str) -> float:
    """Evaluate a mathematical expression."""
    pass

def get_weather(location: str) -> dict:
    """Get current weather for a location."""
    pass
```

### Tool Registry:
```python
TOOLS = {
    "search_web": {
        "function": search_web,
        "schema": SearchInput.model_json_schema(),
        "description": "Search the web for information"
    },
    "calculate": {
        "function": calculate,
        "schema": CalculatorInput.model_json_schema(),
        "description": "Evaluate a mathematical expression"
    },
    "get_weather": {
        "function": get_weather,
        "schema": WeatherInput.model_json_schema(),
        "description": "Get current weather for a location"
    }
}
```

### LLM Selects Tool:
```
User: "What's 25 * 48?"
  → LLM picks: calculate(expression="25 * 48")

User: "What's the weather in Tokyo?"
  → LLM picks: get_weather(location="Tokyo")

User: "Find information about quantum computing"
  → LLM picks: search_web(query="quantum computing")
```

---

## PATTERN 3: Sequential Tool Calls (Chain)

The LLM calls multiple tools in sequence to complete a task.

### Example: Research Task
```
User: "Research Python best practices and summarize the top 3"

Step 1 - REASON: "I need to search for information"
Step 1 - ACT: search_web(query="Python best practices", max_results=10)
Step 1 - OBSERVE: [10 search results]

Step 2 - REASON: "I should filter to only high-quality sources"
Step 2 - ACT: filter_results(results=..., min_score=0.8)
Step 2 - OBSERVE: [5 filtered results]

Step 3 - REASON: "Now I'll summarize the top 3"
Step 3 - ACT: summarize_texts(texts=[...], max_items=3)
Step 3 - OBSERVE: [3 summaries]

Step 4 - REASON: "I have everything, I can respond"
Step 4 - RESPOND: "Here are the top 3 Python best practices: ..."
```

### Implementation Pattern:
```python
def agent_loop(user_query: str, max_iterations: int = 10):
    """ReAct agent loop."""

    messages = [{"role": "user", "content": user_query}]

    for iteration in range(max_iterations):
        # 1. REASON: Get LLM's next action
        response = llm.chat(messages, tools=TOOLS)

        # 2. Check if done
        if response.get("function_call") is None:
            # LLM is responding directly, we're done
            return response["content"]

        # 3. ACT: Execute the tool
        func_name = response["function_call"]["name"]
        func_args = json.loads(response["function_call"]["arguments"])

        tool = TOOLS[func_name]
        result = tool["function"](**func_args)

        # 4. OBSERVE: Add result to conversation
        messages.append({
            "role": "function",
            "name": func_name,
            "content": json.dumps(result)
        })

    return "Max iterations reached"
```

---

## PATTERN 4: Parallel Tool Calls

Some frameworks support calling multiple tools at once.

### Example: Anthropic Claude Tool Use
```python
# LLM decides to call multiple tools in parallel
response = {
    "tool_calls": [
        {
            "name": "get_weather",
            "arguments": {"location": "Paris"}
        },
        {
            "name": "get_weather",
            "arguments": {"location": "London"}
        },
        {
            "name": "get_weather",
            "arguments": {"location": "Berlin"}
        }
    ]
}

# Execute all in parallel
import asyncio

async def execute_tools_parallel(tool_calls):
    tasks = []
    for call in tool_calls:
        func = TOOLS[call["name"]]["function"]
        task = asyncio.create_task(func(**call["arguments"]))
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    return results
```

---

## PATTERN 5: Tool Error Handling

What happens when a tool fails?

### Robust Tool Wrapper:
```python
from pydantic import ValidationError
import traceback

def execute_tool_safely(tool_name: str, arguments: dict) -> dict:
    """
    Execute a tool with error handling.

    Returns:
        {
            "success": bool,
            "result": Any,      # if success
            "error": str,       # if failure
            "error_type": str   # if failure
        }
    """
    try:
        # 1. Get tool
        if tool_name not in TOOLS:
            return {
                "success": False,
                "error": f"Tool '{tool_name}' not found",
                "error_type": "ToolNotFoundError"
            }

        tool = TOOLS[tool_name]

        # 2. Validate inputs (Pydantic)
        input_model = tool.get("input_model")
        if input_model:
            validated_args = input_model(**arguments)
            arguments = validated_args.model_dump()

        # 3. Execute function
        result = tool["function"](**arguments)

        # 4. Validate output (Pydantic)
        output_model = tool.get("output_model")
        if output_model:
            validated_result = output_model(**result)
            result = validated_result.model_dump()

        return {
            "success": True,
            "result": result
        }

    except ValidationError as e:
        return {
            "success": False,
            "error": f"Validation error: {str(e)}",
            "error_type": "ValidationError"
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Execution error: {str(e)}",
            "error_type": type(e).__name__,
            "traceback": traceback.format_exc()
        }
```

### LLM Handles Errors:
```
Step 1 - ACT: search_web(query="", max_results=5)
Step 1 - OBSERVE: {"success": false, "error": "Validation error: query cannot be empty"}

Step 2 - REASON: "The search failed because I didn't provide a query. Let me try again."
Step 2 - ACT: search_web(query="Python tutorials", max_results=5)
Step 2 - OBSERVE: {"success": true, "result": [...]}
```

---

## PATTERN 6: LangChain Tool Pattern

How LangChain wraps your functions:

```python
from langchain_core.tools import Tool   # LangChain 1.x path (0.x: from langchain.tools import Tool)
from pydantic import BaseModel, Field

# Your Pydantic input model
class SearchInput(BaseModel):
    query: str = Field(..., description="Search query")
    max_results: int = Field(5, description="Max results")

# Your function
def search_web(query: str, max_results: int = 5) -> list:
    """Search the web for information."""
    # Implementation
    return [{"title": "Result 1", "url": "..."}]

# Wrap as LangChain tool
search_tool = Tool(
    name="search_web",
    description="Search the web for information. Use this when you need to find current information.",
    func=search_web,
    args_schema=SearchInput  # ← Pydantic model for validation!
)

# LangChain agent can now use it
# LangChain 1.x:  from langchain.agents import create_agent
#                 agent = create_agent(model, tools=[search_tool], system_prompt="...")
# LangChain 0.x (now in langchain-classic):
from langchain_classic.agents import AgentExecutor, create_openai_functions_agent

agent = create_openai_functions_agent(llm, tools=[search_tool], ...)
```

---

## PATTERN 7: Structured Output (No Function Calls)

Sometimes you want structured output without tool calling:

```python
from pydantic import BaseModel, Field
from typing import List

class ExtractedInfo(BaseModel):
    """Structured information extracted from text."""

    main_topic: str = Field(..., description="The main topic")
    key_points: List[str] = Field(..., description="Key points (3-5 items)")
    sentiment: str = Field(..., description="Overall sentiment: positive/negative/neutral")
    confidence: float = Field(..., description="Confidence in extraction (0.0-1.0)", ge=0.0, le=1.0)


# Prompt LLM to return JSON matching this schema
prompt = f"""
Extract information from this text and return JSON matching this schema:
{ExtractedInfo.model_json_schema()}

Text: {user_text}
"""

llm_response = llm.generate(prompt)
extracted = ExtractedInfo.model_validate_json(llm_response)
# Now you have validated structured data!
```

---

## COMPLETE EXAMPLE: Mini RAG Agent

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import json

# ============== TOOLS ==============

class SearchInput(BaseModel):
    query: str = Field(..., description="Search query")
    max_results: int = Field(5, description="Max results", ge=1, le=20)

def search_knowledge_base(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """Search the knowledge base for relevant documents."""
    # Fake implementation
    return [
        {"id": "1", "title": "RAG Overview", "content": "RAG combines retrieval and generation...", "score": 0.95},
        {"id": "2", "title": "RAG Tutorial", "content": "To build a RAG system...", "score": 0.87}
    ]

class FilterInput(BaseModel):
    results: List[Dict[str, Any]] = Field(..., description="Results to filter")
    min_score: float = Field(0.7, description="Minimum score", ge=0.0, le=1.0)

def filter_by_score(results: List[Dict[str, Any]], min_score: float = 0.7) -> List[Dict[str, Any]]:
    """Filter results by relevance score."""
    return [r for r in results if r.get("score", 0) >= min_score]

# ============== TOOL REGISTRY ==============

TOOLS = {
    "search_knowledge_base": {
        "function": search_knowledge_base,
        "input_model": SearchInput,
        "description": "Search the knowledge base for relevant documents"
    },
    "filter_by_score": {
        "function": filter_by_score,
        "input_model": FilterInput,
        "description": "Filter search results by relevance score"
    }
}

# ============== AGENT LOOP ==============

def simple_agent(user_query: str, max_iterations: int = 5):
    """Simple ReAct agent."""

    conversation = [
        {"role": "system", "content": "You are a helpful assistant with access to a knowledge base."},
        {"role": "user", "content": user_query}
    ]

    for i in range(max_iterations):
        print(f"\n--- Iteration {i+1} ---")

        # Get LLM response (mock)
        # In reality, you'd call OpenAI/Anthropic API here
        if i == 0:
            # First iteration: LLM decides to search
            tool_call = {
                "name": "search_knowledge_base",
                "arguments": {"query": "RAG systems", "max_results": 5}
            }
        elif i == 1:
            # Second iteration: LLM decides to filter
            # (In reality, it would see the search results first)
            tool_call = {
                "name": "filter_by_score",
                "arguments": {"results": search_results, "min_score": 0.8}
            }
        else:
            # Third iteration: LLM responds with answer
            return "RAG combines retrieval and generation to provide accurate, grounded responses."

        # Execute tool
        tool_name = tool_call["name"]
        tool_args = tool_call["arguments"]

        print(f"TOOL: {tool_name}")
        print(f"ARGS: {tool_args}")

        result = execute_tool_safely(tool_name, tool_args)

        if result["success"]:
            print(f"RESULT: {result['result']}")
            if tool_name == "search_knowledge_base":
                search_results = result['result']  # Save for next iteration
        else:
            print(f"ERROR: {result['error']}")

    return "Max iterations reached"

# Run the agent
# answer = simple_agent("What is RAG?")
# print(f"\nFinal Answer: {answer}")
```

---

## KEY TAKEAWAYS

1. **ReAct is the standard pattern:** Reason → Act → Observe → Repeat
2. **Tools are registered in a dictionary/registry:** Name, function, schema
3. **LLMs return tool calls as JSON:** Your code parses and executes
4. **Always handle errors gracefully:** Use try/except and return error info
5. **Pydantic validates everything:** Inputs before execution, outputs after
6. **Most frameworks abstract this:** LangChain, CrewAI, etc. do the wiring for you

---

## NEXT STEPS

**You now know:**
✓ The ReAct pattern used by all modern agents
✓ How LLMs call tools (JSON function calls)
✓ How to register and execute tools safely
✓ How LangChain wraps tools

**Next lesson:** [L04: Tool Schema Design](../L04_Tool_Schemas/) — Deep dive into crafting perfect tool schemas for OpenAI, Anthropic, and LangChain.

---

## PRACTICE EXERCISE

Build a simple calculator agent with these tools:
- `add(a: float, b: float) -> float`
- `multiply(a: float, b: float) -> float`
- `get_weather(location: str) -> dict`

**Task:** Implement the tool registry and a simple execution function that:
1. Takes a tool name and arguments
2. Validates with Pydantic
3. Executes the function
4. Returns the result or error

**Hint:** Use the `execute_tool_safely` pattern from above!

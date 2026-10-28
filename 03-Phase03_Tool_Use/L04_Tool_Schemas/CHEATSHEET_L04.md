# L04 Cheat Sheet: Advanced Tool Schemas
> **Quick Reference for Production Patterns**

---

## THE UNIVERSAL TOOL PATTERN

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Callable

class UniversalTool:
    def __init__(self, name, description, input_schema, output_schema, func):
        self.name = name
        self.description = description
        self.input_schema = input_schema
        self.output_schema = output_schema
        self.func = func

    def to_openai(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.input_schema.model_json_schema()
            }
        }

    def to_anthropic(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema.model_json_schema()
        }

    def execute(self, **kwargs) -> dict:
        try:
            validated = self.input_schema(**kwargs)
            result = self.func(validated)
            return {"success": True, "data": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
```

---

## ELIMINATING LLM CONFUSION

### Clear Tool Names
```python
# BAD - Too similar
def search_web(...): pass
def search_docs(...): pass
def search_db(...): pass

# GOOD - Distinct purposes
def search_public_internet(...): pass
def search_internal_documents(...): pass
def query_database(...): pass
```

### Explicit "When to Use"
```python
def search_public_internet(input: WebSearchInput) -> dict:
    """
    Search the public internet for current information.

    **Use this when:**
    - User asks about current events, news, trending topics
    - Need information from public websites
    - Want most recent information available

    **Don't use when:**
    - Internal documents needed → search_internal_documents
    - Database query needed → query_database
    - Info in knowledge base → search_knowledge_base
    """
    pass
```

---

## HANDLING COMPLEX PARAMETERS

### BAD: Ambiguous Nested Dict
```python
# LLM struggles with this
class BadInput(BaseModel):
    filters: Dict[str, Union[str, List[str], Dict[str, Any]]]
```

### GOOD: Explicit Sub-Models
```python
class DateFilter(BaseModel):
    from_date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    to_date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")

class CategoryFilter(BaseModel):
    categories: List[str]
    match_all: bool = False

class GoodInput(BaseModel):
    date_filter: Optional[DateFilter] = None
    category_filter: Optional[CategoryFilter] = None
```

---

## ATOMIC VS WORKFLOW TOOLS

### Atomic Tools (Default Choice)
```python
# Tool 1: Search
def search(query: str) -> List[dict]: pass

# Tool 2: Filter
def filter_results(results: List[dict], min_score: float) -> List[dict]: pass

# Tool 3: Summarize
def summarize(results: List[dict]) -> str: pass

# LLM calls sequentially:
# results = search("Python")
# filtered = filter_results(results, 0.8)
# summary = summarize(filtered)
```

**Pros:** Flexible, reusable, easy to debug
**Cons:** Slower, more API calls

---

### Workflow Tool (For Performance)
```python
class WorkflowInput(BaseModel):
    query: str
    min_score: float = 0.7
    max_results: int = 5

def search_filter_summarize_workflow(input: WorkflowInput) -> dict:
    """Complete workflow in one call."""
    results = search_internal(input.query)
    filtered = filter_internal(results, input.min_score)
    summary = summarize_internal(filtered[:input.max_results])
    return {"summary": summary, "total_results": len(results)}
```

**Pros:** Faster, one call, lower token cost
**Cons:** Less flexible, harder to debug

**Rule:** Atomic for flexibility, workflow for production speed

---

## EDGE CASE HANDLING

### Empty Results
```python
class SmartOutput(BaseModel):
    results: List[dict] = Field(default_factory=list)
    is_empty: bool
    empty_reason: Optional[str] = None
    suggested_alternatives: List[str] = Field(default_factory=list)

def smart_search(input: SearchInput) -> dict:
    results = perform_search(input.query)

    if not results:
        return {
            "results": [],
            "is_empty": True,
            "empty_reason": "No documents match your query",
            "suggested_alternatives": [
                "Try broader search terms",
                "Check spelling",
                "Remove filters"
            ]
        }

    return {"results": results, "is_empty": False}
```

---

### Rate Limiting
```python
class RateLimitedOutput(BaseModel):
    success: bool
    data: Optional[Any] = None
    rate_limited: bool = False
    retry_after_seconds: Optional[int] = None
    remaining_quota: Optional[int] = None

def api_call_with_limits(input: APIInput) -> dict:
    try:
        result = external_api.call(input.endpoint)
        return {
            "success": True,
            "data": result,
            "rate_limited": False,
            "remaining_quota": api.get_quota()
        }
    except RateLimitError as e:
        return {
            "success": False,
            "rate_limited": True,
            "retry_after_seconds": e.retry_after
        }
```

---

### Partial Failures
```python
class BatchResult(BaseModel):
    item_id: str
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None

class BatchOutput(BaseModel):
    total_items: int
    successful: int
    failed: int
    results: List[BatchResult]
    partial_success: bool  # Some succeeded, some failed
    should_retry_failed: bool  # LLM should retry?
```

---

## OPTIMIZATION: TOOL SELECTION

### Problem: 50 tools = 7,500 tokens per request

### Solution: Pre-filter relevant tools
```python
class ToolSelector:
    def select_relevant_tools(
        self,
        user_query: str,
        max_tools: int = 10
    ) -> List[UniversalTool]:
        """Select most relevant tools for query."""
        query_words = set(user_query.lower().split())

        scored_tools = []
        for tool in self.all_tools:
            # Score by keyword overlap
            tool_keywords = self._get_keywords(tool)
            overlap = len(query_words & tool_keywords)

            # Boost if matches example
            if any(ex in user_query for ex in tool.example_queries):
                overlap += 10

            scored_tools.append((overlap, tool))

        # Return top N
        scored_tools.sort(reverse=True, key=lambda x: x[0])
        return [tool for score, tool in scored_tools[:max_tools]]

# Usage:
relevant_tools = selector.select_relevant_tools("Search Python tutorials", max_tools=10)
# Reduced from 50 tools to 10 → 80% token savings!
```

---

## SCHEMA CACHING

```python
from functools import lru_cache

class OptimizedTool(UniversalTool):
    @lru_cache(maxsize=1)
    def to_openai(self) -> dict:
        """Cached schema generation."""
        return super().to_openai()

    @lru_cache(maxsize=1)
    def to_anthropic(self) -> dict:
        """Cached schema generation."""
        return super().to_anthropic()
```

---

## SCHEMA DEBUGGING

### Validate Tool Quality
```python
class SchemaDebugger:
    @staticmethod
    def validate_tool(tool: UniversalTool) -> List[str]:
        issues = []

        # Check description length
        if len(tool.description) < 20:
            issues.append("⚠️ Description too short")

        # Check for guidance
        if not hasattr(tool, 'when_to_use'):
            issues.append("❌ Missing 'when_to_use' guidance")

        # Check examples
        if not hasattr(tool, 'example_queries'):
            issues.append("⚠️ No example queries")

        # Check field descriptions
        schema = tool.input_schema.model_json_schema()
        for field, info in schema.get('properties', {}).items():
            if 'description' not in info:
                issues.append(f"⚠️ Field '{field}' missing description")

        return issues

# Usage:
for tool in all_tools:
    issues = SchemaDebugger.validate_tool(tool)
    if issues:
        print(f"🔧 {tool.name}:")
        for issue in issues:
            print(f"  {issue}")
```

---

### Find Similar Tools
```python
from difflib import SequenceMatcher

def find_similar_tools(tools: List[UniversalTool]) -> List[tuple]:
    similar = []
    for i, tool1 in enumerate(tools):
        for tool2 in tools[i+1:]:
            similarity = SequenceMatcher(
                None,
                tool1.name,
                tool2.name
            ).ratio()

            if similarity > 0.7:
                similar.append((tool1.name, tool2.name, similarity))

    return sorted(similar, key=lambda x: x[2], reverse=True)

# Usage:
similar = find_similar_tools(all_tools)
for tool1, tool2, score in similar:
    print(f"⚠️ {tool1} ↔ {tool2} ({score:.0%} similar)")
```

---

## FRAMEWORK INTEGRATION

### OpenAI
```python
tools = [tool.to_openai() for tool in all_tools]

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[...],
    tools=tools
)

# Parse call
func_name = response.choices[0].message.function_call.name
func_args = json.loads(response.choices[0].message.function_call.arguments)

# Execute
result = tool_registry.execute_tool(func_name, **func_args)
```

---

### Anthropic
```python
tools = [tool.to_anthropic() for tool in all_tools]

response = anthropic.messages.create(
    model="claude-opus-5-5",
    messages=[...],
    tools=tools
)

# Parse call
for block in response.content:
    if block.type == "tool_use":
        result = tool_registry.execute_tool(block.name, **block.input)
```

---

### LangChain
```python
lc_tools = [tool.to_langchain() for tool in all_tools]

agent = create_openai_functions_agent(llm, tools=lc_tools, ...)
executor = AgentExecutor(agent=agent, tools=lc_tools)

result = executor.invoke({"input": user_query})
```

---

## QUICK WINS

1. **Use UniversalTool pattern** - Works with all frameworks
2. **Add "when to use" guidance** - Eliminates confusion
3. **Break complex params into sub-models** - LLM understands structure
4. **Handle edge cases explicitly** - Empty results, rate limits, failures
5. **Implement tool selection** - 80-90% token savings at scale
6. **Cache schemas** - Faster generation
7. **Validate with debugger** - Catch issues before production

---

## COMMON MISTAKES

### Mistake 1: Ambiguous Names
```python
# BAD
def process(...): pass   # Process what?
def handle(...): pass    # Handle what?

# GOOD
def process_payment_transaction(...): pass
def handle_user_authentication(...): pass
```

### Mistake 2: No Edge Case Handling
```python
# BAD
def search(query: str) -> List[dict]:
    return results  # What if empty?

# GOOD
def search(query: str) -> dict:
    return {
        "results": results,
        "is_empty": len(results) == 0,
        "suggestions": [...] if len(results) == 0 else []
    }
```

### Mistake 3: Sending All Tools Every Time
```python
# BAD (50 tools = expensive)
response = llm.chat(messages, tools=all_50_tools)

# GOOD (pre-filter to 10)
relevant = selector.select_relevant_tools(user_query, max_tools=10)
response = llm.chat(messages, tools=relevant)
```

---

## PERFORMANCE BENCHMARKS

| Tools | Without Selection | With Selection (max 10) | Savings |
|-------|------------------|-------------------------|---------|
| 10    | 1,500 tokens     | 1,500 tokens           | 0%      |
| 25    | 3,750 tokens     | 1,500 tokens           | 60%     |
| 50    | 7,500 tokens     | 1,500 tokens           | 80%     |
| 100   | 15,000 tokens    | 1,500 tokens           | 90%     |

**Cost savings with GPT-4:**
- 50 tools: $0.11 → $0.02 (82% savings)
- 100 tools: $0.23 → $0.02 (91% savings)

---

## KEY TAKEAWAYS

1. **Framework-agnostic design** - Build once, use everywhere
2. **Clear boundaries** - Eliminate LLM confusion with distinct names
3. **Explicit schemas** - Sub-models > nested dicts
4. **Edge case handling** - Empty, rate limits, partial failures
5. **Tool selection** - Pre-filter for performance
6. **Schema debugging** - Validate before production
7. **Choose granularity wisely** - Atomic (default) vs workflow (performance)

---

**See also:**
- [README.md](README.md) - Complete L04 guide
- [template_production_rag_tools.py](template_production_rag_tools.py) - Full RAG example
- [template_framework_adapters.py](template_framework_adapters.py) - Framework integration

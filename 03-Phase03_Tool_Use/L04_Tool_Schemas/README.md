# L04: Advanced Tool Schema Design
> **Production Patterns, Framework-Specific Schemas, and Optimization**

---

## PREREQUISITES

Before starting L04, you should have completed:
- ✓ L01: Type Hints & Docstrings
- ✓ L02: Pydantic Fundamentals
- ✓ L03: Function Calling Patterns

**This lesson assumes:** You can build basic tools and understand how LLMs call them.

---

## WHAT'S DIFFERENT IN L04

**L01-L03:** How to build tools that work
**L04:** How to build tools that work **well in production**

You'll learn:
- Framework-specific optimizations
- Schema design for complex tools
- Handling edge cases LLMs struggle with
- Performance optimization
- Advanced validation patterns
- Real-world debugging strategies

---

## THE ADVANCED CHALLENGES

### Challenge 1: Framework Differences

Different frameworks expect slightly different schemas:

```python
# OpenAI expects this:
{
    "type": "function",
    "function": {
        "name": "search",
        "parameters": {...}
    }
}

# Anthropic expects this:
{
    "name": "search",
    "input_schema": {...}
}

# LangChain expects this:
Tool(
    name="search",
    args_schema=SearchInput,  # Pydantic model
    func=search_function
)
```

**Solution:** Design schemas that adapt to all frameworks.

---

### Challenge 2: Complex Multi-Step Tools

Some tools require multiple steps:

```
User: "Find the top 3 Python experts on Twitter and summarize their recent posts"

This requires:
1. Search Twitter for "Python experts"
2. Filter by follower count
3. Get recent posts for top 3
4. Summarize each user's posts
5. Combine results
```

**Question:** One mega-tool or multiple small tools?

---

### Challenge 3: LLM Confusion Points

LLMs struggle with:
- **Similar tool names:** `search_web()` vs `search_docs()` vs `search_db()`
- **Complex parameters:** Nested dicts, optional lists, union types
- **Ambiguous returns:** "Returns a dict" (what's in the dict?)
- **Missing examples:** LLM has to guess how to use it

**Solution:** Schema design patterns that eliminate ambiguity.

---

### Challenge 4: Performance at Scale

```python
# This works for 1 tool:
def my_tool(input: MyInput) -> MyOutput:
    result = expensive_operation()
    return MyOutput(**result)

# But with 50 tools:
# - Schema generation is slow
# - Token costs are high (sending all schemas)
# - LLM takes longer to choose
```

**Solution:** Lazy loading, schema caching, tool selection optimization.

---

## ADVANCED PATTERN 1: Framework-Agnostic Tool Design

### The Universal Tool Template

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Callable
from enum import Enum

class ToolCategory(str, Enum):
    """Tool categories for organization."""
    SEARCH = "search"
    DATA = "data"
    COMPUTE = "compute"
    EXTERNAL_API = "external_api"
    UTILITY = "utility"


class UniversalToolMetadata(BaseModel):
    """Metadata that works across all frameworks."""

    # Core identification
    name: str = Field(..., description="Unique tool name (snake_case)")
    category: ToolCategory = Field(..., description="Tool category")

    # LLM-facing documentation
    description: str = Field(
        ...,
        description="One-sentence description for LLM",
        min_length=10,
        max_length=200
    )
    extended_description: Optional[str] = Field(
        None,
        description="Detailed description with usage context"
    )

    # Usage hints
    when_to_use: str = Field(
        ...,
        description="When should LLM call this tool?"
    )
    when_not_to_use: Optional[str] = Field(
        None,
        description="When should LLM avoid this tool?"
    )

    # Examples
    example_queries: List[str] = Field(
        default_factory=list,
        description="Example user queries that should trigger this tool"
    )

    # Technical metadata
    requires_auth: bool = Field(False, description="Requires authentication")
    estimated_latency_ms: Optional[int] = Field(None, description="Typical response time")
    rate_limit_per_minute: Optional[int] = Field(None, description="Rate limit")
    cost_per_call_usd: Optional[float] = Field(None, description="Cost per invocation")


class UniversalTool:
    """
    A tool wrapper that works with OpenAI, Anthropic, LangChain, etc.
    """

    def __init__(
        self,
        metadata: UniversalToolMetadata,
        input_schema: type[BaseModel],
        output_schema: type[BaseModel],
        func: Callable
    ):
        self.metadata = metadata
        self.input_schema = input_schema
        self.output_schema = output_schema
        self.func = func

    def to_openai_schema(self) -> dict:
        """Convert to OpenAI function calling format."""
        return {
            "type": "function",
            "function": {
                "name": self.metadata.name,
                "description": f"{self.metadata.description}\n\n{self.metadata.when_to_use}",
                "parameters": self.input_schema.model_json_schema()
            }
        }

    def to_anthropic_schema(self) -> dict:
        """Convert to Anthropic tool use format."""
        return {
            "name": self.metadata.name,
            "description": f"{self.metadata.description}\n\n{self.metadata.when_to_use}",
            "input_schema": self.input_schema.model_json_schema()
        }

    def to_langchain_tool(self):
        """Convert to LangChain Tool."""
        from langchain_core.tools import Tool   # LangChain 1.x path

        return Tool(
            name=self.metadata.name,
            description=f"{self.metadata.description} {self.metadata.when_to_use}",
            func=self.execute,
            args_schema=self.input_schema
        )

    def execute(self, **kwargs) -> dict:
        """Execute with validation and error handling."""
        try:
            # Validate input
            validated_input = self.input_schema(**kwargs)

            # Execute function
            result = self.func(validated_input)

            # Validate output
            validated_output = self.output_schema(**result)

            return {
                "success": True,
                "data": validated_output.model_dump(),
                "metadata": {
                    "tool_name": self.metadata.name,
                    "category": self.metadata.category.value
                }
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__,
                "tool_name": self.metadata.name
            }


# ============== EXAMPLE: Advanced Search Tool ==============

class AdvancedSearchInput(BaseModel):
    """Input for advanced search with all edge cases handled."""

    query: str = Field(
        ...,
        description="Search query. Be specific. Example: 'Python async best practices'",
        min_length=3,
        max_length=500,
        examples=["Python async patterns", "machine learning tutorials"]
    )

    max_results: int = Field(
        10,
        description="Maximum results to return. Recommended: 5-10 for quality, 20+ for comprehensiveness",
        ge=1,
        le=100
    )

    filters: Optional[Dict[str, Any]] = Field(
        None,
        description="Optional filters. Examples: {'date_from': '2024-01-01', 'category': 'tech'}",
        examples=[
            {"date_from": "2024-01-01"},
            {"category": "tech", "language": "en"}
        ]
    )

    search_depth: str = Field(
        "normal",
        description="Search depth: 'quick' (fast, less thorough), 'normal' (balanced), 'deep' (slow, comprehensive)",
        pattern="^(quick|normal|deep)$"
    )


class SearchResult(BaseModel):
    """A single search result."""
    id: str
    title: str
    content: str
    score: float = Field(..., ge=0.0, le=1.0)
    url: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AdvancedSearchOutput(BaseModel):
    """Output with comprehensive metadata."""

    results: List[SearchResult] = Field(
        ...,
        description="Search results ordered by relevance"
    )

    total_found: int = Field(
        ...,
        description="Total matching results (may be > len(results))"
    )

    query_time_ms: float = Field(..., description="Query execution time")

    search_metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional search metadata (filters applied, etc.)"
    )


def advanced_search_function(input: AdvancedSearchInput) -> dict:
    """Implementation of advanced search."""
    # Your implementation here
    return {
        "results": [
            {
                "id": "1",
                "title": "Example Result",
                "content": "...",
                "score": 0.95,
                "url": "https://example.com",
                "metadata": {}
            }
        ],
        "total_found": 1,
        "query_time_ms": 45.2,
        "search_metadata": {"depth": input.search_depth}
    }


# Create universal tool
advanced_search_tool = UniversalTool(
    metadata=UniversalToolMetadata(
        name="advanced_search",
        category=ToolCategory.SEARCH,
        description="Search knowledge base with advanced filtering and ranking",
        when_to_use="Use when user asks questions requiring information lookup. Supports date filters, categories, and search depth control.",
        when_not_to_use="Don't use for simple calculations or data that doesn't require search.",
        example_queries=[
            "Find information about RAG systems",
            "Search for Python tutorials from 2024",
            "What are the latest developments in AI?"
        ],
        estimated_latency_ms=100,
        rate_limit_per_minute=60
    ),
    input_schema=AdvancedSearchInput,
    output_schema=AdvancedSearchOutput,
    func=advanced_search_function
)

# Use with any framework:
openai_schema = advanced_search_tool.to_openai_schema()
anthropic_schema = advanced_search_tool.to_anthropic_schema()
langchain_tool = advanced_search_tool.to_langchain_tool()
```

---

## ADVANCED PATTERN 2: Eliminating LLM Confusion

### Problem: Similar Tool Names

```python
# BAD: LLM confuses these
def search_web(query: str): pass
def search_docs(query: str): pass
def search_db(query: str): pass
```

### Solution: Descriptive Names + Clear Boundaries

```python
class WebSearchInput(BaseModel):
    query: str = Field(..., description="Query to search the public internet")

def search_public_internet(input: WebSearchInput) -> dict:
    """
    Search the public internet (Google, Bing, etc.) for current information.

    **Use this when:**
    - User asks about current events, news, or trending topics
    - Information is likely on public websites
    - Need the most recent information available

    **Don't use this when:**
    - User asks about internal documents → use search_internal_documents instead
    - User asks about database records → use query_database instead
    - Information is in your knowledge base → use search_knowledge_base instead
    """
    pass


class InternalDocsInput(BaseModel):
    query: str = Field(..., description="Query to search company internal documents")

def search_internal_documents(input: InternalDocsInput) -> dict:
    """
    Search internal company documentation and knowledge base.

    **Use this when:**
    - User asks about company policies, procedures, or internal docs
    - Need information specific to this organization
    - Looking for private/confidential information

    **Don't use this when:**
    - Need public information → use search_public_internet instead
    - Need structured data → use query_database instead
    """
    pass
```

**Key differences:**
- ✓ Distinct names: "public_internet" vs "internal_documents"
- ✓ Clear use cases in docstring
- ✓ Explicit "Don't use when" guidance
- ✓ Cross-references to other tools

---

### Problem: Complex Nested Parameters

```python
# BAD: LLM struggles with this
class ConfusingInput(BaseModel):
    filters: Dict[str, Union[str, List[str], Dict[str, Any]]]
    # What can filters contain? LLM has to guess!
```

### Solution: Explicit Sub-Models

```python
class DateFilter(BaseModel):
    """Filter by date range."""
    from_date: str = Field(..., description="Start date (YYYY-MM-DD)", pattern=r"^\d{4}-\d{2}-\d{2}$")
    to_date: str = Field(..., description="End date (YYYY-MM-DD)", pattern=r"^\d{4}-\d{2}-\d{2}$")


class CategoryFilter(BaseModel):
    """Filter by categories."""
    categories: List[str] = Field(
        ...,
        description="List of categories to include",
        examples=[["tech", "science"], ["business"]]
    )
    match_all: bool = Field(
        False,
        description="If True, result must match ALL categories. If False, match ANY category."
    )


class SearchFilters(BaseModel):
    """All available search filters."""
    date_range: Optional[DateFilter] = Field(None, description="Filter by date range")
    categories: Optional[CategoryFilter] = Field(None, description="Filter by categories")
    min_score: Optional[float] = Field(None, description="Minimum relevance score (0.0-1.0)", ge=0.0, le=1.0)


class ClearSearchInput(BaseModel):
    query: str = Field(..., description="Search query")
    filters: SearchFilters = Field(
        default_factory=SearchFilters,
        description="Optional filters to narrow results"
    )
```

**Benefits:**
- ✓ LLM sees exactly what each filter can contain
- ✓ Examples show how to structure data
- ✓ Validation prevents invalid combinations
- ✓ Self-documenting structure

---

## ADVANCED PATTERN 3: Multi-Step Tool Design

### Strategy 1: Atomic Tools (Recommended)

Break complex operations into simple, composable tools:

```python
# Tool 1: Search
class SearchInput(BaseModel):
    query: str
    max_results: int = 10

def search_twitter_users(input: SearchInput) -> List[dict]:
    """Find Twitter users matching query."""
    pass


# Tool 2: Filter
class FilterUsersInput(BaseModel):
    users: List[dict]
    min_followers: int

def filter_by_followers(input: FilterUsersInput) -> List[dict]:
    """Filter users by minimum follower count."""
    pass


# Tool 3: Get Posts
class GetPostsInput(BaseModel):
    user_ids: List[str]
    max_posts_per_user: int = 10

def get_recent_posts(input: GetPostsInput) -> Dict[str, List[dict]]:
    """Get recent posts for specified users."""
    pass


# Tool 4: Summarize
class SummarizePostsInput(BaseModel):
    posts: List[dict]
    max_length: int = 200

def summarize_posts(input: SummarizePostsInput) -> str:
    """Summarize a collection of posts."""
    pass
```

**LLM workflow:**
```
1. users = search_twitter_users("Python experts")
2. top_users = filter_by_followers(users, min_followers=10000)
3. posts = get_recent_posts(top_users[:3])
4. summary = summarize_posts(posts)
```

**Pros:**
- ✓ Each tool is simple and testable
- ✓ Reusable in different combinations
- ✓ Easy for LLM to reason about
- ✓ Failure is isolated (one tool fails, others work)

**Cons:**
- ✗ More API calls
- ✗ More tokens used
- ✗ Slower overall

---

### Strategy 2: Workflow Tool (For Performance)

Combine steps into one tool with a workflow parameter:

```python
class TwitterWorkflowInput(BaseModel):
    """Input for multi-step Twitter workflow."""

    query: str = Field(..., description="Search query for users")

    # Step 1: Search
    max_search_results: int = Field(50, description="Max users to find initially")

    # Step 2: Filter
    min_followers: int = Field(10000, description="Minimum follower count")
    max_filtered_users: int = Field(3, description="How many top users to keep")

    # Step 3: Get posts
    max_posts_per_user: int = Field(10, description="Posts to fetch per user")

    # Step 4: Summarize
    summary_max_length: int = Field(200, description="Max summary length in words")

    # Control
    include_intermediate_results: bool = Field(
        False,
        description="Return all intermediate steps (for debugging)"
    )


class TwitterWorkflowOutput(BaseModel):
    """Output from Twitter workflow."""

    # Final result
    summary: str = Field(..., description="Final summary of posts")

    # Metadata
    users_found: int
    users_analyzed: int
    total_posts: int

    # Optional intermediate results
    intermediate_results: Optional[Dict[str, Any]] = None


def twitter_expert_workflow(input: TwitterWorkflowInput) -> dict:
    """
    Complete workflow: Search → Filter → Get Posts → Summarize.

    **Use this when:**
    User wants to find experts and summarize their content in one step.

    **Workflow:**
    1. Search for users matching query
    2. Filter by follower count
    3. Get recent posts from top N users
    4. Summarize all posts

    **Example:**
    Input: "Find top Python experts and summarize their recent tweets"
    Output: Aggregated summary of posts from top 3 Python experts
    """
    intermediate = {}

    # Step 1: Search
    users = search_twitter_users_internal(input.query, input.max_search_results)
    intermediate['users_found'] = len(users)

    # Step 2: Filter
    filtered = filter_users_internal(users, input.min_followers)
    top_users = filtered[:input.max_filtered_users]
    intermediate['filtered_users'] = [u['id'] for u in top_users]

    # Step 3: Get posts
    posts = get_posts_internal([u['id'] for u in top_users], input.max_posts_per_user)
    intermediate['posts'] = posts

    # Step 4: Summarize
    summary = summarize_internal(posts, input.summary_max_length)

    return {
        "summary": summary,
        "users_found": len(users),
        "users_analyzed": len(top_users),
        "total_posts": sum(len(p) for p in posts.values()),
        "intermediate_results": intermediate if input.include_intermediate_results else None
    }
```

**Pros:**
- ✓ One API call
- ✓ Fewer tokens
- ✓ Faster
- ✓ Atomic transaction (all-or-nothing)

**Cons:**
- ✗ Less flexible
- ✗ Harder to debug
- ✗ Can't reuse individual steps
- ✗ More complex schema

---

### When to Use Which?

| Factor | Atomic Tools | Workflow Tool |
|--------|-------------|---------------|
| **Flexibility** | High | Low |
| **Performance** | Slower | Faster |
| **Reusability** | High | Low |
| **Token cost** | Higher | Lower |
| **Debuggability** | Easy | Harder |
| **LLM reasoning** | Simple | Complex |

**Rule of thumb:**
- **Atomic tools:** Default choice, especially early in development
- **Workflow tool:** When performance matters and the workflow is stable

---

## ADVANCED PATTERN 4: Schema Optimization

### Problem: Large Schema = High Token Cost

With 50 tools, sending all schemas to the LLM every request is expensive.

### Solution 1: Tool Selection Pre-Filter

```python
from typing import List, Set
from pydantic import BaseModel, Field

class ToolSelector:
    """Select relevant tools before sending to LLM."""

    def __init__(self, all_tools: List[UniversalTool]):
        self.all_tools = all_tools
        self.tool_by_category = self._index_by_category()
        self.tool_keywords = self._build_keyword_index()

    def _index_by_category(self) -> Dict[ToolCategory, List[UniversalTool]]:
        """Index tools by category."""
        index = {}
        for tool in self.all_tools:
            category = tool.metadata.category
            if category not in index:
                index[category] = []
            index[category].append(tool)
        return index

    def _build_keyword_index(self) -> Dict[str, Set[str]]:
        """Build keyword index for each tool."""
        index = {}
        for tool in self.all_tools:
            keywords = set()
            # Extract keywords from description
            keywords.update(tool.metadata.description.lower().split())
            keywords.update(tool.metadata.when_to_use.lower().split())
            # Add example query keywords
            for example in tool.metadata.example_queries:
                keywords.update(example.lower().split())
            index[tool.metadata.name] = keywords
        return index

    def select_relevant_tools(
        self,
        user_query: str,
        max_tools: int = 10,
        categories: Optional[List[ToolCategory]] = None
    ) -> List[UniversalTool]:
        """
        Select most relevant tools for a user query.

        Args:
            user_query: The user's request
            max_tools: Maximum tools to return
            categories: Optional category filter

        Returns:
            List of relevant tools (sorted by relevance)
        """
        query_words = set(user_query.lower().split())

        # Filter by category if specified
        candidate_tools = []
        if categories:
            for cat in categories:
                candidate_tools.extend(self.tool_by_category.get(cat, []))
        else:
            candidate_tools = self.all_tools

        # Score each tool by keyword overlap
        scored_tools = []
        for tool in candidate_tools:
            tool_keywords = self.tool_keywords[tool.metadata.name]
            overlap = len(query_words & tool_keywords)

            # Boost if query matches example
            example_match = any(
                query_words & set(ex.lower().split())
                for ex in tool.metadata.example_queries
            )
            if example_match:
                overlap += 10

            scored_tools.append((overlap, tool))

        # Sort by score and return top N
        scored_tools.sort(reverse=True, key=lambda x: x[0])
        return [tool for score, tool in scored_tools[:max_tools]]


# Usage
selector = ToolSelector(all_tools)

# User query arrives
user_query = "Find recent Python tutorials"

# Select only relevant tools (reduces from 50 to 5-10)
relevant_tools = selector.select_relevant_tools(user_query, max_tools=10)

# Send only these schemas to LLM
schemas = [tool.to_openai_schema() for tool in relevant_tools]
```

**Benefits:**
- ✓ Reduces token cost by 80-90%
- ✓ Faster LLM responses (fewer tools to consider)
- ✓ Better tool selection (less confusion)

---

### Solution 2: Lazy Schema Generation

```python
from functools import lru_cache

class OptimizedTool(UniversalTool):
    """Tool with cached schema generation."""

    @lru_cache(maxsize=1)
    def to_openai_schema(self) -> dict:
        """Generate OpenAI schema (cached)."""
        return super().to_openai_schema()

    @lru_cache(maxsize=1)
    def to_anthropic_schema(self) -> dict:
        """Generate Anthropic schema (cached)."""
        return super().to_anthropic_schema()

    def get_minimal_schema(self) -> dict:
        """
        Get minimal schema for initial tool selection.

        Returns only name, category, and description (not full parameters).
        """
        return {
            "name": self.metadata.name,
            "category": self.metadata.category.value,
            "description": self.metadata.description
        }


# Two-phase approach:

# Phase 1: Send minimal schemas for all tools
minimal_schemas = [tool.get_minimal_schema() for tool in all_tools]
llm_response_1 = llm.chat(messages, tools=minimal_schemas)

# Phase 2: LLM picks a tool, now send full schema for just that tool
selected_tool_name = llm_response_1["tool_call"]["name"]
selected_tool = next(t for t in all_tools if t.metadata.name == selected_tool_name)
full_schema = selected_tool.to_openai_schema()
llm_response_2 = llm.chat(messages, tools=[full_schema])
```

---

## ADVANCED PATTERN 5: Handling Edge Cases

### Edge Case 1: Tool Returns Empty Results

```python
class SmartSearchOutput(BaseModel):
    """Search output that handles empty results gracefully."""

    results: List[SearchResult] = Field(default_factory=list)
    total_found: int = Field(0)

    # Crucial: Tell LLM what to do if empty
    is_empty: bool = Field(..., description="True if no results found")
    empty_reason: Optional[str] = Field(
        None,
        description="Why no results were found (if applicable)"
    )
    suggested_alternatives: List[str] = Field(
        default_factory=list,
        description="Alternative queries to try if no results"
    )


def smart_search(input: SearchInput) -> dict:
    """
    Search with smart empty result handling.
    """
    results = perform_search(input.query)

    if not results:
        # Provide helpful feedback
        return {
            "results": [],
            "total_found": 0,
            "is_empty": True,
            "empty_reason": "No documents match your query",
            "suggested_alternatives": [
                f"Try broader terms than '{input.query}'",
                "Check spelling",
                "Remove filters if applied"
            ]
        }

    return {
        "results": results,
        "total_found": len(results),
        "is_empty": False,
        "empty_reason": None,
        "suggested_alternatives": []
    }
```

**Why this matters:**
LLMs need guidance on what to do with empty results. Without `suggested_alternatives`, the LLM might just say "I found nothing" instead of trying a different approach.

---

### Edge Case 2: Rate Limiting

```python
class RateLimitedToolOutput(BaseModel):
    """Output that handles rate limiting."""

    success: bool
    data: Optional[Any] = None

    # Rate limit info
    rate_limited: bool = Field(False, description="Whether request was rate limited")
    retry_after_seconds: Optional[int] = Field(None, description="Seconds until can retry")
    remaining_quota: Optional[int] = Field(None, description="Remaining API quota")


def rate_limited_api_call(input: APIInput) -> dict:
    """
    API call with rate limit handling.
    """
    try:
        result = external_api.call(input.endpoint)

        return {
            "success": True,
            "data": result,
            "rate_limited": False,
            "retry_after_seconds": None,
            "remaining_quota": external_api.get_remaining_quota()
        }

    except RateLimitError as e:
        return {
            "success": False,
            "data": None,
            "rate_limited": True,
            "retry_after_seconds": e.retry_after,
            "remaining_quota": 0
        }
```

**LLM can now:**
- Recognize it hit a rate limit
- Wait the appropriate time
- Try an alternative tool
- Inform the user

---

### Edge Case 3: Partial Failures

```python
class BatchResult(BaseModel):
    """Result for one item in a batch."""
    item_id: str
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None


class BatchOutput(BaseModel):
    """Output from batch processing."""

    total_items: int
    successful: int
    failed: int

    results: List[BatchResult]

    # Help LLM decide what to do
    partial_success: bool = Field(
        ...,
        description="True if some succeeded and some failed"
    )
    should_retry_failed: bool = Field(
        ...,
        description="Whether failed items should be retried"
    )


def process_batch(input: BatchInput) -> dict:
    """
    Process multiple items, handling partial failures.
    """
    results = []

    for item in input.items:
        try:
            data = process_item(item)
            results.append(BatchResult(
                item_id=item.id,
                success=True,
                data=data,
                error=None
            ))
        except Exception as e:
            results.append(BatchResult(
                item_id=item.id,
                success=False,
                data=None,
                error=str(e)
            ))

    successful = sum(1 for r in results if r.success)
    failed = len(results) - successful

    return {
        "total_items": len(results),
        "successful": successful,
        "failed": failed,
        "results": results,
        "partial_success": 0 < successful < len(results),
        "should_retry_failed": failed < len(results) / 2  # Retry if < 50% failed
    }
```

---

## PERFORMANCE BENCHMARKS

### Schema Size vs Tool Count

```
Tools | Avg Schema Size | Total Tokens | Cost per Request (GPT-4)
------|----------------|--------------|-------------------------
5     | 150 tokens     | 750 tokens   | $0.01
10    | 150 tokens     | 1,500 tokens | $0.02
25    | 150 tokens     | 3,750 tokens | $0.05
50    | 150 tokens     | 7,500 tokens | $0.11
100   | 150 tokens     | 15,000 tokens| $0.23
```

**With tool selection (max 10 tools sent):**
```
Total Tools | Tools Sent | Total Tokens | Cost Savings
------------|-----------|--------------|-------------
50          | 10        | 1,500        | 80%
100         | 10        | 1,500        | 90%
500         | 10        | 1,500        | 97%
```

---

## DEBUGGING ADVANCED SCHEMAS

### Debug Tool: Schema Validator

```python
class SchemaDebugger:
    """Validate and debug tool schemas."""

    @staticmethod
    def validate_tool(tool: UniversalTool) -> List[str]:
        """
        Validate a tool and return list of issues.

        Returns:
            List of warning/error messages
        """
        issues = []

        # Check description length
        if len(tool.metadata.description) < 20:
            issues.append(f"⚠️  Description too short: {tool.metadata.description}")

        if len(tool.metadata.description) > 200:
            issues.append(f"⚠️  Description too long (>200 chars)")

        # Check for "when_to_use"
        if not tool.metadata.when_to_use:
            issues.append("❌ Missing 'when_to_use' guidance")

        # Check for examples
        if not tool.metadata.example_queries:
            issues.append("⚠️  No example queries provided")

        # Check input schema
        schema = tool.input_schema.model_json_schema()
        if 'properties' not in schema:
            issues.append("❌ Input schema has no properties")
        else:
            for field_name, field_info in schema['properties'].items():
                if 'description' not in field_info:
                    issues.append(f"⚠️  Field '{field_name}' missing description")

        # Check for ambiguous names
        ambiguous_words = ['process', 'handle', 'do', 'run', 'execute']
        tool_words = tool.metadata.name.split('_')
        if any(word in tool_words for word in ambiguous_words):
            issues.append(f"⚠️  Tool name '{tool.metadata.name}' may be too vague")

        return issues

    @staticmethod
    def find_similar_tools(tools: List[UniversalTool]) -> List[tuple]:
        """
        Find tools that might confuse the LLM.

        Returns:
            List of (tool1, tool2, similarity_score) tuples
        """
        from difflib import SequenceMatcher

        similar_pairs = []

        for i, tool1 in enumerate(tools):
            for tool2 in tools[i+1:]:
                # Compare names
                name_similarity = SequenceMatcher(
                    None,
                    tool1.metadata.name,
                    tool2.metadata.name
                ).ratio()

                # Compare descriptions
                desc_similarity = SequenceMatcher(
                    None,
                    tool1.metadata.description,
                    tool2.metadata.description
                ).ratio()

                if name_similarity > 0.7 or desc_similarity > 0.7:
                    similar_pairs.append((
                        tool1.metadata.name,
                        tool2.metadata.name,
                        max(name_similarity, desc_similarity)
                    ))

        return sorted(similar_pairs, key=lambda x: x[2], reverse=True)


# Usage
debugger = SchemaDebugger()

for tool in all_tools:
    issues = debugger.validate_tool(tool)
    if issues:
        print(f"\n🔧 {tool.metadata.name}:")
        for issue in issues:
            print(f"  {issue}")

# Find confusing tool pairs
similar = debugger.find_similar_tools(all_tools)
if similar:
    print("\n⚠️  Similar tools that might confuse LLM:")
    for tool1, tool2, score in similar:
        print(f"  {tool1} ↔ {tool2} ({score:.0%} similar)")
```

---

## REAL-WORLD EXAMPLE: Production RAG System

See [template_production_rag_tools.py](template_production_rag_tools.py) for a complete example with:
- Multi-source search
- Re-ranking
- Citation extraction
- Confidence scoring
- Fallback chains
- Error handling
- Performance optimization

---

## KEY TAKEAWAYS

1. **Design for adaptability** - Use UniversalTool pattern to work with any framework
2. **Eliminate ambiguity** - Clear names, explicit schemas, "when to use" guidance
3. **Choose tool granularity wisely** - Atomic tools (flexible) vs workflow tools (fast)
4. **Optimize for scale** - Tool selection, schema caching, lazy loading
5. **Handle edge cases** - Empty results, rate limits, partial failures
6. **Debug systematically** - Validate schemas, find conflicts, test with LLM

---

## NEXT STEPS

**You now know:**
✓ How to design framework-agnostic tools
✓ How to eliminate LLM confusion
✓ When to use atomic vs workflow tools
✓ How to optimize for performance at scale
✓ How to handle real-world edge cases
✓ How to debug and validate schemas

**Practice:**
1. Browse [template_production_rag_tools.py](template_production_rag_tools.py)
2. Build a universal tool for your use case
3. Run SchemaDebugger on your tools
4. Implement tool selection for 10+ tools

**Advanced reading:**
- OpenAI function calling best practices
- Anthropic tool use guide
- LangChain tool design patterns
- Production agent debugging strategies

---

**Remember:** L04 is about production-ready tools. The patterns here prevent the failures that happen at scale (100+ tools, 1000+ requests/day, multiple LLM providers).

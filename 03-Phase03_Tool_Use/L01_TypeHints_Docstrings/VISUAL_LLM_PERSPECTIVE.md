# VISUAL: How LLMs See Your Python Functions
> **The LLM's X-Ray Vision Into Your Code**

---

## THE TRANSFORMATION PIPELINE

When you give an agent a Python function, it goes through this pipeline:

```
YOUR PYTHON CODE
       |
       | (extraction)
       ↓
FUNCTION SIGNATURE + DOCSTRING
       |
       | (parsing)
       ↓
JSON SCHEMA
       |
       | (LLM reads this)
       ↓
TOOL SELECTION DECISION
```

---

## EXAMPLE 1: SIMPLE SEARCH TOOL

### What You Write:
```python
def search_kb(query: str, limit: int = 5) -> List[dict]:
    """
    Search knowledge base for documents.

    Args:
        query: Search query text
        limit: Max results to return

    Returns:
        List of matching documents
    """
    results = vector_db.similarity_search(query, k=limit)
    return [{"title": r.title, "content": r.content} for r in results]
```

### What the LLM Sees (JSON Schema):
```json
{
  "name": "search_kb",
  "description": "Search knowledge base for documents.",
  "parameters": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "Search query text"
      },
      "limit": {
        "type": "integer",
        "description": "Max results to return",
        "default": 5
      }
    },
    "required": ["query"]
  },
  "returns": {
    "type": "array",
    "items": {"type": "object"},
    "description": "List of matching documents"
  }
}
```

### The LLM's Decision Process:
```
User says: "Find information about RAG systems"
              |
              ↓
LLM thinks: "I need to search for something"
              |
              ↓
LLM scans available tools:
  ✓ search_kb — "Search knowledge base for documents"
              ↓
LLM decides: "This matches! I'll call search_kb"
              |
              ↓
LLM generates:
  {
    "tool": "search_kb",
    "arguments": {
      "query": "RAG systems",
      "limit": 5
    }
  }
```

---

## EXAMPLE 2: THE DIFFERENCE TYPE HINTS MAKE

### Version A: No Type Hints (LLM Guesses Wrong)

```python
def filter_results(data, threshold):
    """Filter results by score."""
    return [r for r in data if r["score"] > threshold]
```

**LLM Schema (Guessed):**
```json
{
  "name": "filter_results",
  "description": "Filter results by score.",
  "parameters": {
    "type": "object",
    "properties": {
      "data": {"type": "unknown"},      // ❌ LLM doesn't know
      "threshold": {"type": "unknown"}  // ❌ LLM doesn't know
    }
  }
}
```

**LLM Might Call It As:**
```json
{
  "tool": "filter_results",
  "arguments": {
    "data": "results",           // ❌ Passing string instead of list!
    "threshold": "0.7"          // ❌ Passing string instead of float!
  }
}
```
**Result:** Runtime error, agent breaks.

---

### Version B: With Type Hints (LLM Gets It Right)

```python
def filter_results(
    data: List[Dict[str, Any]],
    threshold: float
) -> List[Dict[str, Any]]:
    """Filter results by score threshold."""
    return [r for r in data if r["score"] > threshold]
```

**LLM Schema (Precise):**
```json
{
  "name": "filter_results",
  "description": "Filter results by score threshold.",
  "parameters": {
    "type": "object",
    "properties": {
      "data": {
        "type": "array",              // ✓ LLM knows it's a list
        "items": {"type": "object"}   // ✓ Of dictionaries
      },
      "threshold": {
        "type": "number"              // ✓ LLM knows it's numeric
      }
    }
  }
}
```

**LLM Calls It Correctly:**
```json
{
  "tool": "filter_results",
  "arguments": {
    "data": [...],        // ✓ Actual list of dicts
    "threshold": 0.7      // ✓ Actual number
  }
}
```

---

## VISUAL: THE ANATOMY OF AN LLM-READABLE FUNCTION

```python
def calculate_tokens(
    text: str,
    model: str = "gpt-4"
) -> Dict[str, int]:
    """
    Count tokens in text for a specific model.

    Use this when you need to estimate API costs or check token limits.

    Args:
        text: The input text to tokenize
        model: Model name ('gpt-4', 'gpt-3.5-turbo', 'claude-opus-5-5')

    Returns:
        Dictionary with:
        - total_tokens (int): Total token count
        - estimated_cost (float): Estimated cost in USD

    Example:
        result = calculate_tokens("Hello world", model="gpt-4")
        print(result["total_tokens"])  # 2
    """
    # Implementation
    pass
```

### The LLM's Reading Process:

```
┌─────────────────────────────────────────────────────────────────┐
│ STEP 1: Read function name                                      │
│ "calculate_tokens" → This tool calculates tokens                │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 2: Read first line of docstring                            │
│ "Count tokens in text for a specific model."                    │
│ → When to use: When I need to count tokens                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 3: Read second line of docstring                           │
│ "Use this when you need to estimate API costs..."               │
│ → Additional context: For cost estimation and limit checking    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 4: Read Args section                                       │
│ text: str → "The input text to tokenize"                        │
│   ✓ I need to pass the actual text                              │
│   ✓ Type: string                                                │
│                                                                  │
│ model: str = "gpt-4" → "Model name ('gpt-4', ...)"             │
│   ✓ Optional (has default)                                      │
│   ✓ Type: string                                                │
│   ✓ Options listed: gpt-4, gpt-3.5-turbo, claude-opus-5-5        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 5: Read Returns section                                    │
│ "Dictionary with total_tokens (int) and estimated_cost (float)" │
│ → I'll get back a dict with those two keys                      │
│ → I can use result["total_tokens"] afterward                    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 6: Read Example                                            │
│ result = calculate_tokens("Hello world", model="gpt-4")         │
│ → I see how to call it                                          │
│ → I see what the result looks like                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## VISUAL: PARAMETER TYPE MAPPING

### How Type Hints Become JSON Types

```
PYTHON TYPE              →    JSON SCHEMA TYPE
─────────────────────────────────────────────────────────────
str                      →    "type": "string"
int                      →    "type": "integer"
float                    →    "type": "number"
bool                     →    "type": "boolean"

List[str]                →    "type": "array",
                              "items": {"type": "string"}

Dict[str, Any]           →    "type": "object"

Optional[str]            →    "type": "string"  (not required)

Union[int, float]        →    "type": "number"

List[Dict[str, Any]]     →    "type": "array",
                              "items": {"type": "object"}
```

---

## VISUAL: THE DEFAULT VALUE SIGNAL

### With Default (Optional Parameter)
```python
def search(query: str, limit: int = 10):
    pass
```
**LLM sees:**
```json
{
  "parameters": {
    "query": {...},        // required: true
    "limit": {
      "type": "integer",
      "default": 10        // ← LLM knows it's optional
    }
  },
  "required": ["query"]    // ← Only query is required
}
```

### Without Default (Required Parameter)
```python
def search(query: str, limit: int):
    pass
```
**LLM sees:**
```json
{
  "parameters": {
    "query": {...},
    "limit": {...}
  },
  "required": ["query", "limit"]  // ← Both required
}
```

---

## VISUAL: THE DOCSTRING STRUCTURE

```python
def example_tool(param1: str, param2: int = 5) -> dict:
    """
    ┌────────────────────────────────────────────────────────┐
    │ LINE 1: One-sentence summary                           │
    │ → LLM reads this FIRST                                 │
    │ → Decides if tool matches user intent                  │
    └────────────────────────────────────────────────────────┘

    ┌────────────────────────────────────────────────────────┐
    │ OPTIONAL: Extended description                         │
    │ → More context about when/why to use this              │
    │ → "Use this when..." is very helpful                   │
    └────────────────────────────────────────────────────────┘

    Args:
        ┌────────────────────────────────────────────────────┐
        │ param1: Description of what this parameter is      │
        │ → Must match function signature                    │
        │ → Be specific about format/constraints             │
        └────────────────────────────────────────────────────┘
        ┌────────────────────────────────────────────────────┐
        │ param2: Description with (default: 5) noted        │
        │ → Explain what the default means                   │
        │ → List valid options if applicable                 │
        └────────────────────────────────────────────────────┘

    Returns:
        ┌────────────────────────────────────────────────────┐
        │ Description of return value structure              │
        │ → Don't just say "dict"                            │
        │ → List the keys and their types                    │
        │ → Example: "Dict with 'status' (str), 'count' (int)"│
        └────────────────────────────────────────────────────┘

    Example:
        ┌────────────────────────────────────────────────────┐
        │ result = example_tool("test", param2=10)           │
        │ → Shows LLM how to actually call it                │
        │ → Very helpful for complex signatures              │
        └────────────────────────────────────────────────────┘
    """
    pass
```

---

## COMPARISON: POOR VS. EXCELLENT

### Poor (LLM Will Struggle)
```python
def proc(d, t):
    """Process data."""
    return [x for x in d if x > t]
```

**Problems:**
- ❌ Unclear function name
- ❌ No type hints
- ❌ Vague docstring
- ❌ Cryptic parameter names
- ❌ No Args/Returns documentation

**LLM's confusion:**
- "What is d? What is t?"
- "Process what kind of data?"
- "What does it return?"
- "When should I call this?"

---

### Excellent (LLM Will Use Correctly)
```python
def filter_numbers_by_threshold(
    numbers: List[float],
    threshold: float
) -> List[float]:
    """
    Filter a list of numbers, keeping only those above a threshold.

    Use this to remove low values from numeric data.

    Args:
        numbers: List of numeric values to filter
        threshold: Minimum value to keep (numbers > threshold are kept)

    Returns:
        Filtered list containing only numbers greater than threshold

    Example:
        filtered = filter_numbers_by_threshold([1.0, 5.0, 3.0], threshold=2.0)
        # Returns: [5.0, 3.0]
    """
    return [x for x in numbers if x > threshold]
```

**Why this works:**
- ✓ Clear descriptive name
- ✓ Type hints for all parameters
- ✓ Detailed docstring
- ✓ Args section explains each parameter
- ✓ Returns section describes output
- ✓ Example shows usage

**LLM knows:**
- When to call it ("remove low values")
- What to pass (list of numbers, threshold number)
- What it'll get back (filtered list)
- How to use it (example provided)

---

## THE MENTAL MODEL

Think of your function as an API endpoint:

```
┌─────────────────────────────────────────────────────────┐
│                    YOUR FUNCTION                        │
│                                                         │
│  The LLM is a client that only has your API docs       │
│  It cannot see your implementation                     │
│  It makes decisions based ONLY on the docs             │
│                                                         │
│  If your docs are unclear → LLM calls it wrong         │
│  If your docs are detailed → LLM calls it correctly    │
└─────────────────────────────────────────────────────────┘
```

**Therefore:**
- Write type hints like you're defining an API schema
- Write docstrings like you're writing API documentation
- Assume the LLM knows NOTHING about your code logic
- Make everything explicit

---

## KEY TAKEAWAYS

1. **LLMs don't see your code** — only the signature and docstring
2. **Type hints become JSON schema** — be precise
3. **The first docstring line is critical** — it determines tool selection
4. **The Args section is your contract** — document every parameter
5. **Examples help immensely** — show the LLM how to call it

---

**Next:** See [template_search_tools.py](template_search_tools.py) for copy-paste patterns you can use immediately.

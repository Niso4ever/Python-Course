# L01: Type Hints & Docstrings for LLMs
> **How to Write Functions That AI Agents Can Understand**

---

## THE CORE PROBLEM

When you give an AI agent a tool, you're giving it a function to call. But here's the catch:

**The LLM never sees your code implementation. It only sees:**
1. The function name
2. The parameter names and types
3. The docstring description
4. The return type

### Example: What the LLM Sees

**Your Python code:**
```python
def search_knowledge_base(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Search the knowledge base for relevant documents.

    Args:
        query: The search query string
        limit: Maximum number of results to return

    Returns:
        List of documents, each with 'title', 'content', and 'score' fields
    """
    # Implementation hidden from LLM
    results = vector_db.search(query)
    return results[:limit]
```

**What the LLM receives (converted to schema):**
```json
{
  "name": "search_knowledge_base",
  "description": "Search the knowledge base for relevant documents.",
  "parameters": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "The search query string"
      },
      "limit": {
        "type": "integer",
        "description": "Maximum number of results to return",
        "default": 10
      }
    },
    "required": ["query"]
  },
  "returns": {
    "type": "array",
    "description": "List of documents, each with 'title', 'content', and 'score' fields"
  }
}
```

**The LLM uses this schema to decide:**
- When to call this function
- What arguments to pass
- What to expect back

---

## MY SELF-REFLECTION — Why Docstrings Are Critical for AI Tools in 2026

> *Written during L01 study — personal insight on why this matters.*

The **docstring (the triple quotes `"""`)** is not just a comment for humans.
It is the **instruction manual that the LLM reads to understand the tool's intent.**

The orchestration layer (LangChain, CrewAI, Claude tool use, etc.) takes your docstring
and **sends it directly to the LLM** — so the model knows:
- **When** to use this specific tool
- **Why** it exists (what problem it solves)
- **How** to call it correctly

Without a good docstring, the LLM is flying blind. It might call the wrong tool,
pass wrong arguments, or skip the tool entirely because it doesn't understand what it does.

**The docstring IS the contract between your code and the AI agent.**

---

## THE THREE-LAYER DOCUMENTATION SYSTEM

### Layer 1: Type Hints (For Structure)
Type hints tell the LLM what **types** to pass.

```python
# BAD: No type hints
def search(q, n):
    pass

# GOOD: Clear types
def search(query: str, max_results: int) -> List[dict]:
    pass

# EXCELLENT: Precise types
from typing import List, Dict, Any, Optional

def search(
    query: str,
    max_results: int = 10,
    filters: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    pass
```

### Layer 2: Docstrings (For Meaning)
Docstrings tell the LLM **when** to call the function and **what** the parameters mean.

```python
def search(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """
    Search the knowledge base for relevant documents.

    Use this when the user asks questions that require looking up information.

    Args:
        query: The search query string (user's question or keywords)
        max_results: Maximum number of results to return (default: 10)

    Returns:
        List of documents, each with:
        - title (str): Document title
        - content (str): Document content
        - score (float): Relevance score (0.0 to 1.0)

    Example:
        results = search("What is RAG?", max_results=5)
    """
    pass
```

### Layer 3: Parameter Descriptions (For Details)
The `Args:` section is **critical** — this is what the LLM reads first.

```python
def filter_results(
    results: List[Dict[str, Any]],
    min_score: float = 0.7,
    source_type: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Filter search results by score and source type.

    Args:
        results: List of search results from search_knowledge_base()
        min_score: Minimum relevance score (0.0-1.0). Only results >= this score are kept.
        source_type: Optional filter by source ('wikipedia', 'arxiv', 'docs'). None = all sources.

    Returns:
        Filtered list of results matching criteria
    """
    pass
```

---

## VISUAL: HOW LLMS READ YOUR FUNCTION

```
┌─────────────────────────────────────────────────────────────┐
│  def search(query: str, max_results: int = 10) -> List[dict] │
│         │      │              │             │           │     │
│         │      │              │             │           │     │
│      NAME   PARAM1         PARAM2        DEFAULT    RETURN   │
│                 │              │             │          TYPE  │
│                 ▼              ▼             ▼           ▼    │
│         LLM READS:    LLM READS:     LLM SEES:   LLM KNOWS:  │
│         "query is    "max_results   "10 is a    "I'll get    │
│          a string"    is an int"    good         a list      │
│                                      default"     back"       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  """                                                          │
│  Search the knowledge base for relevant documents.           │
│  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^       │
│  LLM READS THIS FIRST: "When should I call this?"            │
│                                                               │
│  Args:                                                        │
│      query: The search query string                          │
│              ^^^^^^^^^^^^^^^^^^^^^^^^^                        │
│              LLM UNDERSTANDS: "Pass user's question here"    │
│                                                               │
│      max_results: Maximum number of results to return        │
│                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^      │
│                    LLM UNDERSTANDS: "How many results?"      │
│  """                                                          │
└─────────────────────────────────────────────────────────────┘
```

---

## THE DOCSTRING FORMATS

### Google Style (Recommended for LLMs)

```python
def calculate_cost(
    model: str,
    input_tokens: int,
    output_tokens: int
) -> float:
    """
    Calculate the cost of an LLM API call.

    Args:
        model: Model name ('gpt-4', 'claude-opus-5-5', etc.)
        input_tokens: Number of input tokens used
        output_tokens: Number of output tokens generated

    Returns:
        Total cost in USD

    Raises:
        ValueError: If model is not recognized
    """
    pass
```

**Why LLMs like this:**
- Clear `Args:` section (easy to parse)
- Each parameter described on one line
- Return type explicitly stated

### NumPy Style (Also Works)

```python
def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """
    Calculate the cost of an LLM API call.

    Parameters
    ----------
    model : str
        Model name ('gpt-4', 'claude-opus-5-5', etc.)
    input_tokens : int
        Number of input tokens used
    output_tokens : int
        Number of output tokens generated

    Returns
    -------
    float
        Total cost in USD
    """
    pass
```

**For agent tools, prefer Google style** — it's more compact and LLMs parse it more reliably.

---

## COMMON TYPE HINTS FOR AGENT TOOLS

### Basic Types
```python
from typing import List, Dict, Any, Optional, Union

# String parameter
query: str

# Integer parameter
limit: int

# Float parameter
threshold: float

# Boolean parameter
strict_mode: bool
```

### Collections
```python
# List of strings
tags: List[str]

# Dictionary with any values
metadata: Dict[str, Any]

# Dictionary with specific types
scores: Dict[str, float]

# List of dictionaries
results: List[Dict[str, Any]]
```

### Optional Parameters
```python
# Parameter can be None
filters: Optional[Dict[str, Any]] = None

# Equivalent to above
filters: Dict[str, Any] | None = None  # Python 3.10+
```

### Union Types
```python
# Parameter can be multiple types
threshold: Union[int, float]  # Can be 5 or 0.75

# With None (same as Optional)
limit: Union[int, None] = None
```

### Complex Return Types
```python
# Returns a list of dicts
-> List[Dict[str, Any]]

# Returns a dict or None
-> Optional[Dict[str, Any]]

# Returns a tuple
-> tuple[str, float]  # (result, confidence_score)

# Returns nothing (void)
-> None
```

---

## THE TEMPLATE LIBRARY

### Template 1: Search Tool
```python
def search_documents(
    query: str,
    max_results: int = 10,
    min_score: float = 0.0,
    source_filter: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Search for relevant documents in the knowledge base.

    Use this when the user asks questions that require looking up information.

    Args:
        query: The search query (user's question or keywords)
        max_results: Maximum number of results to return (default: 10)
        min_score: Minimum relevance score, 0.0-1.0 (default: 0.0)
        source_filter: Optional source type filter ('web', 'docs', 'kb')

    Returns:
        List of documents, each containing:
        - id (str): Unique document ID
        - title (str): Document title
        - content (str): Document text
        - score (float): Relevance score (0.0-1.0)
        - source (str): Source type

    Example:
        docs = search_documents("What is RAG?", max_results=5, min_score=0.7)
    """
    pass
```

### Template 2: Data Processing Tool
```python
def aggregate_results(
    data: List[Dict[str, Any]],
    group_by: str,
    metric: str = "count"
) -> Dict[str, float]:
    """
    Aggregate data by a field and calculate metrics.

    Use this to summarize or group data by a specific field.

    Args:
        data: List of data items (dicts) to aggregate
        group_by: Field name to group by (e.g., 'category', 'source')
        metric: Metric to calculate - 'count', 'sum', 'avg' (default: 'count')

    Returns:
        Dictionary mapping group values to metric results
        Example: {'categoryA': 12.5, 'categoryB': 8.3}

    Raises:
        KeyError: If group_by field doesn't exist in data items
        ValueError: If metric is not recognized
    """
    pass
```

### Template 3: Validation Tool
```python
def validate_input(
    user_input: str,
    max_length: int = 500,
    allowed_chars: Optional[str] = None
) -> tuple[bool, Optional[str]]:
    """
    Validate user input before processing.

    Use this to check if user input is safe and within limits.

    Args:
        user_input: The user's input string to validate
        max_length: Maximum allowed length (default: 500)
        allowed_chars: Optional regex pattern for allowed characters

    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if input passes validation
        - error_message: None if valid, otherwise describes the issue

    Example:
        valid, error = validate_input("Hello!", max_length=100)
        if not valid:
            print(f"Invalid input: {error}")
    """
    pass
```

### Template 4: API Call Tool
```python
from typing import Any, Dict, List, Optional

def call_external_api(
    endpoint: str,
    method: str = "GET",
    params: Optional[Dict[str, Any]] = None,
    timeout: int = 30
) -> Dict[str, Any]:
    """
    Make an HTTP request to an external API.

    Use this to fetch data from external services or APIs.

    Args:
        endpoint: API endpoint URL (e.g., 'https://api.example.com/data')
        method: HTTP method - 'GET', 'POST', 'PUT', 'DELETE' (default: 'GET')
        params: Optional request parameters (query params for GET, body for POST)
        timeout: Request timeout in seconds (default: 30)

    Returns:
        Dictionary containing:
        - status (int): HTTP status code
        - data (Any): Response data
        - error (Optional[str]): Error message if request failed

    Raises:
        requests.RequestException: If network error occurs
        ValueError: If method is not a valid HTTP method
    """
    pass
```

---

## THE MENTAL CHECKLIST

Before exposing a function as an agent tool, ask:

✅ **Does it have type hints?**
- All parameters typed?
- Return type specified?
- Using `Optional` for nullable values?

✅ **Does it have a clear docstring?**
- One-sentence summary at the top?
- `Args:` section with descriptions?
- `Returns:` section describing output?

✅ **Would YOU know when to call it?**
- Is the purpose clear from the description?
- Are parameter meanings obvious?
- Are examples helpful?

✅ **Are the types LLM-friendly?**
- Using standard types (str, int, float, bool)?
- Complex types well-documented?
- Return type matches description?

---

## COMMON MISTAKES

### Mistake 1: Vague Parameter Names
```python
# BAD
def search(q, n):
    pass

# GOOD
def search(query: str, max_results: int):
    pass
```

### Mistake 2: No Type Hints
```python
# BAD
def filter_results(data, threshold):
    pass

# GOOD
def filter_results(
    data: List[Dict[str, Any]],
    threshold: float
) -> List[Dict[str, Any]]:
    pass
```

### Mistake 3: Unclear Docstrings
```python
# BAD
def process(data):
    """Process data."""
    pass

# GOOD
def process_llm_output(output: str) -> Dict[str, Any]:
    """
    Parse and structure LLM output into a dictionary.

    Args:
        output: Raw LLM response string

    Returns:
        Structured data with 'content', 'confidence', and 'metadata' fields
    """
    pass
```

### Mistake 4: Ambiguous Return Types
```python
# BAD: What does it return?
def search(query: str):
    pass

# GOOD: Clear return type
def search(query: str) -> List[Dict[str, Any]]:
    pass

# BETTER: Document the structure
def search(query: str) -> List[Dict[str, Any]]:
    """
    Returns:
        List of results, each with 'title' (str), 'content' (str), 'score' (float)
    """
    pass
```

---

## PRACTICE EXERCISE

**Rewrite this function to be LLM-readable:**

```python
# BEFORE (LLM will fail to use this correctly)
def get_weather(loc, u="c"):
    return weather_api.fetch(loc, u)
```

**Your turn:** Add type hints, parameters, and a docstring.

**Solution:**
```python
from typing import Dict, Any

def get_weather(
    location: str,
    units: str = "celsius"
) -> Dict[str, Any]:
    """
    Fetch current weather information for a location.

    Use this when the user asks about weather, temperature, or forecast.

    Args:
        location: City name or coordinates (e.g., 'London' or '51.5074,-0.1278')
        units: Temperature units - 'celsius' or 'fahrenheit' (default: 'celsius')

    Returns:
        Weather data containing:
        - temperature (float): Current temperature
        - conditions (str): Weather description (e.g., 'sunny', 'rainy')
        - humidity (float): Humidity percentage (0-100)
        - location (str): Resolved location name

    Example:
        weather = get_weather("Paris", units="celsius")
        print(f"It's {weather['temperature']}°C in {weather['location']}")
    """
    return weather_api.fetch(location, units)
```

---

## NEXT STEPS

**You now know:**
✓ How to write type hints that LLMs understand
✓ The Google-style docstring format
✓ What information LLMs need to call your functions
✓ Common patterns for agent tools

**Next lesson:** [L02: Pydantic Fundamentals](../L02_Pydantic_Fundamentals/) — Learn to validate inputs automatically and generate schemas for LLMs.

---

## QUICK REFERENCE

### The Minimal LLM-Readable Function
```python
def tool_name(
    param1: str,
    param2: int = 10
) -> List[Dict[str, Any]]:
    """
    One-sentence description of what this tool does.

    Args:
        param1: What this parameter means
        param2: What this parameter means (default: 10)

    Returns:
        Description of return value structure
    """
    pass
```

**Copy this template every time you create a new agent tool.**

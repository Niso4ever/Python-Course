# Lesson 01 - Pass 1: RECOGNITION
## Learn to SEE Variables and Dictionaries in the Wild

**Goal:** By the end of this pass, you'll instantly recognize variable and dictionary patterns and understand what they store — WITHOUT writing any code.

---

## The Shape Recognition Method

Variables and dictionaries have distinctive VISUAL SHAPES. Learn to recognize them by sight.

> **2026 Note:** You will see TWO labeling styles in real AI code.
> Classic style: `name = "value"` — still valid everywhere
> Type hint style: `name: str = "value"` — same variable, adds a type label before `=`

### Shape 1: The Simple Variable

```python
model_name = "claude-sonnet-5-5"
token_limit = 4096
temperature = 0.7
is_active = True
```

> `temperature` is used in this lesson as an example of a `float`, and you will see it in a lot of existing AI code. Note that the Claude API no longer accepts it: it was removed in API version 2026-10-21 and now returns a 400 error (platform.claude.com model-deprecations page, retrieved 2026-10-28). Don't put it in new Claude calls.

**Visual Pattern:**
```
label = value
label: type = value    ← 2026 style (colon + type before =)
```

**What to recognize:**
- Label on the left
- `=` in the middle
- Value on the right
- Optional `: type` between label and `=`

---

### Shape 2: The Dictionary

```python
config = {
    "key": "value",
    "count": 42,
    "active": True
}
```

**Visual Pattern:**
```
name = {
    "key": value,      ← key always in quotes
    "key": value,      ← comma separates items
}                      ← closing brace
```

---

## Real Examples to RECOGNIZE (Don't Write, Just Read)

### Example 1: LLM Configuration

```python
# Agent setup
model_name: str = "claude-sonnet-5-5"
temperature: float = 0.7
max_tokens: int = 1000
streaming: bool = True
```

**RECOGNIZE THIS:**
- `str` = text type
- `float` = decimal number type
- `int` = whole number type
- `bool` = True/False type
- All four types labeled explicitly

**What it does:** "Store settings for an LLM call."

---

### Example 2: Classic Style (Still Valid)

```python
# Same config, no type hints — works identically:
model_name = "claude-sonnet-5-5"
temperature = 0.7
max_tokens = 1000
streaming = True
```

**RECOGNIZE THIS:**
- Same data, no `: type` annotations
- Both styles produce identical Python — style is a choice

**What it does:** "Exact same settings — just written the older way."

---

### Example 3: Simple Dictionary

```python
# LLM call metadata
llm_call = {
    "model": "claude-sonnet-5-5",
    "tokens_used": 1523,
    "cost_usd": 0.0234,
    "success": True
}
```

**RECOGNIZE THIS:**
- `{` opens the dictionary
- Each line: `"key": value,`
- Keys always in quotes
- Values match their type (text in quotes, number without)
- `}` closes the dictionary

**What it does:** "Label a collection of related data about one LLM call."

---

### Example 4: Accessing Dictionary Values

```python
# The dictionary
result = {
    "answer": "RAG is retrieval-augmented generation.",
    "confidence": 0.94,
    "model": "claude-sonnet-5-5"
}

# Access by key
print(result["answer"])      # "RAG is retrieval-augmented generation."
print(result["confidence"])  # 0.94

# Safe access (won't crash if key missing)
score = result.get("confidence", 0.0)
```

**RECOGNIZE THIS:**
- `dict["key"]` ← direct access (crashes if key missing)
- `dict.get("key", default)` ← safe access (returns default if missing)

**What it does:** "Pull specific values out of the labeled container."

---

### Example 5: Nested Dictionary

```python
# RAG request/response pair
rag_data = {
    "request": {
        "query": "What is RAG?",
        "temperature": 0.7
    },
    "response": {
        "content": "RAG combines retrieval...",
        "tokens": 234
    }
}

# Access nested value
query = rag_data["request"]["query"]
```

**RECOGNIZE THIS:**
- Dictionary inside a dictionary
- Two levels of `{}`
- Access: `outer["key"]["inner_key"]`

**What it does:** "Store a complete request/response pair as structured data."

---

### Example 6: Type Hints in Functions (L05 Preview)

```python
# You will see this often — type hints on function signatures
def call_llm(prompt: str, max_tokens: int = 1000) -> dict:
    result = {
        "content": "...",
        "tokens": 234
    }
    return result
```

**RECOGNIZE THIS:**
- `param: str` ← parameter with type hint
- `= 1000` ← default value
- `-> dict` ← return type hint
- Same `: type` pattern as variables

**What it does:** "Function that takes text, optionally a limit, and returns a dictionary."

---

### Example 7: The 4 Value Types Side by Side

```python
# The 4 types you'll see in every AI config:
agent_config = {
    "name":       "research_agent",   # str   — text (always in quotes)
    "max_calls":  10,                 # int   — whole number (no quotes)
    "threshold":  0.85,              # float — decimal (no quotes)
    "verbose":    True               # bool  — True or False (capital T/F)
}
```

**RECOGNIZE THIS — the type identification rule:**

| Value | Type | Clue |
|:------|:-----|:-----|
| `"text"` | str | Has quotes |
| `42` | int | Whole number, no quotes |
| `0.85` | float | Has decimal point, no quotes |
| `True` / `False` | bool | Capitalized, no quotes |

**What it does:** "Spot any type error in 1 second — wrong quotes = wrong type."

---

### Example 8: Full Agent Config (Real Pattern)

```python
# Real RAG agent configuration
rag_config: dict = {
    "model":               "claude-sonnet-5-5",
    "embedding_model":     "text-embedding-3-small",
    "relevance_threshold": 0.85,
    "max_context_docs":    3,
    "max_tokens":          2000,
    "streaming":           False,
    "metadata": {
        "project":  "enterprise_kb",
        "version":  "2.1",
        "deployed": True
    }
}

# Access patterns:
model      = rag_config["model"]
threshold  = rag_config["relevance_threshold"]
project    = rag_config["metadata"]["project"]   # nested access
```

**RECOGNIZE THIS:**
- Top-level type hint: `rag_config: dict = {`
- Nested dictionary under `"metadata"`
- Mix of all 4 types
- Nested access: `config["metadata"]["project"]`

**What it does:** "Complete configuration for a production RAG agent — one dictionary holds everything."

---

## The Type Recognition Cheat

When reviewing AI code, identify types by sight:

```python
x = "hello"       # str   — quotes present
x = 42            # int   — number, no quotes, no dot
x = 0.7           # float — number, has a dot
x = True          # bool  — capitalized, no quotes
x = {"k": "v"}   # dict  — curly braces
x = ["a", "b"]   # list  — square brackets (L02!)
```

---

## Recognition Exercise: What Type Is It?

```python
api_key = "sk-ant-..."                # → str
retry_count = 3                       # → int
confidence = 0.94                     # → float
use_cache = False                     # → bool
result = {"answer": "...", "ok": True}  # → dict
```

**Answers:** str, int, float, bool, dict

---

## Common AI Patterns (Recognition Cheat Sheet)

### Pattern: LLM Config Dictionary
```python
config = {
    "model": "claude-sonnet-5-5",
    "temperature": 0.7,
    "max_tokens": 1000
}
```
**Recognize:** Setup data for an API call

---

### Pattern: Result Dictionary
```python
result = {
    "content": "...",
    "confidence": 0.94,
    "success": True
}
```
**Recognize:** Structured output from a function or API

---

### Pattern: Type-Hinted Variable
```python
user_query: str = "What is AI?"
token_budget: int = 4096
```
**Recognize:** Same variable — just with documentation labels added

---

## You've Completed Pass 1!

You can now:
✓ **Recognize** variable assignments by sight
✓ **Distinguish** classic style from type-hint style
✓ **Identify** all 4 value types (str, int, float, bool)
✓ **Read** simple and nested dictionaries
✓ **Spot** type errors (number in quotes = wrong type)
✓ **Understand** both access patterns (`dict["key"]` vs `dict.get("key", default)`)

**Next:**
- **Pass C (Visual):** See variables and dicts as shapes and containers
- **Pass 3 (Templates):** Copy and modify real AI config patterns

**Remember:** You're not memorizing. You're training your eyes to SEE patterns.

---

## Pro Tip: The 3-Second Rule

When you see unfamiliar code with variables or dicts:
1. **Second 1:** Is it a simple variable or a dictionary?
2. **Second 2:** What type are the values?
3. **Second 3:** What is it storing? (config? result? metadata?)

That's it. You don't need to understand every detail. Just recognize the pattern.

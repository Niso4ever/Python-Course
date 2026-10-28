# Pass 1: Recognition — Error Reading
## Read These 8 Error Scenarios — Don't Memorize Them

**Goal:** When you see a red traceback, instantly know the error type and the fix direction.

**Your 3-Second Error Read:**
1. **Last line** → error type + message (the actual problem)
2. **Your file + line number** → where YOUR code triggered it
3. **Fix table** → what to do next

---

## Example 1: KeyError — The Most Common AI Error

```
Traceback (most recent call last):
  File "rag_agent.py", line 31, in answer
    context = "\n".join([d["content"] for d in docs])
KeyError: 'content'
```

**Read it:**
- Last line: `KeyError: 'content'` → dictionary doesn't have key `'content'`
- Your code: line 31 in `answer()` — the list comprehension
- The doc dict uses `"text"` not `"content"`

**Fix:**
```python
# Wrong:
context = "\n".join([d["content"] for d in docs])

# Right:
context = "\n".join([d["text"] for d in docs])

# Or: print one doc first to see the real keys
print(docs[0])   # → {'text': '...', 'score': 0.9, 'source': '...'}
```

**What to notice:** Always print the dict before using it. The key name is always the issue.

---

## Example 2: AttributeError — Wrong Object Type

```
Traceback (most recent call last):
  File "agent.py", line 18, in chat
    reply = response.content[0].text
AttributeError: 'str' object has no attribute 'content'
```

**Read it:**
- Last line: `AttributeError: 'str' object has no attribute 'content'`
- `response` is a plain string, not an Anthropic response object
- The function already extracted the text before returning it

**Fix:**
```python
# Problem: call_llm() returned a string, not a raw API response
def call_llm(prompt):
    response = client.messages.create(...)
    return response.content[0].text   # ← already a string

# Wrong usage:
reply = response.content[0].text   # error: can't call .content on str

# Right usage:
reply = call_llm(prompt)   # already a string, use directly
print(reply)

# Debug tip: always check what a function returns
print(type(response))   # → <class 'str'>
```

---

## Example 3: IndexError — Empty List

```
Traceback (most recent call last):
  File "rag_pipeline.py", line 44, in answer
    best_doc = docs[0]
IndexError: list index out of range
```

**Read it:**
- Last line: `IndexError: list index out of range`
- `docs` is an empty list — the search returned no results
- Accessing `[0]` on an empty list always fails

**Fix:**
```python
# Wrong:
best_doc = docs[0]   # crashes if docs is []

# Right: check first
if docs:
    best_doc = docs[0]
else:
    return "No documents found for this query."

# Or one-liner:
best_doc = docs[0] if docs else None
```

**In AI code:** Happens when vector search returns nothing (threshold too high, empty db, bad query).

---

## Example 4: ModuleNotFoundError — Missing pip install

```
Traceback (most recent call last):
  File "chatbot.py", line 1, in <module>
    from langchain_anthropic import ChatAnthropic
ModuleNotFoundError: No module named 'langchain_anthropic'
```

**Read it:**
- Last line: `No module named 'langchain_anthropic'`
- The package is not installed in this Python environment
- Always happens on a new machine or new virtual environment

**Fix:**
```bash
pip install langchain-anthropic
# Note: pip uses hyphens, import uses underscores
# langchain-anthropic → langchain_anthropic
```

**Then run your script again.** The import will work.

---

## Example 5: TypeError — Wrong Data Type

```
Traceback (most recent call last):
  File "cost_tracker.py", line 12, in estimate
    tokens = len(prompt) / 4
TypeError: object of type 'int' has no len()
```

**Read it:**
- Last line: `TypeError: object of type 'int' has no len()`
- `prompt` is an integer, but `len()` only works on strings/lists
- Someone passed a number where text was expected

**Fix:**
```python
# Wrong:
estimate(1000)           # passing token count as int, not a string

# Right:
estimate("What is RAG?") # pass the actual string

# Or convert:
def estimate(prompt):
    prompt = str(prompt)   # defensive conversion
    return len(prompt) / 4
```

---

## Example 6: NameError — Variable Not Defined

```
Traceback (most recent call last):
  File "pipeline.py", line 22, in process
    return format_result(question, anwser)
NameError: name 'anwser' is not defined
```

**Read it:**
- Last line: `NameError: name 'anwser' is not defined`
- Typo! `anwser` instead of `answer`
- Python is case-sensitive and spelling-sensitive

**Fix:**
```python
# Wrong:
return format_result(question, anwser)   # typo

# Right:
return format_result(question, answer)   # correct spelling
```

**Also check:** Was the variable ever assigned? NameError also fires if you use a variable before defining it.

---

## Example 7: ValueError — Right Type, Wrong Value

```
Traceback (most recent call last):
  File "chatbot.py", line 8, in <module>
    client.messages.create(model="claude-4-super", max_tokens=1000, ...)
anthropic.BadRequestError: {'type': 'error', 'error': {'type': 'invalid_request_error',
  'message': "model: model `claude-4-super` does not exist"}}
```

**Read it:**
- Error type: invalid model name
- The string `"claude-4-super"` is not a real Claude model
- The type is correct (string), the value is wrong

**Fix:**
```python
# Wrong:
model = "claude-4-super"   # made up name

# Right (as of 2026):
model = "claude-sonnet-5-5"       # Sonnet
model = "claude-opus-5-5"         # Opus
model = "claude-haiku-5-5"  # Haiku
```

---

## Example 8: A Full Real-World Traceback (Multi-Level)

```
Traceback (most recent call last):
  File "main.py", line 12, in <module>           ← Your entry point
    result = rag.answer("What is RAG?")
  File "rag_agent.py", line 34, in answer        ← Your agent method
    docs = self.db.search(question, top_k=self.top_k)
  File "/site-packages/chromadb/api/client.py", line 203, in query  ← Library code
    return self._collection.query(query_texts=query_texts, ...)
  File "/site-packages/chromadb/api/models/Collection.py", line 87  ← Deep library
    validate_where(where)
ValueError: Expected where value to be a str, int, float, or bool,  ← THE ERROR
  got dict instead
```

**How to read this:**
1. Last line: `ValueError` — wrong type passed somewhere
2. Walk UP to find YOUR code: `rag_agent.py line 34`
3. The `search()` call is passing something wrong
4. `top_k=self.top_k` — check what `self.top_k` actually is

**Fix process:**
```python
# Add a print BEFORE the failing line:
print(f"DEBUG: top_k={self.top_k}, type={type(self.top_k)}")
docs = self.db.search(question, top_k=self.top_k)

# If top_k is a dict instead of int — it was set wrong in __init__
# Fix: make sure self.top_k = 3 (int), not {"k": 3} (dict)
```

---

## Pattern Summary

| Error | One-line diagnosis | One-line fix |
|:------|:-------------------|:-------------|
| `KeyError: 'x'` | Dict has different key name | Print the dict, find real key |
| `IndexError: list index out of range` | List is empty | `if docs:` before accessing |
| `AttributeError: no attribute 'x'` | Wrong object type | `print(type(obj))` to check |
| `ModuleNotFoundError` | pip install missing | `pip install <name>` |
| `TypeError: no len()` | Wrong data type passed | `print(type(var))` before call |
| `NameError: not defined` | Typo or wrong order | Check spelling, check assignment |
| `ValueError: invalid value` | Correct type, bad content | Check model name, check value range |
| `IndentationError` | Missing 4-space indent | Indent the line after `def`/`if`/`for` |
| `JSONDecodeError` | String isn't JSON | `print(text)` before `json.loads()` |
| `FileNotFoundError` | Wrong file path | `print(os.getcwd())` to check location |

---

**Next:** See [PASS_C_VISUAL.md](PASS_C_VISUAL.md) for diagrams showing how to navigate a traceback visually.

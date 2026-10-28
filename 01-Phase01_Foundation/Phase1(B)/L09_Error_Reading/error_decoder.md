# Error Decoder — Quick Scan Reference
## Open this when you get an error. Find your type. Apply the fix.

---

## Step 0: Read the traceback right

```
Traceback (most recent call last):
  File "your_file.py", line XX, in function_name   ← YOUR code
    the_line_that_failed
  File "/site-packages/...", line XX               ← library (skip)
    ...
ErrorType: message here                            ← READ THIS FIRST
```

**Rule:** Last line = error. Your file = where to fix.

---

## The 10 Errors — Quick Table

| Error | One-line cause | One-line fix |
|:------|:--------------|:-------------|
| `KeyError: 'x'` | Key `'x'` not in dict | `print(dict.keys())` → use real key |
| `IndexError: list index out of range` | List is empty or shorter than expected | `if docs:` before `docs[0]` |
| `AttributeError: 'X' has no attribute 'y'` | Wrong object type | `print(type(obj))` → use correct method |
| `ModuleNotFoundError: No module named 'x'` | Package not installed | `pip install x` |
| `TypeError: 'X' object has no len()` | Wrong data type passed | `print(type(var))` → convert if needed |
| `NameError: name 'x' is not defined` | Variable not assigned or typo | Check spelling; check order |
| `ValueError: ...` | Right type, invalid content | Check model name / value range |
| `IndentationError: expected indented block` | Missing 4 spaces after `def`/`if`/`for` | Add 4-space indent |
| `JSONDecodeError: Expecting value` | String is not valid JSON | `print(text)` before `json.loads()` |
| `FileNotFoundError: No such file...` | Wrong path | `print(os.getcwd())` → fix path |

---

## ERROR 1: KeyError

```
KeyError: 'content'
```

**Cause:** You used `dict["content"]` but the key is actually `"text"` or `"page_content"`.

**Diagnosis:**
```python
print(my_dict)           # See all key-value pairs
print(my_dict.keys())    # See just the key names
```

**Fix:**
```python
# Replace wrong key with real key:
doc["content"]       → doc["text"]

# Or use .get() which returns None instead of crashing:
doc.get("content", "default value")
```

**Common in AI:** LangChain docs use `.page_content`, Chroma uses `"text"`, your dicts might use `"content"`.

---

## ERROR 2: IndexError

```
IndexError: list index out of range
```

**Cause:** Accessing `list[0]` on an empty list `[]`.

**Diagnosis:**
```python
print(len(docs))    # → 0 means empty
print(docs)         # → [] confirms empty
```

**Fix:**
```python
if docs:
    result = docs[0]
else:
    result = "No results found"

# One-liner:
result = docs[0] if docs else None
```

**Common in AI:** Vector search returns empty list when no docs match or threshold is too high.

---

## ERROR 3: AttributeError

```
AttributeError: 'str' object has no attribute 'content'
AttributeError: 'NoneType' object has no attribute 'text'
```

**Cause:** Calling `.content`, `.text`, `.page_content` on the wrong type.

**Diagnosis:**
```python
print(type(response))    # Shows what it actually is
print(response)          # Shows the value
```

**Fix:**
```python
# If type is str → use it directly (function already extracted text)
print(response)

# If type is None → function returned nothing
# Add a check: if response is None: return "Error"

# If type is Anthropic message → use correct path:
response.content[0].text
```

---

## ERROR 4: ModuleNotFoundError

```
ModuleNotFoundError: No module named 'langchain_anthropic'
```

**Cause:** Package not installed in current Python environment.

**Fix:**
```bash
pip install langchain-anthropic
# Note: pip uses hyphens (-), import uses underscores (_)
```

**pip → import name mapping:**

| pip install | import |
|:------------|:-------|
| `anthropic` | `anthropic` |
| `langchain-anthropic` | `langchain_anthropic` |
| `langchain-community` | `langchain_community` |
| `langchain-core` | `langchain_core` |
| `python-dotenv` | `dotenv` |
| `dspy` (formerly `dspy-ai`) | `dspy` |
| `crewai` | `crewai` |
| `chromadb` | `chromadb` |

---

## ERROR 5: TypeError

```
TypeError: object of type 'int' has no len()
TypeError: argument should be str, not list
```

**Cause:** Passed the wrong data type to a function.

**Diagnosis:**
```python
print(type(variable))    # See what type it actually is
```

**Fix:**
```python
# Convert to the right type:
str(value)       # → string
int(value)       # → integer
list(value)      # → list
len(str(value))  # len() on the string version
```

---

## ERROR 6: NameError

```
NameError: name 'anwser' is not defined
NameError: name 'result' is not defined
```

**Cause A:** Typo in variable name.
**Cause B:** Using variable before assigning it.

**Fix A:** Check spelling — Python is case-sensitive (`Result` ≠ `result`).
**Fix B:** Move the assignment before the usage.

---

## ERROR 7: ValueError

```
anthropic.BadRequestError: model `claude-99` does not exist
ValueError: temperature must be between 0 and 1
```

**Cause:** Correct data type, but invalid content.

**Fix:**
```python
# Valid Claude models (2026):
"claude-sonnet-5-5"
"claude-opus-5-5"
"claude-haiku-5-5"

# Valid temperature: 0.0 to 1.0
temperature = 0.7   # valid
temperature = 2.0   # invalid → ValueError
```

---

## ERROR 8: IndentationError

```
IndentationError: expected an indented block after 'def' statement
IndentationError: unexpected indent
```

**Cause A:** No indent after `def`, `class`, `if`, `for`, `while`.
**Cause B:** Mixed tabs and spaces (copy-paste issue).

**Fix:**
```python
# WRONG:
def chat(input):
return input        # ← no indent

# RIGHT:
def chat(input):
    return input    # ← 4 spaces
```

**Pro tip:** If copy-pasting from a website/PDF, re-type the indent manually.

---

## ERROR 9: JSONDecodeError

```
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

**Cause:** Called `json.loads()` on a string that isn't JSON.

**Diagnosis:**
```python
print(repr(text))   # Shows exact content including hidden characters
```

**Fix:**
```python
import json

# Safe wrapper:
def safe_json(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        print(f"Not JSON: {e}")
        return {"raw": text}

# Or: tell the LLM to return JSON in your prompt:
# "Respond ONLY with valid JSON. No explanation."
```

---

## ERROR 10: FileNotFoundError

```
FileNotFoundError: [Errno 2] No such file or directory: 'data/docs.pdf'
```

**Cause:** Python is looking for the file in a different directory.

**Diagnosis:**
```python
import os
print(os.getcwd())       # Where Python thinks it is
print(os.listdir('.'))   # Files in current directory
```

**Fix:**
```python
import os

# Check before opening:
if os.path.exists(file_path):
    with open(file_path) as f:
        content = f.read()
else:
    print(f"File not found: {file_path}")

# Use absolute path (never gets confused):
import pathlib
base = pathlib.Path(__file__).parent   # folder of your script
file_path = base / "data" / "docs.pdf"
```

---

## Debug Print Toolkit

```python
# What type is this?
print(type(variable))

# What keys does this dict have?
print(my_dict.keys())
print(my_dict)

# Is this list empty?
print(len(my_list))
print(my_list[:3])   # first 3 items

# Where is Python running from?
import os
print(os.getcwd())

# What does the full response object look like?
import json
print(json.dumps(vars(response), default=str))  # for objects
```

---

## The "Ask Claude" Template

```
Error I got:
[full traceback — all lines from "Traceback" to the error message]

My relevant code:
[the function or class where it failed — 5-20 lines]

What I was trying to do:
[one sentence]
```

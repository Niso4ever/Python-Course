# Lesson 09: Error Reading
## The Fire Alarm Theory

Architect, errors are not failures — they are **fire alarms**. The alarm doesn't tell you the building is broken. It tells you exactly which floor has smoke. Python errors work the same way: they pinpoint the exact location and type of problem.

Most beginners panic at red text. Your job is different: **scan, locate, fix** — 3 steps, 30 seconds.

---

## 1. Anatomy of a Python Error

Every Python error has the same structure:

```
Traceback (most recent call last):          ← "Here's the chain of calls"
  File "agent.py", line 12, in chat         ← Where it started (outer call)
    response = call_llm(self.history)       ← The line that called something
  File "agent.py", line 27, in call_llm    ← Where it broke (inner call)
    return client.messages.create(...)     ← The broken line
KeyError: 'content'                         ← THE ACTUAL ERROR (READ THIS FIRST)
```

**Rule #1:** Read the **last line** first. That's the error.
**Rule #2:** Read **upward** to find which line in YOUR code caused it.
**Rule #3:** The filename + line number tells you exactly where to look.

---

## 2. The 3-Step Fix Process

```
Step 1: READ
  → What is the error TYPE? (KeyError, ImportError, AttributeError, etc.)
  → What is the error MESSAGE? (What key? What attribute?)

Step 2: LOCATE
  → Which FILE and LINE caused it?
  → What line in YOUR code is the culprit?

Step 3: FIX
  → Look up the error type in the cheatsheet
  → Apply the standard fix
```

---

## 3. The 10 Errors You'll See Most

### KeyError — "That label doesn't exist"
```python
# Error:
doc = {"text": "hello", "score": 0.9}
print(doc["content"])  # KeyError: 'content'

# Fix: Check the key name
print(doc["text"])     # correct key
# Or: use .get() which returns None instead of erroring
print(doc.get("content", "not found"))
```
**In AI code:** Almost always a dict with `"text"` vs `"content"` vs `"page_content"`.

---

### IndexError — "That position doesn't exist"
```python
# Error:
docs = []
print(docs[0])    # IndexError: list index out of range

# Fix: Check the list first
if docs:
    print(docs[0])
# Or:
print(docs[0] if docs else "empty list")
```
**In AI code:** RAG results list is empty — no documents matched the query.

---

### AttributeError — "That method/attribute doesn't exist"
```python
# Error:
response = call_llm("hello")
print(response.text)    # AttributeError: 'str' object has no attribute 'text'

# Fix: Check what the function actually returns
print(response)         # It's already a string, not an object
print(response.content[0].text)  # Anthropic response needs this path
```
**In AI code:** Calling `.content` or `.text` on the wrong object type.

---

### ImportError / ModuleNotFoundError — "Package not installed"
```python
# Error:
from langchain_anthropic import ChatAnthropic
# ModuleNotFoundError: No module named 'langchain_anthropic'

# Fix: Install the package
# pip install langchain-anthropic
```
**In AI code:** Every new framework triggers this. See Lesson 08 for the pip name map.

---

### TypeError — "Wrong type of input"
```python
# Error:
def count_tokens(text):
    return len(text) / 4

count_tokens(1234)   # TypeError: object of type 'int' has no len()

# Fix: Convert to string first
count_tokens(str(1234))   # "1234" → works
```
**In AI code:** Passing an int/dict where a string is expected, or vice versa.

---

### NameError — "That variable doesn't exist yet"
```python
# Error:
print(result)    # NameError: name 'result' is not defined

# Fix: Define it first (or check for typo)
result = call_llm("hello")
print(result)
```
**In AI code:** Called a function or variable before assigning it, or typo in the name.

---

### ValueError — "Right type, wrong value"
```python
# Error:
int("hello")   # ValueError: invalid literal for int() with base 10: 'hello'

# Error in AI:
model = "gpt-99"
client.messages.create(model=model, ...)
# ValueError: model 'gpt-99' does not exist
```
**In AI code:** Invalid model name, bad temperature value (>1.0), bad token count.

---

### FileNotFoundError — "That file doesn't exist"
```python
# Error:
with open("docs/report.pdf") as f:
    ...
# FileNotFoundError: [Errno 2] No such file or directory: 'docs/report.pdf'

# Fix: Check path
import os
print(os.getcwd())      # Where Python is looking from
print(os.listdir("."))  # What files exist here
```
**In AI code:** Wrong path to vector database, PDF file, or config file.

---

### IndentationError — "Code not lined up correctly"
```python
# Error:
def chat(self, input):
return input    # IndentationError: expected an indented block

# Fix: Add 4 spaces
def chat(self, input):
    return input
```
**In AI code:** Copy-pasting code that lost its indentation. Always check L3/L4 method bodies.

---

### JSONDecodeError — "That's not valid JSON"
```python
# Error:
import json
json.loads("not json")   # json.decoder.JSONDecodeError: Expecting value

# Fix: Check the string is valid JSON first
text = '{"answer": "yes"}'   # must have quotes, colons, no trailing comma
data = json.loads(text)      # works
```
**In AI code:** LLM returned plain text but you called `json.loads()` on it.

---

## 4. Reading a Real Traceback

```
Traceback (most recent call last):
  File "rag_chatbot.py", line 45, in answer    ← Your code, line 45
    docs = self.db.search(question, top_k=self.top_k)
  File "/site-packages/chroma/client.py", line 203, in search  ← Library code
    return self._collection.query(...)
  File "/site-packages/chroma/collection.py", line 87, in query
    validate_embeddings(query_embeddings)
ValueError: Expected embeddings to be float, got str               ← THE ERROR

How to read this:
1. Last line → ValueError: wrong value type for embeddings
2. Your code → line 45: db.search(question, ...)
3. Root cause → `question` is a string but the db expected a float embedding
4. Fix → pass the question as text; the db's embedding function should convert it
```

---

## 5. What to Say to Claude When Sharing an Error

**Bad (too vague):**
> "My code doesn't work"

**Good (gives Claude everything needed):**
```
I got this error:

KeyError: 'content'
  File "agent.py", line 23, in chat
    return response["content"]

Here's the relevant code:
    response = call_llm(self.history)
    return response["content"]

What's wrong and how do I fix it?
```

**Template for asking Claude:**
```
Error message: [paste full traceback]
Code that caused it: [paste the relevant function]
What I was trying to do: [one sentence]
```

---

## 6. Error Quick-Fix Table

| Error | Means | First thing to check |
|:------|:------|:---------------------|
| `KeyError: 'x'` | Dict doesn't have key `'x'` | Print the dict, find the real key name |
| `IndexError: list index out of range` | List is empty or too short | Check `if docs:` before accessing |
| `AttributeError: has no attribute 'x'` | Wrong object type | Print `type(obj)` to see what it really is |
| `ModuleNotFoundError` | Package not installed | `pip install <name>` (see L6 table) |
| `TypeError: unexpected type` | Wrong data type passed | Print `type(variable)` before the call |
| `NameError: not defined` | Variable never assigned | Check for typo, check order of code |
| `ValueError: invalid value` | Right type, bad value | Check model name, temperature, token limits |
| `FileNotFoundError` | File path is wrong | Print `os.getcwd()`, check actual path |
| `IndentationError` | Code not indented | Add 4 spaces to the line below `def`/`if`/`for` |
| `JSONDecodeError` | String is not JSON | Print the string first, check LLM output format |

---

## 7. Key Takeaways

✓ **Read the last line first** — that's the actual error
✓ **Read upward** to find YOUR code's line number
✓ **Error type** tells you the category of fix
✓ **Error message** tells you the specific detail (which key, which file)
✓ **`print(type(x))`** is your best debug tool — shows what an object really is
✓ **`print(x)`** before a failing line — see exactly what the variable contains
✓ **Share the full traceback with Claude** — never just the last line

**Most common in AI projects:**
- `KeyError` — dict key mismatch (e.g., `"content"` vs `"text"`)
- `AttributeError` — calling `.content[0].text` on a string
- `ModuleNotFoundError` — forgot to `pip install`
- `IndexError` — empty RAG results list

---

## 8. Templates Available

See this lesson folder ([./](./)) for:
- `CHEATSHEET_errors.py` — 10 common errors with examples and fixes (runnable)
- `error_decoder.md` — quick-scan reference card for any error

**Your workflow:**
1. Get an error → read last line first
2. Look up the error type in `error_decoder.md`
3. Apply the fix
4. If stuck → use the "What to say to Claude" template

---

**Remember:** You're not memorizing error types. You're building a reflex: "error → last line → type → fix table → done."

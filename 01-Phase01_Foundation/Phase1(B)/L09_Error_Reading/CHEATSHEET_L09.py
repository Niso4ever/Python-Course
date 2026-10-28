"""
═══════════════════════════════════════════════════════════════════
LESSON 7 CHEATSHEET: Error Reading
═══════════════════════════════════════════════════════════════════

Quick reference for reading and fixing errors in AI projects.
Keep this open while debugging!

═══════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════
# 1. THE 3-STEP FIX PROCESS
# ═══════════════════════════════════════════════════════════

"""
STEP 1: READ (5 seconds)
  → Go to the LAST line of the traceback
  → That's the error type and message

STEP 2: LOCATE (10 seconds)
  → Find YOUR file in the traceback (not /site-packages/)
  → Note the line number
  → Look at that line in your code

STEP 3: FIX (15 seconds)
  → Look up the error type in error_decoder.md
  → Apply the standard fix
  → Or: use the "ask Claude" template below
"""


# ═══════════════════════════════════════════════════════════
# 2. ERROR TYPE QUICK TABLE
# ═══════════════════════════════════════════════════════════

"""
KeyError         → wrong dict key name     → print(dict.keys())
IndexError       → empty list              → if docs: before docs[0]
AttributeError   → wrong object type       → print(type(obj))
ModuleNotFound   → pip install missing     → pip install <name>
TypeError        → wrong data type         → print(type(var))
NameError        → typo / not assigned     → fix spelling / order
ValueError       → bad value               → check model name, range
IndentationError → missing 4 spaces        → indent after def/if/for
JSONDecodeError  → not valid JSON          → print() before json.loads()
FileNotFoundError→ wrong path              → print(os.getcwd())
"""


# ═══════════════════════════════════════════════════════════
# 3. DEBUG PRINT TOOLKIT
# ═══════════════════════════════════════════════════════════

import os
import json

# Check what type a variable is:
def debug_type(var, label="var"):
    print(f"DEBUG {label}: type={type(var).__name__}, value={repr(var)[:80]}")

# Usage:
# debug_type(response, "response")   # → DEBUG response: type=str, value='The answer...'
# debug_type(docs, "docs")           # → DEBUG docs: type=list, value=[{'text': '...


# Check a dict's keys:
def debug_dict(d, label="dict"):
    if isinstance(d, dict):
        print(f"DEBUG {label}: keys={list(d.keys())}")
    else:
        print(f"DEBUG {label}: NOT a dict — type={type(d).__name__}")

# Usage:
# debug_dict(docs[0], "first doc")   # → DEBUG first doc: keys=['text', 'score', 'source']


# Check a list:
def debug_list(lst, label="list"):
    print(f"DEBUG {label}: length={len(lst)}, first={repr(lst[0])[:60] if lst else 'EMPTY'}")

# Usage:
# debug_list(docs, "search results")  # → DEBUG search results: length=3, first={'text':...


# Check file path:
def debug_path(file_path):
    print(f"DEBUG path: looking for '{file_path}'")
    print(f"DEBUG cwd:  running from '{os.getcwd()}'")
    print(f"DEBUG exists: {os.path.exists(file_path)}")

# Usage:
# debug_path("data/documents.pdf")


# ═══════════════════════════════════════════════════════════
# 4. SAFE PATTERNS (prevent common errors)
# ═══════════════════════════════════════════════════════════

# Safe dict access (no KeyError):
def safe_get(d, key, default=None):
    return d.get(key, default)

# Usage:
doc = {"text": "hello", "score": 0.9}
content = safe_get(doc, "content", "no content key")   # → "no content key"
text    = safe_get(doc, "text", "")                    # → "hello"


# Safe list access (no IndexError):
def safe_first(lst, default=None):
    return lst[0] if lst else default

# Usage:
docs = []
first_doc = safe_first(docs, default="no docs found")  # → "no docs found"


# Safe JSON parse (no JSONDecodeError):
def safe_json_parse(text, default=None):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return default or {"raw_text": text}

# Usage:
parsed = safe_json_parse('{"answer": "yes"}')     # → {"answer": "yes"}
parsed = safe_json_parse("plain text response")   # → {"raw_text": "plain text response"}


# Safe file read (no FileNotFoundError):
def safe_read(file_path, default=""):
    if os.path.exists(file_path):
        with open(file_path) as f:
            return f.read()
    else:
        print(f"File not found: {file_path} (cwd: {os.getcwd()})")
        return default


# ═══════════════════════════════════════════════════════════
# 5. THE "ASK CLAUDE" TEMPLATE
# ═══════════════════════════════════════════════════════════

ASK_CLAUDE_TEMPLATE = """
Error I got:
[paste full traceback here — from "Traceback" to the last line]

My code that caused it:
[paste the relevant function — 5-20 lines]

What I was trying to do:
[one sentence description]
"""

# Example of a GOOD error report:
GOOD_EXAMPLE = """
Error I got:

KeyError: 'content'
  File "rag_agent.py", line 31, in answer
    context = "\\n".join([d["content"] for d in docs])

My code:
def answer(self, question):
    docs = self.db.search(question)
    context = "\\n".join([d["content"] for d in docs])
    return self.llm.invoke(context)

What I was trying to do:
Build a context string from retrieved documents to pass to the LLM.
"""


# ═══════════════════════════════════════════════════════════
# 6. READING A TRACEBACK — QUICK STEPS
# ═══════════════════════════════════════════════════════════

"""
Traceback (most recent call last):           ← ignore this header
  File "YOUR_file.py", line 23, in method   ← YOUR code (note line 23)
    the_line_that_broke
  File "/site-packages/...", line 87         ← library code (skip)
    internal_function()
ErrorType: the actual message here           ← READ THIS FIRST

YOUR FOCUS:
  1. Last line  → ErrorType: message
  2. Your file  → "YOUR_file.py", line 23
  3. Skip everything from /site-packages/
"""


# ═══════════════════════════════════════════════════════════
# 7. MOST COMMON AI PROJECT ERRORS
# ═══════════════════════════════════════════════════════════

"""
1. KeyError: 'content'
   → Your doc dict uses "text" not "content"
   → Fix: print(docs[0].keys())

2. AttributeError: 'str' has no attribute 'content'
   → Your call_llm() already returns a string
   → Fix: use response directly, not response.content[0].text

3. IndexError: list index out of range
   → Vector search returned [] (empty)
   → Fix: if docs: before docs[0]

4. ModuleNotFoundError: No module named 'X'
   → Forgot pip install
   → Fix: pip install <name> (see L6 for pip name mapping)

5. JSONDecodeError: Expecting value
   → LLM returned plain text, you called json.loads()
   → Fix: print(response) first; use safe_json_parse()
"""


# ═══════════════════════════════════════════════════════════
# END OF CHEATSHEET
# ═══════════════════════════════════════════════════════════

print("Error reading cheatsheet loaded!")
print("Error → last line → error_decoder.md → fix → done.")

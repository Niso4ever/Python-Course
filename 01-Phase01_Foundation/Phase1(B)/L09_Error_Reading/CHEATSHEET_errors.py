"""
═══════════════════════════════════════════════════════════════════
CHEATSHEET: 10 Common Errors in AI Projects
═══════════════════════════════════════════════════════════════════

Each error shows:
  1. What triggers it
  2. What the error message says
  3. How to fix it

Keep this open when debugging!
═══════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════
# ERROR 1: KeyError — Wrong dict label
# ═══════════════════════════════════════════════════════════

# What triggers it:
doc = {"text": "About RAG...", "score": 0.9, "source": "wiki.pdf"}

# WRONG — key doesn't exist:
# print(doc["content"])   # → KeyError: 'content'

# RIGHT — use the actual key:
print("E1 - KeyError fix:")
print(doc["text"])                          # use real key name
print(doc.get("content", "key not found")) # .get() never crashes

# Diagnosis: print the whole dict first
print(doc.keys())   # → dict_keys(['text', 'score', 'source'])


# ═══════════════════════════════════════════════════════════
# ERROR 2: IndexError — List too short or empty
# ═══════════════════════════════════════════════════════════

docs = []   # empty — vector search returned nothing

# WRONG — accessing empty list:
# first = docs[0]   # → IndexError: list index out of range

# RIGHT — check first:
print("\nE2 - IndexError fix:")
if docs:
    first = docs[0]
    print(first)
else:
    print("No docs returned — check your search query or database")

# One-liner version:
first = docs[0] if docs else None
print(f"first = {first}")


# ═══════════════════════════════════════════════════════════
# ERROR 3: AttributeError — Wrong object type
# ═══════════════════════════════════════════════════════════

def simulated_call_llm(prompt):
    # This function already extracts text — returns a string
    return f"The answer is: {prompt[:20]}..."

response = simulated_call_llm("What is RAG?")

# WRONG — treating string as Anthropic object:
# print(response.content[0].text)   # → AttributeError: 'str' has no 'content'

# RIGHT — it's already a string:
print("\nE3 - AttributeError fix:")
print(response)   # use directly
print(type(response))   # always check: → <class 'str'>


# ═══════════════════════════════════════════════════════════
# ERROR 4: ModuleNotFoundError — Package not installed
# ═══════════════════════════════════════════════════════════

# What triggers it:
# from langchain_anthropic import ChatAnthropic
# → ModuleNotFoundError: No module named 'langchain_anthropic'

# FIX (run in terminal, not Python):
# pip install langchain-anthropic

print("\nE4 - ModuleNotFoundError fix:")
print("Run in terminal: pip install <package-name>")
print("pip uses hyphens:     langchain-anthropic")
print("import uses underscores: langchain_anthropic")


# ═══════════════════════════════════════════════════════════
# ERROR 5: TypeError — Wrong data type
# ═══════════════════════════════════════════════════════════

def count_tokens(text):
    return len(text) // 4   # needs a string

# WRONG — passing an int:
# count_tokens(1000)   # → TypeError: object of type 'int' has no len()

# RIGHT — pass a string:
print("\nE5 - TypeError fix:")
result = count_tokens("What is retrieval-augmented generation?")
print(f"Tokens: {result}")

# Or convert:
def count_tokens_safe(text):
    text = str(text)   # convert anything to string
    return len(text) // 4

print(f"Safe version: {count_tokens_safe(12345)}")
print(f"type check: {type('hello')}")   # → <class 'str'>


# ═══════════════════════════════════════════════════════════
# ERROR 6: NameError — Variable not defined
# ═══════════════════════════════════════════════════════════

question = "What is RAG?"

# WRONG — typo in variable name:
# print(questoin)   # → NameError: name 'questoin' is not defined

# RIGHT — correct spelling:
print("\nE6 - NameError fix:")
print(question)   # spelled correctly

# ALSO WRONG — using before assigning:
# print(result)    # → NameError: result not defined yet
result = "RAG is Retrieval-Augmented Generation"
print(result)     # now it's defined


# ═══════════════════════════════════════════════════════════
# ERROR 7: ValueError — Right type, wrong value
# ═══════════════════════════════════════════════════════════

# WRONG — invalid model name:
# model = "claude-99-ultra"
# → anthropic.BadRequestError: model does not exist

# RIGHT — use a real model name:
print("\nE7 - ValueError fix:")
valid_models = [
    "claude-sonnet-5-5",
    "claude-opus-5-5",
    "claude-haiku-5-5"
]
model = valid_models[0]
print(f"Using model: {model}")

# Also: temperature must be 0.0–1.0
temperature = 0.7   # valid
# temperature = 2.5  # → ValueError: temperature out of range


# ═══════════════════════════════════════════════════════════
# ERROR 8: IndentationError — Missing indent
# ═══════════════════════════════════════════════════════════

# WRONG (would crash before running):
# def chat(self, input):
# return input   ← no indent → IndentationError

# RIGHT — 4 spaces inside def:
def chat(user_input):
    return f"Echo: {user_input}"   # ← 4 spaces

print("\nE8 - IndentationError fix:")
print(chat("Hello"))


# ═══════════════════════════════════════════════════════════
# ERROR 9: JSONDecodeError — String is not JSON
# ═══════════════════════════════════════════════════════════

import json

# WRONG — LLM returned plain text, not JSON:
llm_output = "The answer is: RAG stands for Retrieval-Augmented Generation."
# json.loads(llm_output)   # → JSONDecodeError: Expecting value

# RIGHT — check before parsing:
print("\nE9 - JSONDecodeError fix:")
def safe_json_parse(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        print(f"Not JSON. Raw text: {text[:50]}")
        return {"raw_text": text}

result = safe_json_parse(llm_output)
print(result)

# Valid JSON (what LLM should return if you ask for JSON):
valid_json = '{"answer": "RAG is Retrieval-Augmented Generation", "confidence": 0.9}'
parsed = json.loads(valid_json)
print(f"Parsed: {parsed}")


# ═══════════════════════════════════════════════════════════
# ERROR 10: FileNotFoundError — Wrong path
# ═══════════════════════════════════════════════════════════

import os

# WRONG:
# with open("docs/report.pdf") as f: ...
# → FileNotFoundError: No such file or directory

# DIAGNOSIS:
print("\nE10 - FileNotFoundError fix:")
print(f"Python is looking in: {os.getcwd()}")
print(f"Files here: {os.listdir('.')[:5]}")   # first 5 files

# RIGHT — use os.path.exists() to check first:
file_path = "non_existent_file.pdf"
if os.path.exists(file_path):
    with open(file_path) as f:
        content = f.read()
else:
    print(f"File not found: {file_path}")
    print("Check: is the file in the right folder?")


# ═══════════════════════════════════════════════════════════
# DEMO OUTPUT SUMMARY
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("\n" + "="*60)
    print("All 10 errors demonstrated above — scroll up to review")
    print("Each section shows: WRONG (commented out) → RIGHT (working)")
    print("="*60)
    print("\nQuick Fix Table:")
    print("  KeyError         → print(dict.keys())")
    print("  IndexError       → if list: before [0]")
    print("  AttributeError   → print(type(obj))")
    print("  ModuleNotFound   → pip install <name>")
    print("  TypeError        → print(type(var))")
    print("  NameError        → fix typo, check assignment order")
    print("  ValueError       → check model name / value range")
    print("  IndentationError → add 4 spaces")
    print("  JSONDecodeError  → print() before json.loads()")
    print("  FileNotFoundError→ print(os.getcwd())")

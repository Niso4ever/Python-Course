# Pass C: Visual — Error Reading

**Goal:** See tracebacks as structured signals, not scary red walls of text.

---

## Diagram 1: Traceback Anatomy (Read This Direction)

```
Traceback (most recent call last):
│
├─ File "main.py", line 12, in <module>       ← OUTERMOST call (entry point)
│    result = rag.answer("What is RAG?")
│
├─ File "rag_agent.py", line 34, in answer    ← YOUR CODE (look here!)
│    docs = self.db.search(question)
│
├─ File "/site-packages/chroma.py", line 87   ← library code (skip)
│    validate_where(where)
│
└─ ValueError: Expected str, got dict          ← READ THIS FIRST ◀◀◀
                                                  ↑
                                               Start here, then work UP
```

**Arrow rule:** `↑ Read up from the bottom to find YOUR code.`

---

## Diagram 2: The 3-Step Fix Process

```
RED ERROR APPEARS
      │
      ▼
┌─────────────────────────────┐
│  STEP 1: READ               │
│  → Last line: error type?   │
│  → Error message: what key/ │
│    attribute/file?          │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  STEP 2: LOCATE             │
│  → Find YOUR file + line    │
│  → What line failed?        │
│  → What variable was used?  │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  STEP 3: FIX                │
│  → Look up error in         │
│    error_decoder.md         │
│  → Apply standard fix       │
│  → Or: ask Claude with      │
│    full traceback           │
└─────────────────────────────┘
```

---

## Diagram 3: Error Type Decision Tree

```
GOT AN ERROR?
      │
      ├─ "No module named..."         → ModuleNotFoundError
      │   FIX: pip install <name>
      │
      ├─ "KeyError: 'something'"      → KeyError
      │   FIX: print the dict, find the real key name
      │
      ├─ "list index out of range"    → IndexError
      │   FIX: check if list is empty before accessing [0]
      │
      ├─ "has no attribute 'x'"       → AttributeError
      │   FIX: print(type(obj)) — you have the wrong object type
      │
      ├─ "object of type X has no..." → TypeError
      │   FIX: print(type(var)) — wrong data type passed
      │
      ├─ "is not defined"             → NameError
      │   FIX: typo? check spelling; or variable not assigned yet
      │
      ├─ "invalid value" / "does not exist" → ValueError
      │   FIX: wrong model name, bad temperature, bad token count
      │
      ├─ "No such file or directory"  → FileNotFoundError
      │   FIX: print(os.getcwd()) — check where Python is looking
      │
      ├─ "expected an indented block" → IndentationError
      │   FIX: add 4 spaces to line after def/if/for/class
      │
      └─ "Expecting value"            → JSONDecodeError
          FIX: print the string first — it's not valid JSON
```

---

## Diagram 4: KeyError — The Most Common AI Error

```
THE MISMATCH:

Dict in the database:                   Your code assumes:
┌─────────────────────────┐             ┌─────────────────────────┐
│  {                      │             │  doc["content"]         │
│    "text":  "...",      │      ≠      │        ↑                │
│    "score": 0.9,        │             │   key doesn't exist!    │
│    "source": "wiki"     │             └─────────────────────────┘
│  }                      │
└─────────────────────────┘
         ↑
   real key is "text"

FIX: print(docs[0]) first → see the real keys → update your code
```

---

## Diagram 5: AttributeError — Wrong Object Type

```
WHAT YOU THINK:                        WHAT IT ACTUALLY IS:

response = call_llm("hello")           call_llm() already extracts:
                                           return response.content[0].text
     ↓                                           ↓ returns a string
response.content[0].text              response = "RAG is..."
     ↑                                           ↑
 crashes! str has no .content          already a string, use directly

DIAGNOSIS TOOL:
  print(type(response))
  → <class 'str'>         ← now you know
  → <class 'anthropic.types.Message'>  ← then .content[0].text works
```

---

## Diagram 6: IndexError — The Empty List Trap

```
TIMELINE:

  db.search("obscure query") → returns []   (no matches)
                                    ↓
  docs = []                         (empty list)
                                    ↓
  best = docs[0]                    CRASH: IndexError
                                    ↓
  FIX:
  if docs:                          (check first)
      best = docs[0]                (safe access)
  else:
      return "No results found"

VISUAL:
  docs = [doc1, doc2, doc3]   → docs[0] = doc1  ✓
  docs = []                   → docs[0] = ???    ✗  IndexError
```

---

## Diagram 7: How a Library Traceback Looks vs Your Code

```
Traceback (most recent call last):
┌──────────────────────────────────────────────────────────────┐
│  YOUR CODE ZONE (look here for the fix)                      │
│                                                              │
│  File "my_agent.py", line 23, in answer    ← YOUR FILE      │
│    result = self.db.search(question)                         │
└──────────────────────────────────────────────────────────────┘
┌──────────────────────────────────────────────────────────────┐
│  LIBRARY CODE ZONE (skip this — not your code)               │
│                                                              │
│  File "/lib/chromadb/client.py", line 104  ← LIBRARY        │
│    return self._query(...)                                   │
│  File "/lib/chromadb/collection.py", line 87               │
│    validate_embeddings(embeddings)                           │
└──────────────────────────────────────────────────────────────┘
ValueError: Expected list of floats, got list of strings     ← ERROR

HOW TO SPOT LIBRARY CODE:
  /site-packages/... → library (skip)
  /lib/python3.x/... → library (skip)
  your_file.py       → YOUR code (focus here)
```

---

## Diagram 8: The Debug Print Pattern

```
WHEN STUCK: add print() BEFORE the failing line

ERROR ON LINE 31:
  context = "\n".join([d["content"] for d in docs])  ← crashes

DEBUG VERSION:
  print("=== DEBUG ===")
  print(f"docs count: {len(docs)}")     ← Is it empty?
  if docs:
      print(f"first doc keys: {docs[0].keys()}")  ← What keys exist?
      print(f"first doc: {docs[0]}")              ← Full dict
  context = "\n".join([d["content"] for d in docs])

OUTPUT:
  === DEBUG ===
  docs count: 3
  first doc keys: dict_keys(['text', 'score', 'source'])
  first doc: {'text': 'RAG is...', 'score': 0.92, 'source': 'wiki.pdf'}

DIAGNOSIS: key is 'text' not 'content'
FIX: change d["content"] → d["text"]
REMOVE the debug prints when done.
```

---

## Diagram 9: What to Send Claude When You're Stuck

```
❌ BAD (not enough info):
  "My code crashed, help"

✅ GOOD (everything Claude needs):
  ┌────────────────────────────────────────────────────────────┐
  │  Error I got:                                              │
  │                                                            │
  │  KeyError: 'content'                                       │
  │    File "agent.py", line 31, in answer                     │
  │      context = "\n".join([d["content"] for d in docs])    │
  │                                                            │
  │  My code:                                                  │
  │  def answer(self, question):                               │
  │      docs = self.db.search(question)                       │
  │      context = "\n".join([d["content"] for d in docs])    │
  │      ...                                                   │
  │                                                            │
  │  What I was trying to do:                                  │
  │  Build a context string from retrieved documents           │
  └────────────────────────────────────────────────────────────┘

Claude needs: error type + line + your code + what you wanted
```

---

**Next:** See [PASS3_TEMPLATES.md](PASS3_TEMPLATES.md) for the error reference files.

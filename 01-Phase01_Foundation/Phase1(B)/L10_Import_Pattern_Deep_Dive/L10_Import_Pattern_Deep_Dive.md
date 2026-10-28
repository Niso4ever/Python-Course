# Lesson 10: Import Pattern Deep Dive
## The Ecosystem Theory

In L08 you learned *what* imports are. Now you go deeper: **where packages actually live, how Python finds them, and how to manage them across projects without breaking things.**

This is the hidden knowledge that separates "code that works on my machine" from "code that works everywhere." Every AI engineer hits this wall. After this lesson, you won't.

---

## 1. The Hidden World Under Every Import

When you type `import anthropic`, Python does this in order:

```
1. Check sys.modules       → Already imported this session? Use cached version.
2. Check built-in modules  → Is it part of Python itself? (os, json, sys)
3. Check sys.path          → Search each folder in this list for the package

sys.path typically includes:
  /your/project/folder         ← Your own files
  /home/user/.venv/lib/...    ← Virtual environment packages
  /usr/lib/python3.11/...     ← System Python packages
  /usr/lib/python3.11/site-packages/  ← pip-installed packages
```

**Insight:** This is why the same code can fail on a different machine — `sys.path` is different, and the package isn't installed there.

---

## 2. Virtual Environments — The Sandbox Concept

**The problem:** Project A needs `langchain==0.2`, Project B needs `langchain==0.3`. If you install both globally, they conflict.

**The solution:** Virtual environments — isolated sandboxes per project.

```
YOUR MACHINE
├── system Python (3.11)
│   └── site-packages/         ← global packages (avoid putting AI stuff here)
│
├── project_rag/
│   ├── .venv/                 ← THIS project's sandbox
│   │   └── site-packages/
│   │       ├── langchain 0.2
│   │       └── anthropic 0.28
│   └── rag_agent.py
│
└── project_chatbot/
    ├── .venv/                 ← DIFFERENT sandbox
    │   └── site-packages/
    │       ├── langchain 0.3   ← different version, no conflict
    │       └── anthropic 0.30
    └── chatbot.py
```

**Create and use:**
```bash
# Create:
python -m venv .venv

# Activate (Mac/Linux):
source .venv/bin/activate

# Activate (Windows):
.venv\Scripts\activate

# You'll see: (.venv) at your terminal prompt
# Now pip install goes INTO this sandbox only

# Install your project's packages:
pip install anthropic langchain-anthropic langchain-community
```

---

## 3. requirements.txt — The Package Manifest

**What it is:** A text file listing all packages your project needs. When someone else (or you, on a new machine) gets your code, they run `pip install -r requirements.txt` and get the exact same environment.

```
# requirements.txt
anthropic==0.40.0
langchain==0.3.7
langchain-anthropic==0.3.3
langchain-community==0.3.7
langchain-core==0.3.15
python-dotenv==1.0.1
chromadb==0.5.18
sentence-transformers==3.3.1
```

**Generate it automatically:**
```bash
pip freeze > requirements.txt   # captures ALL installed packages with exact versions
```

**Install from it:**
```bash
pip install -r requirements.txt
```

**Insight:** The `==` pins the exact version. This is what makes your project reproducible. Without it, `pip install langchain` might install a breaking new version next month.

---

## 4. Reading a requirements.txt in 10 Seconds

When you inherit an AI project, the first file to read is `requirements.txt`:

```
# requirements.txt of a RAG project — decoded:

anthropic==0.40.0              ← Direct Claude API calls
langchain==0.3.7               ← LangChain framework
langchain-anthropic==0.3.3     ← LangChain's Claude wrapper
langchain-community==0.3.7     ← Vector stores, document loaders
chromadb==0.5.18               ← Local vector database
sentence-transformers==3.3.1   ← Text embedding model (local, free)
python-dotenv==1.0.1           ← .env file loader
pydantic==2.10.3               ← Data validation (LangChain uses this)
fastapi==0.115.5               ← REST API server
uvicorn==0.32.1                ← Runs FastAPI

VERDICT: This is a production RAG API — not just a script.
         It has a local vector DB, embedding model, and web server.
```

---

## 5. The `.env` Secret (Protecting Your API Keys)

When you make network calls to AI models or external services (like in L19), you need secret API keys. NEVER put these directly into your `.py` files, because you might accidentally share them or push them to GitHub.

**The solution:** A file literally just called `.env`.

```env
# .env
ANTHROPIC_API_KEY=sk-ant-api03-abcdef...
OPENAI_API_KEY=sk-proj-xyz...
```
*Note: Make sure `.env` is listed in your `.gitignore` file!*

**How to load it in Python:**
The `python-dotenv` package (listed in the requirements above) does this magically.

```python
import os
from dotenv import load_dotenv

# This finds the .env file and secretly loads the keys into your system environment
load_dotenv() 

# Now your LangChain/DSPy agents will automatically find their keys!
```

---

## 6. The `__init__.py` Secret

When you see `from langchain_core.prompts import ChatPromptTemplate`, you're navigating a folder tree:

```
langchain_core/                ← package folder
├── __init__.py               ← makes this a Python package (required!)
├── prompts/                  ← sub-package folder
│   ├── __init__.py          ← makes THIS a sub-package
│   ├── chat.py              ← contains ChatPromptTemplate class
│   └── base.py
├── messages/
│   ├── __init__.py
│   └── ...
└── output_parsers/
    └── ...
```

**The insight:** `from langchain_core.prompts import ChatPromptTemplate` literally means:
→ Go into `langchain_core` folder
→ Go into `prompts` folder
→ Import `ChatPromptTemplate` from whatever file exports it

You don't need to know which file — Python's `__init__.py` files handle the routing.

---

## 7. How to Find the Right Import

**Method 1: The error tells you**
```
ImportError: cannot import name 'ChatAnthropic' from 'langchain'
→ Google "ChatAnthropic import" → langchain_anthropic, not langchain
```

**Method 2: Library docs** (always has an "Installation" or "Quickstart" section)

**Method 3: GitHub source code** — search for the class name in the repo

**Method 4: Tab autocomplete in VS Code** — type `from langchain` then press Tab

**Method 5: Ask Claude** — "What is the correct import for `X` in LangChain 0.3?"

---

## 8. Spotting Version Conflicts (The Silent Killer)

```
ERROR (confusing, no obvious traceback):
  AttributeError: 'ChatAnthropic' object has no attribute 'invoke'

REAL CAUSE:
  You have langchain-anthropic==0.1 installed
  But .invoke() was added in 0.2
  The error looks like a code bug — it's actually a version bug.

HOW TO CHECK:
  pip show langchain-anthropic
  → Name: langchain-anthropic
  → Version: 0.1.23      ← too old!

FIX:
  pip install langchain-anthropic --upgrade
```

**The insight:** Many "bugs" in AI code are version mismatches, not logic errors. When AttributeError fires on a well-known library method, check the version first.

---

## 9. Key Takeaways

✓ Python searches `sys.path` in order to find imports
✓ **Virtual environments** isolate packages per project — always use one
✓ **requirements.txt** = the project's package manifest — always check it first
✓ **`pip freeze > requirements.txt`** captures your current environment
✓ **`pip install -r requirements.txt`** reproduces any environment
✓ When a method "doesn't exist" on a library class → check the version
✓ `__init__.py` files make folders into importable packages — you never write these for AI work
✓ Find correct imports via: error messages → docs → GitHub → Claude

**Phase 1B Insight:** This lesson isn't about memorizing — it's about debugging the *environment* not just the *code*. Most "it doesn't work on my machine" problems live here.

---

## Templates Available

See this lesson folder ([./](./)) for:
- `CHEATSHEET_L10.py` — venv commands + pip commands quick reference

This lesson has no `template_*.py` file.

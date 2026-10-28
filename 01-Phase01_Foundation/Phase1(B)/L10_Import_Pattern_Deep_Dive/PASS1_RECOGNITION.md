# Pass 1: Recognition — Import Deep Dive
## Read These 8 Scenarios — Don't Memorize Them

**Goal:** Recognize virtual environments, requirements files, and version management in any AI project.

---

## Example 1: Reading a requirements.txt in 10 Seconds

```
# requirements.txt — a RAG production system
anthropic==0.40.0
langchain==0.3.7
langchain-anthropic==0.3.3
langchain-community==0.3.7
chromadb==0.5.18
sentence-transformers==3.3.1
python-dotenv==1.0.1
fastapi==0.115.5
uvicorn==0.32.1
pydantic==2.10.3
```

**Decode it in 10 seconds:**
- `anthropic` → direct Claude API
- `langchain*` → LangChain framework (4 packages = full RAG stack)
- `chromadb` → local vector database
- `sentence-transformers` → local embedding model (free, no API)
- `fastapi + uvicorn` → REST API server → this is a web service, not just a script
- `pydantic` → data validation (used by LangChain internally)

**Verdict:** Production RAG API. Budget: sentence-transformers is local/free, API costs from anthropic + langchain calls.

---

## Example 2: Virtual Environment Setup Sequence

```bash
# What you see at the start of any AI project setup:

git clone https://github.com/user/rag-project
cd rag-project

python -m venv .venv           # Create isolated sandbox
source .venv/bin/activate      # Activate it (Mac/Linux)
# (.venv) now appears in terminal prompt

pip install -r requirements.txt  # Install all dependencies
cp .env.example .env             # Copy API key template
# (edit .env with your actual keys)

python main.py                   # Run the project
```

**What to notice:**
- `python -m venv .venv` → creates a `.venv/` folder (often in .gitignore)
- `source .venv/bin/activate` → all pip installs now go INTO this sandbox
- `(.venv)` prefix in terminal = you're inside the virtual environment
- `pip install -r requirements.txt` → install everything at once from the manifest

---

## Example 3: Version Pinning vs Loose Requirements

```
# PINNED (exact version — reproducible, strict):
anthropic==0.40.0          → always installs exactly 0.40.0

# MINIMUM VERSION (flexible — gets latest compatible):
anthropic>=0.35.0          → installs 0.35.0 or newer

# RANGE (bounded — common in libraries):
anthropic>=0.35.0,<0.50.0  → any version between these

# UNPINNED (dangerous for production — latest always):
anthropic                  → installs whatever is newest today
```

**Which to use:**
- Production apps → `==` (reproducible, no surprise updates)
- Your own experiments → `>=` or unpinned is fine

---

## Example 4: The `pip freeze` vs `pip install` Workflow

```bash
# STEP 1: Install what you need (experiment freely):
pip install langchain-anthropic
pip install chromadb
pip install sentence-transformers

# STEP 2: Capture the exact state (for sharing/deployment):
pip freeze > requirements.txt
# Now requirements.txt has EVERYTHING with exact versions

# STEP 3: On a new machine / for a teammate:
pip install -r requirements.txt
# Exact same environment, instantly
```

**Insight:** `pip freeze` captures ALL installed packages including dependencies of dependencies. The file will be longer than what you explicitly installed — that's normal.

---

## Example 5: Spotting a Version Mismatch Bug

```
# Error appears:
AttributeError: 'ChatAnthropic' object has no attribute 'ainvoke'

# But the code looks correct:
response = await llm.ainvoke(messages)   # this should work!

# Root cause check:
pip show langchain-anthropic
# → Version: 0.1.4   ← too old! ainvoke was added in 0.2.0

# Fix:
pip install langchain-anthropic --upgrade
# → Successfully installed langchain-anthropic-0.3.3
```

**The pattern:** `AttributeError` on a known library method → suspect version mismatch before suspecting your code.

---

## Example 6: The sys.path Inspection

```python
# When you want to know WHERE Python is looking for packages:
import sys
for path in sys.path:
    print(path)

# Output (in a venv):
# /home/user/project/            ← your project files
# /home/user/project/.venv/lib/python3.11/site-packages  ← venv packages
# /usr/lib/python3.11            ← system Python built-ins

# Output (WITHOUT venv active):
# /home/user/project/
# /usr/local/lib/python3.11/site-packages  ← system packages (shared with all projects!)
```

**Why this matters:** Without a venv, ALL projects share the same packages. Two projects needing different LangChain versions will conflict.

---

## Example 7: The `__init__.py` Discovery Pattern

```python
# When you want to know what's available to import from a package:
import langchain_core
print(dir(langchain_core))   # shows everything exposed at top level

# Navigate the structure:
from langchain_core import prompts
print(dir(prompts))   # shows what's in the prompts subpackage

# Find the source file location:
import langchain_anthropic
print(langchain_anthropic.__file__)
# → /home/user/.venv/lib/python3.11/site-packages/langchain_anthropic/__init__.py
# Now you can open this file to see exactly what's exported
```

---

## Example 8: pyproject.toml — The Modern Alternative

Newer Python projects use `pyproject.toml` instead of `requirements.txt`:

```toml
# pyproject.toml (you'll see this in LangChain, DSPy, CrewAI source repos)
[project]
name = "my-rag-agent"
version = "0.1.0"
requires-python = ">=3.11"

dependencies = [
    "anthropic>=0.35.0",
    "langchain>=0.3.0",
    "langchain-anthropic>=0.3.0",
    "chromadb>=0.5.0",
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "black>=24.0.0",
]
```

**Install from pyproject.toml:**
```bash
pip install -e .        # Install in editable mode (development)
pip install ".[dev]"    # Include dev dependencies
```

**What to notice:** `requires-python = ">=3.11"` — if you see this and your Python is 3.9, that's the problem.

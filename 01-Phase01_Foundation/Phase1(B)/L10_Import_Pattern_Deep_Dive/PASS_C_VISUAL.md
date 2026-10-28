# Pass C: Visual — Import Deep Dive

---

## Diagram 1: Virtual Environment — The Sandbox

```
WITHOUT VENV (dangerous — all projects share packages):

YOUR MACHINE (system Python)
└── site-packages/
    ├── langchain 0.2   ← Project A needs this
    └── langchain 0.3   ← Project B needs this
    CONFLICT! Only one can exist.

WITH VENV (safe — each project isolated):

YOUR MACHINE
├── project_rag/
│   ├── .venv/
│   │   └── site-packages/
│   │       └── langchain 0.2  ← Project A's private copy
│   └── agent.py
│
└── project_chat/
    ├── .venv/
    │   └── site-packages/
    │       └── langchain 0.3  ← Project B's private copy
    └── chatbot.py

No conflict. Each project is self-contained.
```

---

## Diagram 2: Python's Import Search Order

```
import anthropic
        │
        ▼
  sys.modules cache?  ──YES──▶  return cached module (fast!)
        │NO
        ▼
  Built-in module?    ──YES──▶  return built-in (os, json, sys)
        │NO
        ▼
  Search sys.path     (in order):
  ┌─────────────────────────────────┐
  │  1. /your/project/              │ ← your own .py files
  │  2. /project/.venv/site-packages│ ← your pip installs (venv)
  │  3. /usr/lib/python3.11/        │ ← system Python
  │  4. /usr/lib/python3.11/site-packages │ ← system pip installs
  └─────────────────────────────────┘
        │
        ▼ (first match wins)
  Package found → import it
  Package NOT found → ModuleNotFoundError
```

---

## Diagram 3: requirements.txt Lifecycle

```
START PROJECT                    DEVELOP                    SHARE / DEPLOY
──────────────                   ────────                   ──────────────

python -m venv .venv             pip install X              pip freeze > req.txt
source .venv/bin/activate        pip install Y              git add req.txt
                                 pip install Z              git commit
                                                            ↓
                                                      NEW MACHINE:
                                                      pip install -r req.txt
                                                      → exact same environment
```

---

## Diagram 4: Version Number Anatomy

```
langchain-anthropic == 0 . 3 . 3
                       │   │   │
                       │   │   └─ PATCH: bug fixes, safe to upgrade
                       │   └─── MINOR: new features, usually backwards-compatible
                       └─────── MAJOR: breaking changes (0→1 = huge change)

UPGRADE SAFETY:
  0.3.3 → 0.3.4  ✓ safe (bug fix)
  0.3.3 → 0.4.0  ⚠ check changelog (new features)
  0.3.3 → 1.0.0  ✗ breaking changes (read docs!)

PINNING SYNTAX:
  ==0.3.3         exact (reproducible)
  >=0.3.0         minimum
  >=0.3.0,<0.4.0  range (safe minor updates only)
  ~=0.3.3         compatible release (0.3.x only)
```

---

## Diagram 5: Decoding Any requirements.txt

```
SCAN PATTERN (10 seconds):

anthropic*         → Direct Claude API
langchain*         → LangChain framework
openai*            → OpenAI API
dspy*              → DSPy framework
crewai*            → CrewAI multi-agent

chromadb           → Local vector database
faiss*             → In-memory vector database
pinecone*          → Cloud vector database (costs money)
weaviate*          → Cloud/local vector database

sentence-transformers → Local embedding model (free)
openai-embeddings  → OpenAI embeddings (costs money per token)

fastapi, flask     → Web server → this is an API, not a script
uvicorn, gunicorn  → Production web server

redis              → Caching / session store
psycopg2, sqlalchemy → SQL database
```

---

## Diagram 6: The venv Activation States

```
TERMINAL STATE — how to tell if venv is active:

INACTIVE (no venv):
  user@machine:~/project$ python --version
  Python 3.11.4                    ← system Python
  user@machine:~/project$          ← no prefix

ACTIVE (.venv on):
  (.venv) user@machine:~/project$ python --version
  Python 3.11.4                    ← same version, but now uses .venv packages
  (.venv) user@machine:~/project$  ← (.venv) prefix = ACTIVE

ACTIVATION COMMANDS:
  Mac/Linux: source .venv/bin/activate
  Windows:   .venv\Scripts\activate

DEACTIVATION:
  deactivate       (works on all platforms)

CHECK WHICH PYTHON IS ACTIVE:
  which python     (Mac/Linux)
  where python     (Windows)
  → should point to .venv/bin/python, not /usr/bin/python
```

---

## Diagram 7: pip vs pip3 vs python -m pip

```
WHICH pip TO USE? (common confusion)

pip          → might be Python 2 pip on old systems (dangerous)
pip3         → explicitly Python 3 pip (safer)
python -m pip → pip for WHICHEVER python is active (safest)

WITH VENV ACTIVE:
  All three are equivalent — they all use the venv's pip

RECOMMENDATION:
  Always activate venv first, then just use: pip install X
  The venv pip is always the right one.

CHECK: pip --version
  → pip 24.3.1 from /project/.venv/lib/python3.11/site-packages/pip
                          ↑
                     .venv in the path = correct pip
```

---

## Diagram 8: The .gitignore for AI Projects

```
# What to EXCLUDE from git (never commit these):

.venv/          ← virtual environment (huge, machine-specific)
__pycache__/    ← compiled Python bytecode (auto-generated)
*.pyc           ← compiled Python files
.env            ← API keys! NEVER commit this

# Vector database storage (often large):
chroma_db/
*.db
*.sqlite

# Model cache (can be gigabytes):
.cache/
models/
*.bin
*.pt

# What TO INCLUDE:
requirements.txt    ← package manifest (small, essential)
.env.example        ← template with placeholder keys (safe to share)
*.py                ← your actual code
```

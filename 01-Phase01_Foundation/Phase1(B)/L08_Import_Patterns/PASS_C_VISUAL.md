# Pass C: Visual — Import Patterns

**Goal:** See where imports come from and how they connect to your code.

---

## Diagram 1: The Full Import Pipeline

```
THE INTERNET (pypi.org)
┌──────────────────────────────────────────────────────┐
│  langchain        langchain-anthropic   anthropic     │
│  langchain-core   langchain-community  dspy  crewai  │
│  python-dotenv    numpy  pandas  ...                  │
└──────────────────────────────────────────────────────┘
          │
          │  pip install langchain-anthropic
          │  (downloads to your machine)
          ▼
YOUR MACHINE (site-packages folder)
┌──────────────────────────────────────────────────────┐
│  /lib/python3.11/site-packages/                      │
│  ├── langchain_anthropic/                            │
│  ├── langchain_core/                                 │
│  ├── anthropic/                                      │
│  └── ...                                             │
└──────────────────────────────────────────────────────┘
          │
          │  from langchain_anthropic import ChatAnthropic
          │  (loads into memory when script runs)
          ▼
YOUR PYTHON FILE
┌──────────────────────────────────────────────────────┐
│  ChatAnthropic is now available                      │
│  llm = ChatAnthropic(model="claude-sonnet-5-5")      │
└──────────────────────────────────────────────────────┘
```

---

## Diagram 2: Three Import Forms Side by Side

```
FORM 1: import X                FORM 2: from X import Y         FORM 3: import X as Z
──────────────────────          ───────────────────────          ─────────────────────
import anthropic                from anthropic import Anthropic  import numpy as np
         │                               │                               │
         │                               │                               │
You get: anthropic               You get: Anthropic directly      You get: np (short name)
         (the whole box)                 (one tool from box)             (the whole box, renamed)

Usage:                           Usage:                           Usage:
anthropic.Anthropic()            Anthropic()                      np.array([1, 2, 3])
anthropic.APIError               (no prefix needed)               np.mean([1, 2, 3])


WHEN TO USE EACH:
import X        → when you need many things from X, or just one with prefix
from X import Y → when you use Y a lot and want it clean
import X as Y   → industry convention (np, pd, etc.) or long names
```

---

## Diagram 3: Decoding a Package Path

```
from  langchain_community  .  vectorstores  import  Chroma
 │           │              │       │          │       │
 │           │              │       │          │       └─ The class/function you want
 │           │              │       │          └─ Python keyword: "grab this one thing"
 │           │              │       └─ Sub-module (like a folder inside the package)
 │           │              └─ Separator (dot = "go into")
 │           └─ Top-level package name (matches pip install name*)
 └─ Python keyword: "from this package..."

* Note: pip uses hyphens (langchain-community), Python uses underscores (langchain_community)
  pip install langchain-community  →  from langchain_community import ...
  pip install python-dotenv        →  from dotenv import load_dotenv
```

---

## Diagram 4: Built-in vs Third-Party

```
BUILT-IN (no pip needed — Python ships with these)
┌────────────────────────────────────────────────┐
│  import os         → file system, env vars     │
│  import json       → read/write JSON           │
│  import re         → regular expressions       │
│  import sys        → system info               │
│  import time       → timing, sleep             │
│  import pathlib    → file paths                │
│  from typing import List, Dict, Optional       │
└────────────────────────────────────────────────┘

THIRD-PARTY (pip install required)
┌────────────────────────────────────────────────┐
│  pip install anthropic                          │
│      → import anthropic                        │
│                                                │
│  pip install langchain-anthropic               │
│      → from langchain_anthropic import ...     │
│                                                │
│  pip install langchain-community               │
│      → from langchain_community import ...     │
│                                                │
│  pip install python-dotenv                     │
│      → from dotenv import load_dotenv          │
│                                                │
│  pip install dspy                              │
│      → import dspy                             │
│                                                │
│  pip install crewai                            │
│      → from crewai import Agent, Task, Crew    │
└────────────────────────────────────────────────┘

ImportError = missing pip install
```

---

## Diagram 5: LangChain Package Map

```
LangChain is split into multiple packages (install separately):

pip install langchain           →  from langchain import ...
pip install langchain-core      →  from langchain_core import ...
pip install langchain-community →  from langchain_community import ...
pip install langchain-anthropic →  from langchain_anthropic import ...

WHAT LIVES WHERE:

langchain_core/                     ← Core abstractions
├── messages/                       ← HumanMessage, SystemMessage, AIMessage
├── prompts/                        ← ChatPromptTemplate, PromptTemplate
├── output_parsers/                 ← StrOutputParser, JsonOutputParser
├── tools/                          ← @tool decorator, BaseTool
└── runnables/                      ← The "chain" pattern (LCEL)

langchain_community/                ← Third-party integrations
├── vectorstores/                   ← Chroma, FAISS, Pinecone
├── embeddings/                     ← HuggingFaceEmbeddings, OpenAIEmbeddings
├── document_loaders/               ← PDFLoader, WebBaseLoader
└── tools/                          ← Wikipedia, DuckDuckGo, etc.

langchain_anthropic/                ← Anthropic-specific
└── chat_models/                    ← ChatAnthropic

langchain_text_splitters/           ← Document splitting
└── RecursiveCharacterTextSplitter, TokenTextSplitter
```

---

## Diagram 6: The .env Pattern (API Key Safety)

```
WITHOUT .env (DANGEROUS — key in code):
┌──────────────────────────────────────────────────────┐
│  api_key = "sk-ant-api03-..."  ← NEVER DO THIS       │
│                                   Key in git forever  │
└──────────────────────────────────────────────────────┘

WITH .env (SAFE — key separated from code):

.env file (in project root, NEVER commit):      your_script.py:
┌─────────────────────────────────┐             ┌────────────────────────────────────┐
│  ANTHROPIC_API_KEY=sk-ant-...   │             │  from dotenv import load_dotenv     │
│  OPENAI_API_KEY=sk-...          │             │  import os                          │
└─────────────────────────────────┘             │                                    │
         │                                      │  load_dotenv()  ← reads .env       │
         │ load_dotenv() reads this             │  key = os.getenv("ANTHROPIC_API_KEY")│
         └─────────────────────────────────────▶│                                    │
                                                │  client = Anthropic(api_key=key)   │
                                                └────────────────────────────────────┘

.gitignore file (blocks .env from git):
  .env
  *.env
  __pycache__/
```

---

## Diagram 7: What Type of Thing Gets Imported

```
IMPORT RESULT                  HOW YOU USE IT

Class:
  from langchain_anthropic     → llm = ChatAnthropic(model="...")
    import ChatAnthropic           └── create instance (L4 pattern!)

Function:
  from langchain.agents        → agent = create_react_agent(llm, tools, prompt)
    import create_react_agent      └── call directly (L3 pattern!)

Decorator:
  from langchain_core.tools    → @tool
    import tool                    def my_func(query: str) -> str:
                                       └── wraps the function

Constant / Object type:
  from langchain_core.messages → msg = HumanMessage(content="Hello")
    import HumanMessage            └── create instance (special class)

Module-level config call:
  import dspy                  → dspy.configure(lm=lm)
  dspy.LM(...)                     └── global setup (one-time)
```

---

## Diagram 8: Reading a Real Import Block in 10 Seconds

```python
# Step 1: Scan for the FRAMEWORK
import os                                      ← built-in (skip)
from dotenv import load_dotenv                 ← env vars (standard)
from langchain_anthropic import ChatAnthropic  ← LangChain + Claude
from langchain_community.vectorstores import Chroma  ← RAG component
from langchain_core.prompts import ChatPromptTemplate  ← prompts

# Step 2: What's being used?
# ChatAnthropic → the LLM
# Chroma        → the vector database
# ChatPromptTemplate → the prompt builder

# Step 3: Verdict:
# "This is a LangChain RAG project using Claude and Chroma."
# That's all you need to know from the import block.
```

---

## Diagram 9: ImportError — What Happened and How to Fix

```
ERROR:
  ModuleNotFoundError: No module named 'langchain_anthropic'

WHAT HAPPENED:
  Your code has: from langchain_anthropic import ChatAnthropic
  But:           pip install langchain-anthropic  ← was NEVER run

FIX:
  pip install langchain-anthropic
  (then re-run your script)

OTHER COMMON ERRORS:

  ImportError: cannot import name 'ChatAnthropic' from 'langchain'
  → Wrong package. Use: from langchain_anthropic import ChatAnthropic

  ModuleNotFoundError: No module named 'dotenv'
  → pip install python-dotenv  (note: pip name ≠ import name)

RULE:
  pip install name  ←  uses hyphens,  e.g.  langchain-anthropic
  import name       ←  uses underscore, e.g. langchain_anthropic
```

---

**Next:** See [PASS3_TEMPLATES.md](PASS3_TEMPLATES.md) for all available import template files.

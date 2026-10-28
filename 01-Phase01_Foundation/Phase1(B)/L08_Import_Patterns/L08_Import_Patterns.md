# Lesson 08: Import Patterns
## The Hardware Store Theory

> **Version note (checked 2026-10-28):** The LangChain agent code in this lesson is LangChain 0.x style (`from langchain.agents import AgentExecutor, create_react_agent`). You will still meet it in older repos. In LangChain 1.x those legacy pieces live in the separate `langchain-classic` package (`from langchain_classic.agents import AgentExecutor, create_react_agent`), and new code builds agents with `from langchain.agents import create_agent`. The loop you are learning to read is the same.

Architect, you've learned variables, lists, logic, loops, functions, and classes. Every example so far has been **self-contained**. But real AI code always starts with `import` statements — lines that pull in tools other people built.

Think of imports like a **hardware store**:
- Someone else built the hammer (LangChain, Anthropic SDK, DSPy)
- The store stocks it (PyPI — the Python package index)
- You order it (pip install)
- You bring it to your worksite (import)
- You use it (call functions, create classes)

You never have to **build** the hammer. You just need to know **which aisle to go to**.

---

## 1. The Import Syntax (3 Forms You'll Always See)

### Form 1: Import the whole store
```python
import anthropic
import os
import json
```
Use it: `anthropic.Anthropic()` — you prefix everything with the store name.

### Form 2: Import one specific tool
```python
from anthropic import Anthropic
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
```
Use it: `Anthropic()` — no prefix needed, you grabbed the specific tool.

### Form 3: Import with a nickname (alias)
```python
import numpy as np
import pandas as pd
from langchain_openai import ChatOpenAI as OpenAIChat
```
Use it: `np.array(...)` — shorter to type, same tool.

| Form | Pattern | When you see it |
|:-----|:--------|:----------------|
| `import X` | Whole library | `import anthropic`, `import os` |
| `from X import Y` | One specific piece | `from langchain import ChatAnthropic` |
| `import X as Y` | Library with alias | `import numpy as np` |
| `from X import Y as Z` | Piece with alias | `from langchain_core.messages import HumanMessage as HM` |

---

## 2. Where Imports Come From

```
PyPI (pypi.org)           ← The warehouse — 500,000+ packages
    │
    │ pip install langchain
    ▼
Your machine (site-packages)  ← Downloaded and stored locally
    │
    │ import langchain
    ▼
Your Python file          ← Now you can use it
```

**The chain:**
1. Someone writes a library (e.g., LangChain team)
2. They publish it to PyPI
3. You run `pip install langchain`
4. Python stores it in `site-packages/`
5. Your code runs `from langchain import X` → works!

If step 3 is missing → `ImportError: No module named 'langchain'`

---

## 3. Standard Import Blocks for AI Work

### Block A: Anthropic / Claude Direct
```python
import anthropic
from anthropic import Anthropic

# Usage:
client = Anthropic()                    # Uses ANTHROPIC_API_KEY env var
response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1000,
    messages=[{"role": "user", "content": "Hello"}]
)
```

### Block B: LangChain RAG
```python
from langchain_anthropic import ChatAnthropic
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
```

### Block C: LangChain Agents
```python
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import tool
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
```

### Block D: DSPy
```python
import dspy
from dspy import Signature, InputField, OutputField
from dspy.teleprompt import BootstrapFewShot
```

### Block E: Utilities (always useful)
```python
import os
from dotenv import load_dotenv      # Load API keys from .env file
import json                          # Parse/write JSON
from typing import List, Dict, Optional  # Type hints
```

---

## 4. How to Read an Import Line

When you see an import you don't recognize, decode it in three steps:

```python
from langchain_community.vectorstores import Chroma
     │                  │                │       │
     │                  │                │       └─ The specific class/function
     │                  │                └─ import keyword (grab this one thing)
     │                  └─ Sub-package (like a section in the store)
     └─ Top-level package (the "store" — pip install langchain-community)
```

**Translation:** "From the `langchain-community` package, inside the `vectorstores` section, grab the `Chroma` class."

Another example:
```python
from langchain_core.messages import HumanMessage, SystemMessage
```
"From `langchain-core`, inside `messages`, grab both `HumanMessage` and `SystemMessage`."

---

## 5. What Gets Imported (The 4 Types)

### Type 1: A Class (most common in AI)
```python
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-sonnet-5-5")   # Create an instance
```

### Type 2: A Function
```python
from langchain.agents import create_react_agent

agent = create_react_agent(llm, tools, prompt)   # Call it directly
```

### Type 3: A Decorator
```python
from langchain_core.tools import tool

@tool                                             # Used above a function
def my_search(query: str) -> str:
    return search_web(query)
```

### Type 4: A Constant or Config
```python
from langchain_core.messages import HumanMessage

msg = HumanMessage(content="What is RAG?")        # Creates a message object
```

---

## 6. How to Find What to Import

**Method 1: Error message tells you**
```
ImportError: cannot import name 'ChatAnthropic' from 'langchain'
```
→ Google "ChatAnthropic langchain import" → find correct package

**Method 2: Docs / README**
- Every library has an installation section
- LangChain docs show: `from langchain_anthropic import ChatAnthropic`

**Method 3: Copy from working examples**
- GitHub repos, tutorials, Stack Overflow
- Find an example that works, copy the import block

**Method 4: Ask Claude**
- "What is the correct import for ChatAnthropic in LangChain 0.3?"
- Always include the library version for accurate results

---

## 7. The `.env` Pattern — Keeping API Keys Safe

Almost all AI code uses this pattern:
```python
from dotenv import load_dotenv
import os

load_dotenv()   # Reads from .env file in your project folder

api_key = os.getenv("ANTHROPIC_API_KEY")
```

Your `.env` file (never commit this to git!):
```
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
```

**Why:** Never put API keys directly in code. `.env` keeps them separate.

---

## 8. Pattern Recognition Guide

**When you see:**
```python
from langchain_anthropic import ChatAnthropic
```
**Translation:** "LangChain's Anthropic wrapper — creates an LLM object."

**When you see:**
```python
import dspy
dspy.configure(lm=...)
```
**Translation:** "DSPy framework — the `configure` call sets up the global LLM."

**When you see:**
```python
from langchain_community.vectorstores import Chroma
db = Chroma(persist_directory="./chroma_db")
```
**Translation:** "Chroma is a local vector database — importing the class, then creating an instance."

**When you see:**
```python
from typing import List, Dict, Optional
```
**Translation:** "Type hint helpers — used to annotate function signatures. `Optional[str]` means 'str or None'."

---

## 9. Key Takeaways

✓ **`import X`** → bring in the whole library, use `X.thing`
✓ **`from X import Y`** → grab one specific thing, use `Y` directly
✓ **`import X as Y`** → give it a shorter nickname
✓ **Libraries live on PyPI**, installed with `pip install`, then imported
✓ **ImportError** = library not installed (run `pip install <name>`)
✓ **`.env` + `load_dotenv()`** = the standard pattern for API keys
✓ **You don't need to memorize imports** — copy from templates or docs

**Most common AI imports:**
- `anthropic` → direct Claude API
- `langchain_anthropic` → LangChain wrapper for Claude
- `langchain_community.vectorstores` → Chroma, FAISS, Pinecone
- `langchain_core.prompts` → prompt templates
- `dspy` → DSPy framework
- `dotenv` → loading `.env` files

---

## 10. Templates Available

See this lesson folder ([./](./)) for ready-to-use import blocks: `imports_for_anthropic.py`, `imports_for_agents.py`, `imports_for_dspy.py`, `imports_for_rag.py`.

**Your workflow:**
1. Identify what framework you're working with (Anthropic direct / LangChain / DSPy)
2. Open the matching import template
3. Copy the import block into your file
4. Install any missing packages: `pip install <package-name>`

---

**Remember:** You're not memorizing import paths. You're recognizing: "This is a LangChain RAG project — use the RAG import block." Templates handle the rest.

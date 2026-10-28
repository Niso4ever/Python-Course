# Pass 3: Templates Overview — Import Patterns
## Your Lesson 08 Template Library

All templates are in this lesson folder (`Phase1(B)/L08_Import_Patterns/`).
**Your workflow:** Identify your framework → open matching file → copy the import block → paste at top of your file.

---

## Template Files at a Glance

| File | Framework | What it includes |
|:-----|:----------|:-----------------|
| `imports_for_anthropic.py` | Direct Anthropic API | Claude client, streaming, env setup |
| `imports_for_rag.py` | LangChain RAG | Vector stores, embeddings, splitters, prompts |
| `imports_for_agents.py` | LangChain Agents + CrewAI | AgentExecutor, tools, multi-agent |
| `imports_for_dspy.py` | DSPy | Signatures, modules, optimizers |
| `CHEATSHEET_L08.py` | All | Quick lookup for any import |

---

## Template 1: Anthropic Direct

**File:** `imports_for_anthropic.py`
**Use when:** Calling Claude directly without a framework wrapper.

```python
# Minimum needed:
import anthropic
from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()
client = Anthropic()
```

**Variations included:**
1. Minimal setup (just call the API)
2. With streaming response
3. With conversation history
4. With tool use (function calling)

**pip install:** `pip install anthropic python-dotenv`

---

## Template 2: LangChain RAG

**File:** `imports_for_rag.py`
**Use when:** Building a retrieval-augmented generation pipeline.

```python
# Core RAG imports:
from langchain_anthropic import ChatAnthropic
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
```

**Variations included:**
1. Chroma (local) RAG stack
2. FAISS (in-memory) RAG stack
3. Document loading (PDF, web, text)
4. Full LCEL chain imports

**pip install:** `pip install langchain langchain-anthropic langchain-community langchain-text-splitters chromadb sentence-transformers`

---

## Template 3: LangChain Agents + CrewAI

**File:** `imports_for_agents.py`
**Use when:** Building agents that use tools, or multi-agent systems.

```python
# LangChain agents (1.x path; 0.x code wrote `from langchain.agents import ...`):
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_core.tools import tool
from langchain_anthropic import ChatAnthropic

# CrewAI multi-agent:
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool
```

**Variations included:**
1. Basic LangChain ReAct agent
2. LangChain agent with custom tools
3. CrewAI minimal setup
4. CrewAI with built-in tools

**pip install:** `pip install langchain langchain-anthropic crewai crewai-tools`

---

## Template 4: DSPy

**File:** `imports_for_dspy.py`
**Use when:** Using DSPy for declarative, optimizable AI programs.

```python
import dspy
from dspy import Signature, InputField, OutputField
from dspy.teleprompt import BootstrapFewShot, MIPROv2
from dspy.evaluate import Evaluate
```

**Variations included:**
1. Basic DSPy setup (configure + signature)
2. DSPy with optimizer (BootstrapFewShot)
3. DSPy with evaluation
4. DSPy with RAG module

**pip install:** `pip install dspy` (the old name `dspy-ai` is now only an alias)

---

## CHEATSHEET: All Imports Quick Reference

**File:** `CHEATSHEET_L08.py`
**Use:** Keep open for instant lookup. Covers every common import pattern.

Sections:
- All 3 import forms with examples
- Built-in modules (no pip needed)
- Third-party: pip name → import name mapping
- Per-framework import blocks
- `.env` pattern
- ImportError fix guide

---

## Quick Decision Guide

**Which template do I need?**

```
Am I calling Claude directly (no framework)?
  YES → imports_for_anthropic.py

Am I building a RAG system (search docs + generate)?
  YES → imports_for_rag.py

Am I building an agent that uses tools?
  YES → imports_for_agents.py

Am I using DSPy (declarative signatures)?
  YES → imports_for_dspy.py

Am I not sure what framework to use?
  → imports_for_anthropic.py (simplest, always works)
```

---

## Copy-Paste Workflow

**Step 1:** Open the matching template file
**Step 2:** Copy the import block for your use case
**Step 3:** Paste at the TOP of your Python file (before any other code)
**Step 4:** Run `pip install <packages>` for anything missing
**Step 5:** Create your `.env` file with API keys
**Step 6:** Call `load_dotenv()` at the start of your script

---

## pip → import Name Mapping (Quick Reference)

| pip install name | import name |
|:----------------|:------------|
| `anthropic` | `anthropic` |
| `langchain-anthropic` | `langchain_anthropic` |
| `langchain-community` | `langchain_community` |
| `langchain-core` | `langchain_core` |
| `langchain-text-splitters` | `langchain_text_splitters` |
| `python-dotenv` | `dotenv` |
| `chromadb` | `chromadb` |
| `dspy` (formerly `dspy-ai`) | `dspy` |
| `crewai` | `crewai` |
| `sentence-transformers` | `sentence_transformers` |

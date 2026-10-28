# Lesson 08 Templates: Import Patterns

Standard import blocks for every AI framework you'll encounter.

## Learning Materials
1. **PASS1_RECOGNITION.md** - Learn to read any import block in 3 seconds (START HERE)
2. **PASS_C_VISUAL.md** - See where imports come from and how they flow
3. **PASS3_TEMPLATES.md** - Overview of all import templates and when to use each

## Templates
4. **CHEATSHEET_L08.py** - All import patterns quick reference (KEEP OPEN!)
5. **imports_for_anthropic.py** - Direct Claude API (4 variations)
6. **imports_for_rag.py** - LangChain RAG stack (4 variations)
7. **imports_for_agents.py** - LangChain Agents + CrewAI (4 variations)
8. **imports_for_dspy.py** - DSPy framework (4 variations)

## Quick Selection

| Working with | File |
|:-------------|:-----|
| Claude directly (no framework) | imports_for_anthropic.py |
| RAG / vector search | imports_for_rag.py |
| Agents with tools | imports_for_agents.py |
| DSPy signatures | imports_for_dspy.py |
| Any import (quick lookup) | CHEATSHEET_L08.py |

## Learning Path

**Step 1:** Read `PASS1_RECOGNITION.md` (30 min) — 8 real import blocks
**Step 2:** Study `PASS_C_VISUAL.md` (15 min) — 9 diagrams
**Step 3:** Browse `PASS3_TEMPLATES.md` (10 min) — decision guide
**Step 4:** Run any template file to see the reference output

## 3-Second Import Block Read
1. **Framework?** → anthropic / langchain / dspy / crewai
2. **What's imported?** → LLM class, vector store, tools?
3. **Verdict** → "This is a LangChain RAG project with Chroma and Claude"

## The Key Rule
```
pip install name  → uses hyphens:     langchain-anthropic
import name       → uses underscores: langchain_anthropic

ImportError = library not installed → pip install <name>
```

# Phase 3: Tool Use & Function Calling - Index
> **Quick Navigation for All Resources**

---

## 🚀 START HERE

**New to Phase 3?** → [QUICKSTART.md](QUICKSTART.md) (15 min)

**Need a quick reference?** → [CHEATSHEET.md](CHEATSHEET.md) (1-page)

**Want the overview?** → [README.md](README.md) (10 min read)

**Need to understand what you built?** → [SUMMARY.md](SUMMARY.md)

---

## 📚 LESSONS (In Order)

### L01: Type Hints & Docstrings for LLMs
**Time:** 1-2 hours | **Difficulty:** Beginner

**What you'll learn:** How to write functions that LLMs can understand

**Files:**
- [📖 README.md](L01_TypeHints_Docstrings/README.md) - Complete guide
- [👁️ VISUAL_LLM_PERSPECTIVE.md](L01_TypeHints_Docstrings/VISUAL_LLM_PERSPECTIVE.md) - How LLMs "see" your code
- [📝 template_search_tools.py](L01_TypeHints_Docstrings/template_search_tools.py) - 7 ready-to-use search patterns

**Key takeaway:** Type hints + docstrings = LLM-readable functions

---

### L02: Pydantic Fundamentals
**Time:** 2-3 hours | **Difficulty:** Beginner-Intermediate

**What you'll learn:** Data validation and automatic schema generation

**Files:**
- [📖 README.md](L02_Pydantic_Fundamentals/README.md) - Complete Pydantic guide
- [📝 template_agent_schemas.py](L02_Pydantic_Fundamentals/template_agent_schemas.py) - 8 production schemas

**Key takeaway:** Pydantic validates inputs + generates LLM schemas automatically

---

### L03: Function Calling Patterns
**Time:** 1-2 hours | **Difficulty:** Intermediate

**What you'll learn:** How real frameworks use your tools in production

**Files:**
- [📖 README.md](L03_Function_Calling_Patterns/README.md) - Complete function calling guide

**Key takeaway:** The ReAct pattern (Reason → Act → Observe) is everywhere

---

### L04: Advanced Tool Schemas
**Time:** 2-3 hours | **Difficulty:** Advanced

**What you'll learn:** Production patterns, framework interoperability, optimization

**Files:**
- [📖 README.md](L04_Tool_Schemas/README.md) - Complete advanced guide
- [📝 template_production_rag_tools.py](L04_Tool_Schemas/template_production_rag_tools.py) - Production RAG system
- [📝 template_framework_adapters.py](L04_Tool_Schemas/template_framework_adapters.py) - Framework adapters
- [⚡ CHEATSHEET_L04.md](L04_Tool_Schemas/CHEATSHEET_L04.md) - Quick reference

**Key takeaway:** Framework-agnostic tools, edge cases, optimization for scale

---

## 🎯 BY USE CASE

### "I need to build a search tool"
1. Copy [template_search_tools.py](L01_TypeHints_Docstrings/template_search_tools.py)
2. Modify for your use case
3. Done

### "I need schemas for my agent"
1. Copy [template_agent_schemas.py](L02_Pydantic_Fundamentals/template_agent_schemas.py)
2. Pick the pattern you need (search, LLM response, agent config, etc.)
3. Customize
4. Done

### "I need to understand how LangChain tools work"
1. Read [L03 README](L03_Function_Calling_Patterns/README.md)
2. See "Pattern 6: LangChain Tool Pattern"
3. Done

### "I need to integrate with OpenAI/Anthropic"
1. Read [QUICKSTART.md](QUICKSTART.md)
2. Jump to "Step 4: Register With Your Framework"
3. Copy the code for your framework
4. Done

### "My agent isn't calling my tool correctly"
1. Check [CHEATSHEET.md](CHEATSHEET.md) → "Debugging Checklist"
2. Read [VISUAL_LLM_PERSPECTIVE.md](L01_TypeHints_Docstrings/VISUAL_LLM_PERSPECTIVE.md)
3. Fix the schema/docstring
4. Done

---

## 📋 BY SKILL LEVEL

### Beginner (New to AI Agents)
**Path:**
1. [README.md](README.md) - Understand the problem
2. [QUICKSTART.md](QUICKSTART.md) - 5-minute version
3. [L01 README](L01_TypeHints_Docstrings/README.md) - Learn type hints
4. [VISUAL_LLM_PERSPECTIVE.md](L01_TypeHints_Docstrings/VISUAL_LLM_PERSPECTIVE.md) - See what LLMs see
5. Practice: Copy a template and modify it

**Time investment:** 2-3 hours

---

### Intermediate (Know Python, New to Agent Tools)
**Path:**
1. [QUICKSTART.md](QUICKSTART.md) - 15-minute deep dive
2. [L02 README](L02_Pydantic_Fundamentals/README.md) - Learn Pydantic
3. [template_agent_schemas.py](L02_Pydantic_Fundamentals/template_agent_schemas.py) - Copy production patterns
4. [L03 README](L03_Function_Calling_Patterns/README.md) - See how frameworks integrate

**Time investment:** 3-4 hours

---

### Advanced (Building Agents Now)
**Path:**
1. [CHEATSHEET.md](CHEATSHEET.md) - Quick reference (5 min)
2. [template_agent_schemas.py](L02_Pydantic_Fundamentals/template_agent_schemas.py) - Grab what you need
3. [QUICKSTART.md](QUICKSTART.md) → "Step 4" - Integration code
4. Ship it

**Time investment:** 30 minutes

---

## 🔍 BY TOPIC

### Type Hints
- [L01 README](L01_TypeHints_Docstrings/README.md) → "Common Type Hints for Agent Tools"
- [CHEATSHEET.md](CHEATSHEET.md) → "Type Hints Quick Reference"

### Docstrings
- [L01 README](L01_TypeHints_Docstrings/README.md) → "The Docstring Formats"
- [CHEATSHEET.md](CHEATSHEET.md) → "Docstring Template"

### Pydantic
- [L02 README](L02_Pydantic_Fundamentals/README.md) - Full guide
- [CHEATSHEET.md](CHEATSHEET.md) → "Pydantic Quick Methods"
- [template_agent_schemas.py](L02_Pydantic_Fundamentals/template_agent_schemas.py) - Examples

### Validation
- [L02 README](L02_Pydantic_Fundamentals/README.md) → "Validation & Error Handling"
- [CHEATSHEET.md](CHEATSHEET.md) → "Validation Constraints"

### Error Handling
- [L03 README](L03_Function_Calling_Patterns/README.md) → "Pattern 5: Tool Error Handling"
- [CHEATSHEET.md](CHEATSHEET.md) → "Error Handling Wrapper"

### Framework Integration
- [QUICKSTART.md](QUICKSTART.md) → "Step 4: Register With Your Framework"
- [L03 README](L03_Function_Calling_Patterns/README.md) → All patterns
- [CHEATSHEET.md](CHEATSHEET.md) → "Framework Integration"

### ReAct Pattern
- [L03 README](L03_Function_Calling_Patterns/README.md) → "The ReAct Pattern"
- [CHEATSHEET.md](CHEATSHEET.md) → "The ReAct Agent Loop"

---

## 📦 TEMPLATES

### Search Tools
**File:** [template_search_tools.py](L01_TypeHints_Docstrings/template_search_tools.py)

**Includes:**
1. Simple Vector Search
2. Multi-Source Search
3. Filtered Search
4. Hybrid Search (semantic + keyword)
5. Re-ranking Search
6. Conversational Search
7. Similarity Search

---

### Agent Schemas
**File:** [template_agent_schemas.py](L02_Pydantic_Fundamentals/template_agent_schemas.py)

**Includes:**
1. Search Tool Input/Output
2. LLM Response with Citations
3. Agent Configuration
4. Multi-Tool Action Schema
5. Conversation/Message Schemas
6. RAG Document Schema
7. Evaluation Metrics
8. Error Handling Schema

---

## 🎓 LEARNING PATHS

### Path 1: Fast Track (4 hours)
For those who need to ship an agent this week.

**Day 1 (2 hours):**
- Read [QUICKSTART.md](QUICKSTART.md) (30 min)
- Complete the 30-min workshop
- Skim [CHEATSHEET.md](CHEATSHEET.md) (15 min)
- Read [L01 README](L01_TypeHints_Docstrings/README.md) (45 min)

**Day 2 (2 hours):**
- Read [L02 README](L02_Pydantic_Fundamentals/README.md) (1 hour)
- Copy and customize a template (30 min)
- Integrate with your framework (30 min)

**Output:** Production-ready tool

---

### Path 2: Deep Understanding (8-10 hours)
For those building a foundation.

**Week 1:**
- [README.md](README.md) - The why
- [QUICKSTART.md](QUICKSTART.md) - The how
- [L01 README](L01_TypeHints_Docstrings/README.md) + [VISUAL_LLM_PERSPECTIVE.md](L01_TypeHints_Docstrings/VISUAL_LLM_PERSPECTIVE.md)
- Practice exercises

**Week 2:**
- [L02 README](L02_Pydantic_Fundamentals/README.md)
- Build 2-3 tools from scratch
- Study [template_agent_schemas.py](L02_Pydantic_Fundamentals/template_agent_schemas.py)

**Week 3:**
- [L03 README](L03_Function_Calling_Patterns/README.md)
- Build a complete mini agent
- Integrate with real framework

**Output:** Mastery + portfolio projects

---

### Path 3: Reference Use (ongoing)
For experienced developers who need quick answers.

**Keep open while coding:**
- [CHEATSHEET.md](CHEATSHEET.md)

**Refer to when stuck:**
- [QUICKSTART.md](QUICKSTART.md) → Troubleshooting
- [VISUAL_LLM_PERSPECTIVE.md](L01_TypeHints_Docstrings/VISUAL_LLM_PERSPECTIVE.md) → Debugging

**Copy from:**
- [template_search_tools.py](L01_TypeHints_Docstrings/template_search_tools.py)
- [template_agent_schemas.py](L02_Pydantic_Fundamentals/template_agent_schemas.py)

---

## 🔗 QUICK LINKS

| Need | Go To |
|------|-------|
| Quick start | [QUICKSTART.md](QUICKSTART.md) |
| One-page reference | [CHEATSHEET.md](CHEATSHEET.md) |
| Full overview | [README.md](README.md) |
| What's inside | [SUMMARY.md](SUMMARY.md) |
| Type hints guide | [L01 README](L01_TypeHints_Docstrings/README.md) |
| How LLMs see code | [VISUAL_LLM_PERSPECTIVE.md](L01_TypeHints_Docstrings/VISUAL_LLM_PERSPECTIVE.md) |
| Pydantic guide | [L02 README](L02_Pydantic_Fundamentals/README.md) |
| Function calling | [L03 README](L03_Function_Calling_Patterns/README.md) |
| Search templates | [template_search_tools.py](L01_TypeHints_Docstrings/template_search_tools.py) |
| Agent schemas | [template_agent_schemas.py](L02_Pydantic_Fundamentals/template_agent_schemas.py) |

---

## 📊 CURRICULUM STATS

- **Lessons:** 4 complete (L01-L04)
- **Templates:** 20+ production-ready patterns
- **Time to complete:** 6-12 hours (depending on path)
- **Frameworks covered:** OpenAI, Anthropic, LangChain, CrewAI, AutoGen
- **Files:** 15 core documents + templates
- **Lines of code:** ~2500+ in templates (all copy-paste ready)

---

## ✅ COMPLETION CHECKLIST

You've completed Phase 3 when you can:

- [ ] Write a function with proper type hints and docstrings
- [ ] Create a Pydantic model with Field descriptions
- [ ] Generate JSON schema from a Pydantic model
- [ ] Explain what information LLMs see from your function
- [ ] Integrate a tool with OpenAI or Anthropic
- [ ] Handle validation errors gracefully
- [ ] Debug why an LLM isn't calling your tool correctly
- [ ] Build a complete tool in < 30 minutes

---

**Note:** This is a living curriculum. As frameworks evolve, templates will be updated. The core principles (type hints, docstrings, Pydantic validation) are framework-agnostic and future-proof.

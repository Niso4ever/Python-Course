# AI Architect's Template Library
## Copy-Paste-Modify Patterns for Agentic AI

**Purpose:** This folder contains **production-ready templates** with extensive comments explaining every line. These are NOT exercises — they're reference implementations you can use immediately.

---

## How to Use These Templates

### **The Anti-Learning Approach (This Is Good!)**
1. **Don't memorize** — just copy when you need it
2. **Read the comments** — they explain what each line does
3. **Modify values** — change thresholds, names, logic
4. **Let AI adapt** — paste template + ask Claude to customize

### **When AI Generates Code:**
1. Compare AI output to these templates
2. Check if AI followed the same pattern
3. If not, ask: "Rewrite using the pattern from [template name]"

---

## Template Index

This folder holds three files (checked 2026-10-28). The other templates live in their lesson folders under `../Phase1(A)/` and `../Phase1(B)/`; the paths below are relative to `01-Phase01_Foundation/`.

### **In this folder**
- `template_metadata_storage.py` - Dictionary patterns for AI metadata
- `template_rag_pipeline.py` - Complete retrieve → filter → generate flow (the Path B source file)
- `template_rag_pipeline_clone.py` - A byte-for-byte copy of `template_rag_pipeline.py`
- `explanations/` - plain-text blueprints of the three files

### **Data Structures (L01–L02)**
- `Phase1(A)/L01_Labels_and_Types/template_document_metadata.py` - Storing and accessing RAG retrieval results
- `Phase1(A)/L02_Lists_and_Collections/template_conversation_history.py` - List-based conversation tracking

### **Control Flow (L03–L04)**
- `Phase1(A)/L03_Logic_Gates/template_confidence_threshold.py` and `template_safety_guards.py` - Guard rails for AI outputs
- `Phase1(A)/L04_Loops_and_Iteration/template_filter_collection.py` - Filter search results by score/metadata

### **Functions & Classes (L05–L06)**
- `Phase1(A)/L05_Functions_as_Tools/template_llm_caller.py` - Reusable LLM call function
- `Phase1(A)/L06_Classes_as_Blueprints/template_conversation_agent.py` - Stateful multi-turn agent class
- `Phase1(A)/L06_Classes_as_Blueprints/template_rag_agent.py` - RAG system wrapped in a class
- `Phase1(A)/L06_Classes_as_Blueprints/template_multi_tool_agent.py` - Agent that selects and calls tools

---

## Quick Reference: Pattern → Template Mapping

| When you need... | Use this template |
|:-----------------|:------------------|
| Store LLM response metadata | `Templates/template_metadata_storage.py` |
| Track multi-turn conversation | `L02 template_conversation_history.py` |
| Filter vector search results | `L04 template_filter_collection.py` |
| Apply confidence thresholds | `L03 template_confidence_threshold.py` |
| Wrap LLM API calls | `L05 template_llm_caller.py` |
| Build RAG system | `Templates/template_rag_pipeline.py` |
| Create stateful agent | `L06 template_conversation_agent.py` |

---

## Philosophy: Templates Are Scaffolding, Not Training Wheels

**Traditional Learning:**
"Do 100 exercises until you memorize how to write this from scratch"

**AI Architect Learning:**
"Read this template once, recognize the pattern, modify when needed"

You're not copying because you're lazy — you're copying because **your time is better spent on architecture than syntax**.

---

> **Remember:** The best architects don't memorize building codes. They reference them when needed. These templates are your building codes.

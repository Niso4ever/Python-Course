# Lesson 16 Templates: Memory Stack Architecture

Every AI conversation is a goldfish. Memory systems give it an elephant's memory.

## Learning Materials
The lesson file covers all 4 memory layers with deep explanations and code examples.

## Templates
1. **PASS1_RECOGNITION.md** - 8 real memory patterns to recognize from production code
2. **PASS_C_VISUAL.md** - Visual diagrams: memory stack, sliding window, RAG pipeline, LangChain memory classes
3. **CHEATSHEET_L14.py** - Memory pattern reference (keep open while reading code)
4. **template_memory_agent.py** - 4 runnable memory agents: Full History, Sliding Window, Summarization, Persistent (no API needed for demo)

## The Memory Mental Model
```
Layer 4: Episodic  ← Database, files, user profiles (across sessions)
Layer 3: Semantic  ← Vector DB / RAG (knowledge base)
Layer 2: Working   ← Message history (current session)
Layer 1: Context   ← What LLM sees RIGHT NOW (the messages list)
```

## The Key Insight
**All memory = putting the right information into the context window.**
Vector DB, summarization, sliding window — they all just decide what goes in the messages list.

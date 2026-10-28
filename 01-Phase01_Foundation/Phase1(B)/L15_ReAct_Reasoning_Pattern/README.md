# Lesson 17 Templates: ReAct Reasoning Pattern

The detective thinks before acting. Reason → Act → Observe → repeat until done.

## Learning Materials
The lesson file covers the full ReAct loop with examples, LangChain shortcuts, and CoT comparison.

## Templates
1. **PASS1_RECOGNITION.md** - 8 ReAct patterns from real production code
2. **PASS_C_VISUAL.md** - Visual diagrams: T/A/O loop, LangChain ReAct, CoT vs ReAct
3. **CHEATSHEET_L15.py** - Quick reference for all ReAct signals
4. **template_react_patterns.py** - 3 patterns: manual ReAct loop, LangChain ReAct agent, Chain of Thought

## The ReAct Mental Model
```
Thought: "What do I need? Which tool handles it?"
Action:  call_tool(args)
Observe: tool result comes back
→ loop until Thought says "I have the answer"
→ Final Answer
```

## The Key Insight
**Thought is not optional.** Without reasoning before acting, agents loop randomly and miss when they already have the answer.

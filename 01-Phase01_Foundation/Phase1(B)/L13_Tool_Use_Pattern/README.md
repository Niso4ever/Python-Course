# Lesson 17 Templates: Tool Use Pattern

Build agents that call real functions — the bridge from chatbot to agent.

## Learning Materials
The lesson file covers the complete tool use loop with deep insights.

## Templates
1. **template_tool_definition.py** - 6 production-quality tool definitions with excellent descriptions: web_search, calculator, document_reader, RAG_search, code_executor, send_notification (runnable!)
2. **template_tool_executor.py** - 2 patterns: basic tool loop + ToolAgent class with history (runnable!)
3. **CHEATSHEET_L13.py** - Tool skeleton, stop_reason meanings, description quality guide, common mistakes

## The Tool Use Mental Model
```
USER asks question
       ↓
LLM reasons: "do I need a tool?"
       ↓ yes
LLM says: "call web_search('query')"   ← stop_reason = "tool_use"
       ↓
YOUR CODE runs: web_search("query")
       ↓
Result sent back to LLM
       ↓
LLM reasons again with new information
       ↓
LLM gives final answer                 ← stop_reason = "end_turn"
```

## The Key Insight
**Tool description quality = tool selection accuracy.**
Write descriptions that include: what it does + when to use it + when NOT to use it.

# Lesson 16 Templates: Advanced Debugging

Debug silent failures, performance bugs, and intermittent issues in AI projects.

## Learning Materials
The lesson file covers 4 bug categories with detailed examples.

## Templates
1. **template_debug_toolkit.py** - 6 drop-in debug tools: inspect(), audit_rag_call(), @timed, TokenBudget, with_retry(), safe_json() (runnable!)
2. **CHEATSHEET_L12.py** - Quick debug patterns, LangChain switches, stage isolation guide

## The 4 Bug Categories
```
1. Hard Errors      → traceback appears → use error_decoder.md (L7)
2. Silent Failures  → runs but wrong output → print audit every stage
3. Intermittent     → fails sometimes → retry + rate limit handling
4. Performance      → too slow/expensive → TokenBudget + @timed
```

## The Debug Reflex
```
Problem → Add prints at EVERY stage → find which stage produces wrong output
→ Focus fix on that stage → remove prints when fixed
```

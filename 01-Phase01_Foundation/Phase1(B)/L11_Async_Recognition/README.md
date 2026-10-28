# Lesson 17 Templates: Async Recognition

Recognize and understand async/await patterns in AI code.

## Learning Materials
1. **PASS1_RECOGNITION.md** - 8 async scenarios: parallel calls, streaming, batch, FastAPI, DSPy
2. **CHEATSHEET_L11.py** - 5 keywords, patterns, common mistakes, performance math

## Templates
3. **template_async_patterns.py** - 4 patterns: parallel models, batch processing, streaming, retry (runnable!)

## The Mental Model
```
Sync:  Cook one dish completely before starting the next.
Async: Start all dishes at once, check each as it's ready.

asyncio.gather(*tasks) = "Start all dishes at once"
await single_call()    = "Wait for this dish, continue when done"
```

## Key Rules
- `async def` + `await` always go together
- `asyncio.run()` called ONCE at the top level
- Use `AsyncAnthropic()` not `Anthropic()` in async code
- Use `await asyncio.sleep()` not `time.sleep()` in async code
- LangChain async = add `a` prefix: `.invoke()` → `.ainvoke()`

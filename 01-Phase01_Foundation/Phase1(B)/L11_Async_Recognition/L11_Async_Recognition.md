# Lesson 11: Async Recognition
## The Restaurant Kitchen Theory

Imagine two kitchen styles:

**Synchronous (normal Python):** One chef. Takes an order, cooks it completely, serves it, takes the next order. While the pasta boils (3 minutes), the chef stands there waiting. Nothing else happens.

**Asynchronous (async Python):** One chef. Takes order 1, puts pasta on to boil, while it boils → takes order 2, starts sauce, checks pasta, finishes order 1, plates both. The *waiting time* is used productively.

In AI systems, the "pasta boiling" is **API calls** — waiting for Claude to respond. A synchronous app freezes while waiting. An async app handles other requests simultaneously.

---

## 1. The 5 Keywords You'll See

```python
async def   → "This function can pause and resume"
await       → "Pause HERE and wait for this result"
asyncio     → The Python module that manages all async work
asyncio.gather()  → "Run all these at the same time"
asyncio.run()     → "Start the async engine"
```

That's it. You only need to recognize these 5.

---

## 2. What Async Looks Like in AI Code

### Pattern A: Async LLM Call
```python
import asyncio
import anthropic

client = anthropic.AsyncAnthropic()   # ← "Async" in the class name = async client

async def get_answer(question: str) -> str:
    response = await client.messages.create(   # ← await = pause while API responds
        model="claude-sonnet-5-5",
        max_tokens=1000,
        messages=[{"role": "user", "content": question}]
    )
    return response.content[0].text

# Run it:
answer = asyncio.run(get_answer("What is RAG?"))   # ← entry point for async code
```

**What to notice:**
- `AsyncAnthropic` vs `Anthropic` — the async version of the client
- `async def` + `await` always appear together
- `asyncio.run()` is the starting gun — you call this ONCE at the top level

---

### Pattern B: Parallel LLM Calls (The Power Move)
```python
import asyncio
import anthropic

client = anthropic.AsyncAnthropic()

async def call_llm(prompt: str, model: str) -> str:
    response = await client.messages.create(
        model=model,
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

async def compare_models(question: str):
    # Run ALL three calls at the SAME TIME — not one after another
    results = await asyncio.gather(
        call_llm(question, "claude-haiku-5-5"),   # starts immediately
        call_llm(question, "claude-sonnet-5-5"),            # starts immediately
        call_llm(question, "claude-opus-5-5"),              # starts immediately
    )
    # All three finish roughly at the same time
    # Results list preserves the order: [haiku_result, sonnet_result, opus_result]
    return results

answers = asyncio.run(compare_models("Explain RAG in one sentence."))
```

**The insight:** Without async, three API calls take `3 × 2 seconds = 6 seconds`. With `asyncio.gather()`, they take `≈ 2 seconds` — the time of ONE call. This is why real production systems use async.

---

### Pattern C: Async in LangChain
```python
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage

llm = ChatAnthropic(model="claude-sonnet-5-5")

# LangChain methods have async versions — just add 'a' prefix:
# sync:  llm.invoke(messages)
# async: await llm.ainvoke(messages)

async def rag_pipeline(questions: list[str]):
    # Process all questions in parallel
    tasks = [
        llm.ainvoke([HumanMessage(content=q)])  # ← .ainvoke not .invoke
        for q in questions
    ]
    results = await asyncio.gather(*tasks)   # ← * unpacks the list
    return [r.content for r in results]

answers = asyncio.run(rag_pipeline(["What is RAG?", "What is DSPy?", "What is CrewAI?"]))
```

**The `a` prefix pattern in LangChain:**
- `.invoke()` → `.ainvoke()` (async invoke)
- `.stream()` → `.astream()` (async stream)
- `.batch()` → `.abatch()` (async batch)

---

### Pattern D: Streaming Responses
```python
import anthropic
import asyncio

client = anthropic.AsyncAnthropic()

async def stream_response(prompt: str):
    # stream=True makes tokens appear as they're generated
    async with client.messages.stream(
        model="claude-sonnet-5-5",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        async for text in stream.text_stream:   # ← async for = streaming loop
            print(text, end="", flush=True)     # prints each token as it arrives

asyncio.run(stream_response("Tell me about RAG in 3 sentences."))
```

**When you see `async for`:** It's an async loop — waiting for the next item instead of blocking.
**When you see `async with`:** It's an async context manager — usually for streaming or database connections.

---

## 3. Sync vs Async — The Visual

```
SYNCHRONOUS (normal):
─────────────────────────────────────────────────
Time →   0s      2s      4s      6s
         │       │       │       │
Call 1:  ████████│        (waiting)
Call 2:          ████████│        (waiting)
Call 3:                  ████████│
                                 ↑
                              6 seconds total

ASYNCHRONOUS (with asyncio.gather):
─────────────────────────────────────────────────
Time →   0s      2s
         │       │
Call 1:  ████████│  → done
Call 2:  ████████│  → done  (all run AT THE SAME TIME)
Call 3:  ████████│  → done
                 ↑
              2 seconds total ← 3x faster
```

---

## 4. Recognition Patterns — Read, Don't Write

**When you see `async def` in a function:**
→ "This function is designed to run concurrently. Call it with `await` or `asyncio.gather()`."

**When you see `await` before a call:**
→ "Pause here until this API call/operation completes."

**When you see `asyncio.gather(...)`:**
→ "Run all these operations in parallel — the power move."

**When you see `.ainvoke()` or `.astream()`:**
→ "This is the async version of a LangChain/LLM call."

**When you see `asyncio.run(main())`:**
→ "This is the entry point — starts the async engine."

**When you see `async for`:**
→ "This is streaming — processing items as they arrive."

---

## 5. The Mental Model — You DON'T Need to Write This

Your role as AI Architect is to **recognize** async code and understand what it's doing:

| You see | You understand |
|:--------|:---------------|
| `async def process_batch(questions)` | "This processes questions concurrently" |
| `await llm.ainvoke(messages)` | "Wait for LLM response, then continue" |
| `asyncio.gather(*tasks)` | "All tasks run in parallel" |
| `async for token in stream:` | "Process each token as it streams in" |
| `asyncio.run(main())` | "Start the async program" |

When AI generates async code for you, you can evaluate:
- Is `gather()` being used where parallel calls would help?
- Are all `await`s present? (Missing `await` is a common bug)
- Is `asyncio.run()` called exactly once at the top level?

---

## 6. Key Takeaways

✓ **`async def`** = function that can pause and resume
✓ **`await`** = "pause here until this finishes"
✓ **`asyncio.gather()`** = run multiple things in parallel — the speed multiplier
✓ **`asyncio.run()`** = the starting gun — called once
✓ **`.ainvoke()`, `.astream()`** = async versions of LangChain methods (the `a` prefix)
✓ **`async for`** = streaming loop
✓ You will **read** async code constantly in AI projects — you won't write it from scratch
✓ The performance benefit: N API calls take the time of 1 call, not N calls

**Phase 1B Insight:** Any production AI system that makes multiple LLM calls uses async. If you see async in code you're reviewing, it's handling performance at scale — that's good architecture, not complexity for its own sake.

---

## Templates Available

See this lesson folder ([./](./)) for:
- `CHEATSHEET_L11.py` — async patterns quick reference
- `template_async_patterns.py` — 4 async patterns (parallel calls, streaming, batch, retry)

For parallel agent calls, see Phase 6: `06-Phase06_Async/L01_Async_Patterns/template_parallel_agents.py`.

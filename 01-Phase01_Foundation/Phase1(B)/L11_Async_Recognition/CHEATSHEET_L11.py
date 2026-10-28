"""
═══════════════════════════════════════════════════════════════════
LESSON 9 CHEATSHEET: Async Recognition
═══════════════════════════════════════════════════════════════════
Recognize and understand async patterns in AI code.
═══════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════
# 1. THE 5 KEYWORDS
# ═══════════════════════════════════════════════════════════
"""
async def    → function can pause/resume (must be awaited or gathered)
await        → pause here until this operation finishes
asyncio      → the module managing all async work
asyncio.gather()   → run multiple coroutines SIMULTANEOUSLY
asyncio.run()      → start the async engine (called ONCE at top level)
"""

# ═══════════════════════════════════════════════════════════
# 2. THE MINIMAL ASYNC PATTERN
# ═══════════════════════════════════════════════════════════
import asyncio

async def main():
    # All async work goes inside an async def
    result = await some_async_function()
    return result

# Only ONE asyncio.run() per program:
# asyncio.run(main())

# ═══════════════════════════════════════════════════════════
# 3. PARALLEL CALLS — THE CORE PATTERN
# ═══════════════════════════════════════════════════════════
async def parallel_example(items):
    tasks   = [async_function(item) for item in items]  # list of coroutines
    results = await asyncio.gather(*tasks)               # run all at once
    return list(results)                                 # results in same order

# With error tolerance (return_exceptions=True catches errors per task):
async def safe_parallel(items):
    tasks   = [async_function(item) for item in items]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    # Filter out errors:
    good = [r for r in results if not isinstance(r, Exception)]
    return good

# ═══════════════════════════════════════════════════════════
# 4. LANGCHAIN ASYNC — THE 'a' PREFIX
# ═══════════════════════════════════════════════════════════
"""
SYNC              ASYNC
──────────────    ──────────────────
.invoke()     →   .ainvoke()
.stream()     →   .astream()
.batch()      →   .abatch()

Example:
  sync:   response = llm.invoke(messages)
  async:  response = await llm.ainvoke(messages)
"""

# ═══════════════════════════════════════════════════════════
# 5. STREAMING PATTERN
# ═══════════════════════════════════════════════════════════
"""
async with client.messages.stream(...) as stream:
    async for chunk in stream.text_stream:
        print(chunk, end="", flush=True)

KEY WORDS:
  async with  → async context manager (keeps connection open)
  async for   → async loop (waits for next chunk)
"""

# ═══════════════════════════════════════════════════════════
# 6. COMMON MISTAKES TO SPOT
# ═══════════════════════════════════════════════════════════
"""
MISTAKE 1: Missing await
  response = client.messages.create(...)   ← returns a coroutine, not a response!
  FIX: response = await client.messages.create(...)

MISTAKE 2: time.sleep() in async code
  time.sleep(2)           ← blocks EVERYTHING, other tasks freeze
  FIX: await asyncio.sleep(2)  ← non-blocking sleep

MISTAKE 3: asyncio.run() inside async function
  async def main():
      asyncio.run(other_func())   ← error! can't nest run()
  FIX: result = await other_func()

MISTAKE 4: Forgetting AsyncAnthropic
  client = anthropic.Anthropic()   ← sync client, won't work in async
  FIX: client = anthropic.AsyncAnthropic()
"""

# ═══════════════════════════════════════════════════════════
# 7. PERFORMANCE MATH
# ═══════════════════════════════════════════════════════════
"""
Scenario: 10 documents, each takes 2 seconds to summarize

SYNC (sequential):
  10 × 2s = 20 seconds total

ASYNC (parallel with gather):
  ~2 seconds total (limited by slowest call)

ASYNC (batches of 5, 1s pause):
  batch1: ~2s + 1s pause
  batch2: ~2s
  = ~5 seconds total

RULE: Use gather() when you have 2+ independent LLM calls.
"""

# ═══════════════════════════════════════════════════════════
# 8. RECOGNITION QUICK TABLE
# ═══════════════════════════════════════════════════════════
"""
You see                          You understand
────────────────────────────     ────────────────────────────────────
async def process(items)         This handles multiple items concurrently
await llm.ainvoke(messages)      Async LLM call — needs async def around it
asyncio.gather(*tasks)           All tasks run simultaneously
asyncio.run(main())              Entry point — starts the async engine
async for chunk in stream        Streaming — tokens arrive one by one
AsyncAnthropic()                 Async version of the Anthropic client
await asyncio.sleep(n)           Non-blocking pause (rate limit handling)
asyncio.to_thread(sync_func)     Wraps sync code to work in async context
"""

print("Async cheatsheet loaded! Key rule: await = pause without blocking.")

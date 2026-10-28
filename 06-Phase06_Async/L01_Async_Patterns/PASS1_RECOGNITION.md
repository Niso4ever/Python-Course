# L01 — Pass 1: RECOGNITION
## How to Spot Async Patterns in Real Agent Code

**Goal:** After this pass, you can look at any async agent code and instantly identify: What runs concurrently? What blocks? Where are the bottlenecks?

---

## Pattern 1: The `async def` + `await` Shape

This is the atomic unit. Every async pattern is built from this.

```python
# SHAPE: async function that awaits something
async def run_agent(prompt: str) -> str:
    response = await client.chat(prompt)  # ← pauses HERE, lets others run
    return response.text
```

**What to recognize:**
- `async def` = "this function can pause and resume"
- `await` = "pause here, let other things run while I wait"
- Without `await`, the function runs like normal — no concurrency

**☕ Coffee Machine:** `async def` is like putting your order in. `await` is stepping aside so the next person can order while your coffee brews.

---

## Pattern 2: `asyncio.gather()` — The Parallel Launcher

This is the #1 pattern in production agent code. You'll see it everywhere.

```python
# SHAPE: Multiple coroutines launched together
results = await asyncio.gather(
    research_agent(query),      # starts immediately
    writing_agent(query),       # starts immediately (doesn't wait for research)
    review_agent(query),        # starts immediately
)
# results = [research_result, writing_result, review_result]
```

**What to recognize:**
- `asyncio.gather(coro1, coro2, coro3)` = "run all three at once, give me all results when ALL finish"
- The results come back in the SAME ORDER as the arguments — not in completion order
- If one fails, the first error is raised straight away to whoever awaited `gather` — but the other coroutines are **not** cancelled; they keep running and their results are lost to you. Add `return_exceptions=True` to get errors back in the results list instead. (`asyncio.TaskGroup`, Python 3.11+, is the stricter alternative: one failure cancels the rest.)

**Real-world example from CLBench:**
```python
# The benchmark runner evaluates baseline instances in parallel
# Each worker runs one instance independently
baseline_results = await asyncio.gather(
    *[run_baseline_instance(task, system, i) for i in instance_indices]
)
```

---

## Pattern 3: `asyncio.Semaphore` — The Rate Limiter

APIs have rate limits. You can't fire 100 agents at once. A semaphore controls how many run simultaneously.

```python
# SHAPE: Bounded concurrency
semaphore = asyncio.Semaphore(5)  # ← max 5 at a time

async def rate_limited_agent(prompt: str) -> str:
    async with semaphore:          # ← waits here if 5 are already running
        return await client.chat(prompt)

# Now gather can launch 100 tasks, but only 5 run at once
results = await asyncio.gather(
    *[rate_limited_agent(p) for p in prompts]
)
```

**What to recognize:**
- `asyncio.Semaphore(N)` = "at most N of these can run at the same time"
- `async with semaphore:` = "acquire a slot, release when done"
- This is THE pattern for respecting API rate limits

---

## Pattern 4: `asyncio.Queue` — Agent-to-Agent Pipeline

When one agent produces work and another consumes it — a producer/consumer pipeline.

```python
# SHAPE: One agent feeds another through a queue
queue: asyncio.Queue[str] = asyncio.Queue()

async def researcher(queries: list[str]):
    for q in queries:
        result = await research(q)
        await queue.put(result)       # ← feeds the writer
    await queue.put(None)             # ← signals "I'm done"

async def writer():
    while True:
        item = await queue.get()      # ← waits for researcher to produce
        if item is None:
            break
        await write_summary(item)

# Run both at the same time
await asyncio.gather(researcher(queries), writer())
```

**What to recognize:**
- `asyncio.Queue()` = shared mailbox between agents
- `queue.put()` = "here's work for you"
- `queue.get()` = "give me the next piece of work (I'll wait)"
- `None` sentinel = "no more work coming"

---

## Pattern 5: `async for` — Streaming Results

You already saw this in L03. Here's the recognition pattern:

```python
# SHAPE: Process results as they arrive
async for event in agent.stream(prompt):
    if event.type == "text":
        print(event.text, end="", flush=True)   # ← real-time output
    elif event.type == "tool_use":
        print(f"\n[Tool: {event.name}]")
```

**What to recognize:**
- `async for` = "items arrive one at a time, I process each as it comes"
- Different from `gather` — `gather` waits for ALL to finish, `async for` processes each immediately
- This is how streaming chat responses work

---

## Pattern 6: The Sync-to-Async Bridge

When existing synchronous code needs to call async agents. You saw this as Pattern 7 in `CHEATSHEET_L01.py`.

```python
# SHAPE: Wrapping async code for sync callers
def ask_agent(prompt: str) -> str:
    """Sync wrapper. Call from non-async code."""
    return asyncio.run(_async_ask(prompt))

async def _async_ask(prompt: str) -> str:
    result = await agent.run(prompt)
    return result.text
```

**What to recognize:**
- `asyncio.run()` = "start the async engine, run this one thing, shut it down"
- This is the entry point — usually at the top of your program or in a CLI
- **Never nest** `asyncio.run()` inside another async function — that crashes

---

## Recognition Drill: Read This Real Code

Here's a simplified version of what a multi-agent system looks like in production. Try to identify each pattern:

```python
import asyncio

SEMAPHORE = asyncio.Semaphore(3)  # ← Pattern 3: rate limit to 3

async def analyze_document(doc: str) -> dict:        # ← Pattern 1: async def
    async with SEMAPHORE:                             # ← Pattern 3: acquire slot
        summary = await summarize_agent(doc)          # ← Pattern 1: await
        entities = await extract_agent(doc)
        return {"summary": summary, "entities": entities}

async def process_batch(documents: list[str]) -> list[dict]:
    results = await asyncio.gather(                   # ← Pattern 2: parallel
        *[analyze_document(doc) for doc in documents]
    )
    return results

def main():
    docs = load_documents("./data/")
    results = asyncio.run(process_batch(docs))        # ← Pattern 6: sync bridge
    save_results(results)
```

**What you should spot:**
1. `asyncio.Semaphore(3)` → at most 3 documents analyzed at once
2. `asyncio.gather(*[...])` → all documents launched concurrently
3. `asyncio.run()` → entry point from sync `main()`
4. Inside each `analyze_document`, the `summarize` and `extract` calls are SEQUENTIAL (one `await` after another) — they could be made parallel too!

---

## Quick Reference: When You See...

| You See | It Means |
|---------|----------|
| `async def` | This function can pause |
| `await` | Pause here, let others run |
| `asyncio.gather(a, b, c)` | Run a, b, c simultaneously |
| `asyncio.Semaphore(N)` | Max N concurrent |
| `asyncio.Queue()` | Agent-to-agent pipeline |
| `async for` | Process streaming items |
| `asyncio.run()` | Start async from sync code |
| `asyncio.create_task()` | Fire-and-forget background work (keep a reference to the task) |
| `async with asyncio.TaskGroup() as tg:` | Run several tasks; one failure cancels the rest (3.11+) |

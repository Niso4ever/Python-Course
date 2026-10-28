# L01 — Pass 3: TEMPLATES
## Your Async Agent Copy-Paste Library

**Goal:** Five ready-to-use async patterns. Copy, configure, run.

> **2026 Note:** All templates use `DEMO_MODE = True` by default — they simulate API calls with `asyncio.sleep()` so you can see the timing without spending tokens.

---

## Template 1: Parallel Agent Gather

**Use when:** You have 2+ independent agents and want results fast.

```python
import asyncio
import time

DEMO_MODE = True

async def agent_call(name: str, prompt: str, delay: float = 1.0) -> dict:
    """Simulate or make a real agent call."""
    if DEMO_MODE:
        await asyncio.sleep(delay)
        return {"agent": name, "result": f"[{name} response to: {prompt[:30]}...]"}
    # Real: return await client.chat(prompt)

async def run_parallel(prompt: str) -> list[dict]:
    """Run 3 agents simultaneously, return all results."""
    results = await asyncio.gather(
        agent_call("researcher", prompt, delay=2.0),
        agent_call("writer", prompt, delay=1.5),
        agent_call("reviewer", prompt, delay=1.0),
    )
    return results

# Call:
start = time.time()
results = asyncio.run(run_parallel("Explain async patterns"))
elapsed = time.time() - start
print(f"Got {len(results)} results in {elapsed:.1f}s (would be ~4.5s sequential)")
for r in results:
    print(f"  {r['agent']}: {r['result']}")
```

---

## Template 2: Rate-Limited Batch Processing

**Use when:** Processing many items but the API has rate limits.

```python
import asyncio
import time

DEMO_MODE = True
MAX_CONCURRENT = 3

async def process_item(item: str, sem: asyncio.Semaphore) -> dict:
    """Process one item with rate limiting."""
    async with sem:
        if DEMO_MODE:
            await asyncio.sleep(0.5)
            return {"item": item, "status": "done"}
        # Real: return await agent.analyze(item)

async def process_batch(items: list[str]) -> list[dict]:
    """Process all items with bounded concurrency."""
    sem = asyncio.Semaphore(MAX_CONCURRENT)
    results = await asyncio.gather(
        *[process_item(item, sem) for item in items]
    )
    return results

# Call:
items = [f"document_{i}" for i in range(10)]
start = time.time()
results = asyncio.run(process_batch(items))
elapsed = time.time() - start
print(f"Processed {len(results)} items in {elapsed:.1f}s")
print(f"  (Sequential would be {len(items) * 0.5:.1f}s)")
print(f"  (Unlimited parallel would be 0.5s)")
print(f"  (Rate-limited to {MAX_CONCURRENT} concurrent)")
```

---

## Template 3: Producer-Consumer Pipeline

**Use when:** One agent produces work, another consumes it — streaming results.

```python
import asyncio

DEMO_MODE = True

async def producer(queue: asyncio.Queue, items: list[str]):
    """Research agent — produces findings."""
    for item in items:
        if DEMO_MODE:
            await asyncio.sleep(0.3)
            result = f"Finding about {item}"
        else:
            result = await research_agent(item)
        await queue.put(result)
        print(f"  [Producer] Queued: {result}")
    await queue.put(None)  # signal: no more work

async def consumer(queue: asyncio.Queue):
    """Writer agent — consumes and processes findings."""
    processed = []
    while True:
        item = await queue.get()
        if item is None:
            break
        if DEMO_MODE:
            await asyncio.sleep(0.2)
            summary = f"Summary of: {item}"
        else:
            summary = await writer_agent(item)
        processed.append(summary)
        print(f"  [Consumer] Wrote: {summary}")
    return processed

async def run_pipeline(items: list[str]):
    queue: asyncio.Queue[str | None] = asyncio.Queue(maxsize=5)
    # Run both simultaneously — producer feeds consumer
    _, summaries = await asyncio.gather(
        producer(queue, items),
        consumer(queue),
    )
    return summaries

# Call:
items = ["quantum computing", "neural networks", "agent design"]
results = asyncio.run(run_pipeline(items))
print(f"\nPipeline complete: {len(results)} summaries")
```

---

## Template 4: Timeout-Protected Concurrent Agents

**Use when:** Production code — agents that hang must not block the whole system.

```python
import asyncio

DEMO_MODE = True

async def agent_with_timeout(
    name: str,
    prompt: str,
    timeout_s: float = 5.0,
) -> dict:
    """Run a single agent with a timeout guard."""
    async def _call():
        if DEMO_MODE:
            delay = 2.0 if name == "slow_agent" else 0.5
            await asyncio.sleep(delay)
            return f"[{name}] result for: {prompt[:20]}"
        # Real: return await client.chat(prompt)

    try:
        result = await asyncio.wait_for(_call(), timeout=timeout_s)
        return {"agent": name, "status": "ok", "result": result}
    except asyncio.TimeoutError:
        return {"agent": name, "status": "timeout", "result": None}

async def run_with_timeouts(prompt: str):
    """Run multiple agents, each with its own timeout."""
    results = await asyncio.gather(
        agent_with_timeout("fast_agent", prompt, timeout_s=3.0),
        agent_with_timeout("slow_agent", prompt, timeout_s=1.0),  # will timeout
        agent_with_timeout("normal_agent", prompt, timeout_s=3.0),
    )
    for r in results:
        status = "✓" if r["status"] == "ok" else "✗ TIMEOUT"
        print(f"  {r['agent']}: {status}")
    return results

# Call:
asyncio.run(run_with_timeouts("Analyze this dataset"))
```

---

## Template 5: Fire-and-Forget Background Agent

**Use when:** You want to kick off a logging/monitoring agent without waiting for it.

```python
import asyncio

DEMO_MODE = True

async def log_interaction(prompt: str, result: str):
    """Background task — logs to external service, don't wait for it."""
    if DEMO_MODE:
        await asyncio.sleep(1.0)  # simulate slow logging
        print(f"  [Background] Logged interaction ({len(prompt)} chars)")
    # Real: await logging_service.log({"prompt": prompt, "result": result})

# The event loop only keeps weak references to tasks, so an unreferenced
# background task can be garbage-collected before it finishes. Keep them here.
background_tasks: set[asyncio.Task] = set()

def fire_and_forget(coro) -> None:
    task = asyncio.create_task(coro)
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)

async def main_agent(prompt: str) -> str:
    """Main agent — fires background logger, doesn't wait."""
    # Start background logging (fire-and-forget)
    fire_and_forget(log_interaction(prompt, "pending"))

    # Do the actual work
    if DEMO_MODE:
        await asyncio.sleep(0.5)
        result = f"Answer to: {prompt}"
    else:
        result = await agent.run(prompt)

    # Fire another background task with the real result
    fire_and_forget(log_interaction(prompt, result))

    return result  # returns immediately, logging continues in background

async def run():
    result = await main_agent("What is async?")
    print(f"  [Main] Got result: {result}")
    await asyncio.sleep(2)  # give background tasks time to finish

# Call:
asyncio.run(run())
```

---

## Quick Selection Guide

| Need | Template |
|------|----------|
| Run 2+ agents at once | Template 1: Parallel Gather |
| API rate limits | Template 2: Rate-Limited Batch |
| Agent feeds another agent | Template 3: Producer-Consumer |
| Agents that might hang | Template 4: Timeout-Protected |
| Logging without blocking | Template 5: Fire-and-Forget |

"""
CHEATSHEET — Async Patterns for Agents (L01)
Keep this open while reading async agent code.

2026 Note: Standard-library asyncio only, no external libraries. The course
venv runs Python 3.12; TaskGroup and asyncio.timeout() need 3.11+.
"""

import asyncio

# ─── PATTERN 1: Basic async/await ───────────────────────────
async def call_agent(prompt: str) -> str:
    """Any function that calls an API should be async."""
    # await = pause here, let others run while waiting
    result = await some_api_call(prompt)
    return result


# ─── PATTERN 2: Parallel with gather ───────────────────────
async def run_parallel():
    """Run multiple agents simultaneously."""
    a, b, c = await asyncio.gather(
        agent_one("task1"),    # starts immediately
        agent_two("task2"),    # starts immediately
        agent_three("task3"),  # starts immediately
    )
    # a, b, c = results in same order as arguments


# ─── PATTERN 3: Rate-limited with semaphore ────────────────
sem = asyncio.Semaphore(5)     # max 5 concurrent

async def rate_limited(prompt: str) -> str:
    async with sem:            # waits if 5 already running
        return await call_api(prompt)


# ─── PATTERN 4: Queue pipeline ─────────────────────────────
queue: asyncio.Queue[str] = asyncio.Queue()

async def producer():
    await queue.put("data")    # feed the consumer
    await queue.put(None)      # signal: done

async def consumer():
    while (item := await queue.get()) is not None:
        process(item)


# ─── PATTERN 5: Timeout protection ─────────────────────────
async def safe_call(prompt: str, timeout: float = 10.0):
    try:
        return await asyncio.wait_for(call_agent(prompt), timeout)
    except asyncio.TimeoutError:
        return "Agent timed out"


# ─── PATTERN 6: Fire-and-forget ─────────────────────────────
background_tasks: set[asyncio.Task] = set()   # keep a reference, or the task
                                               # can be garbage-collected mid-run
async def main():
    task = asyncio.create_task(log_something())  # runs in background
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)  # forget it once done
    result = await do_real_work()                 # don't wait for logging
    return result


# ─── PATTERN 6b: TaskGroup (Python 3.11+) ──────────────────
# The newer alternative to gather. If one task fails, the group cancels
# the others and raises — nothing keeps running unnoticed.
async def run_group():
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(agent_one("task1"))
        t2 = tg.create_task(agent_two("task2"))
    return t1.result(), t2.result()   # all done once the block exits


# ─── PATTERN 7: Entry point (sync → async) ─────────────────
def cli_main():
    """Call from non-async code (scripts, CLI)."""
    result = asyncio.run(run_parallel())   # starts the event loop
    print(result)


# ═══ COMMON MISTAKES ═══════════════════════════════════════
#
# ✗ WRONG: Calling async function without await
#   result = call_agent("hi")     # returns coroutine, not result!
#
# ✓ RIGHT:
#   result = await call_agent("hi")
#
# ✗ WRONG: Nesting asyncio.run()
#   async def inner():
#       asyncio.run(other())      # CRASHES — already in event loop
#
# ✓ RIGHT:
#   async def inner():
#       await other()             # just await it
#
# ✗ WRONG: Using time.sleep() in async code
#   async def slow():
#       time.sleep(5)             # blocks EVERYTHING
#
# ✓ RIGHT:
#   async def slow():
#       await asyncio.sleep(5)    # pauses only this function


# ═══ QUICK REFERENCE TABLE ═════════════════════════════════
#
# | Need                    | Use                              |
# |-------------------------|----------------------------------|
# | Run 2+ things at once   | asyncio.gather(a, b, c)          |
# | Same, fail-fast + clean | async with asyncio.TaskGroup()   |
# | Limit concurrency       | asyncio.Semaphore(N)             |
# | Pipeline between agents | asyncio.Queue()                  |
# | Timeout protection      | asyncio.wait_for(coro, timeout)  |
# | Background task         | asyncio.create_task(coro) + keep |
# |                         | a reference (set of tasks)       |
# | Start from sync code    | asyncio.run(coro)                |
# | Stream results          | async for item in stream:        |

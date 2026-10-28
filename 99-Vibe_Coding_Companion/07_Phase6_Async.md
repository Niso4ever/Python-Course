# Phase 6 — Async for Agents (Ph6-L01, 1 template)

Tier 1 of the multi-agent landscape: running agents concurrently. These prompts focus heavily on **Mode 5 (Integration)** and **Mode 2 (Specification)**. Without async primitives like `asyncio.gather` and `asyncio.Semaphore`, your multi-agent system will be unbearably slow.

---

## 53. `template_parallel_agents.py` — Ph6-L01 Parallel Gather
**Level 3 (Contract) · Mode 2 (Specification)** — The fundamental parallel run.

#### 📝 VIBE PROMPT
```
CONSTRAINTS: Use `asyncio.gather` to run 3 distinct simulated agent functions. DEMO_MODE uses `asyncio.sleep` to fake API latency. Add a Semaphore to rate-limit execution to 2 concurrent tasks.
REQUEST: Run a researcher, writer, and critic agent concurrently. Ensure they respect the rate limit. Return all results and calculate the speedup vs sequential execution.
VALIDATION: Two agents start at once; the third waits for a free slot. Total time is less than the sum of the three agents' run times. Each agent's timer starts when it gets a slot, so queue time is not counted as work.
```
#### 💻 PRODUCES (essence)
```python
async with semaphore:                      # wait for a slot
    output = await asyncio.wait_for(agent_fn(prompt), timeout=timeout_s)

results = await asyncio.gather(
    *[run_agent_safe(name, fn, prompt, semaphore)
      for name, fn in [("researcher", research_agent),
                       ("writer", writer_agent),
                       ("critic", critic_agent)]]
)
```

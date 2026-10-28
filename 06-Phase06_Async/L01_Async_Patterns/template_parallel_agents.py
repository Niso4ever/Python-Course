"""
Template: Parallel Agents with Rate Limiting
============================================
Three specialist agents run concurrently with a semaphore to
respect API rate limits. Fully runnable in DEMO_MODE.

Usage:
    python template_parallel_agents.py

2026 Note: Standard-library asyncio only, no external libraries. Runs on the
course venv (Python 3.12); TaskGroup and asyncio.timeout() need 3.11+.
"""

import asyncio
import time
from dataclasses import dataclass

# ─── Configuration ──────────────────────────────────────────
DEMO_MODE = True  # Set False + add API key for real calls
MAX_CONCURRENT = 2  # Max agents running at the same time


@dataclass
class AgentResult:
    """Structured result from any agent."""
    agent_name: str
    input_prompt: str
    output: str
    elapsed_seconds: float
    status: str  # "ok" | "timeout" | "error"


# ─── Agent Definitions ─────────────────────────────────────

async def research_agent(prompt: str) -> str:
    """Specialist: finds relevant information."""
    if DEMO_MODE:
        await asyncio.sleep(1.5)  # simulate API latency
        return f"Research findings: '{prompt}' relates to async patterns, concurrency, and event loops."
    # Real: return await client.chat(system="You are a researcher.", prompt=prompt)
    raise NotImplementedError("Set DEMO_MODE = False and implement real API call")


async def writer_agent(prompt: str) -> str:
    """Specialist: writes polished summaries."""
    if DEMO_MODE:
        await asyncio.sleep(1.0)
        return f"Summary: The topic '{prompt}' can be explained as a pattern for running multiple tasks efficiently."
    raise NotImplementedError("Set DEMO_MODE = False and implement real API call")


async def critic_agent(prompt: str) -> str:
    """Specialist: reviews and critiques output."""
    if DEMO_MODE:
        await asyncio.sleep(0.8)
        return f"Review: The explanation of '{prompt}' is clear but could use a concrete example."
    raise NotImplementedError("Set DEMO_MODE = False and implement real API call")


# ─── Orchestration Layer ───────────────────────────────────

async def run_agent_safe(
    name: str,
    agent_fn,
    prompt: str,
    semaphore: asyncio.Semaphore,
    timeout_s: float = 10.0,
) -> AgentResult:
    """Run one agent with rate limiting + timeout + error handling."""
    async with semaphore:  # ← wait for a slot (rate limiting)
        # Start the clock only once the slot is acquired, so time spent
        # queueing is not counted as the agent's own run time.
        start = time.time()
        print(f"  [{name}] Started (slot acquired)")
        try:
            output = await asyncio.wait_for(
                agent_fn(prompt),
                timeout=timeout_s,
            )
            elapsed = time.time() - start
            print(f"  [{name}] Done in {elapsed:.1f}s")
            return AgentResult(
                agent_name=name,
                input_prompt=prompt,
                output=output,
                elapsed_seconds=round(elapsed, 2),
                status="ok",
            )
        except asyncio.TimeoutError:
            elapsed = time.time() - start
            print(f"  [{name}] TIMEOUT after {elapsed:.1f}s")
            return AgentResult(
                agent_name=name,
                input_prompt=prompt,
                output="",
                elapsed_seconds=round(elapsed, 2),
                status="timeout",
            )
        except Exception as e:
            elapsed = time.time() - start
            print(f"  [{name}] ERROR: {e}")
            return AgentResult(
                agent_name=name,
                input_prompt=prompt,
                output="",
                elapsed_seconds=round(elapsed, 2),
                status="error",
            )


async def orchestrate(prompt: str) -> list[AgentResult]:
    """Run all specialist agents concurrently with rate limiting."""
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)

    agents = [
        ("researcher", research_agent),
        ("writer", writer_agent),
        ("critic", critic_agent),
    ]

    print(f"\n{'='*60}")
    print(f"Orchestrator: Running {len(agents)} agents")
    print(f"  Prompt: {prompt}")
    print(f"  Max concurrent: {MAX_CONCURRENT}")
    print(f"{'='*60}\n")

    overall_start = time.time()

    # Launch ALL agents concurrently — semaphore limits how many run at once
    results = await asyncio.gather(
        *[
            run_agent_safe(name, fn, prompt, semaphore)
            for name, fn in agents
        ]
    )

    overall_elapsed = time.time() - overall_start

    # Report
    print(f"\n{'='*60}")
    print(f"Results ({overall_elapsed:.1f}s total):")
    print(f"{'='*60}")
    for r in results:
        icon = "✓" if r.status == "ok" else "✗"
        print(f"  {icon} {r.agent_name} ({r.elapsed_seconds}s): {r.output[:60]}...")

    sequential_time = sum(r.elapsed_seconds for r in results)
    speedup = sequential_time / overall_elapsed if overall_elapsed > 0 else 1
    print(f"\n  Sequential would take: {sequential_time:.1f}s")
    print(f"  Concurrent took:      {overall_elapsed:.1f}s")
    print(f"  Speedup:              {speedup:.1f}x")

    return results


# ─── Entry Point ────────────────────────────────────────────

def main():
    """Sync entry point — start the async orchestrator."""
    prompt = "What are async patterns for AI agents?"
    results = asyncio.run(orchestrate(prompt))

    ok_count = sum(1 for r in results if r.status == "ok")
    print(f"\n✓ {ok_count}/{len(results)} agents completed successfully")


if __name__ == "__main__":
    main()

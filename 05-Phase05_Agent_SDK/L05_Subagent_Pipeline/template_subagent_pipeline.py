"""
TEMPLATE: Two-Agent Pipeline (Subagents)
CURRICULUM PATTERN: Ph5-L05
DESCRIPTION: Orchestrator delegates to a specialist researcher, then synthesizes.
             Output of agent 1 = input of agent 2.
Run with: python template_subagent_pipeline.py
"""

import asyncio
import time
from dataclasses import dataclass
from pydantic import BaseModel, Field

DEMO_MODE = True

# ──────────────────────────────────────────────
# DATA SHAPES
# ──────────────────────────────────────────────

class ResearchResult(BaseModel):
    topic: str = Field(description="What was researched")
    findings: str = Field(description="Key facts found")
    sources: list[str] = Field(description="Source references")

class FinalReport(BaseModel):
    topic: str = Field(description="Original topic")
    research: ResearchResult = Field(description="Raw research from specialist")
    summary: str = Field(description="Synthesized summary from orchestrator")
    agent_chain: list[str] = Field(description="Which agents ran in order")


# ──────────────────────────────────────────────
# DEMO AGENTS
# ──────────────────────────────────────────────

DEMO_RESEARCH: dict[str, ResearchResult] = {
    "quantum": ResearchResult(
        topic="quantum computing",
        findings=(
            "Quantum computing uses qubits that can exist in superposition. "
            "In 2026, IBM has 1000+ qubit processors. Google achieved quantum advantage "
            "in 2019. Error correction remains the key unsolved challenge."
        ),
        sources=["arxiv.org/quantum-2026", "ibm.com/quantum", "nature.com/quantum"]
    ),
    "rag": ResearchResult(
        topic="RAG patterns",
        findings=(
            "RAG (Retrieval-Augmented Generation) retrieves relevant docs before generating. "
            "Key metrics: Precision@k, Recall, answer accuracy. "
            "In 2026, hybrid retrieval (sparse + dense) is the standard approach."
        ),
        sources=["docs.anthropic.com/rag", "arxiv.org/rag-survey"]
    ),
}

def _demo_researcher(topic: str) -> ResearchResult:
    """Simulate the researcher subagent."""
    for key, result in DEMO_RESEARCH.items():
        if key in topic.lower():
            return result
    return ResearchResult(
        topic=topic,
        findings=f"[DEMO] Simulated research findings for '{topic}'. Key facts: fact1, fact2, fact3.",
        sources=["source1.com", "source2.org"]
    )

def _demo_orchestrator(research: ResearchResult) -> str:
    """Simulate the orchestrator synthesizing research into a summary."""
    return (
        f"Based on research into {research.topic}: "
        f"{research.findings[:120]}... "
        f"Sources consulted: {len(research.sources)}."
    )


# ──────────────────────────────────────────────
# AGENT RUNNERS
# ──────────────────────────────────────────────

@dataclass
class AgentConfig:
    model: str
    system_prompt: str

RESEARCHER_CONFIG = AgentConfig(
    model="claude-haiku-5-5",
    system_prompt=(
        "You are a research specialist. Find key facts, statistics, and recent developments. "
        "Be thorough. Cite sources when possible."
    ),
)

ORCHESTRATOR_CONFIG = AgentConfig(
    model="claude-sonnet-5-5",
    system_prompt=(
        "You are an orchestrator. You receive research findings and synthesize them "
        "into a clear, concise summary for a non-technical audience."
    ),
)


async def run_researcher(topic: str) -> ResearchResult:
    """Run the specialist researcher subagent.

    Args:
        topic: The research topic to investigate.

    Returns:
        Structured research result with findings and sources.
    """
    if DEMO_MODE:
        time.sleep(0.1)  # simulate latency
        return _demo_researcher(topic)

    from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage  # type: ignore
    import json

    options = ClaudeAgentOptions(
        model=RESEARCHER_CONFIG.model,
        system_prompt=RESEARCHER_CONFIG.system_prompt,
    )
    async for msg in query(prompt=f"Research this topic thoroughly: {topic}", options=options):
        if isinstance(msg, ResultMessage):
            return ResearchResult(topic=topic, findings=msg.result, sources=[])
    return ResearchResult(topic=topic, findings="No results", sources=[])


async def run_orchestrator(topic: str, research: ResearchResult) -> str:
    """Run the orchestrator to synthesize research into a summary.

    Args:
        topic: Original research topic.
        research: Findings from the researcher subagent.

    Returns:
        Synthesized summary string.
    """
    if DEMO_MODE:
        time.sleep(0.05)
        return _demo_orchestrator(research)

    from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage  # type: ignore

    options = ClaudeAgentOptions(
        model=ORCHESTRATOR_CONFIG.model,
        system_prompt=ORCHESTRATOR_CONFIG.system_prompt,
    )
    prompt = f"Topic: {topic}\n\nResearch findings:\n{research.findings}\n\nWrite a 2-sentence summary."
    async for msg in query(prompt=prompt, options=options):
        if isinstance(msg, ResultMessage):
            return msg.result
    return ""


async def run_pipeline(topic: str) -> FinalReport:
    """Run the full two-agent pipeline: researcher → orchestrator.

    Args:
        topic: The topic to research and summarize.

    Returns:
        FinalReport with research findings and synthesized summary.
    """
    print(f"  [1/2] Researcher agent running... ({RESEARCHER_CONFIG.model})")
    research = await run_researcher(topic)
    print(f"        Found {len(research.findings.split())} words of findings")

    print(f"  [2/2] Orchestrator synthesizing... ({ORCHESTRATOR_CONFIG.model})")
    summary = await run_orchestrator(topic, research)

    return FinalReport(
        topic=topic,
        research=research,
        summary=summary,
        agent_chain=["researcher", "orchestrator"],
    )


# ──────────────────────────────────────────────
# DEMO
# ──────────────────────────────────────────────

async def main() -> None:
    print("Two-Agent Pipeline Demo")
    print("=" * 55)
    print("Flow: User → Orchestrator → Researcher → Orchestrator → Answer\n")

    topics = ["quantum computing trends", "RAG patterns in 2026"]

    for topic in topics:
        print(f"Topic: {topic}")
        report = await run_pipeline(topic)
        print(f"\nRaw research ({len(report.research.findings)} chars):")
        print(f"  {report.research.findings[:120]}...")
        print(f"\nSynthesized summary:")
        print(f"  {report.summary}")
        print(f"\nAgent chain: {' → '.join(report.agent_chain)}")
        print("-" * 55 + "\n")

    print(f"[{'DEMO' if DEMO_MODE else 'REAL API'} MODE]")


if __name__ == "__main__":
    asyncio.run(main())

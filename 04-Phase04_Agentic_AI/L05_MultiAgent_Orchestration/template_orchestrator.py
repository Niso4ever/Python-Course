"""
Template: Multi-Agent Orchestrator — Runnable Demo
====================================================
Run this file as-is: python template_orchestrator.py

DEMO MODE (default): All agents simulated locally. No API key needed.
REAL MODE:           Set DEMO_MODE = False + ANTHROPIC_API_KEY.

What this demonstrates:
  - 3 specialist agents (researcher, writer, analyst)
  - A router orchestrator using structured output
  - Sequential pipeline (research → write)
  - Each specialist has its own persona and tools
"""

import os
import json
from pydantic import BaseModel
from typing import Literal

DEMO_MODE = True  # Set to False + ANTHROPIC_API_KEY for real Claude

# ============================================================
# SYSTEM PROMPTS (specialist personas)
# ============================================================

RESEARCHER_PROMPT = """You are a thorough AI Research Specialist for 2026.
Your job: find accurate, comprehensive information about AI topics.
Always organize findings with clear headings and cite key concepts."""

WRITER_PROMPT = """You are an expert AI Content Writer for 2026.
Your job: transform research and information into clear, engaging prose.
Use concrete examples. Write for a technical but non-expert audience."""

ANALYST_PROMPT = """You are a data-driven AI Systems Analyst for 2026.
Your job: compare, evaluate, and draw conclusions from information.
Present findings as structured comparisons with clear recommendations."""

# ============================================================
# SIMULATED TOOLS (demo data)
# ============================================================

KNOWLEDGE_BASE = {
    "agent loop":      "The agent loop is the fundamental pattern: LLM thinks → tool calls → observe results → repeat until done. It runs inside every framework.",
    "mcp":             "MCP (Model Context Protocol) is Anthropic's 2024 open standard. By 2026 it became the universal connector for AI tools and data sources, replacing custom integrations.",
    "direct api":      "Direct API usage means calling model providers (Anthropic, OpenAI) without framework middleware. More stable, less dependency risk, clearer code.",
    "multi-agent":     "Multi-agent systems use an orchestrator to route tasks to specialized agents. Each specialist has focused tools and a specific persona.",
    "structured output": "Structured output makes LLMs return typed data: Pydantic + client.messages.parse(output_format=...). Replaces fragile JSON parsing from free text.",
}

def simulate_search(query: str) -> str:
    query_lower = query.lower()
    for key, value in KNOWLEDGE_BASE.items():
        if key in query_lower or any(w in query_lower for w in key.split()):
            return value
    return f"General AI knowledge: {query} is a key concept in modern agentic AI systems (2026 context)."

# ============================================================
# DEMO: Simulated LLM responses
# ============================================================

class MockBlock:
    def __init__(self, btype, **kwargs):
        self.type = btype
        for k, v in kwargs.items():
            setattr(self, k, v)

class MockResponse:
    def __init__(self, stop_reason, content):
        self.stop_reason = stop_reason
        self.content = content

def simulate_agent(task: str, agent_type: str) -> str:
    """Simulate what each specialist agent would return."""
    topic_hint = task[:60]
    if agent_type == "researcher":
        result = simulate_search(task.lower())
        return f"[RESEARCH OUTPUT]\n{result}\n\nAdditional context: In 2026, this concept is central to production AI systems and is taught in all major AI engineering programs."
    elif agent_type == "writer":
        return f"[ARTICLE]\n\nUnderstanding {topic_hint[:40]}...\n\nIn the rapidly evolving landscape of 2026 AI development, this topic has become foundational. {simulate_search(task.lower())[:150]}...\n\nConclusion: Teams that master this pattern build more resilient, framework-independent AI systems."
    elif agent_type == "analyst":
        return f"[ANALYSIS]\n\nEvaluation: {topic_hint[:40]}...\n\n• Adoption rate: High (estimated 70% of enterprise AI teams in 2026)\n• Complexity: Medium\n• Stability: High (framework-independent)\n• Recommendation: Prioritize learning this pattern over framework-specific syntax."
    return f"[FALLBACK] I can help with: {task[:50]}..."

def simulate_router(request: str) -> str:
    """Simulate the routing decision."""
    request_lower = request.lower()
    if any(w in request_lower for w in ["research", "find", "what is", "explain", "information"]):
        return "researcher"
    elif any(w in request_lower for w in ["write", "article", "blog", "post", "draft"]):
        return "writer"
    elif any(w in request_lower for w in ["compare", "analyse", "analyze", "evaluate", "which"]):
        return "analyst"
    return "researcher"  # default

# ============================================================
# SPECIALIST RUNNERS
# ============================================================

def run_specialist(task: str, agent_type: str) -> str:
    """Run a specialist agent (demo or real)."""
    if DEMO_MODE:
        return simulate_agent(task, agent_type)
    else:
        import anthropic
        client = anthropic.Anthropic()
        prompts = {
            "researcher": RESEARCHER_PROMPT,
            "writer":     WRITER_PROMPT,
            "analyst":    ANALYST_PROMPT,
        }
        system = prompts.get(agent_type, "You are a helpful assistant.")
        messages = [{"role": "user", "content": task}]

        while True:
            response = client.messages.create(
                model="claude-opus-5-5", max_tokens=2048,
                system=system, messages=messages
            )
            if response.stop_reason == "end_turn":
                return response.content[0].text
            # (simple version without tools for this demo)
            break
        return response.content[0].text

def research_agent(task: str) -> str:
    return run_specialist(task, "researcher")

def writer_agent(task: str) -> str:
    return run_specialist(task, "writer")

def analyst_agent(task: str) -> str:
    return run_specialist(task, "analyst")

def fallback_agent(task: str) -> str:
    return run_specialist(task, "researcher")  # default to researcher

# ============================================================
# DEMO 1: Router Orchestrator
# ============================================================

def demo_router():
    print("\n" + "="*60)
    print("DEMO 1: Router Orchestrator")
    print("="*60)

    requests = [
        "What is the agent loop pattern in AI systems?",
        "Write a short blog post about MCP.",
        "Analyse the benefits of direct API usage vs frameworks.",
    ]

    AGENTS = {
        "researcher": research_agent,
        "writer":     writer_agent,
        "analyst":    analyst_agent,
        "fallback":   fallback_agent,
    }

    for request in requests:
        print(f"\nRequest: {request}")
        route = simulate_router(request)
        print(f"[Router] → {route}")
        result = AGENTS[route](request)
        print(f"Result preview: {result[:120]}...")

# ============================================================
# DEMO 2: Sequential Pipeline
# ============================================================

def demo_pipeline():
    print("\n" + "="*60)
    print("DEMO 2: Sequential Pipeline — Research → Write")
    print("="*60)

    topic = "How MCP is replacing custom tool integrations in 2026"
    print(f"Topic: {topic}")

    print("\n[Step 1] Research Agent working...")
    research = research_agent(f"Research this topic in detail: {topic}")
    print(f"Research output: {research[:100]}...")

    print("\n[Step 2] Writer Agent working (using research as input)...")
    article = writer_agent(f"Write a 300-word article. Use this research:\n\n{research}")
    print(f"Article output: {article[:100]}...")

    print(f"\n[Pipeline complete]")
    print("Full article:")
    print("-"*40)
    print(article)

# ============================================================
# DEMO 3: Parallel (simulated — showing the concept)
# ============================================================

def demo_parallel_concept():
    print("\n" + "="*60)
    print("DEMO 3: Parallel Research — 3 topics simultaneously")
    print("="*60)

    topics = ["agent loop", "MCP", "structured output"]
    print(f"Topics: {topics}")
    print("(In real mode these would run via asyncio.gather — simultaneously)")
    print("(In demo mode we run them sequentially for simplicity)")

    results = {}
    for topic in topics:
        print(f"\n  Researching: '{topic}'...")
        results[topic] = research_agent(f"Explain {topic} in AI systems")
        print(f"  Done: {results[topic][:80]}...")

    print(f"\n[Parallel complete] Researched {len(results)} topics")
    print("Now synthesizing all results...")
    synthesis = writer_agent(
        "Summarize these 3 AI concepts in one paragraph:\n" +
        "\n".join(f"- {k}: {v[:100]}" for k, v in results.items())
    )
    print(f"\nSynthesis: {synthesis[:200]}...")

# ============================================================
# RUN ALL DEMOS
# ============================================================

if __name__ == "__main__":
    demo_router()
    demo_pipeline()
    demo_parallel_concept()

    if DEMO_MODE:
        print("\n" + "="*60)
        print("[DEMO MODE] Set DEMO_MODE = False + ANTHROPIC_API_KEY for real Claude.")

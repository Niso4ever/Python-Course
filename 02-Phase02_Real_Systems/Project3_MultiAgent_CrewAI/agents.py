"""
agents.py — Define the specialist agents for the AI Content Studio.

Each agent has:
  - role: the job title (what kind of expert they are)
  - goal: what they're trying to achieve
  - backstory: context that shapes how the LLM plays this role
  - tools: what tools they can call (optional)
  - verbose: whether to print their reasoning

In 2026, these agent definitions are the "job descriptions"
for your AI workforce. Write them as you would write a job posting.
"""

import os
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("CREWAI_MODEL", "claude-sonnet-5-5")


def build_search_tool():
    """
    Build a web search tool for CrewAI.
    Uses real search if TAVILY_API_KEY is set, otherwise simulated.
    """
    from crewai_tools import SerperDevTool
    try:
        # SerperDev is a reliable search API for CrewAI
        if os.getenv("SERPER_API_KEY"):
            return SerperDevTool()
    except Exception:
        pass

    # Fallback: custom simulated tool
    from crewai.tools import tool

    @tool("Web Search")
    def web_search(query: str) -> str:
        """Search the internet for current information about any topic."""
        # Simulated results with realistic 2026 AI data
        return (
            f"Web search results for: '{query}'\n\n"
            f"Finding 1: AI adoption in enterprises reached 78% in 2026, up from 55% in 2024. "
            f"McKinsey Global Institute estimates $4.4 trillion annual value from AI.\n\n"
            f"Finding 2: Companies with mature AI programs report 2.6x more revenue growth "
            f"than competitors. Time-to-insight cut by 70% on average.\n\n"
            f"Finding 3: Top barriers: data quality (58%), AI talent shortage (47%), "
            f"governance concerns (43%). ROI timeline: 12-18 months median payback.\n\n"
            f"[Simulated search — set SERPER_API_KEY in .env for real results]"
        )

    return web_search


def create_agents(verbose: bool = True):
    """
    Create and return the 3 specialist agents.
    Returns: (researcher, writer, editor)
    """
    from crewai import Agent, LLM

    llm = LLM(model=f"anthropic/{MODEL}")

    search_tool = build_search_tool()

    # ── Agent 1: Researcher ────────────────────────────────────────
    researcher = Agent(
        role="Senior Research Analyst",
        goal=(
            "Find accurate, current, data-rich information on any topic. "
            "Your research becomes the factual foundation that the writer builds on. "
            "Every claim must have a data point. Every trend must have numbers."
        ),
        backstory=(
            "You are a former Bloomberg Intelligence analyst who joined Nexus AI in 2024. "
            "You have 12 years of experience turning raw market data into actionable insight. "
            "You are known for finding the specific statistic that changes how a reader "
            "understands an issue. You never cite vague estimates — always find the number. "
            "In 2026, you use AI search tools to gather intelligence 10x faster than before, "
            "but your judgment about what's credible and what matters hasn't changed."
        ),
        tools=[search_tool],
        llm=llm,
        verbose=verbose,
        memory=True,      # ← remembers what it found across tasks
        max_iter=5        # ← max search iterations before delivering research
    )

    # ── Agent 2: Writer ────────────────────────────────────────────
    writer = Agent(
        role="Senior Content Writer",
        goal=(
            "Transform research notes into compelling, well-structured articles "
            "that are data-driven, readable, and actionable. "
            "Write for intelligent professionals who have 5 minutes, not 50."
        ),
        backstory=(
            "You spent 8 years as a technology journalist at The Economist and Wired "
            "before moving into AI-native content creation in 2025. "
            "You know how to take a dense research brief and extract the three ideas "
            "that actually matter. You write in active voice, use concrete examples, "
            "and never pad word count with fluff. "
            "Your signature style: lead with the most surprising data point, "
            "then explain why it matters, then tell them what to do about it."
        ),
        tools=[],    # ← writer doesn't need tools — just research context + writing skill
        llm=llm,
        verbose=verbose,
        memory=True
    )

    # ── Agent 3: Editor ────────────────────────────────────────────
    editor = Agent(
        role="Editorial Director",
        goal=(
            "Ensure every published article meets the highest standards: "
            "accurate, clear, well-structured, appropriately toned, and ready to publish. "
            "Improve the draft, don't just critique it."
        ),
        backstory=(
            "You led editorial at TechCrunch and then built the AI-native content "
            "review system at Nexus AI. You have seen 50,000 AI-generated articles "
            "and you know exactly where they go wrong: vague language, unsupported claims, "
            "weak conclusions, and burying the lede. "
            "Your edits are surgical — you change what needs changing and leave alone "
            "what works. You always return a polished, publication-ready piece "
            "with a quality score (1-10) and brief notes explaining your changes."
        ),
        tools=[],
        llm=llm,
        verbose=verbose,
        memory=True
    )

    return researcher, writer, editor

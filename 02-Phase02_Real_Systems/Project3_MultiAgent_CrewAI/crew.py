"""
crew.py — Assemble and run the Content Studio Crew.

This is where agents + tasks come together into a running system.
The Crew orchestrates execution: agent 1 runs, passes output to agent 2, etc.

In 2026: crew definitions are version-controlled and deployed as microservices.
Different crews handle different content types (short-form, technical, video scripts).
"""

import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./output")


def run_content_studio(content_brief: dict, verbose: bool = True) -> dict:
    """
    Run the full Content Studio crew on a brief.

    Args:
        content_brief: {
            "topic": str,
            "audience": str,
            "format": str,     # "article" | "briefing" | "report"
            "word_count": int,
            "tone": str
        }

    Returns:
        {
            "output": str,           ← final edited article
            "filepath": str,         ← where it was saved
            "tasks_output": list     ← each agent's raw output
        }
    """
    from crewai import Crew, Process
    from agents import create_agents
    from tasks import create_tasks

    # Step 1: Create specialist agents
    researcher, writer, editor = create_agents(verbose=verbose)

    # Step 2: Create tasks for this specific brief
    tasks = create_tasks(researcher, writer, editor, content_brief)

    # Step 3: Assemble the crew
    crew = Crew(
        agents=[researcher, writer, editor],
        tasks=tasks,
        process=Process.sequential,   # research → write → edit (in order)
        verbose=verbose,
        memory=True,           # ← agents remember context across the session
        # NOTE: CrewAI memory embeds text with OpenAI text-embedding-3-large by default,
        # so memory=True also needs OPENAI_API_KEY, or an embedder={...} dict here
        # (e.g. provider "voyageai" or "ollama"). See docs.crewai.com/en/concepts/memory.
        max_rpm=10,            # ← max API calls per minute (rate limiting)
    )

    # Step 4: Run! (kickoff passes inputs to tasks via {variable} placeholders)
    print(f"\n{'='*60}")
    print(f"CONTENT STUDIO CREW — Starting")
    print(f"Topic: {content_brief['topic'][:60]}")
    print(f"Format: {content_brief.get('format', 'article')} | "
          f"Target: {content_brief.get('word_count', 600)} words")
    print(f"{'='*60}\n")

    result = crew.kickoff()

    # Step 5: Save the final output
    final_content = str(result.raw)
    filepath = save_article(content_brief["topic"], final_content)

    return {
        "output":       final_content,
        "filepath":     filepath,
        "tasks_output": result.tasks_output if hasattr(result, "tasks_output") else []
    }


def save_article(topic: str, content: str) -> str:
    """Save the final article to disk as a Markdown file."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Clean filename
    safe_name = "".join(c if c.isalnum() or c in " -_" else "_" for c in topic)
    safe_name = safe_name.replace(" ", "_")[:50]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename  = f"{safe_name}_{timestamp}.md"
    filepath  = os.path.join(OUTPUT_DIR, filename)

    Path(filepath).write_text(content, encoding="utf-8")
    print(f"\n✅ Article saved to: {filepath}")
    return filepath


def run_demo(content_brief: dict) -> dict:
    """Simulate crew execution without API calls."""
    topic = content_brief["topic"]

    print(f"\n{'='*60}")
    print(f"CONTENT STUDIO CREW — DEMO MODE")
    print(f"Topic: {topic[:60]}")
    print(f"{'='*60}\n")

    print("[RESEARCHER] Searching for data...")
    print("  → web_search('AI enterprise adoption 2026 statistics')")
    print("  ← Found: 78% enterprise adoption, $4.4T value estimate")
    print("  → web_search('AI ROI case studies 2025 2026')")
    print("  ← Found: 2.6x revenue growth, 70% time-to-insight reduction")
    print("  ✓ Research complete\n")

    print("[WRITER] Drafting article...")
    print("  Using research brief from Researcher...")
    print("  Writing hook, analysis sections, and action items...")
    print("  ✓ Draft complete (612 words)\n")

    print("[EDITOR] Reviewing draft...")
    print("  Checking accuracy, clarity, structure, tone...")
    print("  Improving hook: stronger opening statistic")
    print("  Tightening action items: more specific")
    print("  ✓ Editing complete — Quality Score: 8.5/10\n")

    demo_article = f"""# {topic}: What Every Leader Needs to Know in 2026

*By Nexus AI Content Studio — {datetime.now().strftime('%B %d, %Y')}*

---

Seventy-eight percent of enterprises now use AI in at least one business function—
up from 55% just two years ago. That's not a trend. That's a transformation.

## The Numbers That Matter

The McKinsey Global Institute estimates AI could generate $4.4 trillion in annual
value across industries. But averages obscure reality: **companies with mature AI
programs grow 2.6x faster** than those still experimenting.

The time-to-insight for strategic decisions has dropped 70% in AI-native organizations.
Your competitor is getting answers in 4 minutes that used to take 4 hours.

## What's Actually Changing in 2026

**Agents replaced dashboards.** The shift from AI that generates reports to AI that
acts on them is the defining change of 2026. Autonomous agents handle routine
research, data analysis, and report generation — freeing analysts for judgment work.

**The cost curve collapsed.** The cost per AI-generated insight dropped 73% between
2024 and 2026. What required a $200K/year analyst team in 2024 runs for $8,000/month
in 2026. Competitive advantage now comes from application, not access.

## The 12-Month Action Plan

1. **Deploy a RAG system** on your internal documentation — 3-week implementation
2. **Automate your highest-volume knowledge work** first (reports, research, triage)
3. **Measure AI ROI monthly** — build the business case before scaling
4. **Train your team** on AI oversight, not AI operation
5. **Set governance before scale** — define what AI can and cannot decide autonomously

---

*Editor's Note: Quality Score 8.5/10. Strengthened opening hook and sharpened action items.
Publication status: Ready.*

---
*[DEMO MODE — Set ANTHROPIC_API_KEY for real AI-generated content]*
"""

    filepath = save_article(topic, demo_article)
    return {
        "output":   demo_article,
        "filepath": filepath,
        "tasks_output": []
    }

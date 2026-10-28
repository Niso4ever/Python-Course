"""
tasks.py — Define the tasks each agent must complete.

A Task is an assignment: what to do, who does it, and what a good result looks like.
The `expected_output` field is like a rubric — it shapes the agent's response.

In 2026: Tasks are defined by content strategists and reviewed by editors.
The AI agents execute them. This separation of task definition from execution
is what makes multi-agent systems maintainable at scale.
"""

from crewai import Task


def create_tasks(researcher, writer, editor, content_brief: dict):
    """
    Create the 3 sequential tasks for the content studio pipeline.

    Args:
        researcher, writer, editor: Agent instances from agents.py
        content_brief: {
            "topic": str,
            "audience": str,
            "format": str,
            "word_count": int,
            "tone": str
        }

    Returns: [research_task, writing_task, editing_task]
    """
    topic      = content_brief.get("topic", "AI in 2026")
    audience   = content_brief.get("audience", "business executives and technology leaders")
    article_format = content_brief.get("format", "analytical article")
    word_count = content_brief.get("word_count", 600)
    tone       = content_brief.get("tone", "authoritative but accessible")

    # ── Task 1: Research ───────────────────────────────────────────
    research_task = Task(
        description=(
            f"Research the following topic comprehensively: **{topic}**\n\n"
            f"Target audience: {audience}\n\n"
            f"Required research elements:\n"
            f"1. Current market size and growth rates (find specific numbers)\n"
            f"2. 3-5 concrete examples or case studies from 2025-2026\n"
            f"3. Key trends shaping this topic in 2026\n"
            f"4. Common challenges or barriers\n"
            f"5. Expert opinions or analyst predictions\n"
            f"6. Surprising or counterintuitive findings (these make articles shareable)\n\n"
            f"Search multiple angles. Prioritize recent data (2025-2026). "
            f"Record specific statistics with context — not just numbers, but what they mean."
        ),
        expected_output=(
            f"A structured research brief containing:\n"
            f"- Executive Summary: 2-3 sentence overview of what the research found\n"
            f"- Key Statistics: 5-8 specific, sourced data points with context\n"
            f"- Case Studies: 2-3 real examples with outcomes\n"
            f"- Trend Analysis: 3 trends shaping the topic in 2026\n"
            f"- Surprising Findings: 1-2 counterintuitive facts\n"
            f"- Recommended Story Angle: what the writer should emphasize\n"
            f"Format: clean, organized notes ready to hand to a writer."
        ),
        agent=researcher
    )

    # ── Task 2: Writing ────────────────────────────────────────────
    writing_task = Task(
        description=(
            f"Write a {word_count}-word {article_format} on: **{topic}**\n\n"
            f"Audience: {audience}\n"
            f"Tone: {tone}\n\n"
            f"Use the research notes provided by the Research Analyst.\n\n"
            f"Article structure:\n"
            f"1. **Hook** (first sentence): start with the most striking statistic or insight\n"
            f"2. **Context** (1 paragraph): why this matters now, in 2026\n"
            f"3. **Key Findings** (2-3 sections with subheadings): "
            f"data, examples, analysis\n"
            f"4. **Implications** (1 section): what this means for the reader's work\n"
            f"5. **Action Items** (3-5 bullet points): what to do next\n\n"
            f"Style rules:\n"
            f"- Every claim supported by data from the research\n"
            f"- Active voice throughout\n"
            f"- Short sentences (average under 20 words)\n"
            f"- No jargon without explanation\n"
            f"- Subheadings every 150-200 words"
        ),
        expected_output=(
            f"A complete {word_count}-word {article_format} in Markdown format:\n"
            f"- Title: compelling, SEO-aware (under 70 characters)\n"
            f"- Subtitle: descriptive (1 sentence)\n"
            f"- All sections as described in the brief\n"
            f"- Word count within ±10% of {word_count}\n"
            f"- All statistics cited inline in brackets [source: ...]\n"
            f"- Ready for editorial review — no placeholders"
        ),
        agent=writer,
        context=[research_task]   # ← writer receives researcher's output
    )

    # ── Task 3: Editing ────────────────────────────────────────────
    editing_task = Task(
        description=(
            f"Review and improve the article draft about: **{topic}**\n\n"
            f"Editorial checklist:\n"
            f"□ Accuracy: do all statistics check out against the research?\n"
            f"□ Clarity: is every sentence immediately understandable?\n"
            f"□ Structure: does the article flow logically from hook to action?\n"
            f"□ Tone: does it match '{tone}'?\n"
            f"□ Strength of hook: does the first sentence demand attention?\n"
            f"□ Quality of action items: are they specific and achievable?\n"
            f"□ Word count: within target range?\n\n"
            f"Your job: improve the draft, not just annotate it. "
            f"Return the edited article, not a list of suggested changes. "
            f"Add your editor's note at the end."
        ),
        expected_output=(
            f"1. **Edited Article** (full, publication-ready Markdown):\n"
            f"   - All improvements applied directly to the text\n"
            f"   - No tracked changes or annotations in the body\n"
            f"   - Title, subtitle, and all sections complete\n\n"
            f"2. **Editor's Note** (at the end, in italics):\n"
            f"   - Quality Score: X/10\n"
            f"   - Key changes made and why\n"
            f"   - Any remaining concerns\n"
            f"   - Publication readiness: Ready / Needs revision"
        ),
        agent=editor,
        context=[research_task, writing_task]   # ← editor sees both research and draft
    )

    return [research_task, writing_task, editing_task]

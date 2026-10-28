"""
main.py — AI Content Studio CLI

Usage:
    python main.py                    # interactive mode
    python main.py --demo             # demo without API key
    python main.py --topic "AI topic" # run with specific topic
"""

import sys
import os
from dotenv import load_dotenv

load_dotenv()

DEMO_MODE = "--demo" in sys.argv
VERBOSE   = "--quiet" not in sys.argv

SAMPLE_BRIEFS = [
    {
        "topic":      "How AI Agents Are Replacing Knowledge Workers in 2026",
        "audience":   "C-suite executives and business leaders",
        "format":     "analytical article",
        "word_count": 650,
        "tone":       "authoritative, data-driven, direct"
    },
    {
        "topic":      "The ROI of Enterprise AI: Real Numbers from 2025-2026",
        "audience":   "CFOs and finance leaders",
        "format":     "data-driven briefing",
        "word_count": 600,
        "tone":       "precise, evidence-based, actionable"
    },
    {
        "topic":      "Building AI-Ready Teams: Skills That Matter in 2026",
        "audience":   "HR leaders and talent acquisition professionals",
        "format":     "strategic guide",
        "word_count": 700,
        "tone":       "practical, forward-looking, encouraging"
    },
    {
        "topic":      "RAG Systems: Why Every Enterprise Needs One Now",
        "audience":   "CTOs and technical leaders",
        "format":     "technical article",
        "word_count": 600,
        "tone":       "technical but accessible, solution-focused"
    },
]


def print_brief(brief: dict):
    print(f"\n  Topic:    {brief['topic']}")
    print(f"  Audience: {brief['audience']}")
    print(f"  Format:   {brief['format']} | {brief['word_count']} words")
    print(f"  Tone:     {brief['tone']}")


def run_interactive():
    print("\n" + "="*60)
    print("NEXUS AI CONTENT STUDIO")
    print("3-Agent Pipeline: Research → Write → Edit")
    print("="*60)

    print("\nChoose a content brief:\n")
    for i, brief in enumerate(SAMPLE_BRIEFS, 1):
        print(f"  {i}. {brief['topic'][:55]}...")
    print(f"  {len(SAMPLE_BRIEFS)+1}. Enter custom brief")
    print()

    try:
        choice = input("Choice: ").strip()
    except (EOFError, KeyboardInterrupt):
        return

    if choice.isdigit() and 1 <= int(choice) <= len(SAMPLE_BRIEFS):
        brief = SAMPLE_BRIEFS[int(choice) - 1]
    else:
        try:
            topic    = input("Topic: ").strip()
            audience = input("Audience (e.g. 'business executives'): ").strip() or "business leaders"
            wc       = input("Word count (default 600): ").strip()
            brief    = {
                "topic": topic,
                "audience": audience,
                "format": "article",
                "word_count": int(wc) if wc.isdigit() else 600,
                "tone": "professional and informative"
            }
        except (EOFError, KeyboardInterrupt):
            return

    print("\nRunning crew with this brief:")
    print_brief(brief)

    if DEMO_MODE or not os.getenv("ANTHROPIC_API_KEY"):
        from crew import run_demo
        result = run_demo(brief)
    else:
        try:
            from crew import run_content_studio
            result = run_content_studio(brief, verbose=VERBOSE)
        except ImportError as e:
            print(f"\nMissing dependency: {e}")
            print("Run: pip install -r requirements.txt")
            return

    print("\n" + "="*60)
    print("FINAL ARTICLE:")
    print("="*60)
    print(result["output"])
    print(f"\nSaved to: {result['filepath']}")


if __name__ == "__main__":
    if DEMO_MODE or not os.getenv("ANTHROPIC_API_KEY"):
        if not DEMO_MODE:
            print("No ANTHROPIC_API_KEY found — running demo mode.")
        DEMO_MODE = True

    if "--topic" in sys.argv:
        idx = sys.argv.index("--topic")
        topic = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else None
        if topic:
            brief = {
                "topic": topic,
                "audience": "business and technology leaders",
                "format": "analytical article",
                "word_count": 600,
                "tone": "authoritative and actionable"
            }
            if DEMO_MODE:
                from crew import run_demo
                result = run_demo(brief)
            else:
                from crew import run_content_studio
                result = run_content_studio(brief, verbose=VERBOSE)
            print(result["output"])
        else:
            print("Usage: python main.py --topic 'Your topic here'")
    else:
        run_interactive()

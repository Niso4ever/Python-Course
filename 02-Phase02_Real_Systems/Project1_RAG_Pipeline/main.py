"""
main.py — Interactive Nexus AI Knowledge Assistant

Usage:
    python main.py            # Real mode (needs ANTHROPIC_API_KEY + ingest.py run first)
    python main.py --demo     # Demo mode (no API key or DB needed)
    python main.py --verbose  # Show retrieved chunks before answer

In 2026, this runs as a web service with a React frontend.
This version is the core engine — the terminal interface is for development.
"""

import sys
import os
from dotenv import load_dotenv

load_dotenv()

DEMO_MODE = "--demo" in sys.argv
VERBOSE   = "--verbose" in sys.argv or "-v" in sys.argv

BANNER = """
╔═══════════════════════════════════════════════════════════╗
║         NEXUS AI — Internal Knowledge Assistant           ║
║              Powered by Claude Sonnet 5.5                 ║
║                    Version 3.0 (2026)                     ║
╚═══════════════════════════════════════════════════════════╝
"""

SAMPLE_QUESTIONS = [
    "What is NexusRAG and how much does it cost?",
    "What are the open engineering roles and their salaries?",
    "What is the uptime SLA for enterprise customers?",
    "How does Nexus AI handle customer data security?",
    "What is on the 2026 product roadmap?",
    "How many customers does Nexus AI have?",
    "What is the parental leave policy?",
    "Which LLM providers does Nexus AI support?",
]


def print_result(result: dict, verbose: bool = False):
    """Pretty-print a RAG result."""
    print()
    print("─" * 60)
    print("ANSWER:")
    print("─" * 60)
    print(result["answer"])
    print()

    if result["sources"]:
        print(f"Sources: {', '.join(result['sources'])}")

    if result["tokens"]["input"] > 0:
        total_tokens = result["tokens"]["input"] + result["tokens"]["output"]
        # Rough cost estimate: Sonnet 5.5 ~$2/M input, $10/M output (pricing page, 2026-10-28)
        cost = (result["tokens"]["input"] * 0.000002 +
                result["tokens"]["output"] * 0.00001)
        print(f"Tokens: {total_tokens:,} | Cost: ~${cost:.4f}")

    if verbose and result["chunks"]:
        print()
        print("Retrieved chunks:")
        for i, chunk in enumerate(result["chunks"], 1):
            print(f"  [{i}] distance={chunk['distance']:.4f} | "
                  f"{chunk['text'][:80].strip()}...")

    print("─" * 60)


def run_demo():
    """Run in demo mode — no API key or database required."""
    from retriever import answer_demo

    print(BANNER)
    print("  MODE: DEMO (simulated responses)")
    print("  To use real AI: set ANTHROPIC_API_KEY and run `python ingest.py` first")
    print()
    print("Sample questions you can ask:")
    for i, q in enumerate(SAMPLE_QUESTIONS, 1):
        print(f"  {i}. {q}")
    print()
    print("Type 'quit' or 'exit' to stop.")
    print()

    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not question:
            continue
        if question.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        # Handle numeric shortcuts
        if question.isdigit() and 1 <= int(question) <= len(SAMPLE_QUESTIONS):
            question = SAMPLE_QUESTIONS[int(question) - 1]
            print(f"You: {question}")

        result = answer_demo(question)
        print_result(result, verbose=VERBOSE)
        print()


def run_real():
    """Run with real Claude API and ChromaDB."""
    from retriever import answer, search

    # Check if ChromaDB exists
    db_path = os.getenv("CHROMA_DB_PATH", "./chroma_db")
    if not os.path.exists(db_path):
        print("ERROR: ChromaDB not found.")
        print("Run `python ingest.py` first to build the knowledge base.")
        sys.exit(1)

    print(BANNER)
    print("  MODE: REAL (Claude Sonnet 5.5 + ChromaDB)")
    print("  Knowledge base loaded and ready.")
    print()
    print("Sample questions:")
    for i, q in enumerate(SAMPLE_QUESTIONS, 1):
        print(f"  {i}. {q}")
    print()
    print("Type a number (1-8), your own question, or 'quit' to exit.")
    print()

    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not question:
            continue
        if question.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        # Numeric shortcut
        if question.isdigit() and 1 <= int(question) <= len(SAMPLE_QUESTIONS):
            question = SAMPLE_QUESTIONS[int(question) - 1]
            print(f"You: {question}")

        print("Searching knowledge base...")
        try:
            result = answer(question, verbose=VERBOSE)
            print_result(result, verbose=VERBOSE)
        except Exception as e:
            print(f"Error: {e}")
            print("Tip: Make sure ANTHROPIC_API_KEY is set and ingest.py has been run.")
        print()


if __name__ == "__main__":
    if DEMO_MODE:
        run_demo()
    else:
        # Check for API key
        if not os.getenv("ANTHROPIC_API_KEY"):
            print("No ANTHROPIC_API_KEY found. Running in demo mode.")
            print("(Use --demo flag or set ANTHROPIC_API_KEY in .env)\n")
            run_demo()
        else:
            try:
                run_real()
            except ImportError as e:
                print(f"Missing dependency: {e}")
                print("Run: pip install -r requirements.txt")

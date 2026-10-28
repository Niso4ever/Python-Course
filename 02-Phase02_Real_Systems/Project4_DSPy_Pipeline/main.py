"""
main.py — Smart Triage System CLI

Usage:
    python main.py              # interactive mode
    python main.py --demo       # demo without API key
    python main.py --batch      # process batch of sample tickets

In 2026, this runs as:
  - A webhook that fires when a new support ticket arrives
  - A batch processor that runs every 15 minutes
  - A real-time API called by the support portal frontend
"""

import sys
import os
from dotenv import load_dotenv

load_dotenv()

DEMO_MODE = "--demo" in sys.argv
BATCH_MODE = "--batch" in sys.argv

# Sample tickets that demonstrate different scenarios
SAMPLE_TICKETS = [
    {
        "id": "TKT-2026-001",
        "text": (
            "CRITICAL: Our entire production system is down. All NexusRAG API calls "
            "are failing with 503 errors. We have 80,000 active users affected. "
            "This has been happening for 15 minutes. We're losing approximately "
            "$15,000 per minute in revenue. Please escalate immediately."
        )
    },
    {
        "id": "TKT-2026-002",
        "text": (
            "Hello, I noticed I was charged $299 twice this month (Feb 28 and Mar 1). "
            "I think this might be related to my renewal. Can you check and refund "
            "the duplicate charge? My account email is sarah@acmecorp.com."
        )
    },
    {
        "id": "TKT-2026-003",
        "text": (
            "Feature request: It would be really useful if NexusRAG supported "
            "real-time document sync. Right now we have to manually re-ingest "
            "when documents change. Auto-sync with Google Drive would save our "
            "team a lot of time. Is this on your roadmap?"
        )
    },
    {
        "id": "TKT-2026-004",
        "text": (
            "Hi! I'm new to NexusRAG and trying to set up my first knowledge base. "
            "I've uploaded 50 PDFs but the search doesn't seem to return relevant results. "
            "Am I doing something wrong? I followed the quick start guide but I'm stuck."
        )
    },
    {
        "id": "TKT-2026-005",
        "text": (
            "Security concern: one of our ex-employees may still have API access. "
            "They left the company last week and we forgot to revoke their credentials. "
            "We handle medical records (HIPAA) and need this resolved urgently."
        )
    },
]


def run_demo():
    """Demonstrate triage results without API calls."""
    print("\n" + "="*60)
    print("NEXUS AI — SMART TRIAGE SYSTEM (DEMO)")
    print("Powered by DSPy + Claude Haiku 5.5")
    print("="*60)
    print()

    ticket = SAMPLE_TICKETS[0]
    print(f"Ticket: {ticket['id']}")
    print(f"Text: {ticket['text'][:120]}...")
    print()
    print("Running triage pipeline...")
    print()

    # Simulate the 4-step pipeline output
    print("Step 1 [CLASSIFY]")
    print("  → category: technical_issue")
    print("  → subcategory: api_outage")
    print("  → confidence: 0.99")
    print("  → key_issue: Full production outage with 80,000 users affected")
    print()
    print("Step 2 [ASSESS SEVERITY]")
    print("  → severity: CRITICAL 🔴")
    print("  → sla_hours: 2")
    print("  → urgency_reason: Complete service unavailability with revenue loss at $15K/min")
    print()
    print("Step 3 [ROUTE]")
    print("  → team: tier2_technical")
    print("  → agent_tier: specialist")
    print("  → escalate_now: TRUE 🚨")
    print()
    print("Step 4 [DRAFT RESPONSE]")
    print("  → tone: urgent + reassuring")
    print()
    print("─" * 60)
    print("DRAFT EMAIL:")
    print("─" * 60)
    print("""Subject: [CRITICAL] Production Outage — Immediate Response | TKT-2026-001

We have immediately escalated your report to our on-call engineering team.
This is being treated as a Critical incident (P0).

We can confirm we are investigating the 503 errors affecting your production
environment. Our engineers have been paged and are actively investigating.

Timeline: You will receive a status update within 15 minutes, and we are
targeting service restoration within 2 hours. Our engineering lead will
contact you directly at the email associated with your account.

If you need to reach us immediately: call our critical hotline at
1-800-NEXUS-AI (available 24/7 for enterprise customers).

We understand the severity of this situation and the revenue impact.
Our full team is on this.

— Nexus AI Incident Response Team""")
    print("─" * 60)
    print()
    print("[DEMO] Set ANTHROPIC_API_KEY in .env to run real DSPy triage")


def triage_ticket(ticket_text: str, pipeline) -> str:
    """Run a single ticket through the triage pipeline."""
    from pipeline import format_triage_result
    result = pipeline(ticket_text=ticket_text)
    return format_triage_result(result)


def run_batch(pipeline):
    """Process all sample tickets in batch mode."""
    from pipeline import format_triage_result

    print("\n" + "="*60)
    print(f"BATCH TRIAGE — {len(SAMPLE_TICKETS)} tickets")
    print("="*60)

    for ticket in SAMPLE_TICKETS:
        print(f"\nProcessing: {ticket['id']}")
        print(f"Text: {ticket['text'][:80]}...")
        try:
            result = pipeline(ticket_text=ticket["text"])
            print(f"  → {result.severity.upper()} | {result.category} | {result.team}")
            if result.escalate_now:
                print(f"  🚨 ESCALATE NOW")
        except Exception as e:
            print(f"  ERROR: {e}")


def run_interactive(pipeline):
    """Interactive mode: triage tickets one at a time."""
    from pipeline import format_triage_result

    print("\n" + "="*60)
    print("NEXUS AI — SMART TRIAGE SYSTEM")
    print("Powered by DSPy + Claude Haiku 5.5")
    print("="*60)

    print("\nSample tickets (enter number):")
    for i, t in enumerate(SAMPLE_TICKETS, 1):
        print(f"  {i}. [{t['id']}] {t['text'][:65]}...")
    print(f"  {len(SAMPLE_TICKETS)+1}. Enter custom ticket")
    print("  'quit' to exit\n")

    while True:
        try:
            choice = input("Select ticket: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if choice.lower() in ("quit", "exit", "q"):
            break

        if choice.isdigit() and 1 <= int(choice) <= len(SAMPLE_TICKETS):
            ticket_text = SAMPLE_TICKETS[int(choice) - 1]["text"]
            print(f"\nTicket text:\n{ticket_text}\n")
        elif choice.isdigit() and int(choice) == len(SAMPLE_TICKETS) + 1:
            try:
                ticket_text = input("Paste ticket text: ").strip()
            except (EOFError, KeyboardInterrupt):
                break
        else:
            ticket_text = choice  # treat as raw ticket text

        if not ticket_text:
            continue

        print("\nRunning triage...")
        try:
            result = pipeline(ticket_text=ticket_text)
            print(format_triage_result(result))
        except Exception as e:
            print(f"Error: {e}")
        print()


if __name__ == "__main__":
    if DEMO_MODE:
        run_demo()
        exit(0)

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("No ANTHROPIC_API_KEY found — running demo mode.")
        print("(Set in .env for real DSPy triage)\n")
        run_demo()
        exit(0)

    try:
        from pipeline import setup_dspy, load_pipeline

        print("Setting up DSPy...")
        setup_dspy()

        print("Loading triage pipeline...")
        pipeline = load_pipeline()

        if BATCH_MODE:
            run_batch(pipeline)
        else:
            run_interactive(pipeline)

    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Run: pip install -r requirements.txt")

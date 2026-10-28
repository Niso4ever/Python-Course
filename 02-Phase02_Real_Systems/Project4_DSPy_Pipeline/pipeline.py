"""
pipeline.py — DSPy TriagePipeline module.

This is a dspy.Module that chains 4 signatures into a complete pipeline.
Like an L4 class: __init__ sets up the steps, forward() executes them.

The pipeline is composable:
  - Can be used as-is (unoptimized)
  - Can be compiled with BootstrapFewShot (optimized)
  - Can be saved and loaded without re-training

In 2026: compiled pipelines are the artifact that ML teams deploy.
They get versioned, tested, and monitored like any other code.
"""

import os
import dspy
from signatures import ClassifyTicket, AssessSeverity, RouteTicket, DraftResponse

TRIAGE_MODEL       = os.getenv("TRIAGE_MODEL", "anthropic/claude-haiku-5-5")
COMPILED_PATH      = os.getenv("COMPILED_PIPELINE_PATH", "./compiled_triage.json")


def setup_dspy(model: str = TRIAGE_MODEL):
    """Configure DSPy with Anthropic LLM. Call once at startup."""
    lm = dspy.LM(model)
    dspy.configure(lm=lm)
    return lm


class TriagePipeline(dspy.Module):
    """
    Full 4-step ticket triage pipeline.

    Steps:
    1. Classify: what type of ticket is this?
    2. Assess: how severe/urgent is it?
    3. Route: which team handles it?
    4. Draft: write the first-response email

    Each step uses ChainOfThought for better reasoning on ambiguous tickets.
    Step 3 (routing) uses Predict — it's more rule-based, less reasoning needed.
    """

    def __init__(self):
        super().__init__()   # ← required for dspy.Module
        self.classify = dspy.ChainOfThought(ClassifyTicket)    # step 1
        self.assess   = dspy.ChainOfThought(AssessSeverity)    # step 2
        self.route    = dspy.Predict(RouteTicket)              # step 3
        self.draft    = dspy.ChainOfThought(DraftResponse)     # step 4

    def forward(self, ticket_text: str) -> dspy.Prediction:
        """
        Run the full triage pipeline on a single ticket.

        IN:  ticket_text (str) — the raw customer message
        OUT: dspy.Prediction with all fields populated
        """
        # Step 1: Classify
        classification = self.classify(ticket_text=ticket_text)

        # Step 2: Assess severity (uses classification output)
        assessment = self.assess(
            ticket_text=ticket_text,
            category=classification.category,
            key_issue=classification.key_issue
        )

        # Step 3: Route (uses both classification and assessment)
        routing = self.route(
            category=classification.category,
            subcategory=classification.subcategory,
            severity=assessment.severity,
            key_issue=classification.key_issue
        )

        # Step 4: Draft response (uses everything above)
        response = self.draft(
            ticket_text=ticket_text,
            category=classification.category,
            severity=assessment.severity,
            sla_hours=assessment.sla_hours,
            customer_impact=assessment.customer_impact
        )

        # Return a combined prediction with all fields
        # (merge all step outputs into one object)
        return dspy.Prediction(
            # Classification
            category       = classification.category,
            subcategory    = classification.subcategory,
            confidence     = classification.confidence,
            key_issue      = classification.key_issue,
            # Assessment
            severity       = assessment.severity,
            urgency_reason = assessment.urgency_reason,
            sla_hours      = assessment.sla_hours,
            customer_impact= assessment.customer_impact,
            # Routing
            team           = routing.team,
            agent_tier     = routing.agent_tier,
            escalate_now   = routing.escalate_now,
            routing_reason = routing.routing_reason,
            # Response
            email_subject  = response.email_subject,
            email_body     = response.email_body,
            tone           = response.tone,
        )


def load_pipeline(compiled_path: str = COMPILED_PATH) -> TriagePipeline:
    """
    Load a compiled (optimized) pipeline from disk.
    Falls back to unoptimized pipeline if no compiled version exists.
    """
    pipeline = TriagePipeline()

    if os.path.exists(compiled_path):
        try:
            pipeline.load(compiled_path)
            print(f"✓ Loaded optimized pipeline from: {compiled_path}")
        except Exception as e:
            print(f"⚠ Could not load compiled pipeline ({e}). Using unoptimized.")
    else:
        print("ℹ No compiled pipeline found. Using unoptimized baseline.")
        print(f"  Run `python optimizer.py` to train and save an optimized pipeline.")

    return pipeline


def format_triage_result(result: dspy.Prediction) -> str:
    """
    Format a triage result as readable text.
    Used for CLI display and logging.
    """
    escalate_flag = "🚨 ESCALATE NOW" if result.escalate_now else "✓ Normal routing"

    severity_icons = {
        "critical": "🔴",
        "high":     "🟠",
        "medium":   "🟡",
        "low":      "🟢"
    }
    sev_icon = severity_icons.get(str(result.severity).lower(), "⚪")

    return f"""
{'='*60}
TRIAGE RESULT
{'='*60}
{escalate_flag}

CLASSIFICATION
  Category:    {result.category} / {result.subcategory}
  Confidence:  {float(result.confidence):.0%}
  Issue:       {result.key_issue}

SEVERITY
  Level:       {sev_icon} {result.severity.upper()}
  SLA:         Response within {result.sla_hours} hours
  Impact:      {result.customer_impact}
  Reason:      {result.urgency_reason}

ROUTING
  Team:        {result.team}
  Agent tier:  {result.agent_tier}
  Why:         {result.routing_reason}

DRAFT EMAIL
  Subject:     {result.email_subject}
  Tone:        {result.tone}
  ─────────────────────────────────────────
{result.email_body}
{'='*60}"""

"""
signatures.py — DSPy signatures for the Smart Triage System.

Each signature is an input→output declaration.
No prompt text. DSPy generates the prompt from:
  - The class name
  - The class docstring
  - The field names and desc= values
  - (After optimization) few-shot examples from your data

In 2026: signature files are maintained by ML engineers.
They define WHAT the system does. The optimizer figures out HOW.
"""

import dspy


# ═══════════════════════════════════════════════════════════
# SIGNATURE 1: Classify the ticket
# ═══════════════════════════════════════════════════════════
class ClassifyTicket(dspy.Signature):
    """
    Classify a customer support ticket into a category and subcategory.
    Determine what the customer is asking about and how confident you are.
    """
    ticket_text:  str   = dspy.InputField(
        desc="The full text of the customer support ticket, email, or chat message"
    )

    category:     str   = dspy.OutputField(
        desc=(
            "Primary category. One of: "
            "billing, technical_issue, feature_request, account_management, "
            "onboarding, security, compliance, other"
        )
    )
    subcategory:  str   = dspy.OutputField(
        desc="Specific subcategory within the main category (2-5 words)"
    )
    confidence:   float = dspy.OutputField(
        desc="Classification confidence from 0.0 (uncertain) to 1.0 (certain)"
    )
    key_issue:    str   = dspy.OutputField(
        desc="One-sentence summary of the core problem or request"
    )


# ═══════════════════════════════════════════════════════════
# SIGNATURE 2: Assess severity and urgency
# ═══════════════════════════════════════════════════════════
class AssessSeverity(dspy.Signature):
    """
    Assess the severity and business impact of a support ticket.
    Consider: how many users affected, revenue impact, data/security risk,
    and whether the issue is blocking the customer's operations.
    """
    ticket_text:   str = dspy.InputField(
        desc="The full text of the customer support ticket"
    )
    category:      str = dspy.InputField(
        desc="The ticket category already classified"
    )
    key_issue:     str = dspy.InputField(
        desc="One-sentence summary of the core issue"
    )

    severity:      str   = dspy.OutputField(
        desc="One of: critical, high, medium, low"
    )
    urgency_reason: str  = dspy.OutputField(
        desc="Why this severity level — specific business impact in 1-2 sentences"
    )
    sla_hours:     int   = dspy.OutputField(
        desc=(
            "Hours until first human response required. "
            "critical=2, high=8, medium=24, low=72"
        )
    )
    customer_impact: str = dspy.OutputField(
        desc="Brief description of impact on the customer's business (1 sentence)"
    )


# ═══════════════════════════════════════════════════════════
# SIGNATURE 3: Route to the right team
# ═══════════════════════════════════════════════════════════
class RouteTicket(dspy.Signature):
    """
    Determine which team and tier should handle this ticket,
    and whether it requires immediate human escalation.
    """
    category:      str = dspy.InputField()
    subcategory:   str = dspy.InputField()
    severity:      str = dspy.InputField()
    key_issue:     str = dspy.InputField()

    team:          str  = dspy.OutputField(
        desc=(
            "Team responsible. One of: "
            "tier1_support, tier2_technical, billing_team, "
            "security_team, customer_success, engineering, executive_escalation"
        )
    )
    agent_tier:    str  = dspy.OutputField(
        desc="Agent skill level required: junior, senior, specialist, manager"
    )
    escalate_now:  bool = dspy.OutputField(
        desc="True if this requires IMMEDIATE human attention (not just routing)"
    )
    routing_reason: str = dspy.OutputField(
        desc="Why this team and tier (1 sentence)"
    )


# ═══════════════════════════════════════════════════════════
# SIGNATURE 4: Draft the first-response email
# ═══════════════════════════════════════════════════════════
class DraftResponse(dspy.Signature):
    """
    Draft a professional, empathetic first-response email to the customer.
    The email should acknowledge their issue, set expectations, and
    provide any immediate helpful information available.
    """
    ticket_text:     str = dspy.InputField(
        desc="Original customer message"
    )
    category:        str = dspy.InputField()
    severity:        str = dspy.InputField()
    sla_hours:       int = dspy.InputField(
        desc="Hours until they'll receive full resolution or update"
    )
    customer_impact: str = dspy.InputField()

    email_subject:   str = dspy.OutputField(
        desc="Email subject line (concise, professional, references their issue)"
    )
    email_body:      str = dspy.OutputField(
        desc=(
            "Full email body (3-5 paragraphs): "
            "1) Acknowledge and empathize, "
            "2) Confirm you understand the issue, "
            "3) What happens next + timeline, "
            "4) Any immediate self-service help, "
            "5) Professional close. "
            "Do NOT use placeholders like [Name] — write complete sentences."
        )
    )
    tone:            str = dspy.OutputField(
        desc="Tone used: one of empathetic, professional, urgent, reassuring"
    )

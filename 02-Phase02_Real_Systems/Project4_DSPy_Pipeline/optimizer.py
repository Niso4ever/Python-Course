"""
optimizer.py — Train and optimize the triage pipeline using DSPy BootstrapFewShot.

This script:
1. Defines labeled training examples (tickets + correct triage decisions)
2. Defines quality metrics (what "correct" means)
3. Runs the optimizer to find the best few-shot examples
4. Saves the compiled pipeline to disk

In 2026: This runs weekly. New tickets from the previous week that were
human-reviewed get added to the training set. The pipeline continuously
improves without any prompt engineering.

Before running: pip install dspy anthropic
"""

import os
import dspy
from dotenv import load_dotenv
from pipeline import TriagePipeline, setup_dspy, COMPILED_PATH

load_dotenv()


# ═══════════════════════════════════════════════════════════
# TRAINING DATA
# Each example: ticket_text → expected triage outputs
# In production: 100-500 examples from human-reviewed tickets
# ═══════════════════════════════════════════════════════════

TRAINING_EXAMPLES = [
    dspy.Example(
        ticket_text=(
            "URGENT: Our entire production environment is down. All API calls are "
            "returning 503 errors. We have 50,000 active users who cannot access "
            "the platform. This started 20 minutes ago. We're losing $10,000/minute."
        ),
        category="technical_issue",
        severity="critical",
        team="tier2_technical",
        escalate_now=True
    ).with_inputs("ticket_text"),

    dspy.Example(
        ticket_text=(
            "Hi, I was charged twice for my subscription this month. "
            "I see two charges of $299 on my credit card statement from March 1st. "
            "Please refund one of them. Order numbers: INV-2026-8821 and INV-2026-8834."
        ),
        category="billing",
        severity="medium",
        team="billing_team",
        escalate_now=False
    ).with_inputs("ticket_text"),

    dspy.Example(
        ticket_text=(
            "I'd love to see a bulk export feature in NexusRAG. It would be great "
            "to export all search results to CSV or Excel for offline analysis. "
            "Would save our data team hours each week."
        ),
        category="feature_request",
        severity="low",
        team="tier1_support",
        escalate_now=False
    ).with_inputs("ticket_text"),

    dspy.Example(
        ticket_text=(
            "We suspect our API key may have been compromised. I found it in a "
            "public GitHub repository that one of our developers accidentally committed to. "
            "I've already revoked it in the dashboard but I'm worried about unauthorized "
            "access that may have occurred. Can you check our access logs for the past week?"
        ),
        category="security",
        severity="high",
        team="security_team",
        escalate_now=True
    ).with_inputs("ticket_text"),

    dspy.Example(
        ticket_text=(
            "Just getting started with NexusRAG! I've uploaded my first documents "
            "but I'm not sure how to set up the search. The tutorial was a bit confusing. "
            "Is there a video walkthrough or someone who can help me get started?"
        ),
        category="onboarding",
        severity="low",
        team="tier1_support",
        escalate_now=False
    ).with_inputs("ticket_text"),

    dspy.Example(
        ticket_text=(
            "We need a Business Associate Agreement (BAA) for HIPAA compliance. "
            "Our legal team requires this before we can proceed with the enterprise plan. "
            "We're a healthcare company and this is a hard blocker for the purchase."
        ),
        category="compliance",
        severity="high",
        team="customer_success",
        escalate_now=False
    ).with_inputs("ticket_text"),

    dspy.Example(
        ticket_text=(
            "The semantic search results have become noticeably worse over the past week. "
            "Queries that used to return highly relevant results are now returning "
            "unrelated documents. Did something change in the embedding model? "
            "We're on the Professional plan."
        ),
        category="technical_issue",
        severity="high",
        team="tier2_technical",
        escalate_now=False
    ).with_inputs("ticket_text"),

    dspy.Example(
        ticket_text=(
            "Can I add 3 more users to my Starter plan? We have 5 seats and need 8. "
            "Or should I upgrade to Professional?"
        ),
        category="account_management",
        severity="low",
        team="billing_team",
        escalate_now=False
    ).with_inputs("ticket_text"),

    dspy.Example(
        ticket_text=(
            "ERROR: AttributeError: 'NoneType' object has no attribute 'embeddings'. "
            "This is happening when I call the Python SDK: nexus.rag.search(query='test'). "
            "Stack trace attached. Using SDK version 2.4.1 on Python 3.12."
        ),
        category="technical_issue",
        severity="medium",
        team="tier2_technical",
        escalate_now=False
    ).with_inputs("ticket_text"),

    dspy.Example(
        ticket_text=(
            "We're evaluating NexusRAG for our 500-person legal firm. We need to understand "
            "your data handling: where is our data stored, is it used for training, "
            "what's the data deletion policy, and do you have SOC 2 Type II? "
            "We have a board meeting next week where we need to present this."
        ),
        category="security",
        severity="medium",
        team="customer_success",
        escalate_now=False
    ).with_inputs("ticket_text"),
]


# ═══════════════════════════════════════════════════════════
# METRICS: What does "correct" mean?
# ═══════════════════════════════════════════════════════════

def category_accuracy(example: dspy.Example, prediction: dspy.Prediction,
                       trace=None) -> bool:
    """Category must match exactly."""
    try:
        return str(example.category).lower() == str(prediction.category).lower()
    except Exception:
        return False


def severity_accuracy(example: dspy.Example, prediction: dspy.Prediction,
                       trace=None) -> bool:
    """Severity must match exactly."""
    try:
        return str(example.severity).lower() == str(prediction.severity).lower()
    except Exception:
        return False


def escalation_accuracy(example: dspy.Example, prediction: dspy.Prediction,
                         trace=None) -> bool:
    """Escalation flag must match — critical for SLA compliance."""
    try:
        exp = bool(example.escalate_now)
        pred_val = prediction.escalate_now
        # Handle string "True"/"False" if DSPy returns strings
        if isinstance(pred_val, str):
            pred_val = pred_val.lower() == "true"
        return exp == bool(pred_val)
    except Exception:
        return False


def composite_metric(example: dspy.Example, prediction: dspy.Prediction,
                      trace=None) -> float:
    """
    Composite score: weights accuracy across all three outputs.
    Escalation gets highest weight (most business-critical).
    Returns float so optimizer can compare partial scores.
    """
    score = 0.0
    score += 0.30 * float(category_accuracy(example, prediction))
    score += 0.30 * float(severity_accuracy(example, prediction))
    score += 0.40 * float(escalation_accuracy(example, prediction))  # highest weight!
    return score


# ═══════════════════════════════════════════════════════════
# OPTIMIZATION
# ═══════════════════════════════════════════════════════════

def optimize(trainset=None, save_path: str = COMPILED_PATH) -> TriagePipeline:
    """
    Compile (optimize) the triage pipeline using BootstrapFewShot.

    What BootstrapFewShot does:
    1. Runs the pipeline on training examples
    2. Finds which examples lead to correct predictions
    3. Bootstraps (auto-selects) the best few-shot examples
    4. Injects them into the compiled pipeline's prompts

    Result: compiled pipeline performs 15-30% better than baseline.
    """
    print("\n" + "="*60)
    print("TRIAGE PIPELINE OPTIMIZER")
    print("="*60)

    trainset = trainset or TRAINING_EXAMPLES
    print(f"Training examples: {len(trainset)}")
    print(f"Metric: composite (category 30% + severity 30% + escalation 40%)")
    print(f"Optimizer: BootstrapFewShot (max 3 demos per predictor)")
    print()

    # Baseline: measure uncompiled pipeline
    print("Step 1: Measuring baseline performance...")
    baseline = TriagePipeline()
    baseline_scores = []
    for ex in trainset[:5]:   # quick sample
        try:
            pred = baseline(ticket_text=ex.ticket_text)
            score = composite_metric(ex, pred)
            baseline_scores.append(score)
        except Exception as e:
            print(f"  Example failed: {e}")
            baseline_scores.append(0.0)

    avg_baseline = sum(baseline_scores) / len(baseline_scores) if baseline_scores else 0
    print(f"  Baseline score: {avg_baseline:.1%}")

    # Compile
    print("\nStep 2: Running BootstrapFewShot optimizer...")
    print("  (This makes multiple API calls — may take 2-5 minutes)")

    optimizer = dspy.BootstrapFewShot(
        metric=composite_metric,
        max_bootstrapped_demos=3,    # max few-shot examples per step
        max_labeled_demos=4,
        max_errors=5
    )

    compiled = optimizer.compile(
        student=TriagePipeline(),    # fresh pipeline to optimize
        trainset=trainset
    )

    # Save compiled pipeline
    compiled.save(save_path)
    print(f"\n✅ Compiled pipeline saved to: {save_path}")
    print(f"   Load with: pipeline.load('{save_path}')")

    # Measure optimized performance
    print("\nStep 3: Measuring optimized performance...")
    optimized_scores = []
    for ex in trainset[:5]:
        try:
            pred = compiled(ticket_text=ex.ticket_text)
            score = composite_metric(ex, pred)
            optimized_scores.append(score)
        except Exception:
            optimized_scores.append(0.0)

    avg_optimized = sum(optimized_scores) / len(optimized_scores) if optimized_scores else 0
    improvement   = (avg_optimized - avg_baseline) / max(avg_baseline, 0.001)

    print(f"\n{'='*60}")
    print(f"OPTIMIZATION RESULTS")
    print(f"  Baseline:  {avg_baseline:.1%}")
    print(f"  Optimized: {avg_optimized:.1%}")
    print(f"  Improvement: +{improvement:.1%}")
    print(f"{'='*60}")

    return compiled


if __name__ == "__main__":
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set. Set it in .env and try again.")
        exit(1)

    print("Setting up DSPy...")
    setup_dspy()

    compiled = optimize()
    print(f"\nDone! Use the compiled pipeline in main.py for better accuracy.")

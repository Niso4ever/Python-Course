"""
TEMPLATE: Confidence Threshold (Quality Gate)
==============================================
Use: Check if AI response is confident enough to return

COPY this template when you need to:
- Validate LLM response quality
- Check RAG retrieval confidence
- Gate low-quality outputs

2026 NOTE: This template correctly uses if/elif/else.
  Reason: checking a SCORE against a THRESHOLD → if/elif is the right tool.
  match/case is for routing by name/type/status, NOT for numeric comparisons.
"""

# ═══════════════════════════════════════════════════════════
# CONFIGURATION (← MODIFY THESE)
# ═══════════════════════════════════════════════════════════
CONFIDENCE_THRESHOLD = 0.90  # ← Set your quality threshold


# ═══════════════════════════════════════════════════════════
# YOUR DATA (← REPLACE WITH REAL DATA)
# ═══════════════════════════════════════════════════════════
confidence_score = 0.87  # ← From your LLM/RAG system
response = "RAG combines retrieval with generation..."  # ← AI response text


# ═══════════════════════════════════════════════════════════
# ROUTING LOGIC (No changes needed - just works!)
# ═══════════════════════════════════════════════════════════
if confidence_score >= CONFIDENCE_THRESHOLD:
    # ✓ HIGH CONFIDENCE - Safe to return
    action = "return_to_user"
    return_response = response
    flag_for_review = False
    print(f"✓ HIGH CONFIDENCE ({confidence_score:.2f})")
    print(f"  Threshold: {CONFIDENCE_THRESHOLD}")
    print(f"  Action: Returning answer to user")

else:
    # ⚠ LOW CONFIDENCE - Needs review
    action = "escalate_to_human"
    return_response = "Let me connect you with a human expert for this question."
    flag_for_review = True
    print(f"⚠ LOW CONFIDENCE ({confidence_score:.2f})")
    print(f"  Threshold: {CONFIDENCE_THRESHOLD}")
    print(f"  Action: Escalating to human review")


# ═══════════════════════════════════════════════════════════
# RESULT (Use this in your AI system)
# ═══════════════════════════════════════════════════════════
result = {
    "action": action,
    "response": return_response,
    "original_confidence": confidence_score,
    "threshold": CONFIDENCE_THRESHOLD,
    "flagged": flag_for_review
}

print(f"\n{'='*50}")
print(f"RESULT:")
print(f"{'='*50}")
print(f"Action: {result['action']}")
print(f"Flagged: {result['flagged']}")
print(f"Response: {result['response'][:60]}...")


# ═══════════════════════════════════════════════════════════
# MODIFICATION EXAMPLES
# ═══════════════════════════════════════════════════════════
"""
Example 1: Stricter threshold
------------------------------
CONFIDENCE_THRESHOLD = 0.95

Example 2: Custom fallback message
-----------------------------------
return_response = "I'm not confident in this answer. Would you like me to search more sources?"

Example 3: Three-tier system
-----------------------------
if confidence_score >= 0.95:
    action = "high_confidence"
elif confidence_score >= 0.80:
    action = "medium_confidence_with_disclaimer"
else:
    action = "low_confidence_escalate"
"""

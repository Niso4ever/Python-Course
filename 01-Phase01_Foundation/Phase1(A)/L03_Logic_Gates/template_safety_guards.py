"""
TEMPLATE: Safety Guards (Content Moderation)
=============================================
Use: Block toxic/unsafe content before processing

COPY this template when you need to:
- Content moderation
- Authorization checks
- Rate limiting
- Safety filters

2026 NOTE: This template correctly uses if/elif/else.
  Reason: checking THRESHOLDS and BOOLEAN flags → if/elif is the right tool.
  match/case is for routing by name/type/status, NOT for numeric or boolean checks.
"""

# ═══════════════════════════════════════════════════════════
# CONFIGURATION (← MODIFY THESE)
# ═══════════════════════════════════════════════════════════
MAX_TOXICITY = 0.20  # ← Toxicity threshold (0=safe, 1=toxic)
REQUIRE_AUTH = True  # ← Require user authorization?
MAX_REQUESTS_PER_MINUTE = 10  # ← Rate limit


# ═══════════════════════════════════════════════════════════
# YOUR DATA (← REPLACE WITH REAL DATA)
# ═══════════════════════════════════════════════════════════
toxicity_score = 0.15      # ← From moderation API (e.g., Perspective API)
user_is_authorized = True  # ← From your auth system
request_count = 5          # ← From rate limiter
content = "User request text..."  # ← Actual user input


# ═══════════════════════════════════════════════════════════
# SAFETY CHECKS (Add/remove checks as needed)
# ═══════════════════════════════════════════════════════════

if toxicity_score > MAX_TOXICITY:
    # ─────────────────────────────────────────────────────────
    # BLOCK: TOXIC CONTENT
    # ─────────────────────────────────────────────────────────
    status = "blocked_toxic"
    response = "I cannot respond to that request."
    allow_processing = False
    reason = f"Toxicity score {toxicity_score:.2f} exceeds limit {MAX_TOXICITY}"
    severity = "high"

    print(f"🚫 BLOCKED: Toxic Content")
    print(f"   Score: {toxicity_score:.2f} > {MAX_TOXICITY}")
    print(f"   Severity: {severity}")

elif REQUIRE_AUTH and not user_is_authorized:
    # ─────────────────────────────────────────────────────────
    # BLOCK: NOT AUTHORIZED
    # ─────────────────────────────────────────────────────────
    status = "blocked_unauthorized"
    response = "You need to be logged in to access this feature."
    allow_processing = False
    reason = "User not authorized"
    severity = "medium"

    print(f"🚫 BLOCKED: Unauthorized Access")
    print(f"   Auth required: {REQUIRE_AUTH}")
    print(f"   User authorized: {user_is_authorized}")

elif request_count >= MAX_REQUESTS_PER_MINUTE:
    # ─────────────────────────────────────────────────────────
    # BLOCK: RATE LIMIT EXCEEDED
    # ─────────────────────────────────────────────────────────
    status = "blocked_rate_limit"
    response = "You've exceeded the rate limit. Please try again in a minute."
    allow_processing = False
    reason = f"Rate limit exceeded: {request_count}/{MAX_REQUESTS_PER_MINUTE}"
    severity = "low"

    print(f"🚫 BLOCKED: Rate Limit")
    print(f"   Requests: {request_count}/{MAX_REQUESTS_PER_MINUTE}")

else:
    # ─────────────────────────────────────────────────────────
    # APPROVED: ALL CHECKS PASSED
    # ─────────────────────────────────────────────────────────
    status = "approved"
    # UNCOMMENT when you have your processing function:
    # response = process_request(content)

    # For now:
    response = "Processing your request..."
    allow_processing = True
    reason = "Passed all safety checks"
    severity = None

    print(f"✓ APPROVED: All Safety Checks Passed")
    print(f"   Toxicity: {toxicity_score:.2f} <= {MAX_TOXICITY} ✓")
    print(f"   Authorized: {user_is_authorized} ✓")
    print(f"   Rate limit: {request_count}/{MAX_REQUESTS_PER_MINUTE} ✓")


# ═══════════════════════════════════════════════════════════
# RESULT (Use this in your AI system)
# ═══════════════════════════════════════════════════════════
result = {
    "status": status,
    "response": response,
    "allowed": allow_processing,
    "reason": reason,
    "severity": severity,
    "checks": {
        "toxicity_score": toxicity_score,
        "authorized": user_is_authorized,
        "rate_limit": request_count < MAX_REQUESTS_PER_MINUTE
    }
}

print(f"\n{'='*50}")
print(f"SAFETY RESULT:")
print(f"{'='*50}")
print(f"Status: {result['status']}")
print(f"Allowed: {result['allowed']}")
print(f"Reason: {result['reason']}")


# ═══════════════════════════════════════════════════════════
# MODIFICATION EXAMPLES
# ═══════════════════════════════════════════════════════════
"""
Example 1: Add content policy check
------------------------------------
elif violates_content_policy(content):
    status = "blocked_policy"
    response = "This request violates our content policy."
    allow_processing = False

Example 2: Age restriction
---------------------------
elif user_age < 18 and content_is_adult:
    status = "blocked_age"
    response = "This content is restricted to adults."
    allow_processing = False

Example 3: Multi-level moderation
----------------------------------
if toxicity_score > 0.80:
    # Immediate block - severe
    status = "blocked_severe"
    response = "Request blocked."
elif toxicity_score > 0.50:
    # Flag for review - moderate
    status = "flagged_moderate"
    response = process_with_monitoring(content)
elif toxicity_score > 0.20:
    # Warning - mild
    status = "warning_mild"
    response = process_with_disclaimer(content)
else:
    # Safe
    status = "approved"
    response = process_request(content)

Example 4: Geographic restrictions
-----------------------------------
elif user_country in BLOCKED_COUNTRIES:
    status = "blocked_geo"
    response = "This service is not available in your region."
    allow_processing = False
"""

"""
TEMPLATE: Source Validation (Trust Levels)
===========================================
Use: Categorize RAG/data sources by trust level

COPY this template when you need to:
- Validate RAG document sources
- Assign trust levels to data
- Add disclaimers based on source
- Filter by source reliability

2026 NOTE: Two versions below.
- Version A: if/elif/else  (classic, works everywhere)
- Version B: match/case    (Python 3.10+, preferred when routing by source NAME)
"""

# ═══════════════════════════════════════════════════════════
# YOUR DATA (← REPLACE WITH REAL DATA)
# ═══════════════════════════════════════════════════════════
source = "internal_kb"  # ← Document source identifier
document_text = "RAG combines retrieval with generation to provide accurate, grounded answers."
confidence_score = 0.88  # ← Retrieval/relevance score


# ═══════════════════════════════════════════════════════════
# VERSION A: if/elif/else  (classic, still valid)
# ═══════════════════════════════════════════════════════════

if source == "internal_kb":
    # ─────────────────────────────────────────────────────────
    # HIGH TRUST: Internal Knowledge Base
    # ─────────────────────────────────────────────────────────
    trust_level = "high"
    use_directly = True
    add_disclaimer = False
    citation_format = "Source: Internal Knowledge Base"

    print(f"✓ HIGH TRUST: Internal Knowledge Base")

elif source == "verified_api":
    # ─────────────────────────────────────────────────────────
    # HIGH TRUST: Verified External API
    # ─────────────────────────────────────────────────────────
    trust_level = "high"
    use_directly = True
    add_disclaimer = False
    citation_format = "Source: Verified API"

    print(f"✓ HIGH TRUST: Verified API")

elif source == "wikipedia":
    # ─────────────────────────────────────────────────────────
    # MEDIUM TRUST: Public Encyclopedia
    # ─────────────────────────────────────────────────────────
    trust_level = "medium"
    use_directly = True
    add_disclaimer = True
    citation_format = "Source: Wikipedia (public source, independently verify for critical use)"

    print(f"⚠ MEDIUM TRUST: Wikipedia (adding disclaimer)")

elif source == "arxiv":
    # ─────────────────────────────────────────────────────────
    # MEDIUM TRUST: Research Papers
    # ─────────────────────────────────────────────────────────
    trust_level = "medium"
    use_directly = True
    add_disclaimer = True
    citation_format = "Source: arXiv (preprint, not peer-reviewed)"

    print(f"⚠ MEDIUM TRUST: arXiv (research preprint)")

elif source == "web_search":
    # ─────────────────────────────────────────────────────────
    # LOW TRUST: Web Search Results
    # ─────────────────────────────────────────────────────────
    trust_level = "low"
    use_directly = False
    add_disclaimer = True
    citation_format = "Source: Web Search (unverified, use with caution)"

    print(f"⚠ LOW TRUST: Web search (unverified)")

elif source == "user_uploaded":
    # ─────────────────────────────────────────────────────────
    # LOW TRUST: User-Generated Content
    # ─────────────────────────────────────────────────────────
    trust_level = "low"
    use_directly = False
    add_disclaimer = True
    citation_format = "Source: User Upload (not verified by our team)"

    print(f"⚠ LOW TRUST: User-uploaded content")

else:
    # ─────────────────────────────────────────────────────────
    # UNKNOWN: Unrecognized Source
    # ─────────────────────────────────────────────────────────
    trust_level = "unknown"
    use_directly = False
    add_disclaimer = True
    citation_format = "Source: Unknown - Manual verification required"

    print(f"🚫 UNKNOWN SOURCE: {source} - Requires manual review")


# ═══════════════════════════════════════════════════════════
# BUILD RESPONSE BASED ON TRUST LEVEL
# ═══════════════════════════════════════════════════════════

if use_directly:
    # Use the information
    response = document_text

    if add_disclaimer:
        # Add source citation and disclaimer
        response += f"\n\n{citation_format}"
else:
    # Don't use directly - flag for review
    response = f"I found information from {source}, but it requires verification before I can provide it."

# ═══════════════════════════════════════════════════════════
# RESULT (Use this in your AI system)
# ═══════════════════════════════════════════════════════════
result = {
    "source": source,
    "trust_level": trust_level,
    "use_directly": use_directly,
    "disclaimer_added": add_disclaimer,
    "response": response,
    "citation": citation_format,
    "confidence": confidence_score
}

print(f"\n{'='*50}")
print(f"SOURCE VALIDATION RESULT:")
print(f"{'='*50}")
print(f"Source: {result['source']}")
print(f"Trust Level: {result['trust_level']}")
print(f"Use Directly: {result['use_directly']}")
print(f"Citation: {result['citation']}")


# ═══════════════════════════════════════════════════════════
# VERSION B: match/case  (Python 3.10+, 2026 preferred style)
# Use this when routing by source NAME — cleaner, more readable
# ═══════════════════════════════════════════════════════════

match source:
    case "internal_kb":
        trust_level = "high"
        use_directly = True
        add_disclaimer = False
        citation_format = "Source: Internal Knowledge Base"
        print("✓ HIGH TRUST: Internal Knowledge Base")

    case "verified_api":
        trust_level = "high"
        use_directly = True
        add_disclaimer = False
        citation_format = "Source: Verified API"
        print("✓ HIGH TRUST: Verified API")

    case "wikipedia":
        trust_level = "medium"
        use_directly = True
        add_disclaimer = True
        citation_format = "Source: Wikipedia (public source, independently verify for critical use)"
        print("⚠ MEDIUM TRUST: Wikipedia (adding disclaimer)")

    case "arxiv":
        trust_level = "medium"
        use_directly = True
        add_disclaimer = True
        citation_format = "Source: arXiv (preprint, not peer-reviewed)"
        print("⚠ MEDIUM TRUST: arXiv (research preprint)")

    case "web_search":
        trust_level = "low"
        use_directly = False
        add_disclaimer = True
        citation_format = "Source: Web Search (unverified, use with caution)"
        print("⚠ LOW TRUST: Web search (unverified)")

    case "user_uploaded":
        trust_level = "low"
        use_directly = False
        add_disclaimer = True
        citation_format = "Source: User Upload (not verified by our team)"
        print("⚠ LOW TRUST: User-uploaded content")

    case _:                                   # ← catch-all (same as else)
        trust_level = "unknown"
        use_directly = False
        add_disclaimer = True
        citation_format = "Source: Unknown - Manual verification required"
        print(f"🚫 UNKNOWN SOURCE: {source} - Requires manual review")


# ═══════════════════════════════════════════════════════════
# MODIFICATION EXAMPLES
# ═══════════════════════════════════════════════════════════
"""
Example 1: Add company-specific sources
----------------------------------------
elif source == "salesforce_api":
    trust_level = "high"
    use_directly = True
    citation_format = "Source: Salesforce CRM"

elif source == "slack_archive":
    trust_level = "medium"
    use_directly = True
    add_disclaimer = True
    citation_format = "Source: Internal Slack (informal communication)"

Example 2: Combine trust with confidence
-----------------------------------------
if trust_level == "high" and confidence_score > 0.90:
    use_directly = True
    add_disclaimer = False
elif trust_level == "high" and confidence_score > 0.70:
    use_directly = True
    add_disclaimer = True
else:
    use_directly = False

Example 3: Date-based trust
----------------------------
from datetime import datetime, timedelta

if source == "news_api":
    if document_age < timedelta(days=7):
        trust_level = "high"  # Recent news
    elif document_age < timedelta(days=30):
        trust_level = "medium"  # Older news
    else:
        trust_level = "low"  # Outdated

Example 4: Multi-factor trust scoring
--------------------------------------
trust_score = 0

if source in ["internal_kb", "verified_api"]:
    trust_score += 50
if confidence_score > 0.90:
    trust_score += 30
if document_has_citations:
    trust_score += 20

if trust_score >= 80:
    trust_level = "high"
elif trust_score >= 50:
    trust_level = "medium"
else:
    trust_level = "low"
"""

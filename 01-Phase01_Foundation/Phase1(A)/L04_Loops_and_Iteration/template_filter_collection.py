"""
TEMPLATE: Filter Collection
============================
Use: Keep only items matching criteria

COPY this template when you need to:
- Filter RAG results by score
- Keep high-confidence responses
- Select trusted sources
- Remove low-quality items
"""

# ═══════════════════════════════════════════════════════════
# CONFIGURATION (← MODIFY THESE)
# ═══════════════════════════════════════════════════════════
QUALITY_THRESHOLD = 0.80  # ← Set your threshold


# ═══════════════════════════════════════════════════════════
# YOUR DATA (← REPLACE WITH REAL DATA)
# ═══════════════════════════════════════════════════════════
search_results = [
    {"source": "Wikipedia", "score": 0.95, "text": "RAG is..."},
    {"source": "Blog", "score": 0.72, "text": "RAG stands for..."},
    {"source": "ArXiv", "score": 0.88, "text": "Retrieval-Augmented..."},
    {"source": "Forum", "score": 0.65, "text": "I think RAG..."},
    {"source": "Docs", "score": 0.92, "text": "RAG combines..."}
]


# ═══════════════════════════════════════════════════════════
# FILTER LOOP (No changes needed - just works!)
# ═══════════════════════════════════════════════════════════
high_quality = []

for result in search_results:
    if result["score"] > QUALITY_THRESHOLD:  # ← MODIFY condition if needed
        high_quality.append(result)
        print(f"✓ KEPT: {result['source']} (score: {result['score']:.2f})")
    else:
        print(f"✗ FILTERED: {result['source']} (score: {result['score']:.2f})")


# ═══════════════════════════════════════════════════════════
# RESULT
# ═══════════════════════════════════════════════════════════
print(f"\n{'='*50}")
print(f"FILTERING RESULT:")
print(f"{'='*50}")
print(f"Original count: {len(search_results)}")
print(f"After filter: {len(high_quality)}")
print(f"Filtered out: {len(search_results) - len(high_quality)}")
print(f"\nHigh quality results:")
for result in high_quality:
    print(f"  - {result['source']}: {result['score']:.2f}")


# ═══════════════════════════════════════════════════════════
# MODIFICATION EXAMPLES
# ═══════════════════════════════════════════════════════════
"""
Example 1: Filter by multiple conditions
-----------------------------------------
for result in search_results:
    if result["score"] > 0.80 and result["source"] != "Forum":
        high_quality.append(result)

Example 2: Filter by source type
---------------------------------
trusted_sources = ["Wikipedia", "ArXiv", "Docs"]
for result in search_results:
    if result["source"] in trusted_sources:
        high_quality.append(result)

Example 3: Keep top N results
------------------------------
high_quality = []
for result in search_results:
    if result["score"] > 0.70:
        high_quality.append(result)
        if len(high_quality) >= 3:  # Stop at 3
            break

Example 4: Filter with scoring tiers
-------------------------------------
excellent = []
good = []
fair = []

for result in search_results:
    if result["score"] >= 0.90:
        excellent.append(result)
    elif result["score"] >= 0.75:
        good.append(result)
    elif result["score"] >= 0.60:
        fair.append(result)
"""

"""
TEMPLATE: Fallback Chains (Redundancy)
=======================================
Use: Try primary → backup → default logic

COPY this template when you need to:
- Redundant data sources
- Failover systems
- Multiple API attempts
- Graceful degradation

2026 NOTE: This template correctly uses if/elif/else.
  Reason: checking AVAILABILITY (True/False booleans) → if/elif is the right tool.
  match/case is for routing by name/type/status, NOT for boolean availability checks.
"""

# ═══════════════════════════════════════════════════════════
# CONFIGURATION (← MODIFY THESE)
# ═══════════════════════════════════════════════════════════
DEFAULT_RESPONSE = "I'm having trouble accessing my knowledge base. Please try again later."


# ═══════════════════════════════════════════════════════════
# AVAILABILITY CHECKS (← REPLACE WITH REAL HEALTH CHECKS)
# ═══════════════════════════════════════════════════════════
primary_available = False   # ← Check if primary source is up
backup_available = True     # ← Check if backup source is up


# ═══════════════════════════════════════════════════════════
# YOUR DATA
# ═══════════════════════════════════════════════════════════
query = "What is RAG?"  # ← User query


# ═══════════════════════════════════════════════════════════
# FALLBACK CHAIN (Try in order: Primary → Backup → Default)
# ═══════════════════════════════════════════════════════════

if primary_available:
    # ─────────────────────────────────────────────────────────
    # PRIMARY SOURCE (Best option)
    # ─────────────────────────────────────────────────────────
    source_used = "primary_database"

    # UNCOMMENT when you have your primary function:
    # result = query_primary_db(query)

    # For now:
    result = f"High-quality result from primary database for: {query}"
    latency = "fast"
    quality = "high"

    print(f"✓ PRIMARY SOURCE USED")
    print(f"   Database: {source_used}")
    print(f"   Latency: {latency}")
    print(f"   Quality: {quality}")

elif backup_available:
    # ─────────────────────────────────────────────────────────
    # BACKUP SOURCE (Fallback)
    # ─────────────────────────────────────────────────────────
    source_used = "backup_database"

    # UNCOMMENT when you have your backup function:
    # result = query_backup_db(query)

    # For now:
    result = f"Backup result for: {query}"
    latency = "medium"
    quality = "medium"

    print(f"⚠ BACKUP SOURCE USED (Primary unavailable)")
    print(f"   Database: {source_used}")
    print(f"   Latency: {latency}")
    print(f"   Quality: {quality}")

else:
    # ─────────────────────────────────────────────────────────
    # DEFAULT / CACHED RESPONSE (Both sources failed)
    # ─────────────────────────────────────────────────────────
    source_used = "default_cache"
    result = DEFAULT_RESPONSE
    latency = "instant"
    quality = "low"

    print(f"🚫 DEFAULT RESPONSE (All sources unavailable)")
    print(f"   Using: Cached/default response")
    print(f"   Latency: {latency}")
    print(f"   Quality: {quality}")


# ═══════════════════════════════════════════════════════════
# RESULT (Use this in your AI system)
# ═══════════════════════════════════════════════════════════
response = {
    "source": source_used,
    "result": result,
    "latency": latency,
    "quality": quality,
    "query": query,
    "fallback_used": source_used != "primary_database"
}

print(f"\n{'='*50}")
print(f"FALLBACK RESULT:")
print(f"{'='*50}")
print(f"Source: {response['source']}")
print(f"Fallback Used: {response['fallback_used']}")
print(f"Result: {response['result'][:60]}...")


# ═══════════════════════════════════════════════════════════
# MODIFICATION EXAMPLES
# ═══════════════════════════════════════════════════════════
"""
Example 1: Three-tier fallback
-------------------------------
if primary_available:
    result = query_primary()
elif backup_available:
    result = query_backup()
elif cache_available:
    result = get_from_cache()
else:
    result = DEFAULT_RESPONSE

Example 2: Try with timeout
----------------------------
try:
    result = query_primary_with_timeout(query, timeout=2)
    source_used = "primary"
except TimeoutError:
    try:
        result = query_backup_with_timeout(query, timeout=5)
        source_used = "backup"
    except TimeoutError:
        result = DEFAULT_RESPONSE
        source_used = "default"

Example 3: Quality-based fallback
----------------------------------
result = query_primary()

if result["quality_score"] < 0.70:
    # Primary gave low quality, try backup
    backup_result = query_backup()
    if backup_result["quality_score"] > result["quality_score"]:
        result = backup_result
        source_used = "backup"

Example 4: Multi-source aggregation
------------------------------------
results = []

if primary_available:
    results.append(query_primary())
if backup_available:
    results.append(query_backup())

if results:
    # Combine or pick best
    result = merge_results(results)
else:
    result = DEFAULT_RESPONSE

Example 5: Regional fallback
-----------------------------
if region == "us-west" and us_west_db_available:
    result = query_us_west_db()
elif region == "us-east" and us_east_db_available:
    result = query_us_east_db()
elif global_db_available:
    result = query_global_db()
else:
    result = DEFAULT_RESPONSE

Example 6: Cost-based fallback
-------------------------------
# Try cheap option first
if free_tier_available and query_is_simple:
    result = query_free_tier()
elif paid_tier_available:
    result = query_paid_tier()
else:
    result = "Service temporarily unavailable"
"""

"""
TEMPLATE: Find First Match
===========================
Use: Get first item matching condition, then stop

COPY this template when you need to:
- Find best RAG result
- Get first available tool
- Locate specific message
- Early exit on match
"""

# ═══════════════════════════════════════════════════════════
# YOUR DATA (← REPLACE WITH REAL DATA)
# ═══════════════════════════════════════════════════════════
llm_responses = [
    {"answer": "Maybe it's...", "confidence": 0.65, "model": "fast"},
    {"answer": "It's likely...", "confidence": 0.88, "model": "balanced"},
    {"answer": "Definitely...", "confidence": 0.95, "model": "accurate"},
    {"answer": "Certainly...", "confidence": 0.92, "model": "accurate"}
]


# ═══════════════════════════════════════════════════════════
# FIND FIRST PATTERN
# ═══════════════════════════════════════════════════════════
HIGH_CONFIDENCE = 0.90  # ← MODIFY: Your threshold

best_answer = None

for response in llm_responses:
    if response["confidence"] >= HIGH_CONFIDENCE:  # ← MODIFY: Your condition
        best_answer = response
        print(f"✓ FOUND: confidence {response['confidence']:.2f}")
        break  # Stop searching

if best_answer:
    print(f"\nBest answer: {best_answer['answer']}")
    print(f"Confidence: {best_answer['confidence']:.2f}")
else:
    print("\n⚠ No high-confidence answer found")
    print("Consider using lower threshold or fallback")


# ═══════════════════════════════════════════════════════════
# FIND WITH INDEX
# ═══════════════════════════════════════════════════════════
tools = ["search", "calculator", "weather", "translate"]

target_tool = "weather"
position = -1

for i, tool in enumerate(tools):
    if tool == target_tool:
        position = i
        break

if position >= 0:
    print(f"\nFound '{target_tool}' at index {position}")
else:
    print(f"\nTool '{target_tool}' not found")


# ═══════════════════════════════════════════════════════════
# FIND FIRST AVAILABLE
# ═══════════════════════════════════════════════════════════
sources = [
    {"name": "primary_db", "available": False},
    {"name": "backup_db", "available": True},
    {"name": "cache", "available": True}
]

selected_source = None

for source in sources:
    if source["available"]:
        selected_source = source
        print(f"✓ Using: {source['name']}")
        break

if not selected_source:
    print("⚠ No sources available - using fallback")


# ═══════════════════════════════════════════════════════════
# FIND WITH MULTIPLE CONDITIONS
# ═══════════════════════════════════════════════════════════
documents = [
    {"id": 1, "source": "Blog", "score": 0.92, "verified": False},
    {"id": 2, "source": "Wikipedia", "score": 0.88, "verified": True},
    {"id": 3, "source": "ArXiv", "score": 0.95, "verified": True}
]

best_doc = None

for doc in documents:
    # Both conditions must be met
    if doc["score"] > 0.85 and doc["verified"]:
        best_doc = doc
        print(f"✓ Found verified doc: {doc['source']} ({doc['score']:.2f})")
        break

print(f"\n{'='*50}")
print(f"SELECTION RESULT:")
print(f"{'='*50}")
if best_doc:
    print(f"Selected: Document #{best_doc['id']}")
    print(f"Source: {best_doc['source']}")
    print(f"Score: {best_doc['score']:.2f}")
    print(f"Verified: {best_doc['verified']}")
else:
    print("No suitable document found")


# ═══════════════════════════════════════════════════════════
# MODIFICATION EXAMPLES
# ═══════════════════════════════════════════════════════════
"""
Example 1: Find with default fallback
--------------------------------------
result = None
for item in items:
    if matches(item):
        result = item
        break

if result is None:
    result = get_default()

Example 2: Find first error
----------------------------
error_found = None

for log_entry in logs:
    if log_entry["level"] == "ERROR":
        error_found = log_entry
        break

if error_found:
    handle_error(error_found)

Example 3: Find best within budget
-----------------------------------
best_option = None

for option in options:
    if option["cost"] <= budget and option["quality"] > min_quality:
        best_option = option
        break

Example 4: Find with transformation
------------------------------------
match = None

for item in items:
    if meets_criteria(item):
        match = transform(item)  # Convert to needed format
        break

Example 5: Find in nested structure
------------------------------------
found = None

for conversation in all_conversations:
    for message in conversation:
        if message["id"] == target_id:
            found = message
            break
    if found:  # Exit outer loop too
        break
"""

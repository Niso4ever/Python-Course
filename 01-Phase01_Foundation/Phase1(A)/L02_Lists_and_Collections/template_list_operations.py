"""
TEMPLATE: List Operations for AI Systems
==========================================
Copy-paste patterns for working with lists

Usage:
1. Find the pattern that matches your need
2. Copy the code block
3. Modify for your use case
4. Use in your project
"""

# ============================================================================
# PATTERN 1: Search Results Storage (List of Dicts)
# ============================================================================
# This is THE most common pattern in AI - memorize this one!

# Store search/retrieval results
search_results = [
    {
        "doc_id": "doc_001",
        "source": "Wikipedia",
        "content": "Python is a programming language...",
        "relevance_score": 0.95,
        "verified": True
    },
    {
        "doc_id": "doc_002",
        "source": "ArXiv",
        "content": "Machine learning applications...",
        "relevance_score": 0.88,
        "verified": True
    },
    {
        "doc_id": "doc_003",
        "source": "Blog",
        "content": "Tutorial on Python basics...",
        "relevance_score": 0.72,
        "verified": False
    }
]

# Access first result
top_result = search_results[0]
print(f"Top source: {top_result['source']}")

# Access first result's score
top_score = search_results[0]["relevance_score"]
print(f"Best score: {top_score}")

# Count results
num_results = len(search_results)
print(f"Found {num_results} documents")

# Safe access (won't crash if key missing)
confidence = search_results[0].get("confidence", 0.0)


# ============================================================================
# PATTERN 2: Conversation History (Growing List)
# ============================================================================
# How every chatbot maintains context

# Start with empty conversation
conversation_history = []

# Add user message
conversation_history.append({
    "role": "user",
    "content": "What is retrieval-augmented generation?"
})

# Add assistant response
conversation_history.append({
    "role": "assistant",
    "content": "RAG is a technique that combines..."
})

# Add another user message
conversation_history.append({
    "role": "user",
    "content": "Can you give an example?"
})

# Send ENTIRE conversation to LLM
# llm_response = llm.generate(messages=conversation_history)

# Add LLM response
conversation_history.append({
    "role": "assistant",
    "content": "Sure! A common example is..."
})

# Check conversation length
num_messages = len(conversation_history)
print(f"Conversation has {num_messages} messages")

# Get last message
latest_message = conversation_history[-1]
print(f"Latest: {latest_message['content']}")


# ============================================================================
# PATTERN 3: Filtering Results (Building New List)
# ============================================================================
# Remove low-quality results, keep only high-quality ones

# Raw results from vector database
all_results = [
    {"title": "Python Guide", "score": 0.95, "verified": True},
    {"title": "Random Blog", "score": 0.68, "verified": False},
    {"title": "Official Docs", "score": 0.92, "verified": True},
    {"title": "Forum Post", "score": 0.73, "verified": False}
]

# Define quality threshold
RELEVANCE_THRESHOLD = 0.85
REQUIRE_VERIFICATION = True

# Build filtered list
high_quality_results = []

for result in all_results:  # Loop through all results
    # Check if it meets criteria
    passes_score = result["score"] >= RELEVANCE_THRESHOLD
    passes_verification = result["verified"] if REQUIRE_VERIFICATION else True

    if passes_score and passes_verification:
        high_quality_results.append(result)

print(f"Filtered {len(all_results)} → {len(high_quality_results)} results")


# ============================================================================
# PATTERN 4: Source Attribution (Simple List)
# ============================================================================
# Track which sources were used (for transparency)

# Start with empty list
sources_used = []

# Add sources as you use them
sources_used.append("Wikipedia: Python Programming")
sources_used.append("Python.org Official Documentation")
sources_used.append("Real Python Tutorial")

# Display to user
print("Answer based on:")
for i, source in enumerate(sources_used, 1):
    print(f"  {i}. {source}")

# Check how many sources
num_sources = len(sources_used)
print(f"\nUsed {num_sources} sources")


# ============================================================================
# PATTERN 5: Token Usage Tracking (List of Numbers)
# ============================================================================
# Monitor costs and usage

# Track tokens for each LLM call
token_log = []

# Call 1
token_log.append(1523)

# Call 2
token_log.append(892)

# Call 3
token_log.append(2041)

# Analyze usage
total_tokens = sum(token_log)
average_tokens = total_tokens / len(token_log)
max_tokens = max(token_log)
min_tokens = min(token_log)

print(f"Total tokens: {total_tokens}")
print(f"Average: {average_tokens:.0f}")
print(f"Peak usage: {max_tokens}")
print(f"Calls made: {len(token_log)}")


# ============================================================================
# PATTERN 6: Error Collection (Don't Crash, Collect)
# ============================================================================
# Accumulate errors instead of stopping at first failure

# Start with empty error list
errors = []

# Step 1: Try something
try:
    # Simulate operation
    result = perform_search()
except Exception as e:
    errors.append({
        "step": "search",
        "error": str(e),
        "timestamp": "2026-02-27T10:00:00"
    })

# Step 2: Try something else
try:
    # Simulate operation
    filtered = filter_results()
except Exception as e:
    errors.append({
        "step": "filter",
        "error": str(e),
        "timestamp": "2026-02-27T10:00:05"
    })

# Check if any errors occurred
if len(errors) > 0:
    print(f"Warning: {len(errors)} errors occurred:")
    for error in errors:
        print(f"  - {error['step']}: {error['error']}")
else:
    print("All steps completed successfully!")


# ============================================================================
# PATTERN 7: Tool Call History (Agent Actions)
# ============================================================================
# Track what an agent did (for debugging/transparency)

# Track agent's actions
tool_history = []

# Agent uses search tool
tool_history.append({
    "step": 1,
    "tool": "vector_search",
    "input": "Python basics",
    "output": "Found 5 documents",
    "success": True,
    "timestamp": "10:00:00"
})

# Agent uses summarize tool
tool_history.append({
    "step": 2,
    "tool": "summarize",
    "input": "5 documents",
    "output": "Summary: Python is...",
    "success": True,
    "timestamp": "10:00:05"
})

# Review what agent did
print("Agent workflow:")
for action in tool_history:
    status = "✓" if action["success"] else "✗"
    print(f"  {status} Step {action['step']}: {action['tool']}")


# ============================================================================
# PATTERN 8: Batch Processing Results
# ============================================================================
# Process multiple items, collect all results

# Documents to process
documents = [
    "Document about Python",
    "Document about JavaScript",
    "Document about Rust"
]

# Store processing results
processing_results = []

# Process each document
for doc in documents:
    result = {
        "title": doc,
        "word_count": len(doc.split()),
        "processed": True
    }
    processing_results.append(result)

print(f"Processed {len(processing_results)} documents")


# ============================================================================
# PATTERN 9: Dynamic Prompt Building
# ============================================================================
# Build prompts by adding sections

# Example inputs (in a real agent these come from the user and the retriever)
user_question = "What is RAG?"
retrieved_context = "RAG retrieves documents and adds them to the prompt."
context_available = True

# Start with empty list
prompt_parts = []

# Add sections
prompt_parts.append("You are a helpful AI assistant.")
prompt_parts.append(f"User question: {user_question}")

# Conditionally add context
if context_available:
    prompt_parts.append(f"Context: {retrieved_context}")

prompt_parts.append("Answer based on the information above.")

# Combine into final prompt
final_prompt = "\n\n".join(prompt_parts)


# ============================================================================
# PATTERN 10: Relevance Ranking
# ============================================================================
# Sort results by score, keep top N

# Results with scores
results = [
    {"title": "Doc A", "score": 0.88},
    {"title": "Doc B", "score": 0.95},
    {"title": "Doc C", "score": 0.72},
    {"title": "Doc D", "score": 0.91}
]

# Sort by score (highest first)
results.sort(key=lambda x: x["score"], reverse=True)

# Keep top 3
top_results = results[:3]

print("Top 3 results:")
for i, result in enumerate(top_results, 1):
    print(f"  {i}. {result['title']} ({result['score']})")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def safe_list_access(items, index, default=None):
    """
    Safely access list item, return default if out of range

    Args:
        items: The list
        index: Index to access
        default: Value to return if index invalid

    Returns:
        Item at index or default
    """
    try:
        return items[index]
    except IndexError:
        return default


def get_top_n_by_score(items, n=3, score_key="score"):
    """
    Get top N items sorted by score

    Args:
        items: List of dicts with scores
        n: Number of top items to return
        score_key: Dict key containing the score

    Returns:
        List of top N items
    """
    sorted_items = sorted(items, key=lambda x: x.get(score_key, 0), reverse=True)
    return sorted_items[:n]


def filter_by_threshold(items, threshold=0.85, score_key="score"):
    """
    Filter items by minimum score threshold

    Args:
        items: List of dicts with scores
        threshold: Minimum score to keep
        score_key: Dict key containing the score

    Returns:
        Filtered list
    """
    return [item for item in items if item.get(score_key, 0) >= threshold]


# ============================================================================
# COMMON MISTAKES TO AVOID
# ============================================================================

"""
❌ MISTAKE 1: Index out of range
results = []
# first = results[0]  # Crashes if list is empty!

✅ CORRECT:
if len(results) > 0:
    first = results[0]


❌ MISTAKE 2: Modifying list while looping
for item in my_list:
    my_list.remove(item)  # Causes skipping!

✅ CORRECT:
filtered = [item for item in my_list if condition]


❌ MISTAKE 3: Forgetting lists start at 0
tools = ["search", "summarize", "translate"]
# first = tools[1]  # This is the SECOND item!

✅ CORRECT:
first = tools[0]  # First item


❌ MISTAKE 4: Not handling empty lists
results = []
# max_score = max(results)  # ValueError: max() arg is empty

✅ CORRECT:
if len(results) > 0:
    max_score = max(results)
else:
    max_score = 0.0
"""


# ============================================================================
# WHEN TO USE EACH PATTERN
# ============================================================================

"""
Use PATTERN 1 (List of Dicts) when:
- Storing search/retrieval results
- Returning data from APIs
- Managing structured records

Use PATTERN 2 (Growing List) when:
- Building conversation history
- Accumulating items over time
- Don't know final size in advance

Use PATTERN 3 (Filtering) when:
- RAG quality thresholds
- Removing low-quality data
- Building subset of results

Use PATTERN 4 (Simple List) when:
- Source attribution
- Tool names, categories
- Simple collections

Use PATTERN 5 (Numbers List) when:
- Token tracking
- Score analysis
- Metrics aggregation

Use PATTERN 6 (Error Collection) when:
- Multi-step processes
- Need to continue after failures
- Debugging complex workflows

Use PATTERN 7 (Tool History) when:
- Agent transparency
- Auditing agent decisions
- Debugging agent behavior

Use PATTERN 8 (Batch Results) when:
- Processing multiple documents
- Data pipelines
- Bulk operations

Use PATTERN 9 (Dynamic Building) when:
- Flexible prompt construction
- Conditional sections
- Multi-part assembly

Use PATTERN 10 (Ranking) when:
- Sorting by relevance
- Top-N selection
- Priority ordering
"""

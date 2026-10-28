"""
TEMPLATE: Complete RAG (Retrieval-Augmented Generation) Pipeline
==================================================================

Purpose: End-to-end flow from user query → vector search → filter → LLM generation
Use Case: Building Q&A systems, knowledge base assistants, document search

This is the MOST IMPORTANT template for AI Architects.
RAG is the foundation of 80% of modern AI applications.

Pattern Flow:
1. User asks a question
2. Convert question to vector embedding
3. Search vector database for similar documents
4. Filter results by quality threshold
5. Combine top results with user question
6. Send to LLM for final answer generation

Copy this template when:
- Building chatbots with knowledge bases
- Creating document Q&A systems
- Implementing semantic search
- Any time you need "LLM + external knowledge"
"""

# ============================================================================
# STEP 1: Simulated User Query
# ============================================================================

# In production, this comes from user input
user_query = "What is retrieval-augmented generation?"

print(f"User Query: {user_query}")
print("-" * 60)


# ============================================================================
# STEP 2: Vector Search (Simulated)
# ============================================================================

# In production, this would be a real vector database call:
# results = vector_db.search(query=user_query, top_k=5)

# For this template, we simulate the results:
raw_search_results = [
    {
        "content": "RAG combines retrieval systems with large language models...",
        "source": "Wikipedia",
        "relevance_score": 0.947,
        "verified": True,
        "doc_id": "wiki_rag_001"
    },
    {
        "content": "Retrieval-augmented generation improves LLM accuracy by...",
        "source": "ArXiv Paper",
        "relevance_score": 0.923,
        "verified": True,
        "doc_id": "arxiv_2005_11401"
    },
    {
        "content": "RAG is a technique that retrieves relevant documents...",
        "source": "Internal Docs",
        "relevance_score": 0.891,
        "verified": True,
        "doc_id": "internal_rag_guide"
    },
    {
        "content": "Some people confuse RAG with fine-tuning, but they differ...",
        "source": "Blog Post",
        "relevance_score": 0.734,
        "verified": False,
        "doc_id": "blog_rag_2024"
    },
    {
        "content": "Retrieval systems have been used since the 1960s...",
        "source": "Wikipedia",
        "relevance_score": 0.682,
        "verified": True,
        "doc_id": "wiki_ir_history"
    }
]

print(f"Retrieved {len(raw_search_results)} documents from vector DB")
print("-" * 60)


# ============================================================================
# STEP 3: Filter Results by Quality Threshold
# ============================================================================

# ARCHITECTURAL DECISION: Only use high-quality, verified documents
RELEVANCE_THRESHOLD = 0.85  # Minimum score to include (0.0-1.0)
REQUIRE_VERIFICATION = True  # Only use verified sources?

filtered_results = []

print("Filtering results...")
for doc in raw_search_results:
    relevance = doc["relevance_score"]
    verified = doc["verified"]
    source = doc["source"]

    # Quality gates
    passes_relevance = relevance >= RELEVANCE_THRESHOLD
    passes_verification = verified if REQUIRE_VERIFICATION else True

    if passes_relevance and passes_verification:
        filtered_results.append(doc)
        print(f"  ✓ KEPT: {source} (score: {relevance:.3f})")
    else:
        reason = "low score" if not passes_relevance else "unverified"
        print(f"  ✗ FILTERED: {source} (score: {relevance:.3f}) - {reason}")

print(f"\nFinal count: {len(filtered_results)} documents passed filters")
print("-" * 60)


# ============================================================================
# STEP 4: Build Context from Filtered Documents
# ============================================================================

# ARCHITECTURAL DECISION: How to combine multiple documents?
# Option A: Concatenate all content
# Option B: Take only top N
# Option C: Weighted combination
# We'll use Option B: Top 3 documents

MAX_CONTEXT_DOCS = 3
context_docs = filtered_results[:MAX_CONTEXT_DOCS]

# Build the context string
context_parts = []
for i, doc in enumerate(context_docs, start=1):
    # Format: [Source #N] Content
    context_part = f"[{doc['source']} #{i}] {doc['content']}"
    context_parts.append(context_part)

# Join all parts with double newlines
combined_context = "\n\n".join(context_parts)

print("Context for LLM:")
print(combined_context)
print("-" * 60)


# ============================================================================
# STEP 5: Build Prompt for LLM
# ============================================================================

# ARCHITECTURAL PATTERN: System + Context + Query
system_prompt = """You are a helpful AI assistant. Use the provided context to answer the user's question accurately. If the context doesn't contain enough information, say so."""

# Combine everything into final prompt
final_prompt = f"""CONTEXT:
{combined_context}

USER QUESTION:
{user_query}

Please provide a clear, accurate answer based on the context above."""

print("Final Prompt to LLM:")
print(final_prompt)
print("-" * 60)


# ============================================================================
# STEP 6: Call LLM (Simulated)
# ============================================================================

# In production, this would be:
# response = llm.generate(
#     system=system_prompt,
#     prompt=final_prompt,
#     temperature=0.7,
#     max_tokens=500
# )

# Simulated response:
llm_response = """Retrieval-augmented generation (RAG) is a technique that combines retrieval systems with large language models to improve accuracy. According to the provided sources, RAG retrieves relevant documents from a knowledge base and uses them to augment the LLM's response, reducing hallucinations and providing more factual answers."""

print("LLM Response:")
print(llm_response)
print("-" * 60)


# ============================================================================
# STEP 7: Add Metadata for Logging/Evaluation
# ============================================================================

# ARCHITECTURAL BEST PRACTICE: Track everything for debugging
operation_metadata = {
    "user_query": user_query,
    "retrieval": {
        "total_retrieved": len(raw_search_results),
        "after_filtering": len(filtered_results),
        "used_in_context": len(context_docs),
        "relevance_threshold": RELEVANCE_THRESHOLD,
        "require_verification": REQUIRE_VERIFICATION
    },
    "sources_used": [doc["source"] for doc in context_docs],
    "llm": {
        "model": "claude-opus-5-5",  # Would be actual model
        "prompt_length": len(final_prompt),
        "response_length": len(llm_response),
        "temperature": 0.7
    },
    "timestamp": "2026-02-26T14:30:00Z"
}

print("Operation Metadata:")
for key, value in operation_metadata.items():
    print(f"  {key}: {value}")
print("-" * 60)


# ============================================================================
# STEP 8: Return Structured Response
# ============================================================================

# ARCHITECTURAL PATTERN: Always return metadata with response
rag_result = {
    "answer": llm_response,
    "sources": [
        {
            "source": doc["source"],
            "doc_id": doc["doc_id"],
            "score": doc["relevance_score"]
        }
        for doc in context_docs
    ],
    "metadata": operation_metadata,
    "success": True
}

print("Final RAG Result:")
print(f"Answer: {rag_result['answer'][:100]}...")
print(f"Sources: {[s['source'] for s in rag_result['sources']]}")
print("-" * 60)


# ============================================================================
# REFACTORED VERSION: Function-Based Pipeline
# ============================================================================

def rag_pipeline(
    query,
    search_results,
    relevance_threshold=0.85,
    require_verification=True,
    max_context_docs=3
):
    """
    Complete RAG pipeline as a reusable function

    Args:
        query: User's question
        search_results: List of dicts from vector search
        relevance_threshold: Minimum relevance score (0.0-1.0)
        require_verification: Only use verified sources?
        max_context_docs: Max documents to include in context

    Returns:
        Dict with 'answer', 'sources', 'metadata', 'success'
    """

    # Step 1: Filter results
    filtered = []
    for doc in search_results:
        if doc["relevance_score"] >= relevance_threshold:
            if not require_verification or doc["verified"]:
                filtered.append(doc)

    # Step 2: Select top documents
    context_docs = filtered[:max_context_docs]

    # Step 3: Build context
    context_parts = [
        f"[{doc['source']}] {doc['content']}"
        for doc in context_docs
    ]
    context = "\n\n".join(context_parts)

    # Step 4: Build prompt
    prompt = f"""CONTEXT:
{context}

USER QUESTION:
{query}

Answer based on the context above."""

    # Step 5: Call LLM (simulated)
    response = "Generated answer here..."  # Would be real LLM call

    # Step 6: Return structured result
    return {
        "answer": response,
        "sources": [
            {"source": doc["source"], "score": doc["relevance_score"]}
            for doc in context_docs
        ],
        "metadata": {
            "retrieved": len(search_results),
            "filtered": len(filtered),
            "used": len(context_docs)
        },
        "success": True
    }


# Usage:
# result = rag_pipeline(user_query, raw_search_results)
# print(result["answer"])


# ============================================================================
# COMMON MISTAKES & RED FLAGS
# ============================================================================

# ❌ MISTAKE 1: Not filtering low-quality results
# def bad_rag(query, results):
#     context = "\n".join([doc["content"] for doc in results])
#     # Problem: Using ALL results, including irrelevant ones!

# ✅ CORRECT: Always filter
# def good_rag(query, results, min_score=0.85):
#     filtered = [doc for doc in results if doc["score"] >= min_score]


# ❌ MISTAKE 2: Not handling empty results
# def bad_rag(query, results):
#     context = results[0]["content"]  # IndexError if results is empty!

# ✅ CORRECT: Check for empty
# def good_rag(query, results):
#     if not results:
#         return "No relevant documents found"


# ❌ MISTAKE 3: Including too much context (token overflow)
# def bad_rag(query, results):
#     # If results is 100 documents, this could exceed token limit!
#     context = "\n".join([doc["content"] for doc in results])

# ✅ CORRECT: Limit context size
# def good_rag(query, results, max_docs=3):
#     context = "\n".join([doc["content"] for doc in results[:max_docs]])


# ❌ MISTAKE 4: Not tracking sources
# def bad_rag(query, results):
#     return llm_response  # User can't verify where info came from!

# ✅ CORRECT: Return sources with answer
# def good_rag(query, results):
#     return {
#         "answer": llm_response,
#         "sources": [doc["source"] for doc in used_docs]
#     }


# ============================================================================
# RED FLAGS TO SPOT IN AI-GENERATED RAG CODE
# ============================================================================

"""
🚩 RED FLAG 1: No quality filtering
If you see all search results used without filtering, that's wrong.

🚩 RED FLAG 2: No error handling
What if vector search returns 0 results? Code should handle this.

🚩 RED FLAG 3: Hard-coded thresholds
Thresholds (0.85, max_docs=3) should be configurable parameters.

🚩 RED FLAG 4: No source attribution
Users need to know where the answer came from for trust/verification.

🚩 RED FLAG 5: No metadata logging
You need to track retrieval quality for debugging and improvement.
"""


# ============================================================================
# ARCHITECTURAL DECISIONS YOU NEED TO UNDERSTAND
# ============================================================================

"""
When reviewing RAG code, ask these questions:

1. FILTERING STRATEGY:
   - What relevance threshold is used? (0.85 is common)
   - Are unverified sources allowed?
   - What happens if no documents pass filters?

2. CONTEXT BUILDING:
   - How many documents go into context? (3-5 is common)
   - How are they combined? (Concatenation? Summaries?)
   - Is there a token limit check?

3. PROMPT ENGINEERING:
   - Does prompt clearly separate context from query?
   - Is there a system prompt guiding behavior?
   - Does it handle "context doesn't answer question" case?

4. ERROR HANDLING:
   - What if vector search fails?
   - What if LLM call fails?
   - What if results are empty?

5. OBSERVABILITY:
   - Are sources returned with answer?
   - Is retrieval quality tracked?
   - Can you debug which documents were used?
"""


# ============================================================================
# YOUR TASK: Pattern Recognition
# ============================================================================

"""
When you see RAG code, look for this structure:

1. Query → Search
2. Filter results by quality
3. Select top N documents
4. Combine into context
5. Build prompt (context + query)
6. Call LLM
7. Return answer + sources + metadata

If ANY of these steps are missing, that's a red flag.

You DON'T need to write this from scratch.
You DO need to recognize this pattern and verify all steps exist.
"""

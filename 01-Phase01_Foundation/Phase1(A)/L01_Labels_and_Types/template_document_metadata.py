"""
MY PERSONAL TEMPLATE: RAG Document Metadata
============================================
Copy-paste this for storing search result information

Usage:
1. Copy this template
2. Use it for each retrieved document
3. Store in a list for multiple results

2026 note: In real code you may see type-hinted variables:
  document_metadata: dict = {...}      # dict with type label
  search_results: list = [...]         # list with type label
  relevance_score: float = 0.947      # float with type label
  verified: bool = True               # bool with type label
"""

# ============================================================================
# TEMPLATE: Single document from vector search
# ============================================================================

document_metadata = {
    # Identity
    "doc_id": "doc_12345",                    # Unique identifier
    "source": "internal_knowledge_base",      # Where it came from

    # Retrieval quality
    "relevance_score": 0.947,                 # Vector similarity (0.0-1.0)
    "rank": 1,                                # Position in results (1st, 2nd, etc.)

    # Content info
    "content": "The actual text content...",  # The retrieved text
    "content_length": 512,                    # Characters in content
    "chunk_index": 3,                         # Which chunk of original doc

    # Trust signals
    "verified": True,                         # Human-verified source?
    "last_updated": "2026-01-15",            # Freshness date

    # Technical details
    "embedding_model": "text-embedding-3"     # Which embedding used
}

# ============================================================================
# TEMPLATE: Multiple documents (list of dicts)
# ============================================================================

# This is THE most common pattern in RAG systems!
search_results = [
    {
        "doc_id": "doc_001",
        "source": "Wikipedia",
        "relevance_score": 0.95,
        "content": "Python is a programming language...",
        "verified": True
    },
    {
        "doc_id": "doc_002",
        "source": "ArXiv",
        "relevance_score": 0.88,
        "content": "Machine learning applications...",
        "verified": True
    },
    {
        "doc_id": "doc_003",
        "source": "Blog",
        "relevance_score": 0.72,
        "content": "Tutorial on Python basics...",
        "verified": False
    }
]

# Access first document's score
first_score = search_results[0]["relevance_score"]

# Count results
num_results = len(search_results)

# ============================================================================
# FILTERING PATTERN (very common!)
# ============================================================================

# Filter to only high-quality, verified documents
RELEVANCE_THRESHOLD = 0.85

high_quality_docs = []
for doc in search_results:
    if doc["relevance_score"] >= RELEVANCE_THRESHOLD and doc["verified"]:
        high_quality_docs.append(doc)

# ============================================================================
# MODIFY FOR YOUR USE CASE
# ============================================================================

# If you need different metadata:
custom_document = {
    "doc_id": "doc_123",
    "content": "...",
    "score": 0.95,

    # Add your custom fields:
    "category": "technical_docs",
    "language": "en",
    "word_count": 500,
    "author": "John Doe"
}

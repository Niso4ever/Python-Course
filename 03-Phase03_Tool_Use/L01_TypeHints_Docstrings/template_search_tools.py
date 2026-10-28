"""
Template: Search Tools for AI Agents
Copy these patterns when building search functionality for agents.
"""

from typing import List, Dict, Any, Optional


# ============================================================================
# TEMPLATE 1: Simple Vector Search
# ============================================================================

def search_knowledge_base(
    query: str,
    max_results: int = 10,
    min_score: float = 0.0
) -> List[Dict[str, Any]]:
    """
    Search the knowledge base for relevant documents.

    Use this when the user asks questions that require looking up information.

    Args:
        query: The search query (user's question or keywords)
        max_results: Maximum number of results to return (default: 10)
        min_score: Minimum relevance score, 0.0-1.0 (default: 0.0)

    Returns:
        List of documents, each containing:
        - id (str): Unique document ID
        - title (str): Document title
        - content (str): Document text
        - score (float): Relevance score (0.0-1.0)
        - metadata (dict): Additional document metadata

    Example:
        docs = search_knowledge_base("What is RAG?", max_results=5)
        for doc in docs:
            print(f"{doc['title']}: {doc['score']}")
    """
    # Implementation here
    pass


# ============================================================================
# TEMPLATE 2: Multi-Source Search
# ============================================================================

def search_multi_source(
    query: str,
    sources: Optional[List[str]] = None,
    max_results_per_source: int = 5
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Search across multiple data sources simultaneously.

    Use this when you need to check multiple knowledge bases or APIs.

    Args:
        query: The search query string
        sources: List of source names to search ('wikipedia', 'arxiv', 'docs').
                If None, searches all available sources.
        max_results_per_source: Max results from each source (default: 5)

    Returns:
        Dictionary mapping source names to result lists:
        {
            'wikipedia': [
                {'title': str, 'content': str, 'score': float, 'url': str},
                ...
            ],
            'arxiv': [...]
        }

    Example:
        results = search_multi_source(
            "machine learning",
            sources=["wikipedia", "arxiv"],
            max_results_per_source=3
        )
        print(f"Found {len(results['wikipedia'])} Wikipedia results")
    """
    # Implementation here
    pass


# ============================================================================
# TEMPLATE 3: Filtered Search
# ============================================================================

def search_with_filters(
    query: str,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    categories: Optional[List[str]] = None,
    max_results: int = 10
) -> List[Dict[str, Any]]:
    """
    Search with advanced filtering options.

    Use this for searches with time ranges or category constraints.

    Args:
        query: The search query string
        date_from: Start date filter in 'YYYY-MM-DD' format (inclusive)
        date_to: End date filter in 'YYYY-MM-DD' format (inclusive)
        categories: List of categories to filter by (e.g., ['tech', 'science'])
        max_results: Maximum results to return (default: 10)

    Returns:
        List of filtered documents with:
        - id (str): Document ID
        - title (str): Title
        - content (str): Content
        - date (str): Publication date (YYYY-MM-DD)
        - category (str): Document category
        - score (float): Relevance score

    Example:
        docs = search_with_filters(
            "climate change",
            date_from="2023-01-01",
            categories=["science", "environment"]
        )
    """
    # Implementation here
    pass


# ============================================================================
# TEMPLATE 4: Semantic vs Keyword Search
# ============================================================================

def hybrid_search(
    query: str,
    search_type: str = "hybrid",
    semantic_weight: float = 0.7,
    max_results: int = 10
) -> List[Dict[str, Any]]:
    """
    Perform hybrid search combining semantic and keyword matching.

    Use this for best search quality, combining meaning and exact matches.

    Args:
        query: The search query
        search_type: Type of search - 'semantic', 'keyword', or 'hybrid' (default: 'hybrid')
        semantic_weight: Weight for semantic search (0.0-1.0). Keyword weight = 1 - semantic_weight.
                        Only used when search_type is 'hybrid'. (default: 0.7)
        max_results: Maximum results to return (default: 10)

    Returns:
        List of documents with:
        - id (str): Document ID
        - title (str): Title
        - content (str): Content
        - score (float): Combined relevance score
        - semantic_score (float): Semantic similarity score
        - keyword_score (float): Keyword match score

    Raises:
        ValueError: If search_type is not 'semantic', 'keyword', or 'hybrid'
        ValueError: If semantic_weight is not between 0.0 and 1.0

    Example:
        # Mostly semantic, some keyword matching
        results = hybrid_search(
            "explain neural networks",
            search_type="hybrid",
            semantic_weight=0.8
        )
    """
    # Implementation here
    pass


# ============================================================================
# TEMPLATE 5: Re-ranking Search
# ============================================================================

def search_with_reranking(
    query: str,
    initial_results: int = 50,
    final_results: int = 10,
    rerank_model: str = "cross-encoder"
) -> List[Dict[str, Any]]:
    """
    Search with two-stage retrieval and re-ranking.

    Use this for highest quality results when precision is critical.

    Args:
        query: The search query
        initial_results: Number of candidates to retrieve initially (default: 50)
        final_results: Number of results after re-ranking (default: 10)
        rerank_model: Re-ranking model to use - 'cross-encoder' or 'llm' (default: 'cross-encoder')

    Returns:
        List of re-ranked documents (top final_results) with:
        - id (str): Document ID
        - title (str): Title
        - content (str): Content
        - initial_score (float): Score from initial retrieval
        - rerank_score (float): Score after re-ranking
        - final_rank (int): Final ranking position (1-indexed)

    Example:
        # Get top 10 after re-ranking 50 candidates
        results = search_with_reranking(
            "how does attention mechanism work",
            initial_results=50,
            final_results=10
        )
    """
    # Implementation here
    pass


# ============================================================================
# TEMPLATE 6: Conversational Search (with context)
# ============================================================================

def conversational_search(
    current_query: str,
    conversation_history: Optional[List[Dict[str, str]]] = None,
    max_results: int = 10
) -> Dict[str, Any]:
    """
    Search with conversation context for follow-up questions.

    Use this when the search query might reference previous conversation turns.

    Args:
        current_query: The current search query
        conversation_history: List of previous turns with 'role' and 'content' keys:
                             [{'role': 'user', 'content': '...'}, {'role': 'assistant', 'content': '...'}]
        max_results: Maximum results to return (default: 10)

    Returns:
        Dictionary containing:
        - resolved_query (str): Query after resolving conversation references
        - results (list): List of search results (same format as search_knowledge_base)
        - context_used (bool): Whether conversation history influenced the search

    Example:
        history = [
            {'role': 'user', 'content': 'What is Python?'},
            {'role': 'assistant', 'content': 'Python is a programming language...'}
        ]
        result = conversational_search(
            "How do I install it?",  # "it" refers to Python
            conversation_history=history
        )
        print(result['resolved_query'])  # "How do I install Python?"
    """
    # Implementation here
    pass


# ============================================================================
# TEMPLATE 7: Similarity Search for Clustering
# ============================================================================

def find_similar_documents(
    reference_doc_id: str,
    max_results: int = 10,
    similarity_threshold: float = 0.7
) -> List[Dict[str, Any]]:
    """
    Find documents similar to a reference document.

    Use this to find related content or cluster similar documents.

    Args:
        reference_doc_id: ID of the document to find similar items for
        max_results: Maximum similar documents to return (default: 10)
        similarity_threshold: Minimum similarity score, 0.0-1.0 (default: 0.7)

    Returns:
        List of similar documents with:
        - id (str): Document ID
        - title (str): Title
        - content (str): Content
        - similarity (float): Similarity to reference (0.0-1.0)
        - shared_topics (list): Topics in common with reference

    Raises:
        KeyError: If reference_doc_id doesn't exist

    Example:
        similar = find_similar_documents(
            "doc_12345",
            max_results=5,
            similarity_threshold=0.8
        )
    """
    # Implementation here
    pass


# ============================================================================
# USAGE EXAMPLE: Building a RAG Agent
# ============================================================================

if __name__ == "__main__":
    # Example: Using search tools in an agent workflow

    user_query = "What are the best practices for prompt engineering?"

    # Step 1: Initial search
    # The tool bodies above are stubs (`pass` returns None), so fall back to []
    # until you fill them in.
    results = search_knowledge_base(user_query, max_results=10) or []

    # Step 2: Filter by relevance
    high_quality = [r for r in results if r['score'] > 0.75]

    # Step 3: Find similar docs to top result
    similar = []
    if high_quality:
        similar = find_similar_documents(
            high_quality[0]['id'],
            max_results=5
        ) or []

    # Step 4: Combine for context
    all_docs = high_quality + similar

    print(f"Found {len(all_docs)} relevant documents")

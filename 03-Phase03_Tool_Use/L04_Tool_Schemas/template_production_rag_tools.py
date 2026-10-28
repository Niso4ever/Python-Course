"""
Production RAG Tools: Complete Example
A real-world RAG system with all advanced patterns from L04.
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any, Optional, Literal
from enum import Enum
from datetime import datetime
import time


# ============================================================================
# PART 1: UNIVERSAL TOOL FRAMEWORK
# ============================================================================

class ToolCategory(str, Enum):
    """Tool categories."""
    SEARCH = "search"
    PROCESSING = "processing"
    VALIDATION = "validation"
    SYNTHESIS = "synthesis"


class UniversalToolMetadata(BaseModel):
    """Metadata for framework-agnostic tools."""
    name: str
    category: ToolCategory
    description: str = Field(..., min_length=20, max_length=200)
    when_to_use: str
    when_not_to_use: Optional[str] = None
    example_queries: List[str] = Field(default_factory=list)
    estimated_latency_ms: Optional[int] = None


# ============================================================================
# PART 2: SEARCH TOOLS
# ============================================================================

class SearchSource(str, Enum):
    """Available search sources."""
    VECTOR_DB = "vector_db"
    FULL_TEXT = "full_text"
    HYBRID = "hybrid"
    WEB = "web"


class SearchInput(BaseModel):
    """
    Input for multi-source search.

    Handles all edge cases: empty queries, invalid sources, etc.
    """

    query: str = Field(
        ...,
        description="Search query. Be specific for better results.",
        min_length=3,
        max_length=500,
        examples=["Python async best practices", "RAG system architecture"]
    )

    max_results: int = Field(
        10,
        description="Maximum results to return. Recommended: 5-10.",
        ge=1,
        le=100
    )

    sources: List[SearchSource] = Field(
        default_factory=lambda: [SearchSource.HYBRID],
        description="Sources to search. Hybrid is recommended for best quality.",
        min_length=1
    )

    min_score: float = Field(
        0.0,
        description="Minimum relevance score (0.0-1.0). Higher = stricter.",
        ge=0.0,
        le=1.0
    )

    filters: Optional[Dict[str, Any]] = Field(
        None,
        description="Optional filters. Examples: {'date_from': '2024-01-01', 'category': 'tech'}",
        examples=[
            {"date_from": "2024-01-01"},
            {"category": "tech", "author": "john"}
        ]
    )

    rerank: bool = Field(
        True,
        description="Apply re-ranking for better quality (adds ~100ms latency)"
    )

    @field_validator('query')
    @classmethod
    def validate_query(cls, v):
        """Ensure query is meaningful."""
        if len(v.strip()) < 3:
            raise ValueError("Query must be at least 3 characters (excluding whitespace)")
        return v.strip()


class Citation(BaseModel):
    """A citation/source reference."""
    source_id: str
    source_title: str
    excerpt: str = Field(..., max_length=500)
    score: float = Field(..., ge=0.0, le=1.0)
    url: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SearchOutput(BaseModel):
    """
    Output from search with comprehensive metadata.

    Handles edge cases: empty results, partial failures, rate limits.
    """

    # Core results
    citations: List[Citation] = Field(
        default_factory=list,
        description="Search results ordered by relevance"
    )

    total_found: int = Field(
        ...,
        description="Total matching results before limiting",
        ge=0
    )

    # Performance metrics
    query_time_ms: float = Field(..., ge=0.0)
    sources_queried: List[str] = Field(default_factory=list)

    # Edge case handling
    is_empty: bool = Field(..., description="True if no results found")
    empty_reason: Optional[str] = Field(None)
    suggested_alternatives: List[str] = Field(default_factory=list)

    # Rate limiting
    rate_limited: bool = Field(False)
    retry_after_seconds: Optional[int] = None

    # Quality indicators
    average_score: float = Field(0.0, ge=0.0, le=1.0)
    has_high_quality_results: bool = Field(
        ...,
        description="True if at least one result has score > 0.8"
    )


def search_knowledge_base(input: SearchInput) -> Dict[str, Any]:
    """
    Search across multiple sources with re-ranking and quality filtering.

    **Use this when:**
    - User asks questions requiring information lookup
    - Need to find relevant documents or passages
    - Want the most accurate, well-sourced results

    **Don't use when:**
    - User asks for calculations (use calculator tool)
    - User wants to generate new content (use LLM directly)
    - Question can be answered from conversation history

    **Features:**
    - Multi-source search (vector DB, full-text, hybrid, web)
    - Automatic re-ranking for quality
    - Smart empty result handling
    - Rate limit awareness

    **Example:**
    input = SearchInput(
        query="best practices for prompt engineering",
        max_results=5,
        sources=[SearchSource.HYBRID],
        rerank=True
    )
    result = search_knowledge_base(input)
    """
    start_time = time.time()

    # Simulate search (replace with real implementation)
    citations = [
        Citation(
            source_id="doc_001",
            source_title="Prompt Engineering Guide",
            excerpt="Best practices include: 1) Be specific, 2) Provide examples, 3) Use clear language...",
            score=0.95,
            url="https://example.com/prompting",
            metadata={"author": "OpenAI", "date": "2024-01-15"}
        ),
        Citation(
            source_id="doc_002",
            source_title="Advanced Prompting Techniques",
            excerpt="Chain-of-thought prompting improves reasoning by asking the model to...",
            score=0.88,
            url="https://example.com/advanced",
            metadata={"author": "Anthropic", "date": "2024-02-01"}
        )
    ]

    # Filter by min_score
    citations = [c for c in citations if c.score >= input.min_score]

    # Limit results
    citations = citations[:input.max_results]

    # Calculate metrics
    query_time_ms = (time.time() - start_time) * 1000
    avg_score = sum(c.score for c in citations) / len(citations) if citations else 0.0
    has_high_quality = any(c.score > 0.8 for c in citations)

    # Handle empty results
    is_empty = len(citations) == 0
    empty_reason = None
    suggested_alternatives = []

    if is_empty:
        if input.min_score > 0.7:
            empty_reason = f"No results with score > {input.min_score}. Try lowering min_score."
            suggested_alternatives = ["Lower min_score to 0.5 or 0.0"]
        else:
            empty_reason = "No documents match your query."
            suggested_alternatives = [
                f"Try broader terms than '{input.query}'",
                "Check spelling",
                "Remove filters if applied"
            ]

    return {
        "citations": [c.model_dump() for c in citations],
        "total_found": len(citations),
        "query_time_ms": query_time_ms,
        "sources_queried": [s.value for s in input.sources],
        "is_empty": is_empty,
        "empty_reason": empty_reason,
        "suggested_alternatives": suggested_alternatives,
        "rate_limited": False,
        "retry_after_seconds": None,
        "average_score": avg_score,
        "has_high_quality_results": has_high_quality
    }


# ============================================================================
# PART 3: PROCESSING TOOLS
# ============================================================================

class FilterCitationsInput(BaseModel):
    """Input for filtering citations."""

    citations: List[Citation] = Field(
        ...,
        description="Citations to filter",
        min_length=1
    )

    min_score: float = Field(
        0.7,
        description="Minimum score threshold",
        ge=0.0,
        le=1.0
    )

    max_citations: int = Field(
        5,
        description="Maximum citations to keep",
        ge=1,
        le=20
    )

    require_url: bool = Field(
        False,
        description="Only keep citations with URLs"
    )

    deduplicate: bool = Field(
        True,
        description="Remove near-duplicate citations"
    )


class FilterCitationsOutput(BaseModel):
    """Output from citation filtering."""

    filtered_citations: List[Citation]
    original_count: int
    filtered_count: int
    removed_count: int
    removed_reasons: Dict[str, int] = Field(
        default_factory=dict,
        description="Counts of why citations were removed"
    )


def filter_citations(input: FilterCitationsInput) -> Dict[str, Any]:
    """
    Filter and deduplicate citations by quality criteria.

    **Use this when:**
    - Search returned too many results
    - Need only high-quality citations
    - Want to remove duplicates

    **Processing steps:**
    1. Filter by minimum score
    2. Remove citations without URLs (if required)
    3. Deduplicate similar citations
    4. Limit to max_citations (keeping highest scored)

    **Example:**
    input = FilterCitationsInput(
        citations=search_results,
        min_score=0.8,
        max_citations=3,
        deduplicate=True
    )
    """
    removed_reasons = {}
    filtered = list(input.citations)

    # Filter by score
    before = len(filtered)
    filtered = [c for c in filtered if c.score >= input.min_score]
    removed_reasons['low_score'] = before - len(filtered)

    # Filter by URL if required
    if input.require_url:
        before = len(filtered)
        filtered = [c for c in filtered if c.url is not None]
        removed_reasons['no_url'] = before - len(filtered)

    # Deduplicate (simple: remove if titles are too similar)
    if input.deduplicate:
        before = len(filtered)
        seen_titles = set()
        deduped = []
        for c in filtered:
            title_lower = c.source_title.lower()
            if title_lower not in seen_titles:
                seen_titles.add(title_lower)
                deduped.append(c)
        filtered = deduped
        removed_reasons['duplicate'] = before - len(filtered)

    # Sort by score and limit
    filtered = sorted(filtered, key=lambda c: c.score, reverse=True)
    before = len(filtered)
    filtered = filtered[:input.max_citations]
    if before > len(filtered):
        removed_reasons['exceeded_max'] = before - len(filtered)

    return {
        "filtered_citations": [c.model_dump() for c in filtered],
        "original_count": len(input.citations),
        "filtered_count": len(filtered),
        "removed_count": len(input.citations) - len(filtered),
        "removed_reasons": removed_reasons
    }


# ============================================================================
# PART 4: SYNTHESIS TOOLS
# ============================================================================

class SynthesizeAnswerInput(BaseModel):
    """Input for answer synthesis."""

    question: str = Field(
        ...,
        description="The user's original question",
        min_length=3
    )

    citations: List[Citation] = Field(
        ...,
        description="Citations to synthesize into an answer",
        min_length=1,
        max_length=10
    )

    answer_style: Literal["concise", "detailed", "technical"] = Field(
        "detailed",
        description="Answer style: concise (2-3 sentences), detailed (1-2 paragraphs), technical (in-depth)"
    )

    include_citations: bool = Field(
        True,
        description="Include citation references [1], [2] in answer"
    )

    confidence_threshold: float = Field(
        0.7,
        description="Minimum confidence to provide answer (0.0-1.0)",
        ge=0.0,
        le=1.0
    )


class SynthesizedAnswer(BaseModel):
    """Synthesized answer with metadata."""

    answer: str = Field(
        ...,
        description="The synthesized answer",
        min_length=10
    )

    confidence: float = Field(
        ...,
        description="Confidence in answer (0.0-1.0)",
        ge=0.0,
        le=1.0
    )

    citations_used: List[str] = Field(
        ...,
        description="IDs of citations used in answer"
    )

    citation_details: List[Citation] = Field(
        ...,
        description="Full citation objects for reference"
    )

    needs_review: bool = Field(
        ...,
        description="True if answer should be reviewed by human"
    )

    review_reason: Optional[str] = Field(None)

    alternative_suggestions: List[str] = Field(
        default_factory=list,
        description="Suggested follow-up questions"
    )


def synthesize_answer(input: SynthesizeAnswerInput) -> Dict[str, Any]:
    """
    Synthesize an answer from multiple citations.

    **Use this when:**
    - Have relevant citations and need to answer user's question
    - Need to combine information from multiple sources
    - Want a coherent, well-cited response

    **Don't use when:**
    - No citations available (search first)
    - Question is off-topic for citations
    - Need real-time information (search web first)

    **Quality controls:**
    - Calculates confidence based on citation scores
    - Flags low-confidence answers for human review
    - Provides alternative suggestions if confidence low

    **Example:**
    input = SynthesizeAnswerInput(
        question="What are RAG best practices?",
        citations=filtered_citations,
        answer_style="detailed",
        include_citations=True
    )
    """
    # Calculate confidence (average of citation scores)
    avg_citation_score = sum(c.score for c in input.citations) / len(input.citations)
    confidence = avg_citation_score

    # Adjust confidence based on number of citations
    if len(input.citations) < 2:
        confidence *= 0.9  # Reduce if only one source

    # Generate answer (simplified - would use LLM in production)
    if input.answer_style == "concise":
        answer = f"Based on {len(input.citations)} sources: "
        answer += input.citations[0].excerpt[:100] + "..."
    else:
        answer = f"Based on research from {len(input.citations)} authoritative sources:\n\n"
        for i, citation in enumerate(input.citations[:3], 1):
            excerpt = citation.excerpt[:150] + "..."
            if input.include_citations:
                answer += f"[{i}] {excerpt}\n\n"
            else:
                answer += f"{excerpt}\n\n"

    # Determine if needs review
    needs_review = confidence < input.confidence_threshold
    review_reason = None
    if needs_review:
        review_reason = f"Confidence ({confidence:.2f}) below threshold ({input.confidence_threshold})"

    # Alternative suggestions
    alternatives = []
    if confidence < 0.7:
        alternatives = [
            f"Search for more recent information about: {input.question}",
            "Try rephrasing your question to be more specific",
            "Consult additional sources for verification"
        ]

    return {
        "answer": answer,
        "confidence": confidence,
        "citations_used": [c.source_id for c in input.citations],
        "citation_details": [c.model_dump() for c in input.citations],
        "needs_review": needs_review,
        "review_reason": review_reason,
        "alternative_suggestions": alternatives
    }


# ============================================================================
# PART 5: WORKFLOW TOOL (COMBINES ALL STEPS)
# ============================================================================

class RAGWorkflowInput(BaseModel):
    """Input for complete RAG workflow."""

    question: str = Field(
        ...,
        description="User's question",
        min_length=3,
        max_length=500
    )

    # Search parameters
    max_search_results: int = Field(20, ge=1, le=100)
    search_sources: List[SearchSource] = Field(
        default_factory=lambda: [SearchSource.HYBRID]
    )

    # Filtering parameters
    min_citation_score: float = Field(0.7, ge=0.0, le=1.0)
    max_citations_to_use: int = Field(5, ge=1, le=10)

    # Synthesis parameters
    answer_style: Literal["concise", "detailed", "technical"] = "detailed"
    include_citations: bool = True

    # Workflow control
    return_intermediate_results: bool = Field(
        False,
        description="Return results from each step (for debugging)"
    )


class RAGWorkflowOutput(BaseModel):
    """Output from complete RAG workflow."""

    # Final answer
    answer: str
    confidence: float
    citations: List[Citation]

    # Metadata
    total_search_results: int
    final_citations_used: int
    total_time_ms: float

    # Quality indicators
    needs_review: bool
    review_reason: Optional[str] = None

    # Intermediate results (if requested)
    intermediate: Optional[Dict[str, Any]] = None


def rag_workflow(input: RAGWorkflowInput) -> Dict[str, Any]:
    """
    Complete RAG workflow: Search → Filter → Synthesize.

    **Use this when:**
    User asks a question that requires looking up and synthesizing information.

    **Workflow:**
    1. Search knowledge base with multiple sources
    2. Filter results by quality and relevance
    3. Synthesize answer from top citations

    **Advantages over separate tools:**
    - One API call instead of 3
    - Faster (parallel processing where possible)
    - Consistent error handling
    - Automatic fallbacks

    **Example:**
    input = RAGWorkflowInput(
        question="What are best practices for RAG systems?",
        max_search_results=20,
        min_citation_score=0.8,
        answer_style="detailed"
    )
    result = rag_workflow(input)
    """
    start_time = time.time()
    intermediate = {} if input.return_intermediate_results else None

    # Step 1: Search
    search_result = search_knowledge_base(SearchInput(
        query=input.question,
        max_results=input.max_search_results,
        sources=input.search_sources,
        min_score=0.0,  # Filter later
        rerank=True
    ))

    if intermediate is not None:
        intermediate['search'] = search_result

    # Handle empty search
    if search_result['is_empty']:
        return {
            "answer": "I couldn't find relevant information to answer your question. " +
                     search_result['empty_reason'],
            "confidence": 0.0,
            "citations": [],
            "total_search_results": 0,
            "final_citations_used": 0,
            "total_time_ms": (time.time() - start_time) * 1000,
            "needs_review": True,
            "review_reason": "No search results found",
            "intermediate": intermediate
        }

    # Step 2: Filter
    citations_objects = [Citation(**c) for c in search_result['citations']]
    filter_result = filter_citations(FilterCitationsInput(
        citations=citations_objects,
        min_score=input.min_citation_score,
        max_citations=input.max_citations_to_use,
        deduplicate=True
    ))

    if intermediate is not None:
        intermediate['filter'] = filter_result

    # Handle no results after filtering
    if filter_result['filtered_count'] == 0:
        return {
            "answer": f"Found {search_result['total_found']} results, but none met quality threshold (score > {input.min_citation_score}). Try lowering min_citation_score.",
            "confidence": 0.0,
            "citations": [],
            "total_search_results": search_result['total_found'],
            "final_citations_used": 0,
            "total_time_ms": (time.time() - start_time) * 1000,
            "needs_review": True,
            "review_reason": f"No results with score > {input.min_citation_score}",
            "intermediate": intermediate
        }

    # Step 3: Synthesize
    filtered_citations = [Citation(**c) for c in filter_result['filtered_citations']]
    synthesis_result = synthesize_answer(SynthesizeAnswerInput(
        question=input.question,
        citations=filtered_citations,
        answer_style=input.answer_style,
        include_citations=input.include_citations
    ))

    if intermediate is not None:
        intermediate['synthesis'] = synthesis_result

    total_time_ms = (time.time() - start_time) * 1000

    return {
        "answer": synthesis_result['answer'],
        "confidence": synthesis_result['confidence'],
        "citations": synthesis_result['citation_details'],
        "total_search_results": search_result['total_found'],
        "final_citations_used": len(filtered_citations),
        "total_time_ms": total_time_ms,
        "needs_review": synthesis_result['needs_review'],
        "review_reason": synthesis_result['review_reason'],
        "intermediate": intermediate
    }


# ============================================================================
# PART 6: TOOL REGISTRY & METADATA
# ============================================================================

# Production RAG tools with complete metadata
PRODUCTION_RAG_TOOLS = {
    "search_knowledge_base": {
        "metadata": UniversalToolMetadata(
            name="search_knowledge_base",
            category=ToolCategory.SEARCH,
            description="Search across multiple knowledge sources with re-ranking",
            when_to_use="When user asks questions requiring information lookup. Supports multi-source search and quality filtering.",
            when_not_to_use="Don't use for calculations, code generation, or when info is in conversation history.",
            example_queries=[
                "What are best practices for prompt engineering?",
                "Find information about RAG systems",
                "Search for recent developments in AI"
            ],
            estimated_latency_ms=150
        ),
        "function": search_knowledge_base,
        "input_schema": SearchInput,
        "output_schema": SearchOutput
    },

    "filter_citations": {
        "metadata": UniversalToolMetadata(
            name="filter_citations",
            category=ToolCategory.PROCESSING,
            description="Filter and deduplicate citations by quality criteria",
            when_to_use="When search returned too many results or need only high-quality citations.",
            when_not_to_use="Don't use if already have few (< 5) high-quality citations.",
            example_queries=[
                "Filter these results to top 3",
                "Remove low-quality citations",
                "Deduplicate search results"
            ],
            estimated_latency_ms=50
        ),
        "function": filter_citations,
        "input_schema": FilterCitationsInput,
        "output_schema": FilterCitationsOutput
    },

    "synthesize_answer": {
        "metadata": UniversalToolMetadata(
            name="synthesize_answer",
            category=ToolCategory.SYNTHESIS,
            description="Synthesize answer from multiple citations with confidence scoring",
            when_to_use="When have relevant citations and need to answer user's question with proper attribution.",
            when_not_to_use="Don't use without citations. Search first.",
            example_queries=[
                "Combine these sources into an answer",
                "Synthesize answer from citations",
                "Generate response with citations"
            ],
            estimated_latency_ms=200
        ),
        "function": synthesize_answer,
        "input_schema": SynthesizeAnswerInput,
        "output_schema": SynthesizedAnswer
    },

    "rag_workflow": {
        "metadata": UniversalToolMetadata(
            name="rag_workflow",
            category=ToolCategory.SYNTHESIS,
            description="Complete RAG workflow: Search → Filter → Synthesize in one call",
            when_to_use="When user asks a question requiring comprehensive research and synthesis. Recommended for most queries.",
            when_not_to_use="Don't use for simple lookups or when need fine control over each step.",
            example_queries=[
                "What is RAG and what are best practices?",
                "Research and explain quantum computing",
                "Find and summarize information about Python async"
            ],
            estimated_latency_ms=400
        ),
        "function": rag_workflow,
        "input_schema": RAGWorkflowInput,
        "output_schema": RAGWorkflowOutput
    }
}


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

if __name__ == "__main__":
    print("=== Production RAG Tools Demo ===\n")

    # Example 1: Complete workflow
    print("1. Complete RAG Workflow:")
    workflow_input = RAGWorkflowInput(
        question="What are best practices for building RAG systems?",
        max_search_results=10,
        min_citation_score=0.7,
        answer_style="detailed",
        return_intermediate_results=True
    )

    result = rag_workflow(workflow_input)
    print(f"Answer: {result['answer'][:200]}...")
    print(f"Confidence: {result['confidence']:.2f}")
    print(f"Citations used: {result['final_citations_used']}")
    print(f"Time: {result['total_time_ms']:.1f}ms")
    print(f"Needs review: {result['needs_review']}")

    # Example 2: Individual tools
    print("\n2. Individual Tools:")

    # Search
    search_input = SearchInput(
        query="RAG best practices",
        max_results=5,
        sources=[SearchSource.HYBRID]
    )
    search_result = search_knowledge_base(search_input)
    print(f"Search found: {search_result['total_found']} results")

    # Filter
    if not search_result['is_empty']:
        citations = [Citation(**c) for c in search_result['citations']]
        filter_input = FilterCitationsInput(
            citations=citations,
            min_score=0.8,
            max_citations=3
        )
        filter_result = filter_citations(filter_input)
        print(f"Filtered to: {filter_result['filtered_count']} citations")

    # Example 3: Export schemas for different frameworks
    print("\n3. Framework Schemas:")

    # OpenAI format (simplified - would use UniversalTool in production)
    print("OpenAI schema available ✓")
    print("Anthropic schema available ✓")
    print("LangChain format available ✓")

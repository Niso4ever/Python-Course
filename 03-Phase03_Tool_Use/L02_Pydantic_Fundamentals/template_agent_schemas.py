"""
Template: Pydantic Schemas for AI Agents
Production-ready patterns for tool inputs, outputs, and configurations.
"""

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Dict, Any, Optional, Literal, Union
from datetime import datetime


# ============================================================================
# PATTERN 1: Search Tool Input/Output
# ============================================================================

class SearchToolInput(BaseModel):
    """Input schema for a search tool."""

    query: str = Field(
        ...,
        description="The search query string",
        min_length=1,
        max_length=500
    )
    max_results: int = Field(
        10,
        description="Maximum number of results to return",
        ge=1,
        le=100
    )
    filters: Optional[Dict[str, Any]] = Field(
        None,
        description="Optional filters (e.g., {'category': 'tech', 'date_from': '2024-01-01'})"
    )


class SearchResult(BaseModel):
    """A single search result."""

    id: str = Field(..., description="Unique result ID")
    title: str = Field(..., description="Result title")
    content: str = Field(..., description="Result content/snippet")
    score: float = Field(..., description="Relevance score (0.0-1.0)", ge=0.0, le=1.0)
    source: str = Field(..., description="Source name or URL")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class SearchToolOutput(BaseModel):
    """Output schema for a search tool."""

    results: List[SearchResult] = Field(
        default_factory=list,
        description="List of search results"
    )
    total_results: int = Field(..., description="Total number of results found", ge=0)
    query_time_ms: float = Field(..., description="Query execution time in milliseconds", ge=0.0)
    query_processed: str = Field(..., description="The actual query that was executed")


# ============================================================================
# PATTERN 2: LLM Response with Citations
# ============================================================================

class Citation(BaseModel):
    """A citation/source reference."""

    source_id: str = Field(..., description="ID of the source document")
    source_name: str = Field(..., description="Name or title of the source")
    excerpt: str = Field(..., description="Relevant excerpt from the source")
    confidence: float = Field(
        ...,
        description="Confidence in this citation (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    url: Optional[str] = Field(None, description="URL to the source if available")


class StructuredLLMResponse(BaseModel):
    """Structured output from an LLM with citations and metadata."""

    answer: str = Field(..., description="The main answer text", min_length=1)

    citations: List[Citation] = Field(
        default_factory=list,
        description="Sources used to generate the answer"
    )

    confidence: float = Field(
        ...,
        description="Overall confidence in the answer (0.0-1.0)",
        ge=0.0,
        le=1.0
    )

    reasoning: Optional[str] = Field(
        None,
        description="Chain-of-thought reasoning (if available)"
    )

    needs_human_review: bool = Field(
        False,
        description="Whether this answer should be reviewed by a human"
    )

    tags: List[str] = Field(
        default_factory=list,
        description="Relevant topic tags"
    )

    generated_at: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp when response was generated"
    )

    @model_validator(mode="after")
    def validate_citations(self):
        """Ensure high-confidence answers have citations.

        Checks two fields together, so it runs after the whole model is built
        (Pydantic v2 model_validator). A field_validator only sees the fields
        declared above it, and 'confidence' is declared below 'citations'.
        """
        if self.confidence > 0.8:
            if len(self.citations) == 0:
                raise ValueError("High confidence answers must have at least one citation")
        return self


# ============================================================================
# PATTERN 3: Agent Configuration
# ============================================================================

class ModelConfig(BaseModel):
    """LLM model configuration."""

    provider: Literal["openai", "anthropic", "google", "local"] = Field(
        ...,
        description="LLM provider"
    )

    model_name: str = Field(
        ...,
        description="Specific model name (e.g., 'gpt-4', 'claude-opus-5-5')"
    )

    temperature: float = Field(
        0.7,
        description="Sampling temperature (0.0 = deterministic, 2.0 = very random)",
        ge=0.0,
        le=2.0
    )

    max_tokens: int = Field(
        2000,
        description="Maximum tokens in response",
        ge=1,
        le=128000
    )

    top_p: float = Field(
        1.0,
        description="Nucleus sampling parameter",
        ge=0.0,
        le=1.0
    )


class AgentConfig(BaseModel):
    """Complete configuration for an AI agent."""

    # Identity
    name: str = Field(..., description="Agent name", min_length=1)
    role: str = Field(..., description="Agent's role/specialty")
    goal: str = Field(..., description="Agent's primary goal")
    backstory: Optional[str] = Field(None, description="Agent's background/context")

    # Model settings
    # Named llm_config, not model_config: Pydantic v2 reserves model_config for class settings.
    llm_config: ModelConfig = Field(..., description="LLM configuration")

    # Capabilities
    available_tools: List[str] = Field(
        default_factory=list,
        description="List of tool names this agent can use"
    )

    max_iterations: int = Field(
        10,
        description="Maximum reasoning iterations",
        ge=1,
        le=50
    )

    # Behavior
    allow_delegation: bool = Field(
        False,
        description="Whether this agent can delegate to other agents"
    )

    verbose: bool = Field(
        False,
        description="Whether to output detailed logs"
    )

    requires_approval: bool = Field(
        True,
        description="Whether actions require human approval"
    )

    # Safety
    timeout_seconds: int = Field(
        300,
        description="Maximum execution time in seconds",
        ge=1,
        le=3600
    )

    max_cost_usd: Optional[float] = Field(
        None,
        description="Maximum allowed cost in USD (None = no limit)",
        ge=0.0
    )


# ============================================================================
# PATTERN 4: Multi-Tool Action Schema
# ============================================================================

class ToolAction(BaseModel):
    """A single tool invocation."""

    tool_name: str = Field(..., description="Name of the tool to invoke")
    parameters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Parameters to pass to the tool"
    )
    reason: Optional[str] = Field(
        None,
        description="Why this tool was chosen"
    )


class AgentAction(BaseModel):
    """Complete action plan from an agent."""

    thought: str = Field(..., description="Agent's reasoning/thinking")

    actions: List[ToolAction] = Field(
        ...,
        description="List of tool actions to execute (in order)",
        min_length=1
    )

    expected_outcome: str = Field(
        ...,
        description="What the agent expects to achieve"
    )

    @field_validator('actions')
    @classmethod
    def validate_actions(cls, v):
        """Ensure action list is not too long."""
        if len(v) > 5:
            raise ValueError("Cannot execute more than 5 actions in one step")
        return v


class AgentObservation(BaseModel):
    """Result from executing agent actions."""

    action_results: List[Dict[str, Any]] = Field(
        ...,
        description="Results from each action (same order as actions)"
    )

    errors: List[str] = Field(
        default_factory=list,
        description="Any errors that occurred"
    )

    total_time_ms: float = Field(..., description="Total execution time", ge=0.0)


# ============================================================================
# PATTERN 5: Conversation/Message Schemas
# ============================================================================

class Message(BaseModel):
    """A single message in a conversation."""

    role: Literal["system", "user", "assistant", "function"] = Field(
        ...,
        description="Message role"
    )

    content: str = Field(..., description="Message content")

    name: Optional[str] = Field(
        None,
        description="Name of the function (if role is 'function')"
    )

    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata (timestamps, model info, etc.)"
    )


class Conversation(BaseModel):
    """A complete conversation thread."""

    id: str = Field(..., description="Unique conversation ID")

    messages: List[Message] = Field(
        default_factory=list,
        description="List of messages in chronological order"
    )

    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Conversation-level metadata"
    )

    created_at: datetime = Field(
        default_factory=datetime.now,
        description="When the conversation started"
    )

    def add_message(self, role: str, content: str, **kwargs) -> None:
        """Helper method to add a message to the conversation."""
        self.messages.append(
            Message(role=role, content=content, metadata=kwargs)
        )

    def get_context_window(self, max_messages: int = 10) -> List[Message]:
        """Get the most recent N messages."""
        return self.messages[-max_messages:]


# ============================================================================
# PATTERN 6: RAG Document Schema
# ============================================================================

class DocumentMetadata(BaseModel):
    """Metadata for a document."""

    source: str = Field(..., description="Source of the document")
    author: Optional[str] = Field(None, description="Document author")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    category: Optional[str] = Field(None, description="Document category")
    tags: List[str] = Field(default_factory=list, description="Document tags")


class Document(BaseModel):
    """A document in the knowledge base."""

    id: str = Field(..., description="Unique document ID")
    title: str = Field(..., description="Document title")
    content: str = Field(..., description="Full document content", min_length=1)
    summary: Optional[str] = Field(None, description="Document summary")
    metadata: DocumentMetadata = Field(..., description="Document metadata")
    embeddings: Optional[List[float]] = Field(None, description="Vector embeddings")


class DocumentChunk(BaseModel):
    """A chunk of a larger document."""

    chunk_id: str = Field(..., description="Unique chunk ID")
    document_id: str = Field(..., description="Parent document ID")
    content: str = Field(..., description="Chunk content", min_length=1)
    chunk_index: int = Field(..., description="Position in original document", ge=0)
    start_char: int = Field(..., description="Start character position", ge=0)
    end_char: int = Field(..., description="End character position", ge=0)
    embeddings: Optional[List[float]] = Field(None, description="Vector embeddings")


# ============================================================================
# PATTERN 7: Evaluation/Scoring Schema
# ============================================================================

class EvaluationMetrics(BaseModel):
    """Metrics for evaluating agent/LLM output."""

    accuracy: float = Field(
        ...,
        description="Accuracy score (0.0-1.0)",
        ge=0.0,
        le=1.0
    )

    relevance: float = Field(
        ...,
        description="Relevance score (0.0-1.0)",
        ge=0.0,
        le=1.0
    )

    coherence: float = Field(
        ...,
        description="Coherence score (0.0-1.0)",
        ge=0.0,
        le=1.0
    )

    completeness: float = Field(
        ...,
        description="Completeness score (0.0-1.0)",
        ge=0.0,
        le=1.0
    )

    overall: float = Field(
        ...,
        description="Overall score (0.0-1.0)",
        ge=0.0,
        le=1.0
    )

    feedback: Optional[str] = Field(
        None,
        description="Human feedback or comments"
    )


# ============================================================================
# PATTERN 8: Error Handling Schema
# ============================================================================

class ToolError(BaseModel):
    """Error information from a tool execution."""

    tool_name: str = Field(..., description="Name of the tool that failed")
    error_type: str = Field(..., description="Type of error (e.g., 'ValidationError', 'TimeoutError')")
    error_message: str = Field(..., description="Error message")
    parameters_used: Dict[str, Any] = Field(..., description="Parameters that were passed")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the error occurred")
    recoverable: bool = Field(..., description="Whether the agent can retry")


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    # Example 1: Create a search tool input
    search_input = SearchToolInput(
        query="best practices for prompt engineering",
        max_results=5,
        filters={"category": "ai", "date_from": "2024-01-01"}
    )
    print("Search Input Schema:")
    print(SearchToolInput.model_json_schema())

    # Example 2: Create an LLM response with citations
    response = StructuredLLMResponse(
        answer="Prompt engineering involves...",
        citations=[
            Citation(
                source_id="doc_123",
                source_name="OpenAI Guide",
                excerpt="Best practices include...",
                confidence=0.95,
                url="https://platform.openai.com/docs"
            )
        ],
        confidence=0.92,
        tags=["prompt-engineering", "llm", "best-practices"]
    )

    # Example 3: Create an agent configuration
    agent_config = AgentConfig(
        name="ResearchAgent",
        role="Research Specialist",
        goal="Find and synthesize information",
        llm_config=ModelConfig(
            provider="anthropic",
            model_name="claude-opus-5-5",
            temperature=0.3
        ),
        available_tools=["search", "summarize", "cite"],
        requires_approval=False
    )

    # Example 4: Build a conversation
    convo = Conversation(id="conv_123")
    convo.add_message("user", "What is RAG?")
    convo.add_message("assistant", "RAG stands for Retrieval-Augmented Generation...")

    print(f"\nConversation has {len(convo.messages)} messages")

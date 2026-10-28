"""
TEMPLATE: Metadata Storage for AI Operations
==============================================

Purpose: Store structured data about LLM calls, RAG retrievals, and agent operations
Use Case: Logging, debugging, cost tracking, quality monitoring

Pattern: Dictionary (key-value pairs)
When to use: ANY time you need to store multiple attributes about something

Copy this template when:
- Tracking LLM API calls
- Storing search result metadata
- Logging agent decisions
- Recording evaluation metrics
"""

# ============================================================================
# BASIC PATTERN: Single Operation Metadata
# ============================================================================

# Example 1: LLM API Call Metadata
llm_call_metadata = {
    "model": "claude-opus-5-5",      # Which model was used
    "provider": "anthropic",                 # Which provider (anthropic, openai, etc.)
    "tokens_used": 1523,                     # Total tokens consumed
    "input_tokens": 412,                     # Prompt tokens
    "output_tokens": 1111,                   # Completion tokens
    "latency_ms": 842,                       # Response time in milliseconds
    "temperature": 0.7,                      # Sampling temperature
    "cost_usd": 0.0234,                      # Estimated cost
    "success": True,                         # Did the call succeed?
    "timestamp": "2026-02-26T14:30:00Z"     # When did this happen
}

# How to access values:
model_used = llm_call_metadata["model"]
cost = llm_call_metadata["cost_usd"]

print(f"Used {model_used} - Cost: ${cost}")
# Output: Used claude-opus-5-5 - Cost: $0.0234


# ============================================================================
# PATTERN 2: RAG Retrieval Metadata
# ============================================================================

# Example 2: Document Retrieval Result
document_metadata = {
    "source": "internal_knowledge_base",     # Where document came from
    "doc_id": "doc_12345",                   # Unique identifier
    "relevance_score": 0.947,                # Vector similarity score (0.0-1.0)
    "chunk_index": 3,                        # Which chunk of the document
    "verified": True,                        # Was this human-verified?
    "last_updated": "2026-01-15",           # Document freshness
    "content_length": 512,                   # Characters in this chunk
    "embedding_model": "text-embedding-3"    # Which embedding model
}

# Common operations:
if document_metadata["relevance_score"] > 0.90:
    print("High-quality match")

if document_metadata["verified"]:
    print("Trusted source")


# ============================================================================
# PATTERN 3: Agent Decision Metadata
# ============================================================================

# Example 3: Agent Decision Tracking
agent_decision = {
    "step": 4,                               # Which step in the workflow
    "decision": "use_search_tool",           # What action was chosen
    "confidence": 0.85,                      # How confident (0.0-1.0)
    "reasoning": "User query requires external knowledge",  # Why this choice
    "alternatives_considered": [             # What other options existed
        "use_calculator",
        "use_summarizer"
    ],
    "execution_time_ms": 245,                # How long to decide
    "tool_called": "vector_search",          # Which tool was used
    "tool_success": True                     # Did the tool work?
}


# ============================================================================
# PATTERN 4: Nested Metadata (Metadata within Metadata)
# ============================================================================

# Example 4: Complete LLM Call with Context
full_llm_operation = {
    "request": {
        "user_query": "What is retrieval-augmented generation?",
        "system_prompt": "You are a helpful AI assistant.",
        "temperature": 0.7,
        "max_tokens": 500
    },
    "retrieval": {
        "query": "RAG retrieval-augmented generation",
        "num_results": 5,
        "top_score": 0.94,
        "sources": ["Wikipedia", "ArXiv", "Internal Docs"]
    },
    "response": {
        "content": "RAG is a technique that combines...",
        "tokens": 234,
        "latency_ms": 1240
    },
    "evaluation": {
        "factuality_score": 0.92,
        "relevance_score": 0.88,
        "toxicity_score": 0.01
    }
}

# Accessing nested data:
user_question = full_llm_operation["request"]["user_query"]
top_source = full_llm_operation["retrieval"]["sources"][0]
factuality = full_llm_operation["evaluation"]["factuality_score"]


# ============================================================================
# COMMON MISTAKES & HOW TO AVOID THEM
# ============================================================================

# ❌ MISTAKE 1: Using = instead of :
# wrong_dict = {"key" = "value"}  # SyntaxError!

# ✅ CORRECT:
correct_dict = {"key": "value"}


# ❌ MISTAKE 2: Forgetting quotes around keys
# wrong_dict = {model: "claude"}  # NameError: 'model' not defined

# ✅ CORRECT:
correct_dict = {"model": "claude"}


# ❌ MISTAKE 3: Accessing keys that don't exist
metadata = {"score": 0.95}
# value = metadata["confidence"]  # KeyError: 'confidence'

# ✅ CORRECT: Check if key exists first
if "confidence" in metadata:
    value = metadata["confidence"]
else:
    value = None  # Default value

# OR use .get() with default
value = metadata.get("confidence", 0.0)  # Returns 0.0 if key missing


# ❌ MISTAKE 4: Not handling None values
metadata = {"score": None}  # Sometimes APIs return None
# if metadata["score"] > 0.80:  # TypeError: '>' not supported for None

# ✅ CORRECT: Check for None
if metadata["score"] is not None and metadata["score"] > 0.80:
    print("High score")


# ============================================================================
# RED FLAGS TO SPOT IN AI-GENERATED CODE
# ============================================================================

# 🚩 RED FLAG 1: Storing sensitive data in plain dicts
# NEVER DO THIS:
api_key_storage = {
    "api_key": "sk-1234567890",  # ⚠️ Security risk!
    "password": "secret123"       # ⚠️ Never store plain passwords
}
# USE: Environment variables or secret managers instead


# 🚩 RED FLAG 2: Inconsistent key names
retrieval_1 = {"relevance_score": 0.95}
retrieval_2 = {"relevanceScore": 0.88}  # ⚠️ Different naming style!
# USE: Consistent naming (snake_case recommended in Python)


# 🚩 RED FLAG 3: Magic numbers without explanation
config = {
    "threshold": 0.7,  # ⚠️ Why 0.7? What does this control?
}
# BETTER: Add comments or use descriptive keys
config = {
    "confidence_threshold": 0.7,  # Minimum confidence for accepting LLM output
}


# ============================================================================
# USAGE IN REAL AI SYSTEMS
# ============================================================================

def log_llm_call(prompt, response, model="claude-opus-5-5"):
    """
    Example function showing how to use metadata in production

    This function would be called every time you interact with an LLM
    to track costs, performance, and quality.
    """
    metadata = {
        "timestamp": "2026-02-26T14:30:00Z",  # Would use real timestamp
        "model": model,
        "prompt_length": len(prompt),
        "response_length": len(response),
        "success": response is not None
    }

    # In production, you'd send this to a logging service
    print(f"LLM Call: {metadata}")

    return metadata


# Example usage:
user_query = "What is Python?"
llm_response = "Python is a programming language..."
call_metadata = log_llm_call(user_query, llm_response)


# ============================================================================
# QUICK REFERENCE: Common Metadata Patterns
# ============================================================================

"""
LLM CALL METADATA:
{
    "model": str,           # Model name
    "tokens": int,          # Token count
    "cost": float,          # USD cost
    "latency_ms": int,      # Response time
    "success": bool         # Did it work?
}

DOCUMENT METADATA:
{
    "source": str,          # Where it came from
    "score": float,         # Relevance (0.0-1.0)
    "verified": bool,       # Is it trusted?
    "doc_id": str          # Unique identifier
}

AGENT DECISION METADATA:
{
    "step": int,            # Which step
    "action": str,          # What action
    "confidence": float,    # How confident (0.0-1.0)
    "reasoning": str        # Why this choice
}
"""


# ============================================================================
# YOUR TASK: Pattern Recognition
# ============================================================================

"""
When you see this in AI-generated code:

    result = {
        "status": "success",
        "data": processed_output,
        "metrics": {"accuracy": 0.92}
    }

You should immediately recognize:
1. This is a dictionary (curly braces)
2. It has 3 keys: "status", "data", "metrics"
3. "metrics" contains nested metadata
4. This is likely a function return value with metadata

You DON'T need to memorize the syntax.
You DO need to recognize this is "metadata storage pattern."
"""

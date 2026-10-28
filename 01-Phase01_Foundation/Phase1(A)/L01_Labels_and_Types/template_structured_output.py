"""
MY PERSONAL TEMPLATE: Structured LLM Output
============================================
How to make LLMs return data in a specific format

Usage:
1. Define your desired output structure
2. Include it in the prompt
3. LLM returns data in that exact format
4. Easy to parse and use in your code
"""

# ============================================================================
# PATTERN 1: Simple Abstract + Bullet Points
# ============================================================================

# Define the structure you want
desired_output_format = {
    "abstract": "High-level summary",
    "bullet_points": [
        "Key point 1",
        "Key point 2",
        "Key point 3"
    ]
}

# Build your prompt to request this format
prompt_template = """
Please analyze the following topic and return your response in this EXACT JSON format:

{{
    "abstract": "A concise 1-2 sentence summary",
    "bullet_points": [
        "First key insight",
        "Second key insight",
        "Third key insight"
    ]
}}

Topic: {user_topic}

IMPORTANT: Return ONLY valid JSON, no other text before or after.
"""

# Fill in the topic
user_topic = "What is retrieval-augmented generation?"
final_prompt = prompt_template.format(user_topic=user_topic)

# Send to LLM (simulated response)
llm_response = {
    "abstract": "RAG is a technique that enhances LLM responses by retrieving relevant documents from a knowledge base before generation.",
    "bullet_points": [
        "Combines vector search with language models",
        "Reduces hallucinations by grounding in real documents",
        "Widely used in Q&A systems and chatbots"
    ]
}

# Now you can access structured data easily
print("Summary:", llm_response["abstract"])
print("\nKey Points:")
for point in llm_response["bullet_points"]:
    print(f"  • {point}")


# ============================================================================
# PATTERN 2: Multi-Section Structured Output
# ============================================================================

# More complex structure for detailed analysis
comprehensive_format = {
    "abstract": "High-level overview",
    "key_concepts": [
        "Concept 1",
        "Concept 2"
    ],
    "use_cases": [
        "Use case 1",
        "Use case 2"
    ],
    "pros": [
        "Advantage 1",
        "Advantage 2"
    ],
    "cons": [
        "Limitation 1",
        "Limitation 2"
    ],
    "conclusion": "Final takeaway"
}

prompt_for_comprehensive = """
Analyze this topic and return a JSON object with these exact fields:

{{
    "abstract": "One sentence overview",
    "key_concepts": ["concept 1", "concept 2", "concept 3"],
    "use_cases": ["use case 1", "use case 2"],
    "pros": ["advantage 1", "advantage 2"],
    "cons": ["limitation 1", "limitation 2"],
    "conclusion": "Final summary"
}}

Topic: {topic}

Return ONLY valid JSON.
"""


# ============================================================================
# PATTERN 3: Nested Structure (RAG System Output)
# ============================================================================

# Structure for a complete RAG response with metadata
rag_structured_output = {
    "response": {
        "abstract": "Main answer to the question",
        "detailed_explanation": "Longer explanation if needed",
        "confidence": 0.92
    },
    "sources": [
        {
            "source_name": "Wikipedia",
            "relevance": 0.95,
            "key_quote": "Direct quote from source"
        },
        {
            "source_name": "ArXiv",
            "relevance": 0.88,
            "key_quote": "Another relevant quote"
        }
    ],
    "metadata": {
        "query": "Original user question",
        "total_sources_found": 5,
        "sources_used": 2
    }
}

# Prompt for RAG system
rag_prompt = """
Answer the user's question using the provided sources.
Return your response in this JSON format:

{{
    "response": {{
        "abstract": "Direct answer in 1-2 sentences",
        "detailed_explanation": "More detailed explanation",
        "confidence": 0.0-1.0 score
    }},
    "sources": [
        {{
            "source_name": "Name of source",
            "relevance": 0.0-1.0 score,
            "key_quote": "Supporting quote from this source"
        }}
    ],
    "metadata": {{
        "query": "The original question",
        "total_sources_found": number,
        "sources_used": number
    }}
}}

Question: {question}

Sources:
{sources}

Return ONLY valid JSON.
"""


# ============================================================================
# PATTERN 4: Custom Format for Your Specific Needs
# ============================================================================

# Example: Code explanation output
code_explanation_format = {
    "summary": "What this code does in one sentence",
    "line_by_line": [
        {"line": 1, "explanation": "What line 1 does"},
        {"line": 2, "explanation": "What line 2 does"}
    ],
    "key_concepts": ["Concept used in this code"],
    "potential_issues": ["Possible bugs or improvements"]
}

# Example: Document summarization
document_summary_format = {
    "title": "Document title",
    "abstract": "One sentence summary",
    "main_topics": ["Topic 1", "Topic 2", "Topic 3"],
    "key_findings": ["Finding 1", "Finding 2"],
    "action_items": ["Action 1", "Action 2"],
    "sentiment": "positive/negative/neutral"
}

# Example: Conversation analysis
conversation_analysis_format = {
    "summary": "What this conversation was about",
    "user_intent": "What the user wanted",
    "agent_response_quality": 0.85,
    "topics_discussed": ["Topic 1", "Topic 2"],
    "resolution_status": "resolved/pending/escalated",
    "next_steps": ["Step 1", "Step 2"]
}


# ============================================================================
# HOW TO USE THIS IN PRACTICE
# ============================================================================

def get_structured_summary(topic: str) -> dict:
    """
    Get a structured summary from LLM

    Args:
        topic: What to summarize

    Returns:
        Dictionary with abstract and bullet_points
    """

    prompt = f"""
    Analyze this topic and return JSON in this format:

    {{{{
        "abstract": "One sentence summary",
        "bullet_points": ["point 1", "point 2", "point 3"]
    }}}}

    Topic: {topic}

    Return ONLY valid JSON.
    """

    # In real code, you'd call the LLM here:
    # response = llm.generate(prompt)
    # parsed = json.loads(response)

    # Simulated response:
    result = {
        "abstract": f"Summary of {topic}",
        "bullet_points": [
            "First key insight",
            "Second key insight",
            "Third key insight"
        ]
    }

    return result


# Example usage:
summary = get_structured_summary("Machine learning basics")
print("Abstract:", summary["abstract"])
for point in summary["bullet_points"]:
    print(f"  • {point}")


# ============================================================================
# PARSING LLM RESPONSE (Important!)
# ============================================================================

import json

# LLM returns a STRING that looks like JSON
llm_raw_response = '''
{
    "abstract": "This is the summary",
    "bullet_points": ["Point 1", "Point 2", "Point 3"]
}
'''

# Parse it into a Python dictionary
parsed_output = json.loads(llm_raw_response)

# Now you can use it
print(parsed_output["abstract"])
print(parsed_output["bullet_points"][0])


# ============================================================================
# ERROR HANDLING (Important!)
# ============================================================================

def safe_parse_llm_output(raw_response: str) -> dict | None:
    """
    Safely parse LLM response, handle errors

    Args:
        raw_response: String from LLM

    Returns:
        Parsed dict or None if invalid
    """
    try:
        parsed = json.loads(raw_response)

        # Validate required fields exist
        if "abstract" in parsed and "bullet_points" in parsed:
            return parsed
        else:
            print("Error: Missing required fields")
            return None

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON - {e}")
        return None


# ============================================================================
# TIPS FOR GETTING CONSISTENT OUTPUT
# ============================================================================

"""
TIP 1: Be very explicit in your prompt
- Show the EXACT format
- Use examples
- Say "Return ONLY JSON, no other text"

TIP 2: Modern LLMs are good at JSON
- Claude 3, GPT-4 understand JSON natively
- Include "IMPORTANT: Return valid JSON" in prompt

TIP 3: Validate the response
- Check that required fields exist
- Handle missing or malformed data gracefully

TIP 4: Use system prompts
system_prompt = "You are a helpful assistant that ALWAYS returns valid JSON."

TIP 5: Consider using JSON mode (some APIs support this)
# OpenAI example:
# response = client.chat.completions.create(
#     model="gpt-4",
#     response_format={"type": "json_object"},
#     messages=[...]
# )
"""


# ============================================================================
# YOUR CUSTOM TEMPLATE
# ============================================================================

# Copy this and modify for your specific use case:
my_custom_output = {
    "abstract": "High-level details",  # Your field
    "bullet_points": [                 # Your field
        "Key takeaway 1",
        "Key takeaway 2"
    ]
    # Add more fields as needed:
    # "confidence": 0.95,
    # "sources": [...],
    # "metadata": {...}
}

# Your prompt template:
my_prompt = """
[Describe the task]

Return response in this JSON format:
{format}

[Any additional instructions]

Return ONLY valid JSON.
"""

# Use it:
formatted_prompt = my_prompt.format(format=json.dumps(my_custom_output, indent=2))

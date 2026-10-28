"""
DEMO: Try This with Claude RIGHT NOW
=====================================
Copy the prompt below and paste it into Claude to see structured output in action!
"""

# ============================================================================
# EXAMPLE PROMPT - Copy This and Send to Claude
# ============================================================================

example_prompt = """
Please analyze the topic "Retrieval-Augmented Generation (RAG)" and return your response in this EXACT JSON format:

{
    "abstract": "A concise 1-2 sentence high-level summary",
    "bullet_points": [
        "First key takeaway or insight",
        "Second key takeaway or insight",
        "Third key takeaway or insight",
        "Fourth key takeaway or insight"
    ]
}

IMPORTANT: Return ONLY the JSON object, no other text before or after.
"""

print("=" * 70)
print("COPY THE PROMPT BELOW AND SEND IT TO CLAUDE:")
print("=" * 70)
print(example_prompt)
print("=" * 70)

# ============================================================================
# WHAT CLAUDE WILL RETURN (Example)
# ============================================================================

# Claude's response will look like this:
expected_response = """{
    "abstract": "RAG is a technique that enhances large language models by retrieving relevant information from external knowledge bases before generating responses, improving accuracy and reducing hallucinations.",
    "bullet_points": [
        "Combines vector database search with LLM generation for factual grounding",
        "Significantly reduces hallucinations by using real source documents",
        "Enables LLMs to access up-to-date information beyond training data",
        "Widely used in enterprise chatbots, Q&A systems, and knowledge management tools"
    ]
}"""

print("\nCLAUDE WILL RETURN SOMETHING LIKE:")
print(expected_response)

# ============================================================================
# HOW TO USE THE RESPONSE IN YOUR CODE
# ============================================================================

import json

# After Claude returns the JSON, parse it:
response_dict = json.loads(expected_response)

# Now you can access the structured data:
print("\n" + "=" * 70)
print("ACCESSING THE STRUCTURED DATA:")
print("=" * 70)

print(f"\nAbstract: {response_dict['abstract']}")

print("\nKey Points:")
for i, point in enumerate(response_dict['bullet_points'], 1):
    print(f"{i}. {point}")

# ============================================================================
# TRY IT YOURSELF - Modify for Different Topics
# ============================================================================

def create_structured_prompt(topic: str, num_points: int = 4) -> str:
    """
    Generate a prompt that requests structured output

    Args:
        topic: What to analyze
        num_points: How many bullet points to request

    Returns:
        Formatted prompt string
    """
    return f"""
Please analyze the topic "{topic}" and return your response in this EXACT JSON format:

{{
    "abstract": "A concise 1-2 sentence high-level summary",
    "bullet_points": [
        {', '.join([f'"Point {i}"' for i in range(1, num_points + 1)])}
    ]
}}

IMPORTANT: Return ONLY the JSON object, no other text before or after.
"""


# Try different topics:
print("\n" + "=" * 70)
print("TRY THESE PROMPTS WITH CLAUDE:")
print("=" * 70)

topics = [
    "Machine Learning Basics",
    "Python for AI Development",
    "Vector Databases",
    "LangChain Framework"
]

for topic in topics:
    print(f"\n--- Prompt for: {topic} ---")
    print(create_structured_prompt(topic, num_points=3))

# ============================================================================
# ADVANCED: Custom Fields
# ============================================================================

advanced_prompt_template = """
Analyze "{topic}" and return JSON with these fields:

{{
    "abstract": "One sentence overview",
    "bullet_points": ["point 1", "point 2", "point 3"],
    "pros": ["advantage 1", "advantage 2"],
    "cons": ["limitation 1", "limitation 2"],
    "use_cases": ["use case 1", "use case 2"]
}}

Return ONLY valid JSON.
"""

print("\n" + "=" * 70)
print("ADVANCED EXAMPLE - Multiple Fields:")
print("=" * 70)
print(advanced_prompt_template.format(topic="Retrieval-Augmented Generation"))

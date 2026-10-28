"""
TEMPLATE: Prompt Formatter
===========================
Use: Build LLM prompts from separate parts

COPY this when you need to:
- Format RAG prompts
- Build system prompts
- Create structured messages
- Combine context + question

2026 note: All functions use type hints.
  def fn(param: str) -> str:  — same logic, adds type labels
"""

# ═══════════════════════════════════════════════════════════
# TEMPLATE 1: RAG Prompt Formatter
# ═══════════════════════════════════════════════════════════
def format_rag_prompt(question: str, context: str, max_length: int = 2000) -> str:
    """
    Combine question + context into LLM prompt.
    IN:  question (str), context (str), max_length (int)
    OUT: formatted prompt (str)
    """
    prompt = f"""Context:
{context}

Question: {question}

Answer based only on the context above:"""

    return prompt[:max_length]  # ← MODIFY: Your max length


# ═══════════════════════════════════════════════════════════
# TEMPLATE 2: System Prompt Builder
# ═══════════════════════════════════════════════════════════
def build_system_prompt(agent_name: str, role: str, guidelines: str, tone: str = "professional") -> str:
    """
    Build a system prompt for an agent.
    IN:  agent_name, role, guidelines, tone
    OUT: system prompt string
    """
    return f"""You are {agent_name}, a {role}.

Tone: {tone}

Guidelines:
{guidelines}

Always be accurate, concise, and helpful."""


# ═══════════════════════════════════════════════════════════
# TEMPLATE 3: Multi-Document Context Builder
# ═══════════════════════════════════════════════════════════
def build_context_from_docs(docs: list, separator: str = "\n\n---\n\n") -> str:
    """
    Combine multiple documents into single context string.
    IN:  docs (list of dicts with 'text' and 'source')
    OUT: context string with source citations
    """
    parts = []
    for i, doc in enumerate(docs, 1):
        parts.append(f"[Source {i}: {doc['source']}]\n{doc['text']}")
    return separator.join(parts)


# ═══════════════════════════════════════════════════════════
# TEMPLATE 4: Structured Output Prompt
# ═══════════════════════════════════════════════════════════
def format_structured_output_prompt(question: str, output_format: dict) -> str:
    """
    Force LLM to return specific JSON format.
    IN:  question (str), output_format (dict showing expected structure)
    OUT: prompt that requests structured JSON
    """
    import json
    format_str = json.dumps(output_format, indent=2)

    return f"""Answer this question: {question}

Return your response in this EXACT JSON format:
{format_str}

Return only the JSON, no other text."""


# ═══════════════════════════════════════════════════════════
# DEMO (Run this file to see examples)
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    # Test Template 1
    print("="*60)
    print("TEMPLATE 1: RAG Prompt")
    print("="*60)
    prompt = format_rag_prompt(
        question="What is RAG?",
        context="RAG stands for Retrieval-Augmented Generation..."
    )
    print(prompt)

    # Test Template 2
    print("\n" + "="*60)
    print("TEMPLATE 2: System Prompt")
    print("="*60)
    sys_prompt = build_system_prompt(
        agent_name="ResearchBot",
        role="AI research assistant",
        guidelines="- Always cite sources\n- Be objective\n- Admit uncertainty"
    )
    print(sys_prompt)

    # Test Template 3
    print("\n" + "="*60)
    print("TEMPLATE 3: Multi-Doc Context")
    print("="*60)
    docs = [
        {"text": "RAG combines retrieval...", "source": "Wikipedia"},
        {"text": "Vector databases store...", "source": "ArXiv"}
    ]
    context = build_context_from_docs(docs)
    print(context)

    # Test Template 4
    print("\n" + "="*60)
    print("TEMPLATE 4: Structured Output")
    print("="*60)
    output_format = {
        "answer": "string",
        "confidence": "float between 0 and 1",
        "sources": ["list", "of", "strings"]
    }
    structured_prompt = format_structured_output_prompt("What is AI?", output_format)
    print(structured_prompt)

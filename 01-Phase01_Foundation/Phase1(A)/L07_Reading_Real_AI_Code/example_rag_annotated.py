"""
LESSON 5: RAG SYSTEM EXAMPLE (ANNOTATED)
========================================
This shows a complete RAG (Retrieval-Augmented Generation) system
broken down into L1-L4 patterns.

A RAG system: Search → Retrieve Context → Generate Answer
"""

# ═══════════════════════════════════════════════════════════
# L1.5: LIST OF DICTS - Knowledge Base (THE PATTERN!)
# ═══════════════════════════════════════════════════════════
knowledge_base = [
    {
        "id": "doc1",
        "text": "RAG (Retrieval-Augmented Generation) combines retrieval with LLM generation. It searches a knowledge base first, then uses results as context.",
        "source": "Wikipedia",
        "embedding": [0.1, 0.3, 0.8, 0.2]  # Simplified vector
    },
    {
        "id": "doc2",
        "text": "Vector databases store embeddings (numerical representations) of text. They enable semantic search based on meaning, not just keywords.",
        "source": "ArXiv",
        "embedding": [0.2, 0.4, 0.7, 0.1]
    },
    {
        "id": "doc3",
        "text": "Semantic search finds similar meanings. Unlike keyword search, it understands context. 'Happy' and 'joyful' are semantically similar.",
        "source": "Blog",
        "embedding": [0.3, 0.2, 0.6, 0.4]
    },
    {
        "id": "doc4",
        "text": "Python is a programming language popular for AI development. It has libraries like LangChain, DSPy, and CrewAI.",
        "source": "Documentation",
        "embedding": [0.9, 0.1, 0.2, 0.3]
    }
]

print("✓ L1.5 PATTERN SPOTTED: knowledge_base is a list of dictionaries")
print(f"  Total documents: {len(knowledge_base)}")
print(f"  First doc ID: {knowledge_base[0]['id']}")
print()


# ═══════════════════════════════════════════════════════════
# L3: FUNCTION - Calculate similarity (simplified)
# ═══════════════════════════════════════════════════════════
def calculate_similarity(vec1, vec2):
    """
    Simplified similarity calculation (dot product)
    Real systems use cosine similarity, but this shows the concept
    """
    # L2.5: Loop to multiply and sum
    similarity = sum(a * b for a, b in zip(vec1, vec2))
    return similarity

print("✓ L3 PATTERN SPOTTED: calculate_similarity is a function/tool")
print(f"  Test similarity: {calculate_similarity([1, 0], [1, 0])}")
print()


# ═══════════════════════════════════════════════════════════
# L3: FUNCTION - Search function (the retrieval part!)
# ═══════════════════════════════════════════════════════════
def search_knowledge(query_text, query_embedding, top_k=2):
    """
    Search the knowledge base and return most similar documents
    Input: query embedding
    Output: LIST OF DICTS (L1.5!)
    """
    # L1.5: Create empty list for results
    results = []

    # L2.5: Loop through all documents
    for doc in knowledge_base:
        # L3: Calculate similarity score
        score = calculate_similarity(query_embedding, doc["embedding"])

        # L1: Create result dictionary
        result = {
            "text": doc["text"],
            "source": doc["source"],
            "score": score,
            "doc_id": doc["id"]
        }

        # L1.5: Add to results list
        results.append(result)

    # Sort by score (highest first) and return top K
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]

print("✓ L3 PATTERN SPOTTED: search_knowledge is a function")
print("  It returns a LIST OF DICTS (L1.5!)")
print()


# ═══════════════════════════════════════════════════════════
# L1: DICTIONARY - User query
# ═══════════════════════════════════════════════════════════
user_query = {
    "question": "What is RAG?",
    "user_id": "user_123",
    "timestamp": "2026-02-28",
    "embedding": [0.15, 0.35, 0.75, 0.15]  # Simplified embedding
}

print("✓ L1 PATTERN SPOTTED: user_query is a dictionary")
print(f"  Question: {user_query['question']}")
print()


# ═══════════════════════════════════════════════════════════
# STEP 1: RETRIEVE - Search for relevant documents
# ═══════════════════════════════════════════════════════════
print("="*60)
print("STEP 1: RETRIEVAL")
print("="*60)

retrieved_docs = search_knowledge(
    user_query["question"],
    user_query["embedding"],
    top_k=2
)

print(f"✓ Retrieved {len(retrieved_docs)} documents")
for i, doc in enumerate(retrieved_docs):  # ← L2.5: Loop!
    print(f"\n  Doc {i+1}:")
    print(f"    Score: {doc['score']:.3f}")
    print(f"    Source: {doc['source']}")
    print(f"    Text: {doc['text'][:60]}...")

print()


# ═══════════════════════════════════════════════════════════
# L3: FUNCTION - Format RAG prompt
# ═══════════════════════════════════════════════════════════
def format_rag_prompt(question, docs):
    """
    Combine retrieved docs with user question
    Input: question (string), docs (LIST OF DICTS)
    Output: formatted prompt (string)
    """
    # L2.5 + L1.5: Loop through list, extract text from each dict
    context_parts = []
    for doc in docs:
        context_parts.append(f"[{doc['source']}]: {doc['text']}")

    context = "\n\n".join(context_parts)

    # Format the complete prompt
    prompt = f"""Context from knowledge base:
{context}

Question: {question}

Answer based on the context above:"""

    return prompt

print("✓ L3 PATTERN SPOTTED: format_rag_prompt is a function")
print()


# ═══════════════════════════════════════════════════════════
# STEP 2: GENERATE - Create prompt for LLM
# ═══════════════════════════════════════════════════════════
print("="*60)
print("STEP 2: GENERATION (Prompt Formatting)")
print("="*60)

rag_prompt = format_rag_prompt(user_query["question"], retrieved_docs)
print(rag_prompt)
print()


# ═══════════════════════════════════════════════════════════
# L3: FUNCTION - Simulate LLM call
# ═══════════════════════════════════════════════════════════
def call_llm(prompt):
    """
    In real code, this calls Claude/GPT API
    For now, we simulate it
    """
    # Simulated response
    return "RAG combines retrieval with generation. It first searches a knowledge base for relevant information, then uses that context to generate accurate, grounded answers."

llm_answer = call_llm(rag_prompt)

print("="*60)
print("STEP 3: LLM RESPONSE")
print("="*60)
print(llm_answer)
print()


# ═══════════════════════════════════════════════════════════
# L1: DICTIONARY - Complete RAG result
# ═══════════════════════════════════════════════════════════
final_result = {
    "question": user_query["question"],
    "answer": llm_answer,
    "sources": [doc["source"] for doc in retrieved_docs],  # ← L1.5: List comprehension!
    "confidence": max([doc["score"] for doc in retrieved_docs]),  # Highest score
    "retrieved_docs": len(retrieved_docs)
}

print("="*60)
print("FINAL RESULT (DICTIONARY):")
print("="*60)
print(f"Question: {final_result['question']}")
print(f"Answer: {final_result['answer']}")
print(f"Sources: {', '.join(final_result['sources'])}")
print(f"Confidence: {final_result['confidence']:.3f}")
print(f"Docs Retrieved: {final_result['retrieved_docs']}")
print()


# ═══════════════════════════════════════════════════════════
# L2: LOGIC GATE - Quality control
# ═══════════════════════════════════════════════════════════
CONFIDENCE_THRESHOLD = 0.5

if final_result["confidence"] < CONFIDENCE_THRESHOLD:
    print("⚠️  L2 PATTERN: Low confidence detected!")
    print(f"   Confidence {final_result['confidence']:.3f} < {CONFIDENCE_THRESHOLD}")
    print("   Action: Flag for human review")
else:
    print("✓ L2 PATTERN: High confidence result")
    print(f"   Confidence {final_result['confidence']:.3f} >= {CONFIDENCE_THRESHOLD}")
    print("   Action: Safe to return to user")

print()


# ═══════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════
print("="*60)
print("🎯 PATTERNS USED IN THIS RAG SYSTEM:")
print("="*60)
print("   L1:   Dictionaries for user query and final result")
print("   L1.5: List of dicts for knowledge base and search results")
print("   L2:   If/else for confidence threshold")
print("   L2.5: For loops to process documents")
print("   L3:   Functions for search, format, LLM call")
print()
print("💡 INSIGHT: RAG = Search (L3) + List manipulation (L1.5) + Logic (L2)")
print("   The 'advanced' RAG system is just your L1-L4 patterns!")

"""
LESSON 5: PRACTICE - IDENTIFY THE PATTERNS
==========================================
Below are real-world code snippets from AI projects.
Your mission: Identify which lesson pattern each line uses.

After each code block, check your answers!
"""

print("="*60)
print("PATTERN IDENTIFICATION PRACTICE")
print("="*60)
print()
print("For each code block, identify:")
print("  L1   = Dictionary")
print("  L1.5 = List (especially list of dicts)")
print("  L2   = Logic gate (if/else)")
print("  L2.5 = Loop (for/while)")
print("  L3   = Function")
print("  L4   = Class")
print()


# ═══════════════════════════════════════════════════════════
# EXERCISE 1: Conversation Manager
# ═══════════════════════════════════════════════════════════
print("="*60)
print("EXERCISE 1: Conversation Manager")
print("="*60)
print()

code_1 = '''
conversation_history = []

system_prompt = {
    "role": "system",
    "content": "You are a helpful AI assistant"
}

conversation_history.append(system_prompt)

user_message = {"role": "user", "content": "Hello!"}
conversation_history.append(user_message)

if len(conversation_history) > 10:
    conversation_history = conversation_history[-10:]
'''

print(code_1)
print()
print("IDENTIFY THE PATTERNS:")
print("Line 1: conversation_history = []")
input("Your answer: ")
print("✓ L1.5 - Create empty list")
print()

print("Line 3-6: system_prompt = {...}")
input("Your answer: ")
print("✓ L1 - Dictionary with role and content")
print()

print("Line 8: conversation_history.append(system_prompt)")
input("Your answer: ")
print("✓ L1.5 - Add to list using .append()")
print()

print("Line 13: if len(conversation_history) > 10:")
input("Your answer: ")
print("✓ L2 - Logic gate (condition check)")
print()

print("Line 14: conversation_history[-10:]")
input("Your answer: ")
print("✓ L1.5 - List slicing (keep last 10 items)")
print()
print()


# ═══════════════════════════════════════════════════════════
# EXERCISE 2: RAG Retrieval
# ═══════════════════════════════════════════════════════════
print("="*60)
print("EXERCISE 2: RAG Retrieval")
print("="*60)
print()

code_2 = '''
def search_documents(query, top_k=3):
    results = []

    for doc in document_database:
        score = calculate_similarity(query, doc["embedding"])

        if score > 0.7:
            results.append({
                "text": doc["text"],
                "score": score,
                "source": doc["source"]
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]
'''

print(code_2)
print()
print("IDENTIFY THE PATTERNS:")
print("Line 1: def search_documents(query, top_k=3):")
input("Your answer: ")
print("✓ L3 - Function definition")
print()

print("Line 2: results = []")
input("Your answer: ")
print("✓ L1.5 - Create empty list")
print()

print("Line 4: for doc in document_database:")
input("Your answer: ")
print("✓ L2.5 - Loop through collection")
print()

print("Line 5: score = calculate_similarity(...)")
input("Your answer: ")
print("✓ L3 - Function call")
print()

print("Line 7: if score > 0.7:")
input("Your answer: ")
print("✓ L2 - Logic gate (threshold check)")
print()

print("Line 8-12: results.append({...})")
input("Your answer: ")
print("✓ L1.5 - Add dictionary to list (list of dicts!)")
print()

print("Line 15: return results[:top_k]")
input("Your answer: ")
print("✓ L1.5 - List slicing (return first top_k items)")
print()
print()


# ═══════════════════════════════════════════════════════════
# EXERCISE 3: Agent Class
# ═══════════════════════════════════════════════════════════
print("="*60)
print("EXERCISE 3: Agent Class")
print("="*60)
print()

code_3 = '''
class RAGAgent:
    def __init__(self, model_name, vector_db):
        self.model = model_name
        self.db = vector_db
        self.query_count = 0

    def search_and_answer(self, question):
        # Retrieve
        docs = self.db.search(question, top_k=3)
        self.query_count += 1

        # Format
        context = "\\n".join([d["text"] for d in docs])

        # Generate
        answer = self.model.invoke(f"Context: {context}\\nQ: {question}")

        return {
            "question": question,
            "answer": answer,
            "sources": [d["source"] for d in docs]
        }

agent = RAGAgent("claude-opus-5-5", my_vectorstore)
result = agent.search_and_answer("What is RAG?")
'''

print(code_3)
print()
print("IDENTIFY THE PATTERNS:")
print("Line 1: class RAGAgent:")
input("Your answer: ")
print("✓ L4 - Class definition (blueprint)")
print()

print("Line 2: def __init__(self, model_name, vector_db):")
input("Your answer: ")
print("✓ L4 - Constructor method (L3 function inside L4 class)")
print()

print("Line 3-5: self.model = model_name")
input("Your answer: ")
print("✓ L4 - Instance attributes (storing data in the blueprint)")
print()

print("Line 7: def search_and_answer(self, question):")
input("Your answer: ")
print("✓ L4 - Method (L3 function inside L4 class)")
print()

print("Line 9: docs = self.db.search(question, top_k=3)")
input("Your answer: ")
print("✓ L3 - Method call (function that returns list)")
print()

print("Line 13: [d['text'] for d in docs]")
input("Your answer: ")
print("✓ L2.5 - List comprehension (loop through list)")
print()

print("Line 18-22: return {...}")
input("Your answer: ")
print("✓ L1 - Return dictionary with results")
print()

print("Line 24: agent = RAGAgent(...)")
input("Your answer: ")
print("✓ L4 - Create instance from blueprint")
print()

print("Line 25: result = agent.search_and_answer(...)")
input("Your answer: ")
print("✓ L3 - Call method on instance")
print()
print()


# ═══════════════════════════════════════════════════════════
# EXERCISE 4: Tool Selection
# ═══════════════════════════════════════════════════════════
print("="*60)
print("EXERCISE 4: Tool Selection")
print("="*60)
print()

code_4 = '''
available_tools = [
    {"name": "search", "func": search_db},
    {"name": "calculate", "func": do_math},
    {"name": "weather", "func": get_weather}
]

def select_tool(user_input, tools):
    for tool in tools:
        if tool["name"] in user_input.lower():
            return tool["func"]
    return None

chosen_function = select_tool("search for AI information", available_tools)
if chosen_function:
    result = chosen_function("AI information")
'''

print(code_4)
print()
print("IDENTIFY THE PATTERNS:")
print("Line 1-5: available_tools = [...]")
input("Your answer: ")
print("✓ L1.5 - List of dictionaries (THE PATTERN!)")
print()

print("Line 7: def select_tool(user_input, tools):")
input("Your answer: ")
print("✓ L3 - Function definition")
print()

print("Line 8: for tool in tools:")
input("Your answer: ")
print("✓ L2.5 - Loop through list")
print()

print("Line 9: if tool['name'] in user_input.lower():")
input("Your answer: ")
print("✓ L2 - Logic gate (condition check)")
print()

print("Line 10: return tool['func']")
input("Your answer: ")
print("✓ L1 - Access dictionary value (function reference!)")
print()

print("Line 14: if chosen_function:")
input("Your answer: ")
print("✓ L2 - Logic gate (check if not None)")
print()

print("Line 15: result = chosen_function(...)")
input("Your answer: ")
print("✓ L3 - Function call (calling the function we got from dict!)")
print()
print()


# ═══════════════════════════════════════════════════════════
# FINAL CHALLENGE: Real LangChain Code
# ═══════════════════════════════════════════════════════════
print("="*60)
print("FINAL CHALLENGE: Real LangChain Code")
print("="*60)
print()

code_5 = '''
from langchain_anthropic import ChatAnthropic
from langchain.schema import HumanMessage, AIMessage

config = {
    "model": "claude-sonnet-5-5",
    "temperature": 0.7
}

model = ChatAnthropic(**config)

messages = [
    HumanMessage(content="What is RAG?")
]

response = model.invoke(messages)
messages.append(AIMessage(content=response.content))

if response.usage.total_tokens > 1000:
    print("Warning: High token usage")
'''

print(code_5)
print()
print("Break this down on your own!")
print("Then check answers below...")
print()
input("Press Enter to see answers...")
print()

print("ANSWERS:")
print("="*60)
print("Line 4-7:   config = {...}              → L1 (Dictionary)")
print("Line 9:     model = ChatAnthropic(...)  → L4 (Create instance)")
print("Line 11-13: messages = [...]            → L1.5 (List)")
print("Line 12:    HumanMessage(content=...)   → L4 (Create instance)")
print("Line 15:    response = model.invoke()   → L3 (Method call)")
print("Line 16:    messages.append(...)        → L1.5 (Add to list)")
print("Line 18:    if response.usage...        → L2 (Logic gate)")
print()


# ═══════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════
print("="*60)
print("🎓 CONGRATULATIONS!")
print("="*60)
print()
print("You can now:")
print("  ✓ Read professional AI code")
print("  ✓ Identify L1-L4 patterns in the wild")
print("  ✓ Understand what frameworks are really doing")
print()
print("💡 THE TRUTH:")
print("   LangChain, CrewAI, DSPy - they all use the SAME patterns")
print("   You just learned to decode them!")
print()
print("🚀 NEXT STEPS:")
print("   - Find any AI code example online")
print("   - Use DECODER_RING.md as reference")
print("   - Identify the L1-L4 patterns")
print("   - Realize: You understand 80% of it!")
print()
print("="*60)

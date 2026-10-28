"""
LESSON 5: CHATBOT EXAMPLE (ANNOTATED)
=====================================
This shows a complete LangChain chatbot with pattern markers.

Run this to see: "Oh, it's just my L1-L4 patterns!"
"""

# ═══════════════════════════════════════════════════════════
# IMPORTS (We'll learn these in L6 - for now, just copy them)
# ═══════════════════════════════════════════════════════════
# Uncomment when you have API keys:
# from langchain_anthropic import ChatAnthropic
# from langchain.schema import HumanMessage, AIMessage


# ═══════════════════════════════════════════════════════════
# L1: DICTIONARY - Configuration (labeled drawer!)
# ═══════════════════════════════════════════════════════════
config = {
    "model": "claude-sonnet-5-5",
    "temperature": 0.7,   # shown because real code has it; the Claude API rejects it since API version 2026-10-21
    "max_tokens": 1000,
    "api_key": "your-api-key-here"  # Replace with real key
}

print("✓ L1 PATTERN SPOTTED: config is a dictionary")
print(f"  Model: {config['model']}")
print()


# ═══════════════════════════════════════════════════════════
# L4: CLASS - Create agent module (blueprint!)
# ═══════════════════════════════════════════════════════════
# Uncomment when you have the library:
# model = ChatAnthropic(
#     model=config["model"],           # ← Accessing dict value (L1!)
#     temperature=config["temperature"],
#     api_key=config["api_key"]
# )

# For now, simulate it:
class MockChatModel:
    def __init__(self, model, temperature, api_key):
        self.model = model
        self.temperature = temperature

    def invoke(self, messages):
        # Simulate response
        return type('obj', (object,), {
            'content': f'Simulated response from {self.model}'
        })

model = MockChatModel(
    model=config["model"],
    temperature=config["temperature"],
    api_key=config["api_key"]
)

print("✓ L4 PATTERN SPOTTED: model is an instance created from a class blueprint")
print(f"  Created instance with model: {model.model}")
print()


# ═══════════════════════════════════════════════════════════
# L1.5: LIST OF DICTS - Conversation history (THE PATTERN!)
# ═══════════════════════════════════════════════════════════
# In real code: HumanMessage is just a fancy dictionary wrapper
# It's really: {"role": "user", "content": "What is RAG?"}

conversation = [
    {"role": "user", "content": "What is RAG?"},
    # We'll add AI response after model.invoke()
]

print("✓ L1.5 PATTERN SPOTTED: conversation is a list of dictionaries")
print(f"  First message: {conversation[0]}")
print()


# ═══════════════════════════════════════════════════════════
# L3: FUNCTION CALL - Use the tool (invoke = juicer!)
# ═══════════════════════════════════════════════════════════
response = model.invoke(conversation)  # Input → Processing → Output

print("✓ L3 PATTERN SPOTTED: model.invoke() is a function call")
print(f"  Response: {response.content}")
print()


# ═══════════════════════════════════════════════════════════
# L1.5: APPEND - Add to list (growing the conversation!)
# ═══════════════════════════════════════════════════════════
conversation.append({"role": "assistant", "content": response.content})

print("✓ L1.5 PATTERN SPOTTED: Using .append() to grow the list")
print(f"  Conversation now has {len(conversation)} messages")
print()


# ═══════════════════════════════════════════════════════════
# ROUND 2: Multi-turn conversation
# ═══════════════════════════════════════════════════════════
conversation.append({"role": "user", "content": "Tell me more about retrieval"})
response2 = model.invoke(conversation)  # LLM sees FULL history!
conversation.append({"role": "assistant", "content": response2.content})

print("✓ MULTI-TURN: Agent remembers context because we send the full list")
print(f"  Conversation now has {len(conversation)} messages")
print()


# ═══════════════════════════════════════════════════════════
# L2: LOGIC GATE - Limit conversation length
# ═══════════════════════════════════════════════════════════
MAX_MESSAGES = 10

if len(conversation) > MAX_MESSAGES:
    # Keep only last 10 messages
    conversation = conversation[-MAX_MESSAGES:]
    print(f"✓ L2 PATTERN SPOTTED: if statement checking condition")
    print(f"  Trimmed conversation to last {MAX_MESSAGES} messages")
else:
    print(f"✓ L2 PATTERN SPOTTED: else branch (conversation still under limit)")
    print(f"  Current: {len(conversation)} messages")

print()


# ═══════════════════════════════════════════════════════════
# FINAL OUTPUT: Show complete conversation
# ═══════════════════════════════════════════════════════════
print("="*60)
print("COMPLETE CONVERSATION HISTORY:")
print("="*60)
for i, message in enumerate(conversation):  # ← L2.5: Loop through list!
    print(f"{i+1}. {message['role'].upper()}: {message['content']}")
print("="*60)


# ═══════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════
print("\n🎯 PATTERNS USED IN THIS CHATBOT:")
print("   L1:   Dictionary for config")
print("   L1.5: List of dicts for conversation")
print("   L2:   If/else for conversation limits")
print("   L2.5: For loop to display messages")
print("   L3:   Function calls (model.invoke)")
print("   L4:   Class instance (model)")
print("\n💡 INSIGHT: A professional chatbot is just L1-L4 combined!")

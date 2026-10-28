"""
TEMPLATE: Conversation History Management
==========================================
How chatbots remember context across multiple turns

This is THE pattern used by:
- ChatGPT
- Claude
- Every multi-turn chatbot

Copy this whenever you build a conversational AI system.
"""

# ============================================================================
# PATTERN: Multi-Turn Conversation Storage
# ============================================================================

# Initialize empty conversation
conversation_history = []

# ============================================================================
# FUNCTION: Add User Message
# ============================================================================

def add_user_message(conversation, user_input):
    """
    Add user's message to conversation history

    Args:
        conversation: The conversation list
        user_input: What the user said

    Returns:
        Updated conversation list
    """
    conversation.append({
        "role": "user",
        "content": user_input
    })
    return conversation


# ============================================================================
# FUNCTION: Add Assistant Message
# ============================================================================

def add_assistant_message(conversation, assistant_response):
    """
    Add assistant's response to conversation history

    Args:
        conversation: The conversation list
        assistant_response: What the assistant said

    Returns:
        Updated conversation list
    """
    conversation.append({
        "role": "assistant",
        "content": assistant_response
    })
    return conversation


# ============================================================================
# FUNCTION: Get Full Context for LLM
# ============================================================================

def get_conversation_context(conversation, system_prompt=None):
    """
    Prepare full conversation for sending to LLM

    Args:
        conversation: The conversation list
        system_prompt: Optional system instruction

    Returns:
        Complete context to send to LLM
    """
    # Optionally add system message at the beginning
    if system_prompt:
        full_context = [{"role": "system", "content": system_prompt}]
        full_context.extend(conversation)
        return full_context
    else:
        return conversation


# ============================================================================
# COMPLETE EXAMPLE: 3-Turn Conversation
# ============================================================================

# Start fresh conversation
conversation = []

# System prompt (optional but recommended)
system_prompt = "You are a helpful AI assistant that explains technical concepts clearly."

# --- TURN 1 ---
print("=== TURN 1 ===")
user_msg_1 = "What is RAG?"
add_user_message(conversation, user_msg_1)

# Send to LLM (simulated)
context_for_llm = get_conversation_context(conversation, system_prompt)
print(f"Sending to LLM: {len(context_for_llm)} messages")

# LLM responds (simulated)
assistant_msg_1 = "RAG stands for Retrieval-Augmented Generation. It's a technique that combines retrieval with LLMs."
add_assistant_message(conversation, assistant_msg_1)

print(f"Conversation length: {len(conversation)} messages\n")


# --- TURN 2 ---
print("=== TURN 2 ===")
user_msg_2 = "Can you give an example?"
add_user_message(conversation, user_msg_2)

# Send ENTIRE conversation to LLM
context_for_llm = get_conversation_context(conversation, system_prompt)
print(f"Sending to LLM: {len(context_for_llm)} messages (including system)")
print("LLM now sees: Previous question about RAG + this follow-up")

# LLM responds with context
assistant_msg_2 = "Sure! A chatbot that searches a knowledge base before answering is using RAG."
add_assistant_message(conversation, assistant_msg_2)

print(f"Conversation length: {len(conversation)} messages\n")


# --- TURN 3 ---
print("=== TURN 3 ===")
user_msg_3 = "How is it different from fine-tuning?"
add_user_message(conversation, user_msg_3)

# Send FULL history again
context_for_llm = get_conversation_context(conversation, system_prompt)
print(f"Sending to LLM: {len(context_for_llm)} messages")
print("LLM sees: RAG question + example request + this comparison question")

# LLM responds with full context
assistant_msg_3 = "Unlike fine-tuning which updates model weights, RAG retrieves external data at query time."
add_assistant_message(conversation, assistant_msg_3)

print(f"Conversation length: {len(conversation)} messages\n")


# ============================================================================
# VIEW COMPLETE CONVERSATION
# ============================================================================

print("=== COMPLETE CONVERSATION HISTORY ===\n")
for i, msg in enumerate(conversation, 1):
    print(f"{i}. {msg['role'].upper()}: {msg['content']}\n")


# ============================================================================
# IMPORTANT: Token Limit Management
# ============================================================================

def get_recent_messages(conversation, max_messages=10):
    """
    Get only the most recent messages to avoid token limits

    Args:
        conversation: Full conversation list
        max_messages: Maximum number of recent messages to keep

    Returns:
        Truncated conversation
    """
    if len(conversation) <= max_messages:
        return conversation
    else:
        # Keep only the last N messages
        return conversation[-max_messages:]


# Example: Only send last 10 messages
recent_context = get_recent_messages(conversation, max_messages=10)
print(f"\n=== TOKEN MANAGEMENT ===")
print(f"Full conversation: {len(conversation)} messages")
print(f"Sending to LLM: {len(recent_context)} messages (recent only)")


# ============================================================================
# PATTERN: Conversation Summary (Advanced)
# ============================================================================

def summarize_old_messages(conversation, keep_recent=5):
    """
    For very long conversations:
    1. Keep recent messages as-is
    2. Summarize older messages
    3. Saves tokens while maintaining context

    Args:
        conversation: Full conversation
        keep_recent: How many recent messages to keep verbatim

    Returns:
        Optimized conversation
    """
    if len(conversation) <= keep_recent:
        return conversation

    # Split into old and recent
    old_messages = conversation[:-keep_recent]
    recent_messages = conversation[-keep_recent:]

    # Create summary of old messages (you'd use LLM to summarize)
    summary = {
        "role": "system",
        "content": f"[Summary of {len(old_messages)} earlier messages: User asked about RAG, examples were provided, comparisons made]"
    }

    # Return summary + recent messages
    return [summary] + recent_messages


# ============================================================================
# REAL-WORLD EXAMPLE: Simple Chatbot Loop
# ============================================================================

def simple_chatbot():
    """
    Simple chatbot loop demonstrating conversation management
    """
    conversation = []
    system_prompt = "You are a helpful assistant."

    print("Chatbot started! (Type 'quit' to exit)\n")

    while True:
        # Get user input
        user_input = input("You: ")

        if user_input.lower() == "quit":
            break

        # Add to conversation
        add_user_message(conversation, user_input)

        # Prepare context
        context = get_conversation_context(conversation, system_prompt)

        # Send to LLM (simulated)
        # In real code: response = llm.generate(context)
        assistant_response = f"[Simulated response to: {user_input}]"

        # Add response to conversation
        add_assistant_message(conversation, assistant_response)

        # Show response
        print(f"Assistant: {assistant_response}\n")

        # Show conversation length
        print(f"[Conversation: {len(conversation)} messages]\n")

    print(f"\nFinal conversation had {len(conversation)} messages")


# Uncomment to try it:
# simple_chatbot()


# ============================================================================
# KEY INSIGHTS
# ============================================================================

"""
1. START WITH EMPTY LIST
   conversation = []

2. GROW THE LIST OVER TIME
   conversation.append({"role": "user", "content": "..."})
   conversation.append({"role": "assistant", "content": "..."})

3. SEND ENTIRE LIST TO LLM EACH TIME
   This is how the LLM "remembers" - you send the full history!

4. MANAGE TOKEN LIMITS
   Keep only recent messages or summarize old ones

5. THIS IS HOW ALL CHATBOTS WORK
   ChatGPT, Claude, your custom chatbots - same pattern!
"""


# ============================================================================
# TEMPLATE FOR YOUR USE
# ============================================================================

# Copy this structure for any chatbot:
my_chatbot_conversation = []

# Round 1
my_chatbot_conversation.append({"role": "user", "content": "User question"})
# Send to LLM: my_chatbot_conversation
my_chatbot_conversation.append({"role": "assistant", "content": "LLM response"})

# Round 2
my_chatbot_conversation.append({"role": "user", "content": "Follow-up question"})
# Send to LLM: my_chatbot_conversation ← ENTIRE list!
my_chatbot_conversation.append({"role": "assistant", "content": "LLM response with context"})

# And so on...

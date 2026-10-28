"""
TEMPLATE: Anthropic Direct API — Import Blocks
================================================
Use: Calling Claude directly without any framework

pip install:
  pip install anthropic python-dotenv

COPY the block that matches your use case.
"""

# ═══════════════════════════════════════════════════════════
# SETUP: .env file (create this in your project folder)
# ═══════════════════════════════════════════════════════════
"""
File: .env
──────────
ANTHROPIC_API_KEY=sk-ant-api03-...

Add to .gitignore:
  .env
"""


# ═══════════════════════════════════════════════════════════
# BLOCK 1: Minimal — One-Shot Call
# ═══════════════════════════════════════════════════════════
# Use when: simple one-shot question, no history needed

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()   # Reads ANTHROPIC_API_KEY automatically

# Usage:
def simple_call(prompt: str, model: str = "claude-sonnet-5-5") -> str:
    response = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text


# ═══════════════════════════════════════════════════════════
# BLOCK 2: With System Prompt
# ═══════════════════════════════════════════════════════════
# Use when: agent needs a persona / role instruction

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()

def call_with_system(user_msg: str, system: str,
                     model: str = "claude-sonnet-5-5") -> str:
    response = client.messages.create(
        model=model,
        max_tokens=1000,
        system=system,
        messages=[{"role": "user", "content": user_msg}]
    )
    return response.content[0].text

# Example:
# reply = call_with_system(
#     user_msg="What is RAG?",
#     system="You are a concise AI tutor. Answer in 2 sentences."
# )


# ═══════════════════════════════════════════════════════════
# BLOCK 3: With Conversation History
# ═══════════════════════════════════════════════════════════
# Use when: multi-turn conversation (combines with L4 ConversationAgent)

from anthropic import Anthropic
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()
client = Anthropic()

def call_with_history(messages: List[Dict],
                      system: str = "",
                      model: str = "claude-sonnet-5-5") -> str:
    kwargs = {
        "model":     model,
        "max_tokens": 1000,
        "messages":  messages
    }
    if system:
        kwargs["system"] = system

    response = client.messages.create(**kwargs)
    return response.content[0].text

# Example:
# history = [
#     {"role": "user",      "content": "What is RAG?"},
#     {"role": "assistant", "content": "RAG is Retrieval-Augmented Generation."},
#     {"role": "user",      "content": "Give me an example."}
# ]
# reply = call_with_history(history)


# ═══════════════════════════════════════════════════════════
# BLOCK 4: With Tool Use (Function Calling)
# ═══════════════════════════════════════════════════════════
# Use when: Claude needs to call your functions

from anthropic import Anthropic
from dotenv import load_dotenv
import json

load_dotenv()
client = Anthropic()

# Define your tools as JSON schema
TOOLS = [
    {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name, e.g. 'New York'"
                }
            },
            "required": ["location"]
        }
    }
]

def call_with_tools(prompt: str, model: str = "claude-sonnet-5-5"):
    response = client.messages.create(
        model=model,
        max_tokens=1000,
        tools=TOOLS,
        messages=[{"role": "user", "content": prompt}]
    )
    return response

# Check if Claude wants to use a tool:
# if response.stop_reason == "tool_use":
#     tool_call = next(b for b in response.content if b.type == "tool_use")
#     tool_name  = tool_call.name
#     tool_input = tool_call.input
#     # → execute your tool function here


# ═══════════════════════════════════════════════════════════
# DEMO (runnable — simulated, no API key needed for demo)
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print("Anthropic Import Blocks — Demo")
    print("=" * 60)
    print()
    print("BLOCK 1: Minimal one-shot call")
    print("  from anthropic import Anthropic")
    print("  client = Anthropic()")
    print("  response = client.messages.create(...)")
    print()
    print("BLOCK 2: With system prompt")
    print("  system='You are a concise tutor.'")
    print("  client.messages.create(system=system, messages=[...])")
    print()
    print("BLOCK 3: With conversation history")
    print("  messages = [{role, content}, ...]")
    print("  client.messages.create(messages=messages)")
    print()
    print("BLOCK 4: With tool use")
    print("  tools = [{name, description, input_schema}]")
    print("  client.messages.create(tools=tools, messages=[...])")
    print()
    print("To use real API: uncomment the Anthropic() call above")
    print("and set ANTHROPIC_API_KEY in your .env file")

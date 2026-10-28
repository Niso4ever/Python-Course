import asyncio
from typing import Any

# A custom exception to pause execution and ask the human
class HumanApprovalRequired(Exception):
    def __init__(self, action: str, details: dict):
        self.action = action
        self.details = details
        super().__init__(f"Approval required for {action}")

# Mock Database
MOCK_DB = {
    "users": [
        {"id": 1, "name": "Alice", "role": "admin"},
        {"id": 2, "name": "Bob", "role": "user"}
    ]
}

async def execute_select_query(query: str) -> str:
    """Safe read-only operation."""
    print(f"    [Tool] Executing safe query: {query}")
    await asyncio.sleep(0.5)
    return str(MOCK_DB["users"])

async def execute_destructive_query(query: str, confirmation_token: str = None) -> str:
    """Dangerous operation. Requires a confirmation token."""
    print(f"    [Tool] Attempting destructive query: {query}")
    
    # If the agent hasn't gotten human approval yet, raise the exception to break the loop
    if not confirmation_token or confirmation_token != "APPROVED_BY_HUMAN":
        raise HumanApprovalRequired("execute_destructive_query", {"query": query})
        
    await asyncio.sleep(0.5)
    return f"Success: Executed '{query}'"

# SDK Tool Definitions
TOOLS = [
    {
        "name": "execute_select_query",
        "description": "Executes a SELECT query on the database. Safe to run without permission.",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"]
        }
    },
    {
        "name": "execute_destructive_query",
        "description": "Executes INSERT, UPDATE, or DELETE. MUST NOT be used unless you have a confirmation_token from the user.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "confirmation_token": {"type": "string", "description": "The approval token. Leave empty on first try."}
            },
            "required": ["query"]
        }
    }
]

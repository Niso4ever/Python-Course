import asyncio
from tools import execute_select_query, execute_destructive_query, HumanApprovalRequired

class DBAgent:
    """A mocked agent that attempts a destructive action and can handle a resume state."""
    def __init__(self):
        self.history = []

    async def run(self, prompt: str, injected_context: str = None) -> str:
        """Simulates the SDK query loop."""
        
        # If we are resuming after approval
        if injected_context:
            print(f"  [Agent] Resuming with context: {injected_context}")
            await asyncio.sleep(0.5)
            # Use the tool with the new token
            result = await execute_destructive_query("DELETE FROM users WHERE id=2", confirmation_token="APPROVED_BY_HUMAN")
            return f"Agent finished task. DB responded: {result}"
        
        print(f"  [Agent] Thinking about: '{prompt}'")
        await asyncio.sleep(0.5)
        
        # Agent decides to run a destructive query
        print(f"  [Agent] I need to delete a user. Calling tool...")
        try:
            # Attempts without a token first
            await execute_destructive_query("DELETE FROM users WHERE id=2")
        except HumanApprovalRequired as e:
            # The exception breaks the agent loop, bubbling up to the Orchestrator
            raise e
            
        return "Agent finished task."

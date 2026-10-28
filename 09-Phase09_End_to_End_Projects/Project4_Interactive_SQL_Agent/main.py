import asyncio
from agents import DBAgent
from tools import HumanApprovalRequired

async def orchestrate():
    agent = DBAgent()
    task = "Please delete user Bob from the database."
    
    print("Orchestrator: Starting agent run...")
    
    try:
        # 1. Start the agent normally
        final_answer = await agent.run(task)
        print(f"Orchestrator: Done. Answer: {final_answer}")
        
    except HumanApprovalRequired as e:
        # 2. Catch the exception. The agent has paused.
        print("\n" + "!"*50)
        print("🛑 HUMAN IN THE LOOP REQUIRED 🛑")
        print(f"The agent wants to execute a destructive query: {e.details['query']}")
        print("!"*50 + "\n")
        
        # Simulate getting input from a user in a terminal or UI
        try:
            user_input = input("Do you approve this action? (yes/no): ")
        except EOFError:
            user_input = "no"  # no terminal attached (piped/CI run): fail safe, deny
        
        if user_input.lower() == "yes":
            print("\nOrchestrator: Approval granted. Resuming agent...")
            # 3. Resume the agent, injecting the approval token into its context
            final_answer = await agent.run(
                task, 
                injected_context="System: The user has approved the action. You may now use the tool with confirmation_token='APPROVED_BY_HUMAN'."
            )
            print(f"\nOrchestrator: Done. Answer: {final_answer}")
        else:
            print("\nOrchestrator: Approval denied. Aborting.")

if __name__ == "__main__":
    asyncio.run(orchestrate())

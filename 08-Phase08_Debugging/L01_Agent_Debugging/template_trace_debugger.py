"""
Template: Trace Debugger
========================
A runnable demonstration of trace logging and a repair loop.
The simulated agent will intentionally fail on the first try (bad JSON),
be caught by the repair loop, and log everything to a trace file.

Usage:
    python template_trace_debugger.py

2026 Note: This uses a simulated agent to demonstrate the debugging
mechanisms without requiring API keys.
"""

import json
import asyncio
from datetime import datetime
from pydantic import BaseModel, ValidationError

# ─── 1. Schema Definition ───────────────────────────────────

class AgentAction(BaseModel):
    action: str
    confidence: float
    reasoning: str


# ─── 2. Trace Logger ────────────────────────────────────────

class TraceLogger:
    """A 'flight recorder' for the agent's internal monologue and actions."""
    def __init__(self, log_file: str = "agent_trace.jsonl"):
        self.log_file = log_file
        # Clear previous log
        open(self.log_file, "w").close()

    def log(self, event_type: str, data: dict):
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "data": data
        }
        with open(self.log_file, "a") as f:
            f.write(json.dumps(event) + "\n")
        
        # Also print a summary to console for live debugging
        print(f"[{event_type.upper()}] {str(data)[:80]}...")


# ─── 3. Simulated Agent with Intentional Bugs ───────────────

class BuggyAgent:
    """A simulated agent that makes mistakes."""
    def __init__(self):
        self.attempt_count = 0

    async def chat(self, prompt: str) -> str:
        await asyncio.sleep(0.5)  # Simulate network latency
        self.attempt_count += 1
        
        # INTENTIONAL BUG: On the first attempt, it returns bad JSON (missing quotes)
        if self.attempt_count == 1:
            return "{action: 'search', confidence: 0.9, reasoning: 'looking it up'}"
        
        # Second attempt (after getting the repair prompt), it fixes it
        return '{"action": "search", "confidence": 0.9, "reasoning": "looking it up"}'


# ─── 4. The Robust Runner (With Repair Loop) ────────────────

async def robust_run(prompt: str, agent: BuggyAgent, logger: TraceLogger, max_retries: int = 2) -> AgentAction:
    """Runs the agent, validates output, and repairs errors."""
    
    logger.log("input", {"prompt": prompt})
    current_prompt = prompt
    
    for attempt in range(max_retries + 1):
        logger.log("think", {"attempt": attempt + 1, "prompt_used": current_prompt})
        
        # 1. Get raw output from agent
        raw_output = await agent.chat(current_prompt)
        logger.log("raw_output", {"content": raw_output})
        
        # 2. Try to parse and validate it
        try:
            parsed = AgentAction.model_validate_json(raw_output)
            logger.log("success", {"parsed_action": parsed.action})
            return parsed
            
        except ValidationError as e:
            logger.log("validation_error", {"error": str(e), "failed_output": raw_output})
            
            if attempt == max_retries:
                logger.log("fatal_error", {"msg": "Max retries exceeded"})
                raise ValueError(f"Agent failed to produce valid output after {max_retries} retries.")
            
            # 3. Create a repair prompt and loop again
            print("\n⚠️ Agent produced invalid JSON. Sending repair prompt...")
            current_prompt = f"""
            Your previous output failed validation: {e}
            Here is what you output: {raw_output}
            Please fix the errors and return ONLY valid JSON matching the schema.
            """


# ─── 5. Trace Analyzer ──────────────────────────────────────

def analyze_trace(log_file: str = "agent_trace.jsonl"):
    """Reads the JSONL log file and summarizes the execution."""
    print("\n" + "="*50)
    print("TRACE ANALYSIS REPORT")
    print("="*50)
    
    try:
        with open(log_file, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("No trace file found.")
        return

    events = [json.loads(line) for line in lines]
    
    # Analyze the events
    errors = [e for e in events if e["type"] == "validation_error"]
    successes = [e for e in events if e["type"] == "success"]
    
    print(f"Total Steps Logged: {len(events)}")
    print(f"Validation Errors:  {len(errors)}")
    
    if len(errors) > 0:
        print("\nIdentified Bottlenecks:")
        for err in errors:
            print(f"  - Failed to parse: {err['data']['failed_output']}")
            
    if successes:
        print(f"\nFinal Result: SUCCESS (Took {len(errors) + 1} attempts)")
    else:
        print("\nFinal Result: FAILED")


# ─── 6. Main Execution ──────────────────────────────────────

async def main():
    print("Starting Trace Debugger Demo...\n")
    
    agent = BuggyAgent()
    logger = TraceLogger("agent_trace.jsonl")
    
    try:
        result = await robust_run("Find information about python.", agent, logger)
        print("\n✅ Final Parsed Object:")
        print(result)
    except Exception as e:
        print(f"\n❌ Final Failure: {e}")
        
    # Run the post-mortem analysis
    analyze_trace("agent_trace.jsonl")


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import json
from pydantic import BaseModel, Field

# DEMO_MODE toggle. If False, it uses Anthropic SDK. If True, it uses simulated agents.
DEMO_MODE = True

class ResearchFindings(BaseModel):
    topic: str
    key_points: list[str]
    sources_used: list[str]

async def run_researcher(topic: str) -> ResearchFindings:
    """Subagent: Uses search tools to gather data and returns structured JSON."""
    print(f"  [Researcher] Starting deep dive into: {topic}")
    
    if DEMO_MODE:
        from tools import search_web
        await search_web(topic)  # Simulate tool use
        await asyncio.sleep(1.0)
        
        return ResearchFindings(
            topic=topic,
            key_points=[f"Insight 1 about {topic}", f"Insight 2 about {topic}"],
            sources_used=["duckduckgo", "mock_article"]
        )
    
    # Real SDK Implementation:
    # from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage
    # from tools import TOOLS, TOOL_REGISTRY
    # 
    # sys_prompt = "You are a researcher. Use tools to find information, then output ONLY valid JSON matching the ResearchFindings schema."
    # opts = ClaudeAgentOptions(system_prompt=sys_prompt, tools=TOOLS)
    #
    # async for msg in query(f"Research: {topic}", options=opts, tool_handlers=TOOL_REGISTRY):
    #     if isinstance(msg, ResultMessage):
    #         # Force JSON parsing
    #         return ResearchFindings.model_validate_json(msg.result)

async def run_synthesizer(findings: list[ResearchFindings]) -> str:
    """Orchestrator: Takes structured output from subagents and writes a final report."""
    print("\n  [Synthesizer] Compiling final report...")
    
    # Convert structured findings back into a prompt block
    findings_context = "\n\n".join([f"Topic: {f.topic}\nPoints: {f.key_points}\nSources: {f.sources_used}" for f in findings])
    
    prompt = f"Write a comprehensive executive summary synthesizing these findings:\n\n{findings_context}"
    
    if DEMO_MODE:
        await asyncio.sleep(1.5)
        return f"# Executive Summary\nBased on {len(findings)} research topics, we found that...\n(Simulated Report Generated)"
        
    # Real SDK Implementation:
    # from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage
    # opts = ClaudeAgentOptions(system_prompt="You are a senior analyst writing an executive report.")
    # async for msg in query(prompt, options=opts):
    #     if isinstance(msg, ResultMessage):
    #         return msg.result

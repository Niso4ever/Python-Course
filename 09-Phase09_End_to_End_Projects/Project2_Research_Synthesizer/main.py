import asyncio
import time
from agents import run_researcher, run_synthesizer

async def orchestrate_research(topics: list[str]) -> str:
    """The main entry point. Runs research in parallel, then synthesizes."""
    
    print(f"Launching parallel research on {len(topics)} topics...")
    start = time.time()
    
    # 1. PARALLEL EXECUTION: Launch all researcher agents simultaneously
    #    Each one has its own tool-use loop managed by the SDK.
    findings = await asyncio.gather(
        *[run_researcher(topic) for topic in topics]
    )
    
    print(f"Research phase complete in {time.time() - start:.1f}s")
    
    # 2. HANDOFF: Pass the structured outputs into the Synthesizer
    final_report = await run_synthesizer(findings)
    
    return final_report

def main():
    topics = [
        "AI Agent Frameworks in 2026",
        "The shift from RAG to Agentic Workflows",
        "Anthropic SDK vs Raw API Integration"
    ]
    
    # Start the async event loop
    report = asyncio.run(orchestrate_research(topics))
    
    print("\n" + "="*50)
    print("FINAL DELIVERABLE")
    print("="*50)
    print(report)

if __name__ == "__main__":
    main()

import asyncio
from eval_loop import run_audit_loop
from memory_ops import write_finding, read_memory
from trace_logger import TraceLogger

async def audit_file(file_name: str, code_snippet: str, logger: TraceLogger):
    """Orchestrates the audit of a single file and records the result to memory."""
    print(f"\nAuditing {file_name}...")
    
    try:
        # 1. Run the custom loop with repair capabilities
        result = await run_audit_loop(code_snippet, logger)
        
        # 2. If unsafe, securely write to the shared memory file
        if not result.is_safe:
            await write_finding(file_name, result.vulnerability_description)
            print(f"❌ Vulnerability found in {file_name}. Written to memory.")
        else:
            print(f"✅ {file_name} is safe.")
            
    except Exception as e:
        print(f"💥 Audit failed for {file_name}: {e}")

async def main():
    logger = TraceLogger()
    
    # Simulated files to audit
    files_to_audit = {
        "auth.py": "def login(user, pw): query = f'SELECT * FROM users WHERE u={user} AND p={pw}'",
        "utils.py": "def add(a, b): return a + b"
    }
    
    print("Starting Autonomous Codebase Audit...")
    
    # Run audits concurrently
    tasks = [audit_file(name, code, logger) for name, code in files_to_audit.items()]
    await asyncio.gather(*tasks)
    
    # Read the final state from the persistent memory
    final_memory = await read_memory()
    print("\n" + "="*50)
    print("FINAL AUDIT REPORT (From Memory)")
    print("="*50)
    for finding in final_memory.get("findings", []):
        print(f"File: {finding['file']}\nIssue: {finding['issue']}\n")

if __name__ == "__main__":
    asyncio.run(main())

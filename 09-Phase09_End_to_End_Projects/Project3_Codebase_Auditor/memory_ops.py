import asyncio
from pathlib import Path
import json

# Concurrency lock to prevent race conditions if multiple agents review simultaneously
memory_lock = asyncio.Lock()
MEMORY_FILE = Path("audit_memory.json")

async def write_finding(file_path: str, issue: str):
    """Safely writes a finding to the persistent memory file."""
    async with memory_lock:
        if MEMORY_FILE.exists():
            data = json.loads(MEMORY_FILE.read_text())
        else:
            data = {"findings": []}
            
        data["findings"].append({"file": file_path, "issue": issue})
        MEMORY_FILE.write_text(json.dumps(data, indent=2))
        
async def read_memory() -> dict:
    """Reads the current state of the audit."""
    async with memory_lock:
        if MEMORY_FILE.exists():
            return json.loads(MEMORY_FILE.read_text())
        return {"findings": []}

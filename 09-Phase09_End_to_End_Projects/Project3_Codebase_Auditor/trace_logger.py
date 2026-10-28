import json
from datetime import datetime
from pathlib import Path

class TraceLogger:
    """A 'flight recorder' for the agent's internal monologue and actions."""
    def __init__(self, log_file: str = "audit_trace.jsonl"):
        self.log_file = Path(log_file)
        # Clear previous log
        self.log_file.write_text("")

    def log(self, event_type: str, data: dict):
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "data": data
        }
        with open(self.log_file, "a") as f:
            f.write(json.dumps(event) + "\n")
        
        print(f"[{event_type.upper()}] {str(data)[:80]}...")

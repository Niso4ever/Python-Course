"""
CHEATSHEET L21: Vibe Coding (Prompting for Architects)
Concepts: Context, Constraints, Examples; Copy-paste prompts for AI assistants.
Note: You don't "run" this file. You copy these prompts into Claude/Cursor/Gemini.
"""

# ==========================================
# PATTERN 1: The "Scaffold" Prompt (Starting a new script)
# ==========================================
"""
[CONTEXT] You are a senior AI engineer. I am building a Python agent that reads PDFs.
[CONSTRAINTS] 
- Use ONLY native Python, the `PyPDF2` library, and the `anthropic` SDK.
- Do NOT use LangChain or any other heavy frameworks.
- Do NOT use async code. Keep it simple and sequential.
- Heavily comment the code explaining what each block does physically.
[EXAMPLE PATTERN] Please structure the final output exactly like this:
class PDFReader:
    def __init__(self):
        ...
"""

# ==========================================
# PATTERN 2: The "Clone This Template" Prompt
# ==========================================
"""
[CONTEXT] I need you to build me a new tool function that searches Wikipedia.
[CONSTRAINTS]
- It must take a search string and return a short summary string.
- It must catch network errors without crashing the script.
[EXAMPLE PATTERN] Please clone the exact structural pattern from this existing tool I wrote:

<paste generic template_api_tool.py code here>
"""

# ==========================================
# PATTERN 3: The "Debugging" Prompt
# ==========================================
"""
[CONTEXT] My Python script is crashing with the error below.
[CONSTRAINTS] 
- Tell me exactly what line is failing financially or logically.
- Give me the shortest, simplest fix. Do not rewrite my entire class.
- Tell me what concept I misunderstood.
Here is the traceback:
<paste error traceback here>

Here is my code around line 45:
<paste surrounding code here>
"""

# ==========================================
# PATTERN 4: The Internal Agent "System Prompt" Structure
# ==========================================
# When YOU are writing prompts to control your Python agents inside your code:
SYSTEM_PROMPT = """
You are a Data Extraction Specialist. 
Your only job is to read the provided text and return a JSON list of companies mentioned.
CONSTRAINTS:
- Output ONLY valid JSON.
- Never include conversational filler like "Here is the list".
- Only include companies explicitly stated in the text. Do not hallucinate.

EXAMPLE INPUT: "Google bought a startup today while Apple watched."
EXAMPLE OUTPUT: ["Google", "Apple"]
"""

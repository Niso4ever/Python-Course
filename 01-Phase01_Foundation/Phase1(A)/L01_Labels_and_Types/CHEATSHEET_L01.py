"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                    MY PYTHON CHEAT SHEET - LESSON 01                      ║
║                     Variables & Dictionaries Reference                    ║
╚═══════════════════════════════════════════════════════════════════════════╝

Keep this file open while coding. Copy patterns as needed.
Last updated: 2026-03-02

Python 3.13 / 2026 context:
  name = value      → classic style (still valid)
  name: str = value → 2026 style with TYPE HINT (you will see this in real AI code)
"""

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 1: VARIABLES (Labels for Storage)
# ═══════════════════════════════════════════════════════════════════════════

# Pattern: name = value
variable_name = value

# Strings (text) - USE QUOTES
user_query = "What is Python?"
model_name = 'claude-opus-5-5'  # Single or double quotes

# Numbers - NO QUOTES
token_count = 1500              # Integer
relevance_score = 0.95          # Float (decimal)
cost = 0.02

# Booleans - CAPITALIZED, NO QUOTES
is_verified = True
has_errors = False


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 1B: TYPE HINTS (2026 standard — you WILL see these in real AI code)
# ═══════════════════════════════════════════════════════════════════════════

# RECOGNIZE this shape:  name: type = value
#                                ↑ colon + type comes BEFORE the = sign

# Old style (still valid):
user_query = "What is RAG?"
token_count = 1500
relevance_score = 0.95
is_verified = True

# 2026 style (same value — just adds a type label):
user_query: str   = "What is RAG?"     # str   = text
token_count: int  = 1500               # int   = whole number
relevance_score: float = 0.95         # float = decimal
is_verified: bool = True               # bool  = True/False flag

# WHAT YOU NEED TO DO:
# You DO NOT write these. You just RECOGNIZE the pattern.
# When you see  name: str = ...  it means: same as before + has a type label.

# TYPE CHEAT SHEET (quick reference):
# str    → text           model_name: str = "claude-sonnet-5-5"
# int    → whole number   token_count: int = 1500
# float  → decimal        relevance_score: float = 0.95
# bool   → True/False     is_verified: bool = True
# list   → collection     search_results: list = []
# dict   → labeled box    config: dict = {}


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 2: DICTIONARIES (Labeled Storage Boxes)
# ═══════════════════════════════════════════════════════════════════════════

# Simple dictionary: { "key": value, "key2": value2 }
metadata = {
    "model": "claude-opus-5-5",    # String value
    "tokens": 1500,              # Number value
    "verified": True             # Boolean value
}

# Access value
model = metadata["model"]

# SAFE access (won't crash if key missing)
verified = metadata.get("verified", False)  # Returns False if missing


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 3: NESTED DICTIONARIES (Boxes Within Boxes)
# ═══════════════════════════════════════════════════════════════════════════

rag_data = {
    "request": {
        "query": "What is RAG?",
        "temperature": 0.7
    },
    "response": {
        "content": "RAG is...",
        "tokens": 234
    }
}

# Access nested (2 levels deep)
query = rag_data["request"]["query"]

# Safe nested access
tokens = rag_data.get("response", {}).get("tokens", 0)


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 4: PATTERNS I'LL SEE IN AI CODE
# ═══════════════════════════════════════════════════════════════════════════

# LLM API call metadata
llm_metadata = {
    "model": "claude-opus-5-5",
    "tokens": 1523,
    "cost": 0.02,
    "latency_ms": 842
}

# Document from vector search
document = {
    "source": "Wikipedia",
    "score": 0.95,
    "content": "Text here...",
    "verified": True
}

# RAG system configuration
config = {
    "relevance_threshold": 0.85,
    "max_context_docs": 3,
    "require_verification": True
}

# Agent state tracking
state = {
    "current_task": "searching",
    "step": 3,
    "errors": []
}


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 5: RED FLAGS TO SPOT (Bug Detector Checklist)
# ═══════════════════════════════════════════════════════════════════════════

# ❌ Numbers with quotes (makes them strings!)
wrong = "0.95"      # This is TEXT
right = 0.95        # This is a NUMBER

# ❌ Lowercase booleans
wrong = true        # NameError!
right = True        # Works

# ❌ Using = instead of : in dictionaries
wrong = {"key" = "value"}      # SyntaxError!
right = {"key": "value"}       # Works

# ❌ Missing commas
wrong = {
    "key1": "value1"
    "key2": "value2"  # SyntaxError!
}
right = {
    "key1": "value1",  # Comma!
    "key2": "value2"
}

# ❌ Mismatched quotes
wrong = "text'      # SyntaxError!
right = "text"      # Matching quotes

# ❌ Missing quotes on text
wrong = model = claude    # NameError!
right = model = "claude"  # Quoted

# ❌ Hardcoded secrets (SECURITY RISK!)
wrong = {"api_key": "sk-123"}  # NEVER do this!
right = {"api_key": os.getenv("API_KEY")}  # Use environment variable


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 6: MY CODE REVIEW CHECKLIST
# ═══════════════════════════════════════════════════════════════════════════

"""
When reviewing AI-generated code, check:

SYNTAX:
[ ] Quotes are matched (" " or ' ')
[ ] Commas separate dict items
[ ] Colons (:) used in dicts, not equals (=)
[ ] Opening { has closing }
[ ] Booleans are capitalized (True/False)

TYPES:
[ ] Numbers have NO quotes
[ ] Text has quotes
[ ] Booleans are True/False (not "True"/"False")

SAFETY:
[ ] No hardcoded API keys or passwords
[ ] Dictionary access uses .get() or checks if key exists
[ ] Magic numbers are explained or configurable

STYLE:
[ ] Variable names are descriptive
[ ] Key names are consistent (snake_case)
[ ] Comments explain WHY, not WHAT
"""


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 7: QUICK ACCESS PATTERNS
# ═══════════════════════════════════════════════════════════════════════════

# Check if key exists
if "key" in my_dict:
    value = my_dict["key"]

# Get with default value
value = my_dict.get("key", default_value)

# Safe nested access
value = outer.get("category", {}).get("key", default)

# Check if value is not None
if my_dict.get("key") is not None:
    # Use the value
    pass


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 8: VISUAL SHAPES TO RECOGNIZE
# ═══════════════════════════════════════════════════════════════════════════

"""
SHAPE             SYMBOL          MEANING
────────────────────────────────────────────────
Variable          name = value    Label a value
String            "text"          Text data
Number            42 or 0.95      Numeric data
Boolean           True/False      Yes/No flag
Dictionary        { }             Labeled container
Dict pair         "key": value    Label: content
Nested dict       {{"key": ""}}   Box in box
Access            dict["key"]     Get value
Safe access       .get("key", 0)  Get or default
"""


# ═══════════════════════════════════════════════════════════════════════════
# END OF CHEAT SHEET
# ═══════════════════════════════════════════════════════════════════════════
# Keep this file open as reference. Copy patterns as needed. Don't memorize!

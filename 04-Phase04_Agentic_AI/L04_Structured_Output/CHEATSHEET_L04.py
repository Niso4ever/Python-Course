"""
CHEATSHEET L04 — Structured Output
=====================================
Keep this open while reading Pydantic / structured output code.

SECTION 1: PYDANTIC MODEL SHAPES
SECTION 2: CONVERTING MODEL TO TOOL
SECTION 3: FORCING STRUCTURED OUTPUT
SECTION 4: PARSING THE RESULT
SECTION 5: TYPE TRANSLATION TABLE
SECTION 6: 3-SECOND RECOGNITION
"""

from pydantic import BaseModel, Field
from typing import Optional, Literal

# ============================================================
# SECTION 1: PYDANTIC MODEL SHAPES
# ============================================================

class BasicModel(BaseModel):
    required_str:   str              # required — must be provided
    required_int:   int              # required
    required_float: float            # required

class ModelWithOptionals(BaseModel):
    required_field: str
    optional_list:  list[str] = []           # optional — default empty list
    optional_val:   Optional[str] = None     # optional — default None
    optional_bool:  bool = False             # optional — default False

class ModelWithConstraints(BaseModel):
    score: float = Field(ge=0.0, le=1.0)    # ge=greater_equal, le=less_equal
    level: Literal["low", "medium", "high"] # only these values
    tags: list[str] = Field(default_factory=list)

# ============================================================
# SECTION 2: CONVERTING MODEL TO TOOL
# ============================================================

tool = {
    "name": "MyModel",                       # ← must match class name (or any name you want)
    "description": "What this schema extracts or evaluates",
    "input_schema": MyModel.model_json_schema()   # ← Pydantic generates JSON schema
}

# ============================================================
# SECTION 3: FORCING STRUCTURED OUTPUT
# ============================================================

# CURRENT (GA, checked 2026-10-28): native structured outputs — no tool needed
response = client.messages.parse(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "..."}],
    output_format=MyModel,                 # ← Pydantic class = schema
)
result = response.parsed_output            # ← validated MyModel instance

# OLDER (still in lots of code): force a tool. Returns HTTP 400 on
# claude-opus-5-5, claude-sonnet-5-5, claude-fable-5-1 — recognise it, don't write it.

response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=[tool],
    tool_choice={"type": "tool", "name": "MyModel"},   # ← FORCE: LLM must fill schema
    messages=[{"role": "user", "content": "..."}]
)
# response.stop_reason will always be "tool_use"
# response.content[0] will always be a tool_use block

# ============================================================
# SECTION 4: PARSING THE RESULT
# ============================================================

data_dict = response.content[0].input     # ← the filled-in dict from LLM
result = MyModel(**data_dict)              # ← typed Pydantic object
# OR:
result = MyModel.model_validate(data_dict) # ← same, with extra validation

# Access typed fields:
result.required_str    # str — not "str"
result.required_int    # int — not "42"

# Safe version (handles validation errors):
try:
    result = MyModel(**data_dict)
except ValidationError as e:
    result = None   # handle gracefully

# ============================================================
# SECTION 5: TYPE TRANSLATION TABLE
# ============================================================

# Pydantic type      → JSON schema type
# str                → {"type": "string"}
# int                → {"type": "integer"}
# float              → {"type": "number"}
# bool               → {"type": "boolean"}
# list[str]          → {"type": "array", "items": {"type": "string"}}
# Optional[str]      → nullable, not in "required"
# Literal["a","b"]   → {"enum": ["a", "b"]}
# Field(ge=0,le=1)   → {"minimum": 0, "maximum": 1}
# = default          → not in "required" list

# ============================================================
# SECTION 6: 3-SECOND RECOGNITION
# ============================================================

# Spot structured output code by looking for:
#
# 1. SCHEMA    → class MyThing(BaseModel): fields...
# 2. TOOL      → MyThing.model_json_schema() in a tool dict
# 3. FORCE     → tool_choice={"type": "tool", "name": "MyThing"}
# 4. PARSE     → MyThing(**response.content[0].input)
#
# All 4 present → structured output pattern confirmed.
"""
MINIMAL COMPLETE EXAMPLE:

from pydantic import BaseModel
client = anthropic.Anthropic()

class Result(BaseModel):
    answer: str
    confidence: float

tool = {"name": "Result", "description": "Structured answer.", "input_schema": Result.model_json_schema()}
response = client.messages.create(
    model="claude-opus-4-6", max_tokens=512,
    tools=[tool],
    tool_choice={"type": "tool", "name": "Result"},
    messages=[{"role": "user", "content": "What is RAG?"}]
)
result = Result(**response.content[0].input)
print(result.answer)       # "RAG combines retrieval..."
print(result.confidence)   # 0.92
"""

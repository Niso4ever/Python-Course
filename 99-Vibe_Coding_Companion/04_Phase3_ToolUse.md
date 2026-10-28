# Phase 3 — Tool Use & Function Calling (L01–L04, 4 templates)

This is the Architect's home turf: **Level 3 (Contract)** everywhere. Tool
schemas and Pydantic models *are* contracts — the Field Manual literally points
Level 3 at "L05, Phase 3 L01–L02." If you only master one Spec Level, master this one.

---

## 37. `template_search_tools.py` — Ph3-L01 Type Hints + Docstrings
**Level 3 (Contract) · Mode 2 (Specification)**

#### 📝 VIBE PROMPT
```
CONSTRAINTS: Full type hints (typing module). Google-style docstrings with Args/Returns.
             Signatures use only JSON-compatible types (str, int, float, bool, list, dict).
REQUEST: Search tool functions — vector_search, keyword_search, hybrid_search — each
         typed and documented well enough that an LLM can select them correctly.
VALIDATION: Every param + return is hinted; docstrings describe WHEN to use each tool.
```
#### 💻 PRODUCES (essence)
```python
def vector_search(query: str, top_k: int = 5) -> list[dict[str, Any]]:
    """Semantic search over the knowledge base.

    Args:  query: natural-language question.  top_k: max results.
    Returns: list of {doc_id, content, score} dicts.
    """
```

---

## 38. `template_agent_schemas.py` — Ph3-L02 Pydantic
**Level 3 (Contract) · Mode 2**

#### 📝 VIBE PROMPT
```
CONSTRAINTS: Pydantic v2 BaseModel. EVERY field needs Field(description="..."). Use
             Literal for enums, validators for ranges.
REQUEST: Input/output schemas for a search tool + an agent config model, with validation.
VALIDATION: score must be 0.0–1.0 (validator rejects 1.5); bad input raises ValidationError.
```
#### 💻 PRODUCES (essence)
```python
class SearchInput(BaseModel):
    query: str = Field(description="User's natural-language query")
    top_k: int = Field(default=5, ge=1, le=20, description="Max results")
    mode: Literal["vector", "keyword"] = Field(description="Search strategy")
```

---

## 39. `template_framework_adapters.py` — Ph3-L04 Tool Schemas
**Level 3 (Contract) · Mode 5 (Integration)** — adapter pattern across vendors.

#### 📝 VIBE PROMPT
```
CONSTRAINTS: One universal tool interface (ABC). Adapters convert to each vendor format.
REQUEST: A Tool abstraction that exports to OpenAI, Anthropic, AND LangChain schemas from
         a single source-of-truth definition.
VALIDATION: Defining a tool once yields all three formats; adding a vendor = one new adapter.
```
#### 💻 PRODUCES (essence)
```python
class Tool(BaseModel):
    name: str; description: str; parameters: dict
    def to_anthropic(self) -> dict: return {"name": self.name, "input_schema": self.parameters}
    def to_openai(self) -> dict:    return {"type": "function", "function": {...}}
```

---

## 40. `template_production_rag_tools.py` — Ph3-L04 Production RAG
**Level 4 (Test Cases) · Mode 2** — the hardened, real-world version.

#### 📝 VIBE PROMPT
```
CONSTRAINTS: Pydantic + Enum + validators. Production-grade: every advanced L04 pattern.
REQUEST: A complete RAG tool set — typed search input, scored results, source enum,
         freshness filtering, and confidence gating.
VALIDATION:
  - empty query → ValidationError.
  - unknown source enum value rejected.
  - results below min_confidence excluded; stale docs filtered by date.
```
#### 💻 PRODUCES (essence)
```python
class SourceType(str, Enum):
    INTERNAL = "internal_kb"; WEB = "web"; ACADEMIC = "academic"
class RAGResult(BaseModel):
    content: str = Field(description="Retrieved chunk")
    score: float = Field(ge=0.0, le=1.0, description="Relevance")
    source: SourceType = Field(description="Origin of the chunk")
```

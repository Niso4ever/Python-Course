# Lesson 07: Reading Real AI Code

These are **annotated examples** showing how real AI frameworks use your L01–L06 patterns.

## What's Inside

1. **L07_Reading_Real_AI_Code.md** — Main lesson with 4 annotated examples
2. **DECODER_RING.md** — Quick reference for translating fancy code to L01–L06
3. **example_chatbot_annotated.py** — Complete LangChain chatbot with pattern markers
4. **example_rag_annotated.py** — RAG system broken down to L01–L06 patterns
5. **example_function_calling_annotated.py** — Agent that picks tools
6. **practice_identify_patterns.py** — Test yourself: Find the patterns

## How to Use These

**Don't run them yet** — most require API keys and library installations.

**Instead:**
1. **Read** the code
2. **Identify** which Lesson each line comes from (L01–L06)
3. **Recognize** the pattern (dict, list, logic gate, loop, function, class)
4. **Understand** what it's doing

When you see code in the wild, you'll think: "Oh, that's just L02 list of dicts!"

## The Patterns You're Looking For

| Pattern | Lesson | Signal |
|:--------|:-------|:-------|
| `{}` dictionary | **L01** | Labeled drawers, config, metadata |
| `name: str` type hint | **L01** | Variable type annotation |
| `[]` list / list of dicts | **L02** | Collections, history, results |
| `if/elif/else` | **L03** | Score or boolean check |
| `match/case` | **L03** | Routing by name or status |
| `for/while` | **L04** | Loops, iteration |
| `def fn(x: str) -> dict:` | **L05** | Functions with type hints |
| `class Agent:` | **L06** | Standard class — does things |
| `@dataclass class Config:` | **L06** | Config container |
| `class Output(BaseModel):` | **L06** | Pydantic — validated data |

## The Goal

By the end of Lesson 07, you should:
- See professional AI code as just L01–L06 combinations
- Not be intimidated by LangChain / CrewAI / DSPy / Anthropic SDK
- Recognize 80% of any AI codebase is list manipulation

---

**Next:** L08 — Import patterns (how `from langchain import ChatAnthropic` actually works)

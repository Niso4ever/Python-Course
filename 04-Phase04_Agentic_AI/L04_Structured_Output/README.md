# Lesson 20: Structured Output
## Making LLMs Return Typed Data Instead of Free Text

> **2026 Note:** In 2024 you'd use LangChain's output parsers or Pydantic validators to wrangle LLM text into structured data. By 2026, providers expose structured output natively — Pydantic BaseModel + `client.messages.parse(output_format=...)` is the standard pattern. No framework required.

> **Update (2026-10-28): native structured outputs replaced the `tool_choice` trick.**
> `client.messages.parse(model=..., max_tokens=..., messages=..., output_format=MyModel)` returns
> `response.parsed_output`, already a validated `MyModel` instance. It is GA (no beta header) on every current model.
> The forced-tool pattern taught below (`tool_choice={"type": "tool", "name": ...}` or `{"type": "any"}`)
> **returns a 400 error on claude-opus-5-5, claude-sonnet-5-5 and claude-fable-5-1**. Keep recognising it, because
> older code is full of it, but write new code with `messages.parse`. If you need a tool call with schema-exact
> arguments, use `tool_choice={"type": "auto"}` plus `"strict": True` on the tool.
> Sources: platform.claude.com/docs/en/build-with-claude/structured-outputs and
> platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools#forcing-tool-use.


## Learning Materials
1. **PASS1_RECOGNITION.md** — Learn to read Pydantic models and structured output patterns (START HERE)
2. **PASS_C_VISUAL.md** — See the schema → typed response flow
3. **PASS3_TEMPLATES.md** — Copy-paste structured output patterns

## Templates
4. **CHEATSHEET_L04.py** — Quick reference (KEEP OPEN while reading output parsing code)
5. **template_structured_extractor.py** — Runnable demo: extract typed data from text

## The One Shape to Recognize

```python
from pydantic import BaseModel

class MyOutput(BaseModel):       # ← the schema
    field1: str
    field2: int
    field3: bool

# Current pattern (GA): the API fills in this schema directly
response = client.messages.parse(
    model="claude-opus-4-6", max_tokens=1024,
    messages=messages,
    output_format=MyOutput,                              # ← the schema
)
result = response.parsed_output                          # ← typed object

# Older pattern you will still see in existing code (400 on Opus 5.5 / Sonnet 5.5 / Fable 5.1):
# response = client.messages.create(tools=[schema_as_tool],
#                                   tool_choice={"type": "tool", "name": "MyOutput"}, messages=messages)
# result = MyOutput(**response.content[0].input)
```

**3-second recognition:** See `BaseModel` + `output_format=` + `parsed_output` (new) or `tool_choice={"type":"tool"}` + `model_validate` (old) → you found structured output.

## Learning Path
**Step 1:** Read `PASS1_RECOGNITION.md` (30 min)
**Step 2:** Study `PASS_C_VISUAL.md` (15 min)
**Step 3:** Browse `PASS3_TEMPLATES.md` (10 min)
**Step 4:** Run `template_structured_extractor.py` to see Pydantic validation in action

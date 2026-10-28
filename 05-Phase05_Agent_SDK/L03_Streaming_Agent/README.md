# L03 — Streaming Agent

> **Metaphor:** Non-streaming is waiting for a full letter to arrive. Streaming is watching
> someone write the letter in real time — word by word, as it appears.

---

## The Shift

Non-streaming (Phase 4 default) — response arrives complete:

```python
response = client.messages.create(model=..., messages=...)
print(response.content[0].text)   # nothing until fully done
```

Streaming — tokens arrive live:

```python
with client.messages.stream(model=..., messages=...) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)   # prints each token as it arrives
```

---

## Why It Matters

For short answers: no visible difference.
For long answers (research, writing, code): streaming feels alive. The user sees progress.
For tool-using agents: streaming lets you show "thinking..." before the tool fires.

---

## The Streaming + Tool Use Pattern

Streaming with tools has an important interrupt:

```
token → token → token → [tool_use block detected]
         INTERRUPT STREAM
         execute tool locally
         inject tool_result into messages
         restart stream for next response
token → token → token → end_turn
```

The key: you must intercept `tool_use` events inside the stream and handle them before continuing.

---

## Three Stream Modes

| Mode | When to use |
|------|------------|
| `stream.text_stream` | Text tokens only — simplest, ignores tool events |
| `stream.get_final_message()` | Stream but collect full message at end |
| Manual event loop | Full control — see every event type including tool_use |

---

## Architect's Question

> "Does my user need to see progress, or does the result only make sense when complete?
> Streaming is UX — use it when waiting feels bad. Skip it when results need to be atomic."

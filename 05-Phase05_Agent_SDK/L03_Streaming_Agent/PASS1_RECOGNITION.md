# L03 — Pass 1: RECOGNITION
## Learn to SEE Streaming Patterns

**Goal:** When you see streaming code, instantly recognize which mode it uses and what it handles — without writing a single line.

> **2026 Note:** Streaming is a UX decision more than a technical one. The model works the same either way. You add streaming when users need to see progress — long research answers, code generation, complex explanations. Learn to spot when it's missing and when it's right.

---

## The Three Shapes of Streaming

### Shape 1: The Context Manager
```python
with client.messages.stream(...) as stream:
    ...
```
**Recognize:** `with ... as stream:` — the streaming context manager. Everything inside this block has access to the live token stream.

### Shape 2: The text_stream Iterator
```python
for text in stream.text_stream:
    print(text, end="", flush=True)
```
**Recognize:** `stream.text_stream` is the simplest loop. Each `text` is a string chunk (1–10 characters). `end=""` and `flush=True` are always paired with streaming — they prevent buffering.

### Shape 3: The Final Message Collector
```python
final = stream.get_final_message()
```
**Recognize:** After the stream loop, `get_final_message()` gives you the complete structured response — useful when you need both live display AND the full object.

---

## Real Examples to RECOGNIZE (Don't Write, Just Read)

### Example 1: The Minimum Streaming Call
```python
import anthropic
client = anthropic.Anthropic()

with client.messages.stream(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Explain RAG in 3 sentences."}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
print()
```
**Recognize:** Bare minimum. No system prompt, no tools. Just stream text as it arrives. `print()` at the end adds the final newline.

---

### Example 2: Stream + Collect Final Message
```python
with client.messages.stream(
    model="claude-sonnet-5-5",
    max_tokens=512,
    messages=[{"role": "user", "content": query}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
    final = stream.get_final_message()

print(f"\nTokens: {final.usage.input_tokens} in, {final.usage.output_tokens} out")
```
**Recognize:** Stream text for UX + collect `final` for metadata. `final.usage` gives exact token counts for cost calculation.

---

### Example 3: With System Prompt
```python
with client.messages.stream(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    system="You are a technical writer. Use bullet points.",
    messages=[{"role": "user", "content": "List 5 benefits of streaming."}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```
**Recognize:** `system=` is a top-level parameter to `messages.stream()`, not inside messages. Same as non-streaming API.

---

### Example 4: Raw Event Loop (Full Control)
```python
with client.messages.stream(model=..., max_tokens=..., messages=[...]) as stream:
    for event in stream:
        if event.type == "content_block_delta" and hasattr(event.delta, "text"):
            print(event.delta.text, end="", flush=True)
        elif event.type == "message_delta":
            stop = event.delta.stop_reason   # "end_turn" or "tool_use"
```
**Recognize:** Iterating `stream` (not `stream.text_stream`) gives raw event objects. Use when you need to intercept `tool_use` events or inspect stop reasons mid-stream.

---

### Example 5: Streaming Wrapped in a Function
```python
def stream_answer(query: str, system: str = "") -> str:
    full = ""
    with client.messages.stream(
        model="claude-sonnet-5-5", max_tokens=1024, system=system,
        messages=[{"role": "user", "content": query}]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            full += text
    print()
    return full

answer = stream_answer("Explain the agent loop")
```
**Recognize:** Accumulating into `full` while streaming — both live display AND full string returned. Common production pattern.

---

### Example 6: Streaming with Progress Indicator
```python
print("Thinking", end="", flush=True)
with client.messages.stream(model=..., messages=[...]) as stream:
    first_token = True
    for text in stream.text_stream:
        if first_token:
            print("\r" + " " * 10 + "\r", end="")  # clear "Thinking..."
            first_token = False
        print(text, end="", flush=True)
```
**Recognize:** `\r` (carriage return) overwrites the previous line. Shows "Thinking..." until first token arrives, then switches to live text. Common CLI UX pattern.

---

### Example 7: Non-Streaming vs Streaming — Spot the Difference
```python
# Non-streaming — waits for complete response
response = client.messages.create(model=..., messages=[...])
print(response.content[0].text)   # nothing until fully done

# Streaming — tokens arrive live
with client.messages.stream(model=..., messages=[...]) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)   # each token prints immediately
```
**Recognize:** `messages.create()` = wait and get all. `messages.stream()` = get tokens live. Same model, same cost, different UX.

---

### Example 8: Streaming in Async Context
```python
async def stream_async(query: str) -> str:
    async_client = anthropic.AsyncAnthropic()
    full = ""
    async with async_client.messages.stream(
        model="claude-sonnet-5-5",
        max_tokens=512,
        messages=[{"role": "user", "content": query}]
    ) as stream:
        async for text in stream.text_stream:
            print(text, end="", flush=True)
            full += text
    print()
    return full
```
**Recognize:** `AsyncAnthropic` + `async with` + `async for` — the async variant of streaming. Use in FastAPI, asyncio apps, or Agent SDK integrations.

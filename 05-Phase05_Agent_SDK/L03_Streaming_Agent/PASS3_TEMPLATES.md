# L03 — Pass 3: TEMPLATES
## Your Streaming Copy-Paste Library

**Goal:** Five streaming patterns. Copy the one that fits, replace the query, run.

> **2026 Note:** Streaming is a UX decision. All templates use `import anthropic` directly since `client.messages.stream()` is still the cleanest streaming API. The Agent SDK's `query()` handles streaming internally — use these templates when you want explicit control over the stream.

---

## Template 1: Simple Text Stream
**Use when:** User needs to see a long response arrive live — the most common case

```python
import anthropic
client = anthropic.Anthropic()

def stream_response(query: str, system: str = "") -> str:
    """Stream response to stdout, return full text."""
    full = ""
    with client.messages.stream(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": query}]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            full += text
    print()
    return full

# Call:
answer = stream_response("Explain RAG in 3 paragraphs.")
# → tokens print as they arrive, full text returned when done
```

---

## Template 2: Stream + Collect Usage Metrics
**Use when:** You want live display AND token usage for cost tracking

```python
import anthropic
client = anthropic.Anthropic()

def stream_with_metrics(query: str) -> dict:
    """Stream response and return result with token usage.

    Returns:
        Dict with 'text', 'input_tokens', 'output_tokens', 'cost_usd'.
    """
    full = ""
    with client.messages.stream(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": query}]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            full += text
        final = stream.get_final_message()
    print()

    input_tok  = final.usage.input_tokens
    output_tok = final.usage.output_tokens
    cost = (input_tok / 1000 * 0.003) + (output_tok / 1000 * 0.015)

    return {"text": full, "input_tokens": input_tok,
            "output_tokens": output_tok, "cost_usd": round(cost, 6)}

# Call:
result = stream_with_metrics("What is the agent loop?")
print(f"\nCost: ${result['cost_usd']:.6f}")
```

---

## Template 3: Stream With Progress Indicator
**Use when:** Response may take several seconds — show user the agent is working

```python
import anthropic, sys, time, threading
client = anthropic.Anthropic()

def _spinner(stop_event: threading.Event) -> None:
    frames = ["⠋", "⠙", "⠸", "⠴", "⠦", "⠇"]
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r{frames[i % len(frames)]} Thinking...")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write("\r" + " " * 20 + "\r")

def stream_with_spinner(query: str) -> str:
    stop = threading.Event()
    spinner = threading.Thread(target=_spinner, args=(stop,))
    spinner.start()

    full = ""
    with client.messages.stream(
        model="claude-sonnet-5-5", max_tokens=1024,
        messages=[{"role": "user", "content": query}]
    ) as stream:
        stop.set(); spinner.join()          # clear spinner when first token arrives
        for text in stream.text_stream:
            print(text, end="", flush=True)
            full += text
    print()
    return full
```

---

## Template 4: Async Stream (For FastAPI / Async Contexts)
**Use when:** Building an async web API or using streaming inside an async function

```python
import anthropic
async_client = anthropic.AsyncAnthropic()

async def stream_async(query: str, system: str = "") -> str:
    """Async streaming — use inside FastAPI endpoints or async functions."""
    full = ""
    async with async_client.messages.stream(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": query}]
    ) as stream:
        async for text in stream.text_stream:
            print(text, end="", flush=True)
            full += text
    print()
    return full

# FastAPI usage:
# @app.post("/stream")
# async def endpoint(req: Request) -> StreamingResponse:
#     async def gen():
#         async for text in async_client.messages.stream(...).text_stream:
#             yield text
#     return StreamingResponse(gen(), media_type="text/plain")
```

---

## Template 5: Stream With Tool Use Interception
**Use when:** Streaming an agent that also calls tools — you need to handle both

```python
import anthropic, json
client = anthropic.Anthropic()

def stream_with_tools(query: str, tools: list, tool_map: dict) -> str:
    """Stream a response that may include tool calls.

    Intercepts tool_use events, executes them, then continues streaming.
    """
    messages = [{"role": "user", "content": query}]
    full_text = ""

    while True:
        tool_calls = []
        current_text = ""

        with client.messages.stream(model="claude-sonnet-5-5", max_tokens=1024,
                                    tools=tools, messages=messages) as stream:
            for event in stream:
                if hasattr(event, "delta") and hasattr(event.delta, "text"):
                    print(event.delta.text, end="", flush=True)
                    current_text += event.delta.text
                elif event.type == "content_block_start" and hasattr(event.content_block, "type"):
                    if event.content_block.type == "tool_use":
                        tool_calls.append({"id": event.content_block.id,
                                           "name": event.content_block.name, "input": {}})
            final = stream.get_final_message()

        if final.stop_reason == "end_turn":
            full_text += current_text
            break

        # Execute tools and loop
        tool_results = []
        for call in tool_calls:
            result = tool_map.get(call["name"], lambda a: "unknown tool")(call["input"])
            tool_results.append({"type": "tool_result", "tool_use_id": call["id"], "content": str(result)})

        messages += [{"role": "assistant", "content": final.content},
                     {"role": "user", "content": tool_results}]

    print()
    return full_text
```

---

## Quick Selection Guide

| Need | Template |
|------|----------|
| Basic live display | Template 1: Simple Text Stream |
| Live display + cost tracking | Template 2: Stream + Metrics |
| Show spinner while waiting | Template 3: Progress Indicator |
| FastAPI / async web app | Template 4: Async Stream |
| Agent with tools + streaming | Template 5: Tool Interception |

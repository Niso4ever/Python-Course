"""
CHEATSHEET L03 — Streaming Agent
Three ways to stream Claude responses.
"""
import anthropic
client = anthropic.Anthropic()

# ── 1. SIMPLEST: text_stream (text tokens only) ───────────────────────────────
with client.messages.stream(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Explain RAG in 3 sentences."}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
print()  # newline after stream ends

# ── 2. STREAM + COLLECT FINAL MESSAGE ────────────────────────────────────────
with client.messages.stream(model="claude-sonnet-5-5", max_tokens=512,
                             messages=[{"role":"user","content":"..."}]) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
    final = stream.get_final_message()  # structured Message object

# ── 3. RAW EVENT LOOP (full control, needed for tools) ───────────────────────
with client.messages.stream(model="claude-sonnet-5-5", max_tokens=512,
                             messages=[...]) as stream:
    for event in stream:
        if event.type == "content_block_delta" and hasattr(event.delta, "text"):
            print(event.delta.text, end="", flush=True)
        elif event.type == "message_delta":
            pass  # stop_reason available here

# ── 4. STREAMING WITH TOOLS (interrupt pattern) ──────────────────────────────
# There is no stream event of type "tool_use". A tool call arrives as a
# content_block_start whose content_block.type == "tool_use", then input_json_delta
# chunks. Simplest: print text live, then read finished tool calls from the final message.
# with client.messages.stream(tools=TOOLS, ...) as stream:
#     for text in stream.text_stream:
#         print(text, end="", flush=True)
#     final = stream.get_final_message()
# for block in final.content:
#     if block.type == "tool_use":
#         result = dispatch_tool(block.name, block.input)
#         # append tool_result, start a new stream call for the continuation

# ── 5. STREAMING DECISION ────────────────────────────────────────────────────
# Use streaming when:   user waits for long responses (research, writing, code)
# Skip streaming when:  response is short / atomic / must be complete before use

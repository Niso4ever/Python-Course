# L03 — Visual: Streaming Agent Flow

## Non-Streaming vs. Streaming

```
NON-STREAMING                           STREAMING
─────────────────────────               ──────────────────────────────────
response = client.messages.create(...)  with client.messages.stream(...) as s:
                                            for text in s.text_stream:
[....2 seconds of silence....]              print(text, end="", flush=True)
                                        # ↑ tokens print as they arrive
print(response.content[0].text)
# "Quantum computing uses quantum
#  mechanical phenomena to process..."
                                        # Q...u...a...n...t...u...m...
```

---

## Token Stream Timeline

```
Time ──────────────────────────────────────────────────────────────────►

Non-streaming:
  send ──────────────────────────────────────────── receive ──── print
                        (waiting)                   (all at once)

Streaming:
  send ── receive[Q] ── receive[uantum] ── receive[ computing] ── ...
           print         print              print
  (each chunk prints immediately as it arrives)
```

---

## Streaming with Tool Use — The Interrupt Pattern

```
Stream starts:
  "Let me look that up... "     ← text tokens flowing

Tool use block detected:
  ┌─────────────────────────────────────────┐
  │  STREAM PAUSES                          │
  │  Tool: search_knowledge_base            │
  │  Input: {"query": "quantum computing"}  │
  └──────────────┬──────────────────────────┘
                 │
                 ▼ execute tool locally
                 result = "Quantum computing uses..."
                 │
                 ▼ inject tool_result into messages
                 │
  ┌──────────────┴──────────────────────────┐
  │  STREAM RESTARTS (new API call)         │
  └─────────────────────────────────────────┘
  "Based on the search results, quantum computing..."
  ← text tokens flowing again
```

---

## Three Ways to Handle the Stream

```
METHOD 1: text_stream (simplest)
  for text in stream.text_stream:
      print(text, end="")
  # ✓ prints text tokens  ✗ ignores tool events

METHOD 2: get_final_message (collect + stream)
  with client.messages.stream(...) as stream:
      for text in stream.text_stream:
          print(text, end="")                  # show progress
      final = stream.get_final_message()       # get complete object
  # ✓ shows progress AND gives structured result

METHOD 3: raw event loop (full control)
  with client.messages.stream(...) as stream:
      for event in stream:
          if event.type == "content_block_delta":
              print(event.delta.text, end="")
          elif event.type == "tool_use":
              handle_tool(event)               # intercept tools
  # ✓ complete control  ✗ more code
```

---

## Stream Event Types in Order

```
message_start          ← stream begins, gives message ID
content_block_start    ← a new block starts (text or tool_use)
content_block_delta    ← token arrives (text) or input accumulates (tool)
content_block_stop     ← block complete
message_delta          ← stop_reason announced ("end_turn" or "tool_use")
message_stop           ← stream ends
```

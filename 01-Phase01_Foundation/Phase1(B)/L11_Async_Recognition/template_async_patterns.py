"""
TEMPLATE: Async Patterns for AI
=================================
Use: Parallel LLM calls, streaming, batch processing

pip install: pip install anthropic langchain-anthropic python-dotenv

COPY the pattern you need.
"""
import asyncio
import time
from dotenv import load_dotenv

load_dotenv()

# ═══════════════════════════════════════════════════════════
# PATTERN 1: Parallel Multi-Model Calls
# ═══════════════════════════════════════════════════════════
import anthropic

async def call_model(client, prompt: str, model: str) -> dict:
    """Single async LLM call with timing."""
    start = time.time()
    response = await client.messages.create(
        model=model,
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )
    elapsed = round(time.time() - start, 2)
    return {
        "model":   model,
        "answer":  response.content[0].text,
        "seconds": elapsed,
        "tokens":  response.usage.output_tokens
    }

async def compare_models_parallel(prompt: str) -> list[dict]:
    """Run the same prompt on 3 models simultaneously."""
    client = anthropic.AsyncAnthropic()
    models = [
        "claude-haiku-5-5",
        "claude-sonnet-5-5",
        "claude-opus-5-5",
    ]
    tasks   = [call_model(client, prompt, m) for m in models]
    results = await asyncio.gather(*tasks)
    return list(results)


# ═══════════════════════════════════════════════════════════
# PATTERN 2: Batch Processing with Rate Limit Handling
# ═══════════════════════════════════════════════════════════
async def process_batch(prompts: list[str],
                        model: str = "claude-haiku-5-5",
                        batch_size: int = 5,
                        delay_between_batches: float = 1.0) -> list[str]:
    """
    Process a large list of prompts in batches.
    Avoids rate limits by pausing between batches.

    IN:  prompts (list of str), model, batch_size, delay
    OUT: list of responses (str)
    """
    client  = anthropic.AsyncAnthropic()
    results = []

    for i in range(0, len(prompts), batch_size):
        batch = prompts[i:i + batch_size]
        print(f"Processing batch {i//batch_size + 1} ({len(batch)} items)...")

        tasks = [
            client.messages.create(
                model=model,
                max_tokens=500,
                messages=[{"role": "user", "content": p}]
            )
            for p in batch
        ]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        for resp in responses:
            if isinstance(resp, Exception):
                results.append(f"ERROR: {resp}")
            else:
                results.append(resp.content[0].text)

        # Pause between batches to respect rate limits
        if i + batch_size < len(prompts):
            await asyncio.sleep(delay_between_batches)

    return results


# ═══════════════════════════════════════════════════════════
# PATTERN 3: Streaming Response
# ═══════════════════════════════════════════════════════════
async def stream_response(prompt: str,
                          model: str = "claude-sonnet-5-5") -> str:
    """
    Stream LLM response token by token.
    Prints each token as it arrives, returns full text.

    IN:  prompt (str), model (str)
    OUT: full response text (str)
    """
    client    = anthropic.AsyncAnthropic()
    full_text = ""

    async with client.messages.stream(
        model=model,
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        async for chunk in stream.text_stream:
            print(chunk, end="", flush=True)
            full_text += chunk
    print()  # newline at end
    return full_text


# ═══════════════════════════════════════════════════════════
# PATTERN 4: Async with Retry (Production-Ready)
# ═══════════════════════════════════════════════════════════
async def resilient_call(prompt: str,
                         model: str = "claude-sonnet-5-5",
                         max_retries: int = 3) -> str:
    """
    LLM call with exponential backoff retry.
    Handles rate limits and temporary failures.

    IN:  prompt, model, max_retries
    OUT: response text (str)
    """
    client = anthropic.AsyncAnthropic()

    for attempt in range(max_retries):
        try:
            response = await client.messages.create(
                model=model,
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text

        except anthropic.RateLimitError:
            wait = 2 ** attempt  # 1s, 2s, 4s
            print(f"Rate limited. Retry {attempt+1}/{max_retries} in {wait}s...")
            await asyncio.sleep(wait)

        except anthropic.APIStatusError as e:
            if e.status_code == 529:  # overloaded
                await asyncio.sleep(5)
            else:
                raise

    raise RuntimeError(f"Failed after {max_retries} retries")


# ═══════════════════════════════════════════════════════════
# DEMO (simulated — won't make real API calls)
# ═══════════════════════════════════════════════════════════
async def demo():
    print("=" * 60)
    print("Async Patterns Demo (simulated)")
    print("=" * 60)
    print()
    print("PATTERN 1: Parallel model comparison")
    print("  3 models run simultaneously → takes time of 1 call")
    print("  Usage: results = await compare_models_parallel(prompt)")
    print()
    print("PATTERN 2: Batch processing with rate limiting")
    print("  Large lists split into batches with pause between")
    print("  Usage: results = await process_batch(prompts, batch_size=5)")
    print()
    print("PATTERN 3: Streaming response")
    print("  Tokens appear as they're generated")
    print("  Usage: text = await stream_response(prompt)")
    print()
    print("PATTERN 4: Resilient call with retry")
    print("  Handles rate limits automatically with backoff")
    print("  Usage: text = await resilient_call(prompt)")
    print()
    print("To use with real API: set ANTHROPIC_API_KEY in .env")
    print("Run: asyncio.run(compare_models_parallel('What is RAG?'))")

if __name__ == "__main__":
    asyncio.run(demo())

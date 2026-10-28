import asyncio
import time
from types import SimpleNamespace
from extractor import extract_record

DEMO_MODE = True  # True: fake client, no API key, no cost. False: real API call.

# Simulated raw data batch
RAW_DATA_BATCH = [
    "Alice Jones bought 2 widgets (SKU-100) for $15.50 each on 2026-06-20. Her email is alice@example.com.",
    "Bob Smith returned his order from yesterday (2026-06-19). He had bought a super-gadget (SKU-200) for $99.99.",
    "Order by Charlie on 2026-06-21: 5x SKU-300 at $4.00, 1x SKU-100 at $15.50. Total $35.50. Customer complained it arrived late."
]

# We must respect API rate limits.
MAX_CONCURRENT_CALLS = 2
semaphore = asyncio.Semaphore(MAX_CONCURRENT_CALLS)

class FakeClient:
    """Stands in for AsyncAnthropic in demo mode: same call shape, canned reply."""

    def __init__(self) -> None:
        self.messages = self

    async def create(self, **kwargs) -> SimpleNamespace:
        await asyncio.sleep(1.0)  # simulate API latency
        canned = {
            "customer_name": "Simulated Customer",
            "email": "sim@example.com",
            "purchase_date": "2026-06-20",
            "items": [{"product_id": "SKU-SIM", "quantity": 1, "unit_price_usd": 10.0}],
            "total_value_usd": 10.0,
            "is_flagged": False,
        }
        block = SimpleNamespace(type="tool_use", name=kwargs["tools"][0]["name"], input=canned)
        return SimpleNamespace(content=[block])


async def process_single_record(raw_text: str) -> dict:
    """Wraps the extraction call with rate limiting and timing."""
    async with semaphore:
        print(f"Processing: {raw_text[:40]}...")
        
        # Demo mode swaps only the client. extract_record() still runs its
        # real parsing and Pydantic validation on the fake tool_use reply.
        record = await extract_record(raw_text, llm=FakeClient() if DEMO_MODE else None)
        
        if record:
            return record.model_dump()
        return {"error": "Failed to parse", "raw": raw_text}


async def main():
    print(f"Starting batch extraction pipeline for {len(RAW_DATA_BATCH)} records...")
    start_time = time.time()
    
    # Launch all tasks concurrently, constrained by the semaphore
    tasks = [process_single_record(text) for text in RAW_DATA_BATCH]
    results = await asyncio.gather(*tasks)
    
    elapsed = time.time() - start_time
    print(f"\nPipeline complete in {elapsed:.2f}s")
    
    # Print the structured, validated data
    import json
    for i, res in enumerate(results):
        print(f"\n--- Record {i+1} ---")
        print(json.dumps(res, indent=2, default=str))

if __name__ == "__main__":
    asyncio.run(main())

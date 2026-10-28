import asyncio
import json
from anthropic import AsyncAnthropic
from schema import CustomerRecord

# Initialize the async client
client = AsyncAnthropic()

# Convert the Pydantic schema to an Anthropic tool definition
def schema_to_tool() -> dict:
    return {
        "name": "extract_customer_record",
        "description": "Extracts structured customer data from raw text.",
        "input_schema": CustomerRecord.model_json_schema()
    }

async def extract_record(raw_text: str, llm=None) -> CustomerRecord | None:
    """Uses the LLM as a fuzzy parser to force output into a strict schema.

    Args:
        raw_text: One unstructured purchase description.
        llm: Optional client with the same `messages.create` shape. Demo mode
            passes a fake one, so the parsing and validation below still run.

    Returns:
        A validated CustomerRecord, or None if extraction failed.
    """
    llm = llm or client
    try:
        response = await llm.messages.create(
            # Model IDs age out — verify against the latest list before shipping.
            # As of 2026: claude-opus-4-8 (most capable), claude-sonnet-4-6 (balanced), claude-haiku-5-5 (fast).
            model="claude-opus-4-8",
            max_tokens=1024,
            system="You are a data extraction pipeline. Extract the exact facts. If a fact is missing, omit it or use a default. Calculate the total value if not explicitly stated.",
            messages=[{"role": "user", "content": raw_text}],
            tools=[schema_to_tool()],
            # FORCE the model to use the tool, guaranteeing structured output.
            # 2026 caution: forced tool_choice ("tool" or "any") returns a 400
            # error on the newest models (Claude Opus 5.5, Sonnet 5.5, Fable 5.1,
            # Mythos 5.1). There, use tool_choice "auto" with strict tool use
            # (strict: true on the tool), or structured outputs
            # (output_config.format). Check the model you call before shipping.
            tool_choice={"type": "tool", "name": "extract_customer_record"}
        )
        
        # The model MUST return a tool_use block due to tool_choice
        for block in response.content:
            if block.type == "tool_use" and block.name == "extract_customer_record":
                # Validate the raw JSON against our strict Pydantic model
                return CustomerRecord.model_validate(block.input)
                
        return None
        
    except Exception as e:
        print(f"Extraction failed: {e}")
        return None

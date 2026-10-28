"""
Template: Structured Output Extractor — Runnable Demo
=======================================================
Run this file as-is: python template_structured_extractor.py

DEMO MODE (default): Simulated LLM responses. No API key needed.
REAL MODE:           Set DEMO_MODE = False + ANTHROPIC_API_KEY.

What this demonstrates:
  - Pydantic model definition
  - Native structured outputs: client.messages.parse(output_format=Model)
    returns response.parsed_output, already a validated Pydantic object
    (GA, no beta header; checked 2026-10-28 against
    platform.claude.com/docs/en/build-with-claude/structured-outputs)
  - Converting model to tool schema (the older tool_choice trick; see note below)
  - Parsing typed Python objects from responses

NOTE (2026-10-28): the older pattern, forcing a tool with
tool_choice={"type": "tool", "name": ...}, returns a 400 error on
claude-opus-5-5, claude-sonnet-5-5 and claude-fable-5-1. Use messages.parse.
  - The evaluator (quality gate) pattern
  - Safe extraction with error handling
"""

import os
import json
from pydantic import BaseModel, Field, ValidationError
from typing import Optional, Literal

DEMO_MODE = True  # Set to False + ANTHROPIC_API_KEY for real Claude

# ============================================================
# SCHEMAS (Pydantic models)
# ============================================================

class PersonInfo(BaseModel):
    name: str
    age: int
    occupation: str
    city: str

class EvaluationResult(BaseModel):
    score: int                                        # 1–10
    passes: bool
    reasoning: str
    action: Literal["accept", "retry", "escalate"]
    suggestions: list[str]

class DocumentSummary(BaseModel):
    title: str
    main_topic: str
    key_points: list[str]
    sentiment: Literal["positive", "neutral", "negative"]
    word_count_estimate: int
    confidence: float = Field(ge=0.0, le=1.0)

# ============================================================
# TOOL SCHEMA BUILDER
# ============================================================

def build_tool(model_class, description: str) -> dict:
    """Convert a Pydantic model to an Anthropic tool schema."""
    return {
        "name": model_class.__name__,
        "description": description,
        "input_schema": model_class.model_json_schema()
    }

# ============================================================
# DEMO: Simulated LLM responses
# ============================================================

class MockBlock:
    def __init__(self, btype, **kwargs):
        self.type = btype
        for k, v in kwargs.items():
            setattr(self, k, v)

class MockResponse:
    def __init__(self, stop_reason, content):
        self.stop_reason = stop_reason
        self.content = content

DEMO_RESPONSES = {
    "PersonInfo": MockResponse("tool_use", [
        MockBlock("tool_use", id="tu_01", name="PersonInfo", input={
            "name": "Sarah Chen",
            "age": 32,
            "occupation": "AI Research Scientist",
            "city": "San Francisco"
        })
    ]),
    "EvaluationResult_bad": MockResponse("tool_use", [
        MockBlock("tool_use", id="tu_02", name="EvaluationResult", input={
            "score": 2,
            "passes": False,
            "reasoning": "The definition is completely incorrect. RAG stands for Retrieval-Augmented Generation, not Random Access Generation.",
            "action": "retry",
            "suggestions": [
                "Correct the acronym to Retrieval-Augmented Generation",
                "Explain what retrieval means in this context",
                "Describe how it combines with generation"
            ]
        })
    ]),
    "EvaluationResult_good": MockResponse("tool_use", [
        MockBlock("tool_use", id="tu_03", name="EvaluationResult", input={
            "score": 9,
            "passes": True,
            "reasoning": "Accurate, concise definition covering both retrieval and generation aspects.",
            "action": "accept",
            "suggestions": ["Could mention grounding as a benefit"]
        })
    ]),
    "DocumentSummary": MockResponse("tool_use", [
        MockBlock("tool_use", id="tu_04", name="DocumentSummary", input={
            "title": "The Rise of Agentic AI in 2026",
            "main_topic": "Agentic AI systems and their adoption in enterprise",
            "key_points": [
                "Agent loops replace traditional workflow automation",
                "MCP becomes the standard for tool connectivity",
                "Direct API usage overtakes framework-based development",
                "Multi-agent systems handle complex reasoning tasks"
            ],
            "sentiment": "positive",
            "word_count_estimate": 850,
            "confidence": 0.91
        })
    ])
}

def demo_create(model_name: str, messages: list) -> MockResponse:
    return DEMO_RESPONSES.get(model_name, DEMO_RESPONSES["PersonInfo"])

class MockParsedResponse:
    """Shaped like the ParsedMessage that client.messages.parse() returns."""
    def __init__(self, parsed_output):
        self.parsed_output = parsed_output

def demo_parse(demo_key: str, model_class) -> MockParsedResponse:
    """Simulate messages.parse(): canned JSON, validated into model_class."""
    raw = demo_create(demo_key, [])
    return MockParsedResponse(model_class.model_validate(raw.content[0].input))

# ============================================================
# CORE EXTRACTOR FUNCTION
# ============================================================

def extract_structured(text: str, model_class, description: str):
    """
    Force the LLM to extract text into a typed Pydantic object.
    Returns typed object or None on failure.
    """
    messages = [{"role": "user", "content": f"{description}\n\nExtract structured information from:\n\n{text}"}]

    try:
        if DEMO_MODE:
            response = demo_parse(model_class.__name__, model_class)
        else:
            import anthropic
            client = anthropic.Anthropic()
            response = client.messages.parse(
                model="claude-opus-5-5",
                max_tokens=1024,
                messages=messages,
                output_format=model_class,      # ← the Pydantic class IS the schema
            )

        return response.parsed_output           # ← already a validated model_class instance

    except ValidationError as e:
        print(f"  Validation error: {e}")
        return None
    except Exception as e:
        print(f"  Extraction error: {e}")
        return None

# ============================================================
# DEMO 1: Extract Person Info
# ============================================================

def demo_person_extraction():
    print("\n" + "="*60)
    print("DEMO 1: Structured Extraction — PersonInfo")
    print("="*60)

    text = "Dr. Sarah Chen is a 32-year-old AI Research Scientist based in San Francisco. She specializes in large language models and agentic systems."

    print(f"Input text: {text[:80]}...")
    person = extract_structured(text, PersonInfo, "Extract person details from text.")

    if person:
        print(f"\nExtracted PersonInfo:")
        print(f"  name:       {person.name}")
        print(f"  age:        {person.age}  ← typed int")
        print(f"  occupation: {person.occupation}")
        print(f"  city:       {person.city}")
        print(f"\ntype(person.age) = {type(person.age).__name__}  ← not 'str', it's int!")

# ============================================================
# DEMO 2: Quality Gate / Evaluator
# ============================================================

def demo_evaluator():
    print("\n" + "="*60)
    print("DEMO 2: Quality Gate — EvaluationResult")
    print("="*60)

    bad_answer  = "RAG stands for Random Access Generation."
    good_answer = "RAG (Retrieval-Augmented Generation) combines a retrieval system with an LLM to ground responses in real documents."

    for label, answer, demo_key in [
        ("BAD ANSWER",  bad_answer,  "EvaluationResult_bad"),
        ("GOOD ANSWER", good_answer, "EvaluationResult_good")
    ]:
        print(f"\n--- Evaluating {label} ---")
        print(f"  Answer: {answer[:60]}...")

        messages = [{"role": "user", "content": f"Q: What is RAG?\nA: {answer}\nEvaluate 1-10."}]

        if DEMO_MODE:
            response = demo_parse(demo_key, EvaluationResult)
        else:
            import anthropic
            client = anthropic.Anthropic()
            response = client.messages.parse(
                model="claude-opus-5-5", max_tokens=1024,
                messages=messages,
                output_format=EvaluationResult,
            )

        result = response.parsed_output
        print(f"  Score:     {result.score}/10")
        print(f"  Passes:    {result.passes}")
        print(f"  Action:    '{result.action}'")
        print(f"  Reasoning: {result.reasoning[:80]}...")

# ============================================================
# DEMO 3: Document Summarizer
# ============================================================

def demo_document_summary():
    print("\n" + "="*60)
    print("DEMO 3: Document Summary — DocumentSummary")
    print("="*60)

    document = """
    The Rise of Agentic AI in 2026

    This year marked a turning point in AI deployment. Agent loops have replaced
    traditional workflow automation across industries. The Model Context Protocol
    (MCP) became the universal standard for connecting AI models to tools, making
    framework-specific integrations obsolete. Most enterprise teams now use direct
    API calls rather than heavyweight frameworks like LangChain or CrewAI.
    Multi-agent systems have emerged as the dominant architecture for complex
    reasoning tasks, with orchestrator-specialist patterns seeing wide adoption.
    """

    summary = extract_structured(document, DocumentSummary,
                                  "Summarize a document into structured fields.")

    if summary:
        print(f"\nExtracted DocumentSummary:")
        print(f"  title:              {summary.title}")
        print(f"  main_topic:         {summary.main_topic}")
        print(f"  key_points:         {len(summary.key_points)} points")
        for i, point in enumerate(summary.key_points[:3], 1):
            print(f"    {i}. {point}")
        print(f"  sentiment:          {summary.sentiment}")
        print(f"  word_count_est:     {summary.word_count_estimate}")
        print(f"  confidence:         {summary.confidence}")

# ============================================================
# RUN ALL DEMOS
# ============================================================

if __name__ == "__main__":
    demo_person_extraction()
    demo_evaluator()
    demo_document_summary()

    if DEMO_MODE:
        print("\n" + "="*60)
        print("[DEMO MODE] Set DEMO_MODE = False + ANTHROPIC_API_KEY for real Claude.")

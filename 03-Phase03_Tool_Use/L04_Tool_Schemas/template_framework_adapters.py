"""
Framework Adapters: Convert tools between OpenAI, Anthropic, LangChain, etc.
Production-ready patterns for framework interoperability.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Callable
from abc import ABC, abstractmethod


# ============================================================================
# UNIVERSAL TOOL INTERFACE
# ============================================================================

class ToolInterface(ABC):
    """Abstract interface all tools must implement."""

    @abstractmethod
    def get_name(self) -> str:
        """Return tool name."""
        pass

    @abstractmethod
    def get_description(self) -> str:
        """Return tool description."""
        pass

    @abstractmethod
    def get_input_schema(self) -> type[BaseModel]:
        """Return Pydantic input schema."""
        pass

    @abstractmethod
    def execute(self, **kwargs) -> dict:
        """Execute the tool with validated inputs."""
        pass


# ============================================================================
# FRAMEWORK ADAPTERS
# ============================================================================

class OpenAIAdapter:
    """Adapter for OpenAI function calling format."""

    @staticmethod
    def to_schema(tool: ToolInterface) -> dict:
        """
        Convert tool to OpenAI function calling schema.

        Returns format expected by openai.ChatCompletion.create(tools=...)
        """
        input_schema = tool.get_input_schema().model_json_schema()

        return {
            "type": "function",
            "function": {
                "name": tool.get_name(),
                "description": tool.get_description(),
                "parameters": input_schema
            }
        }

    @staticmethod
    def parse_function_call(response: dict) -> tuple[str, dict]:
        """
        Parse function call from OpenAI response.

        Args:
            response: OpenAI chat completion response

        Returns:
            (function_name, arguments_dict)
        """
        import json

        choice = response["choices"][0]
        message = choice["message"]

        # Check for function call
        if "function_call" in message:
            func_call = message["function_call"]
            return (
                func_call["name"],
                json.loads(func_call["arguments"])
            )

        # Check for tool calls (newer format)
        if "tool_calls" in message:
            tool_call = message["tool_calls"][0]  # Get first tool call
            return (
                tool_call["function"]["name"],
                json.loads(tool_call["function"]["arguments"])
            )

        raise ValueError("No function call found in response")

    @staticmethod
    def format_tool_response(
        function_name: str,
        result: dict,
        tool_call_id: Optional[str] = None
    ) -> dict:
        """
        Format tool execution result for OpenAI.

        Args:
            function_name: Name of the function that was called
            result: Result from function execution
            tool_call_id: Optional tool call ID (for newer format)

        Returns:
            Message dict to add to conversation
        """
        import json

        if tool_call_id:
            # Newer format
            return {
                "role": "tool",
                "tool_call_id": tool_call_id,
                "content": json.dumps(result)
            }
        else:
            # Older format
            return {
                "role": "function",
                "name": function_name,
                "content": json.dumps(result)
            }


class AnthropicAdapter:
    """Adapter for Anthropic Claude tool use format."""

    @staticmethod
    def to_schema(tool: ToolInterface) -> dict:
        """
        Convert tool to Anthropic tool use schema.

        Returns format expected by anthropic.messages.create(tools=...)
        """
        input_schema = tool.get_input_schema().model_json_schema()

        return {
            "name": tool.get_name(),
            "description": tool.get_description(),
            "input_schema": input_schema
        }

    @staticmethod
    def parse_tool_use(response: dict) -> tuple[str, dict]:
        """
        Parse tool use from Anthropic response.

        Args:
            response: Anthropic message response

        Returns:
            (tool_name, tool_input)
        """
        content = response.get("content", [])

        for block in content:
            if block.get("type") == "tool_use":
                return (
                    block["name"],
                    block["input"]
                )

        raise ValueError("No tool use found in response")

    @staticmethod
    def format_tool_result(
        tool_use_id: str,
        result: dict,
        is_error: bool = False
    ) -> dict:
        """
        Format tool execution result for Anthropic.

        Args:
            tool_use_id: ID from tool_use block
            result: Result from function execution
            is_error: Whether the result is an error

        Returns:
            Message dict to add to conversation
        """
        import json

        return {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use_id,
                    "content": json.dumps(result),
                    "is_error": is_error
                }
            ]
        }


class LangChainAdapter:
    """Adapter for LangChain tool format."""

    @staticmethod
    def to_tool(tool: ToolInterface):
        """
        Convert to LangChain Tool.

        Returns:
            LangChain Tool instance
        """
        from langchain_core.tools import Tool   # LangChain 1.x: Tool is no longer re-exported from langchain.tools

        return Tool(
            name=tool.get_name(),
            description=tool.get_description(),
            func=tool.execute,
            args_schema=tool.get_input_schema()
        )

    @staticmethod
    def to_structured_tool(tool: ToolInterface):
        """
        Convert to LangChain StructuredTool.

        Returns:
            LangChain StructuredTool instance
        """
        from langchain_core.tools import StructuredTool

        return StructuredTool(
            name=tool.get_name(),
            description=tool.get_description(),
            func=tool.execute,
            args_schema=tool.get_input_schema()
        )


# ============================================================================
# UNIVERSAL TOOL WRAPPER
# ============================================================================

class UniversalTool(ToolInterface):
    """
    A tool that works with all frameworks.

    Implements ToolInterface and provides adapters for:
    - OpenAI function calling
    - Anthropic tool use
    - LangChain tools
    - CrewAI tools (via LangChain adapter)
    - AutoGen tools
    """

    def __init__(
        self,
        name: str,
        description: str,
        input_schema: type[BaseModel],
        output_schema: Optional[type[BaseModel]],
        func: Callable
    ):
        self.name = name
        self.description = description
        self.input_schema = input_schema
        self.output_schema = output_schema
        self.func = func

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description

    def get_input_schema(self) -> type[BaseModel]:
        return self.input_schema

    def execute(self, **kwargs) -> dict:
        """Execute with validation and error handling."""
        try:
            # Validate input
            validated_input = self.input_schema(**kwargs)

            # Execute function
            result = self.func(validated_input)

            # Validate output if schema provided
            if self.output_schema:
                if isinstance(result, dict):
                    validated_output = self.output_schema(**result)
                    result = validated_output.model_dump()

            return {
                "success": True,
                "data": result
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }

    # Framework-specific methods
    def to_openai(self) -> dict:
        """Convert to OpenAI format."""
        return OpenAIAdapter.to_schema(self)

    def to_anthropic(self) -> dict:
        """Convert to Anthropic format."""
        return AnthropicAdapter.to_schema(self)

    def to_langchain(self):
        """Convert to LangChain Tool."""
        return LangChainAdapter.to_tool(self)

    def to_langchain_structured(self):
        """Convert to LangChain StructuredTool."""
        return LangChainAdapter.to_structured_tool(self)


# ============================================================================
# TOOL REGISTRY WITH MULTI-FRAMEWORK SUPPORT
# ============================================================================

class ToolRegistry:
    """Registry that manages tools for multiple frameworks."""

    def __init__(self):
        self.tools: Dict[str, UniversalTool] = {}

    def register(self, tool: UniversalTool) -> None:
        """Register a tool."""
        self.tools[tool.get_name()] = tool

    def get_tool(self, name: str) -> Optional[UniversalTool]:
        """Get tool by name."""
        return self.tools.get(name)

    def get_all_tools(self) -> List[UniversalTool]:
        """Get all registered tools."""
        return list(self.tools.values())

    # Framework exports
    def to_openai_tools(self) -> List[dict]:
        """Export all tools in OpenAI format."""
        return [tool.to_openai() for tool in self.tools.values()]

    def to_anthropic_tools(self) -> List[dict]:
        """Export all tools in Anthropic format."""
        return [tool.to_anthropic() for tool in self.tools.values()]

    def to_langchain_tools(self) -> List:
        """Export all tools in LangChain format."""
        return [tool.to_langchain() for tool in self.tools.values()]

    # Execution
    def execute_tool(self, name: str, **kwargs) -> dict:
        """Execute a tool by name."""
        tool = self.get_tool(name)
        if not tool:
            return {
                "success": False,
                "error": f"Tool '{name}' not found"
            }

        return tool.execute(**kwargs)


# ============================================================================
# COMPLETE EXAMPLE: MULTI-FRAMEWORK TOOL
# ============================================================================

# Define schemas
class WeatherInput(BaseModel):
    """Input for weather tool."""
    location: str = Field(..., description="City name or coordinates")
    units: str = Field("celsius", description="Temperature units (celsius/fahrenheit)")


class WeatherOutput(BaseModel):
    """Output from weather tool."""
    location: str
    temperature: float
    conditions: str
    humidity: float


# Define function
def get_weather(input: WeatherInput) -> dict:
    """Get current weather for a location."""
    # Fake implementation
    return {
        "location": input.location,
        "temperature": 15.0 if input.units == "celsius" else 59.0,
        "conditions": "cloudy",
        "humidity": 65.0
    }


# Create universal tool
weather_tool = UniversalTool(
    name="get_weather",
    description="Get current weather for a location. Use when user asks about weather or temperature.",
    input_schema=WeatherInput,
    output_schema=WeatherOutput,
    func=get_weather
)


# ============================================================================
# USAGE WITH DIFFERENT FRAMEWORKS
# ============================================================================

def demo_openai():
    """Demo: Using tool with OpenAI."""
    print("=== OpenAI Format ===")

    # Get schema
    schema = weather_tool.to_openai()
    print("Schema:", schema)

    # Use with OpenAI (pseudo-code)
    """
    import openai

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "What's the weather in Paris?"}],
        tools=[schema]
    )

    # Parse response
    func_name, args = OpenAIAdapter.parse_function_call(response)

    # Execute tool
    result = weather_tool.execute(**args)

    # Format result
    tool_message = OpenAIAdapter.format_tool_response(func_name, result)
    """


def demo_anthropic():
    """Demo: Using tool with Anthropic."""
    print("\n=== Anthropic Format ===")

    # Get schema
    schema = weather_tool.to_anthropic()
    print("Schema:", schema)

    # Use with Anthropic (pseudo-code)
    """
    import anthropic

    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-opus-5-5",
        messages=[{"role": "user", "content": "What's the weather in Paris?"}],
        tools=[schema]
    )

    # Parse response
    tool_name, tool_input = AnthropicAdapter.parse_tool_use(response)

    # Execute tool
    result = weather_tool.execute(**tool_input)

    # Format result
    tool_result = AnthropicAdapter.format_tool_result(
        response.content[0].id,
        result
    )
    """


def demo_langchain():
    """Demo: Using tool with LangChain."""
    print("\n=== LangChain Format ===")

    # Convert to LangChain tool
    lc_tool = weather_tool.to_langchain()
    print("Tool:", lc_tool)

    # Use with LangChain agent (pseudo-code, LangChain 0.x style).
    # In LangChain 1.x, AgentExecutor/create_openai_functions_agent live in
    # langchain-classic; new code uses `from langchain.agents import create_agent`.
    """
    from langchain.agents import AgentExecutor, create_openai_functions_agent
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model="gpt-4")

    agent = create_openai_functions_agent(
        llm=llm,
        tools=[lc_tool],
        prompt=prompt
    )

    executor = AgentExecutor(agent=agent, tools=[lc_tool])
    result = executor.invoke({"input": "What's the weather in Paris?"})
    """


def demo_registry():
    """Demo: Tool registry with multiple frameworks."""
    print("\n=== Tool Registry Demo ===")

    # Create registry
    registry = ToolRegistry()

    # Register tools
    registry.register(weather_tool)

    # Add more tools...
    # registry.register(calculator_tool)
    # registry.register(search_tool)

    # Export for different frameworks
    openai_tools = registry.to_openai_tools()
    anthropic_tools = registry.to_anthropic_tools()
    langchain_tools = registry.to_langchain_tools()

    print(f"Registered {len(registry.get_all_tools())} tools")
    print(f"OpenAI format: {len(openai_tools)} tools")
    print(f"Anthropic format: {len(anthropic_tools)} tools")
    print(f"LangChain format: {len(langchain_tools)} tools")

    # Execute tool
    result = registry.execute_tool("get_weather", location="Paris", units="celsius")
    print(f"Execution result: {result}")


# ============================================================================
# ADVANCED: STREAMING SUPPORT
# ============================================================================

class StreamingTool(UniversalTool):
    """Tool with streaming support for long-running operations."""

    def execute_stream(self, **kwargs):
        """Execute tool and yield results progressively."""
        # Validate input
        validated_input = self.input_schema(**kwargs)

        # Execute with streaming
        try:
            for chunk in self.func(validated_input, stream=True):
                yield {
                    "success": True,
                    "chunk": chunk,
                    "done": False
                }

            # Final message
            yield {
                "success": True,
                "chunk": None,
                "done": True
            }

        except Exception as e:
            yield {
                "success": False,
                "error": str(e),
                "done": True
            }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("Framework Adapters Demo\n")

    demo_openai()
    demo_anthropic()
    demo_langchain()
    demo_registry()

    print("\n✓ All frameworks supported!")

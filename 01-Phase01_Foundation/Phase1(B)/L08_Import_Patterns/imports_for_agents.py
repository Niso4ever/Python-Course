"""
TEMPLATE: Agent Imports — LangChain + CrewAI
=============================================
Use: Building agents with tools, or multi-agent systems

pip install:
  LangChain agents:  pip install langchain langchain-classic langchain-anthropic python-dotenv
  (New LangChain 1.x code uses `from langchain.agents import create_agent` instead of
   create_react_agent + AgentExecutor; the blocks below keep the classic shape.)
  CrewAI:            pip install crewai crewai-tools python-dotenv

COPY the block that matches your use case.
"""

# ═══════════════════════════════════════════════════════════
# BLOCK 1: LangChain ReAct Agent (Basic)
# ═══════════════════════════════════════════════════════════
# Use when: single agent with 1-3 tools, ReAct reasoning loop

from langchain_classic.agents import AgentExecutor, create_react_agent  # LangChain 1.x; 0.x code wrote `from langchain.agents import ...`
from langchain_core.tools import tool
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Define a tool with the @tool decorator:
# @tool
# def web_search(query: str) -> str:
#     """Search the web for information."""
#     return search_results(query)   # your search function
#
# @tool
# def calculator(expression: str) -> str:
#     """Evaluate a math expression."""
#     return str(eval(expression))
#
# Setup:
# llm     = ChatAnthropic(model="claude-sonnet-5-5")
# tools   = [web_search, calculator]
# prompt  = PromptTemplate.from_template("Answer: {input}\n{agent_scratchpad}")
# agent   = create_react_agent(llm, tools, prompt)
# runner  = AgentExecutor(agent=agent, tools=tools, verbose=True)
# result  = runner.invoke({"input": "What is 42 * 7?"})


# ═══════════════════════════════════════════════════════════
# BLOCK 2: LangChain Agent with Built-in Tools
# ═══════════════════════════════════════════════════════════
# Use when: using pre-built tools (Wikipedia, DuckDuckGo, etc.)
# pip install langchain-community duckduckgo-search wikipedia

from langchain_classic.agents import AgentExecutor, create_react_agent  # LangChain 1.x; 0.x code wrote `from langchain.agents import ...`
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Setup:
# search_tool = DuckDuckGoSearchRun()
# wiki_tool   = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
# tools       = [search_tool, wiki_tool]
# llm         = ChatAnthropic(model="claude-sonnet-5-5")
# prompt      = PromptTemplate.from_template("Answer: {input}\n{agent_scratchpad}")
# agent       = create_react_agent(llm, tools, prompt)
# runner      = AgentExecutor(agent=agent, tools=tools)
# result      = runner.invoke({"input": "Who invented the telephone?"})


# ═══════════════════════════════════════════════════════════
# BLOCK 3: CrewAI — Minimal Multi-Agent
# ═══════════════════════════════════════════════════════════
# Use when: 2+ agents with distinct roles collaborating on a task

from crewai import Agent, Task, Crew
from dotenv import load_dotenv

load_dotenv()

# Define agents:
# researcher = Agent(
#     role="Research Analyst",
#     goal="Find accurate, up-to-date information on any topic",
#     backstory="Expert researcher with access to web search",
#     llm="claude-sonnet-5-5",
#     verbose=True
# )
#
# writer = Agent(
#     role="Content Writer",
#     goal="Write clear, structured summaries of research findings",
#     backstory="Experienced technical writer",
#     llm="claude-sonnet-5-5"
# )
#
# Define tasks:
# research_task = Task(
#     description="Research the topic: {topic}",
#     expected_output="A detailed summary with key facts",
#     agent=researcher
# )
#
# write_task = Task(
#     description="Write a 3-paragraph summary of the research",
#     expected_output="A clean, structured article",
#     agent=writer
# )
#
# Run:
# crew   = Crew(agents=[researcher, writer], tasks=[research_task, write_task])
# result = crew.kickoff(inputs={"topic": "Retrieval-Augmented Generation"})


# ═══════════════════════════════════════════════════════════
# BLOCK 4: CrewAI with Built-in Tools
# ═══════════════════════════════════════════════════════════
# Use when: CrewAI agents need web search, file reading, etc.
# pip install crewai crewai-tools

from crewai import Agent, Task, Crew
from crewai_tools import (
    SerperDevTool,        # Google search (needs SERPER_API_KEY)
    WebsiteSearchTool,    # Search a specific website
    FileReadTool,         # Read local files
    DirectoryReadTool,    # Read a directory of files
)
from dotenv import load_dotenv

load_dotenv()

# Setup with tools:
# search_tool = SerperDevTool()   # requires SERPER_API_KEY in .env
# file_tool   = FileReadTool()
#
# researcher = Agent(
#     role="Researcher",
#     goal="Find and summarize information",
#     tools=[search_tool],         # Tools assigned per agent
#     llm="claude-sonnet-5-5"
# )


# ═══════════════════════════════════════════════════════════
# QUICK REFERENCE: Agent Component Imports
# ═══════════════════════════════════════════════════════════
"""
COMPONENT             IMPORT                                              WHAT IT DOES
──────────────────    ──────────────────────────────────────────────      ──────────────────
Agent Builder (1.x)   from langchain.agents import create_agent           Builds and runs an agent
ReAct Agent (classic) from langchain_classic.agents import create_react_agent  0.x-style builder
Agent Runner (classic) from langchain_classic.agents import AgentExecutor   0.x-style loop runner
Tool Decorator        from langchain_core.tools import tool               Marks a function as a tool
LLM (Claude)          from langchain_anthropic import ChatAnthropic       The thinking brain
Prompt Template       from langchain_core.prompts import PromptTemplate   Formats agent prompt
Web Search            from langchain_community.tools import DuckDuckGoSearchRun  Search tool
Wikipedia             from langchain_community.tools import WikipediaQueryRun    Wiki lookup
CrewAI Agent          from crewai import Agent                            Multi-agent participant
CrewAI Task           from crewai import Task                             What the agent does
CrewAI Crew           from crewai import Crew                             Orchestrates agents
CrewAI Search         from crewai_tools import SerperDevTool              Google search for CrewAI
"""


# ═══════════════════════════════════════════════════════════
# DEMO (prints reference — no installs needed)
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print("Agent Import Blocks — Reference")
    print("=" * 60)
    print()
    print("BLOCK 1: LangChain ReAct Agent")
    print("  create_react_agent + AgentExecutor")
    print("  @tool decorator for custom functions")
    print()
    print("BLOCK 2: LangChain with Built-in Tools")
    print("  DuckDuckGoSearchRun, WikipediaQueryRun")
    print("  Drop-in tools, no API key needed")
    print()
    print("BLOCK 3: CrewAI Minimal")
    print("  Agent + Task + Crew → crew.kickoff()")
    print("  Multiple agents with distinct roles")
    print()
    print("BLOCK 4: CrewAI with Tools")
    print("  SerperDevTool (Google search)")
    print("  FileReadTool, WebsiteSearchTool")

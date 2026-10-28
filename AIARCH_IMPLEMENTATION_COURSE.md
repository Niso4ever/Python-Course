# AIarch Implementation Course
## "From Architect to Builder: Hands-On Agentic AI Development"

**Course Type:** Step 2 - Implementation Layer
**Prerequisite:** AIarch Curriculum (8 weeks) + Vibe Coder's Field Manual
**Duration:** 6 weeks
**Philosophy:** You designed it in AIarch. Now build it, deploy it, and ship it.

> **Status note (2026-10-28):** This document is a plan, not a folder in the tree. Parts of it now exist as lessons: async agents (`06-Phase06_Async`), evaluation (`07-Phase07_Evals`, cf. Week 3), trace-based debugging (`08-Phase08_Debugging`, cf. Week 6 observability), four end-to-end projects (`09-Phase09_End_to_End_Projects`), and native-loop plus SDK agents (Phase 4 L02 and Ph4-L08, Phase 5). The weekly projects below (20 tools, LangGraph, deployment, Postgres/Redis memory) have not been built.

---

## THE CORE THESIS

```
AIarch (Step 1)  →  You learn to THINK like an architect
                    - What to build
                    - Why to build it this way
                    - How to design contracts and schemas
                    - How to specify intent to AI

Implementation   →  You learn to SHIP like an engineer
(Step 2)            - How to build production systems
                    - How to test, evaluate, and iterate
                    - How to deploy and monitor
                    - How to integrate frameworks when needed
```

**The Relationship:**
- **AIarch = The Blueprint** (schemas, contracts, architecture decisions)
- **Implementation = The Construction** (working systems, deployed agents, production code)

**The Shift:**
- AIarch: "Here's how to design a tool schema that an LLM can understand"
- Implementation: "Here's how to build a working agent that uses 10 tools and doesn't break"

---

## THE IDENTITY STATEMENT

```
In AIarch, you became an architect who designs systems.

In Implementation, you become a builder who ships systems.

You still think architecturally (that never goes away).
You still use vibe coding (that's your superpower).

But now you're building REAL, DEPLOYED, PRODUCTION-READY AGENTS
that solve REAL PROBLEMS for REAL USERS.

Your currency is not just architectural judgment.
It's working code that runs 24/7 without you watching it.
```

---

## WHAT THIS COURSE ADDS TO AIARCH

| AIarch Teaches | Implementation Adds |
|----------------|---------------------|
| Design tool schemas | Build 20 production tools and debug when they fail |
| Understand ReAct pattern | Implement ReAct in 3 frameworks and compare trade-offs |
| Specify intent declaratively | Build complete systems from specs in single sessions |
| Design memory architecture | Implement persistent memory with SQL/Redis and handle edge cases |
| Evaluate quality conceptually | Build evaluation pipelines with metrics, datasets, and CI/CD |
| Plan multi-agent systems | Deploy multi-agent systems to production and monitor them |
| Read code fluently | Debug production failures at 3am |
| Think about guardrails | Implement safety layers that catch every edge case |

---

## THE 6-WEEK STRUCTURE

```
WEEK 1: Building Your Tool Arsenal
  → Implement 20 production-ready tools
  → Test, debug, and document each one
  → Build tool registry system

WEEK 2: Agents in Production
  → Build 5 complete agents in 3 frameworks (OpenAI SDK, LangGraph, native)
  → Compare performance, cost, reliability
  → Choose frameworks based on requirements

WEEK 3: Quality & Evaluation Systems
  → Build evaluation datasets
  → Implement automated testing
  → Create quality dashboards
  → Set up CI/CD for agents

WEEK 4: State, Memory & Persistence
  → Implement conversation memory (SQLite, Postgres, Redis)
  → Build context compression systems
  → Handle long-running agent sessions
  → Recover from failures gracefully

WEEK 5: Multi-Agent Orchestration
  → Build 3 multi-agent systems (parallel, sequential, hierarchical)
  → Implement agent handoffs
  → Build agent communication protocols
  → Handle coordination failures

WEEK 6: Production Deployment & Monitoring
  → Deploy agents to production (cloud, serverless, containers)
  → Implement observability (logging, tracing, metrics)
  → Build alerting and incident response
  → Create user-facing interfaces
```

---

## DETAILED WEEK-BY-WEEK BREAKDOWN

---

### **WEEK 1: BUILDING YOUR TOOL ARSENAL**

**AIarch Foundation:**
- L05: Functions as Tools
- L13: Tool Use Pattern
- Phase 3 L01-L02: Type Hints + Pydantic

**What You'll Build:**

#### Project 1.1: The Essential 20 Tools
Build and test these production-ready tools:

**Search & Retrieval:**
1. Web search (Google/Serper/Brave API)
2. Wikipedia lookup
3. ArXiv paper search
4. News search (current events)
5. Company information (Clearbit/Hunter.io)

**Data & Analysis:**
6. SQL database query
7. CSV file analysis
8. JSON data extraction
9. Statistical analysis (mean, median, trends)
10. Chart generation (matplotlib/plotly)

**Communication:**
11. Email sender (SendGrid/Resend)
12. Slack message poster
13. SMS sender (Twilio)
14. Push notification (Pushover/OneSignal)

**File Operations:**
15. PDF text extraction
16. Image analysis (OCR, description)
17. File download/upload (S3/GCS)
18. Markdown to HTML converter

**Utilities:**
19. Date/time calculator
20. Currency converter (live rates)

**Deliverables:**
- ✅ All 20 tools implemented with Pydantic schemas
- ✅ Test suite for each tool (happy path + edge cases)
- ✅ Tool registry system (discover available tools)
- ✅ Documentation for each tool (when to use, limitations)
- ✅ Error handling patterns (retries, fallbacks, graceful degradation)

**Vibe Coding Practice:**
- Use Template Injection (Field Manual) to match AIarch patterns
- Operate at Specification Level 3 (contracts)
- Use Constraint Sandwich for each tool build

**Learning Outcomes:**
- ✅ You can build production tools, not just design them
- ✅ You understand API integration patterns
- ✅ You know how to handle failures gracefully
- ✅ You have a reusable tool library for all future projects

---

### **WEEK 2: AGENTS IN PRODUCTION**

**AIarch Foundation:**
- L15: ReAct Reasoning Pattern
- L17: Multi-Agent Patterns
- L14: Memory Architecture

**What You'll Build:**

#### Project 2.1: The Same Agent, Three Ways
Build a "Research Assistant" agent using:
1. **Native Python** (manual ReAct loop, no framework)
2. **OpenAI Agents SDK** (using Week 1 tools)
3. **LangGraph** (state machine approach)

**Agent Specification:**
```
AGENT: Research Assistant
TOOLS: web_search, wikipedia, arxiv_search, email_sender
CAPABILITY: Research a topic, synthesize findings, email summary
MEMORY: Remember conversation history across sessions
QUALITY GATE: Fact-check claims before including in summary
```

#### Project 2.2: Framework Comparison Matrix
Create comparison based on:
- **Development speed**: Time to build
- **Debugging ease**: How easy to find issues
- **Performance**: Latency, token usage
- **Cost**: API calls made
- **Flexibility**: Can you customize behavior?
- **Observability**: Can you see what's happening?

#### Project 2.3: Framework Decision Guide
Create your own guide:
```
Use Native Python when:
- Maximum control needed
- Custom orchestration logic
- No framework dependencies desired

Use OpenAI Agents SDK when:
- Rapid prototyping
- OpenAI-centric stack
- Built-in tracing valuable

Use LangGraph when:
- Complex state management
- Need graph visualization
- SQL persistence required
```

**Deliverables:**
- ✅ 3 working implementations of same agent
- ✅ Performance comparison report
- ✅ Framework decision guide
- ✅ "When I Got Stuck" debugging diary (learning from failures)

**Vibe Coding Practice:**
- Build all 3 in parallel (one session per framework)
- Use Session Architecture (Orient → Build → Checkpoint → Close)
- Document architectural decisions (ARCHITECTURE.md)

**Learning Outcomes:**
- ✅ You can choose frameworks based on requirements, not hype
- ✅ You understand trade-offs between control and convenience
- ✅ You've debugged real framework-specific issues
- ✅ You can defend architectural decisions with evidence

---

### **WEEK 3: QUALITY & EVALUATION SYSTEMS**

**AIarch Foundation:**
- L03: Logic Gates
- L16: DSPy Signature Paradigm
- Vibe Coder's Field Manual: Evaluation Mode

**What You'll Build:**

#### Project 3.1: Evaluation Dataset Builder
Build a system to create evaluation datasets:

```python
# Example dataset structure
class EvaluationCase(BaseModel):
    input: str
    expected_output: str
    evaluation_criteria: list[str]
    difficulty: Literal["easy", "medium", "hard"]
    tags: list[str]

# Example cases
cases = [
    EvaluationCase(
        input="What is the capital of France?",
        expected_output="Paris",
        evaluation_criteria=["factual_accuracy", "conciseness"],
        difficulty="easy",
        tags=["geography", "factual"]
    ),
    EvaluationCase(
        input="Compare React and Vue.js for a large enterprise application",
        expected_output="[detailed comparison with trade-offs]",
        evaluation_criteria=["completeness", "balance", "depth", "practical_advice"],
        difficulty="hard",
        tags=["technical", "comparison"]
    )
]
```

**Build:**
- Dataset of 100 test cases for your Research Assistant
- Automated dataset generation (use LLM to create edge cases)
- Dataset versioning (track changes over time)

#### Project 3.2: Automated Evaluation Pipeline
Build multi-level evaluation:

**Level 1: Deterministic Checks**
```python
def eval_length(output: str, max_length: int) -> bool:
    return len(output) <= max_length

def eval_contains_keywords(output: str, keywords: list[str]) -> bool:
    return all(kw in output.lower() for kw in keywords)
```

**Level 2: LLM-as-Judge**
```python
class JudgeEvaluation(BaseModel):
    score: float  # 0.0 to 1.0
    criteria_scores: dict[str, float]
    reasoning: str
    issues: list[str]

def llm_judge(output: str, criteria: list[str]) -> JudgeEvaluation:
    # Use LLM to evaluate output against criteria
    pass
```

**Level 3: Human Review**
```python
class HumanReview(BaseModel):
    approved: bool
    feedback: str
    suggested_improvements: list[str]
```

#### Project 3.3: Quality Dashboard
Build a dashboard showing:
- Pass rate over time (% of tests passing)
- Performance by difficulty (easy vs. hard cases)
- Cost per evaluation (token usage)
- Failure patterns (what breaks most often)
- Regression detection (did new version break old tests)

#### Project 3.4: CI/CD Integration
Set up automated testing:
```yaml
# .github/workflows/test-agent.yml
name: Test Agent Quality
on: [push, pull_request]
jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run evaluation suite
        run: python evaluate_agent.py
      - name: Check pass rate
        run: |
          if [ $(jq .pass_rate results.json) < 0.8 ]; then
            echo "Pass rate below 80%!"
            exit 1
          fi
```

**Deliverables:**
- ✅ 100-case evaluation dataset
- ✅ Multi-level evaluation pipeline
- ✅ Quality dashboard (Gradio/Streamlit)
- ✅ CI/CD integration with pass/fail gates
- ✅ Regression test suite

**Vibe Coding Practice:**
- Use Debugging Mode (Evidence Packages) when tests fail
- Document expected vs. actual for every failure
- Build test cases using Specification Level 4 (test cases)

**Learning Outcomes:**
- ✅ You can measure agent quality objectively
- ✅ You catch regressions before production
- ✅ You understand evaluation trade-offs (cost vs. accuracy)
- ✅ You have evidence for "this agent is better than before"

---

### **WEEK 4: STATE, MEMORY & PERSISTENCE**

**AIarch Foundation:**
- L14: Memory Stack Architecture
- L02: Lists and Collections (conversation history)
- Phase 3 L02: Pydantic (data persistence)

**What You'll Build:**

#### Project 4.1: Memory Backend Implementations
Implement conversation memory using 3 backends:

**1. SQLite (local development)**
```python
class SQLiteMemory:
    def save_message(self, session_id: str, message: Message)
    def get_history(self, session_id: str, limit: int) -> list[Message]
    def clear_session(self, session_id: str)
    def compress_old_messages(self, session_id: str, keep_recent: int)
```

**2. PostgreSQL (production-ready)**
```python
class PostgresMemory:
    # Same interface as SQLite
    # + Concurrent session handling
    # + Full-text search on history
    # + Backup/restore capabilities
```

**3. Redis (high-performance)**
```python
class RedisMemory:
    # Same interface
    # + TTL-based expiration
    # + Pub/sub for multi-agent coordination
    # + Distributed locking
```

#### Project 4.2: Context Window Management
Build intelligent memory compression:

```python
class ContextManager:
    def __init__(self, max_tokens: int = 4096):
        self.max_tokens = max_tokens

    def compress_history(self, messages: list[Message]) -> list[Message]:
        """
        Strategies:
        1. Keep first message (system prompt) always
        2. Keep last N messages always
        3. Summarize middle messages
        4. Remove redundant information
        5. Keep important facts (extracted entities, decisions)
        """
        pass

    def extract_key_facts(self, messages: list[Message]) -> list[str]:
        """Extract important information to preserve."""
        pass

    def summarize_range(self, messages: list[Message]) -> str:
        """Summarize a range of messages into one."""
        pass
```

#### Project 4.3: Long-Running Sessions
Handle sessions that last days/weeks:

**Challenges to solve:**
- Token budget exhaustion (conversation grows forever)
- Context drift (agent forgets what it's doing)
- Session resumption (user comes back tomorrow)
- Memory cleanup (delete old sessions)

**Build:**
```python
class LongRunningSession:
    def __init__(self, session_id: str, memory: MemoryBackend):
        self.session_id = session_id
        self.memory = memory
        self.context_manager = ContextManager()

    def add_message(self, message: Message):
        """Add message and trigger compression if needed."""
        self.memory.save_message(self.session_id, message)
        if self.get_token_count() > self.context_manager.max_tokens:
            self.compress()

    def compress(self):
        """Compress old messages to free up token budget."""
        history = self.memory.get_history(self.session_id, limit=1000)
        compressed = self.context_manager.compress_history(history)
        # Save summary, delete old messages
        self.memory.save_summary(self.session_id, summary)
        self.memory.delete_old_messages(self.session_id, before=cutoff_time)

    def resume(self) -> str:
        """Generate a resume prompt for returning users."""
        return f"Welcome back! Last time we discussed: {self.get_summary()}"
```

#### Project 4.4: Failure Recovery
Handle failures gracefully:

```python
class RobustAgent:
    def __init__(self, memory: MemoryBackend):
        self.memory = memory

    def run(self, session_id: str, user_input: str):
        try:
            # Save user input immediately
            self.memory.save_message(session_id, Message(role="user", content=user_input))

            # Process
            response = self.agent.chat(user_input)

            # Save response
            self.memory.save_message(session_id, Message(role="assistant", content=response))

            return response

        except Exception as e:
            # Log failure
            self.memory.save_error(session_id, error=str(e), timestamp=now())

            # Attempt recovery
            if self.is_recoverable(e):
                return self.retry_with_fallback(session_id, user_input)
            else:
                return self.graceful_error_message(e)

    def retry_with_fallback(self, session_id: str, user_input: str):
        """Try simpler approach on failure."""
        # Example: Use cheaper model, disable some tools, simplify prompt
        pass
```

**Deliverables:**
- ✅ 3 memory backend implementations (SQLite, Postgres, Redis)
- ✅ Context compression system with multiple strategies
- ✅ Long-running session handler (works for 30-day conversations)
- ✅ Failure recovery system (retry, fallback, graceful degradation)
- ✅ Memory cleanup utilities (delete old sessions, export conversations)
- ✅ Performance benchmarks (which backend for which use case)

**Vibe Coding Practice:**
- Use Integration Mode (Assembly Spec) to connect components
- Build with contracts (specify interfaces clearly)
- Test edge cases (what happens when Postgres is down?)

**Learning Outcomes:**
- ✅ You can build production-grade memory systems
- ✅ You understand persistence trade-offs (SQLite vs. Redis)
- ✅ You can handle multi-day conversations without breaking
- ✅ You recover gracefully from failures

---

### **WEEK 5: MULTI-AGENT ORCHESTRATION**

**AIarch Foundation:**
- L17: Multi-Agent Patterns
- Tools vs. Handoffs (from extraction doc)
- Agent as Tool pattern (composition)

**What You'll Build:**

#### Project 5.1: Parallel Research Team
Build a system where multiple agents work simultaneously:

```python
"""
USER REQUEST: "Research electric vehicles and create a market report"

ORCHESTRATION:
- Market Analyst Agent → researches market size, trends, growth
- Technology Agent → researches battery tech, charging infrastructure
- Competitor Agent → researches Tesla, BYD, GM, Rivian
- Regulatory Agent → researches policies, incentives, regulations

All run in PARALLEL → Results merged → Report generated
"""

class ParallelResearchTeam:
    def __init__(self):
        self.market_agent = Agent(name="market", tools=[...])
        self.tech_agent = Agent(name="tech", tools=[...])
        self.competitor_agent = Agent(name="competitor", tools=[...])
        self.regulatory_agent = Agent(name="regulatory", tools=[...])
        self.report_writer = Agent(name="writer", tools=[...])

    async def research(self, topic: str) -> str:
        # Run all agents in parallel
        results = await asyncio.gather(
            self.market_agent.run(f"Research {topic} market"),
            self.tech_agent.run(f"Research {topic} technology"),
            self.competitor_agent.run(f"Research {topic} competitors"),
            self.regulatory_agent.run(f"Research {topic} regulations"),
        )

        # Merge results
        combined = self.merge_research(results)

        # Generate final report
        report = await self.report_writer.run(
            f"Write a comprehensive report on {topic} using this research:\n{combined}"
        )

        return report
```

#### Project 5.2: Sequential Pipeline
Build an assembly-line agent system:

```python
"""
USER REQUEST: "Create a blog post about AI agents"

PIPELINE:
1. Research Agent → gathers information
2. Outline Agent → creates structure
3. Writer Agent → writes first draft
4. Editor Agent → improves clarity, fixes grammar
5. SEO Agent → optimizes for search engines
6. Publisher Agent → formats and publishes

Each agent receives OUTPUT from previous agent as INPUT
"""

class ContentPipeline:
    def create_blog_post(self, topic: str) -> PublishedPost:
        # Stage 1: Research
        research = self.research_agent.run(topic)

        # Stage 2: Outline
        outline = self.outline_agent.run(research)

        # Stage 3: Write
        draft = self.writer_agent.run(outline)

        # Stage 4: Edit
        edited = self.editor_agent.run(draft)

        # Stage 5: SEO
        optimized = self.seo_agent.run(edited)

        # Stage 6: Publish
        published = self.publisher_agent.run(optimized)

        return published
```

#### Project 5.3: Hierarchical Manager-Worker System
Build a manager that delegates to specialist workers:

```python
"""
USER REQUEST: "Plan my wedding"

HIERARCHY:
                    [Wedding Planner Manager]
                            |
        +-------------------+-------------------+
        |                   |                   |
    [Venue Agent]     [Catering Agent]    [Entertainment Agent]
        |
    [Manager calls on specialists based on task]
"""

class WeddingPlannerSystem:
    def __init__(self):
        # Manager agent with access to all specialists
        self.manager = Agent(
            name="Wedding Planner",
            tools=[
                self.venue_agent.as_tool(),
                self.catering_agent.as_tool(),
                self.entertainment_agent.as_tool(),
                self.photography_agent.as_tool(),
                self.flowers_agent.as_tool(),
            ],
            instructions="You are a wedding planner who delegates to specialists."
        )

        # Specialist agents (workers)
        self.venue_agent = Agent(name="Venue", tools=[venue_search, booking])
        self.catering_agent = Agent(name="Catering", tools=[menu_design, vendor_search])
        # ... etc.

    def plan_wedding(self, requirements: WeddingRequirements) -> WeddingPlan:
        """Manager decides which specialists to call and in what order."""
        return self.manager.run(requirements)
```

#### Project 5.4: Conditional Routing (Intent-Based)
Build a router that sends requests to the right specialist:

```python
"""
USER REQUEST: [could be anything]

ROUTER:
- Analyzes intent
- Routes to appropriate specialist
- Returns specialist's response

SPECIALISTS:
- Customer Support Agent (complaints, questions)
- Technical Support Agent (bugs, errors)
- Sales Agent (pricing, features)
- Billing Agent (invoices, payments)
"""

class CustomerServiceRouter:
    def __init__(self):
        self.router = Agent(
            name="Router",
            instructions="Analyze the user's request and route to the right specialist.",
            tools=[
                self.support_agent.as_tool(),
                self.tech_agent.as_tool(),
                self.sales_agent.as_tool(),
                self.billing_agent.as_tool(),
            ]
        )

    def handle_request(self, user_request: str) -> str:
        """Router automatically picks the right agent."""
        return self.router.run(user_request)
```

#### Project 5.5: Agent Communication Protocols
Build systems for agents to communicate:

**Pattern A: Shared Memory (Blackboard)**
```python
class Blackboard:
    """Shared state that all agents can read/write."""
    def __init__(self):
        self.facts = {}
        self.tasks = Queue()
        self.results = {}

    def post_fact(self, agent_name: str, fact: str):
        self.facts[f"{agent_name}:{timestamp}"] = fact

    def read_all_facts(self) -> list[str]:
        return list(self.facts.values())
```

**Pattern B: Message Passing**
```python
class MessageBus:
    """Agents send messages to each other."""
    async def send(self, from_agent: str, to_agent: str, message: str):
        await self.queues[to_agent].put(Message(from_agent, message))

    async def receive(self, agent_name: str) -> Message:
        return await self.queues[agent_name].get()
```

**Pattern C: Handoffs (Control Transfer)**
```python
# Agent A starts, then hands off to Agent B
result = agent_a.run(input)
if result.needs_specialist:
    final_result = agent_b.run(result.context)
else:
    final_result = result
```

**Deliverables:**
- ✅ 4 multi-agent orchestration patterns implemented
- ✅ Performance comparison (parallel vs. sequential vs. hierarchical)
- ✅ Communication protocol implementations (3 patterns)
- ✅ Failure handling (what if one agent fails in the pipeline?)
- ✅ Coordination debugging tools (visualize agent interactions)
- ✅ Decision guide: "When to use which pattern"

**Vibe Coding Practice:**
- Use Exploration Mode (Scaffold Requests) to design architectures
- Use Integration Mode to wire agents together
- Document coordination logic clearly

**Learning Outcomes:**
- ✅ You can build complex multi-agent systems
- ✅ You understand coordination patterns (parallel, sequential, hierarchical)
- ✅ You can debug coordination failures
- ✅ You know when to use which orchestration pattern

---

### **WEEK 6: PRODUCTION DEPLOYMENT & MONITORING**

**AIarch Foundation:**
- All Tiers (applying everything learned)
- Vibe Coder's Field Manual (full workflow)

**What You'll Build:**

#### Project 6.1: Cloud Deployment (3 Platforms)
Deploy the same agent to:

**1. AWS Lambda (Serverless)**
```python
# Lambda function handler
def lambda_handler(event, context):
    user_input = event['body']
    session_id = event['session_id']

    agent = MyAgent(memory=DynamoDBMemory())
    response = agent.run(session_id, user_input)

    return {
        'statusCode': 200,
        'body': response
    }
```

**2. Google Cloud Run (Containerized)**
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

**3. Fly.io (Long-running)**
```toml
# fly.toml
[env]
  PORT = "8080"

[[services]]
  internal_port = 8080
  protocol = "tcp"
```

**Build comparison matrix:**
- Cold start time
- Cost (per 1M requests)
- Scalability
- Ease of deployment
- Monitoring capabilities

#### Project 6.2: Observability Stack
Implement production monitoring:

**1. Structured Logging**
```python
import structlog

logger = structlog.get_logger()

def agent_run(session_id: str, input: str):
    logger.info(
        "agent_started",
        session_id=session_id,
        input_length=len(input),
        timestamp=now()
    )

    try:
        response = agent.process(input)
        logger.info(
            "agent_completed",
            session_id=session_id,
            output_length=len(response),
            duration=elapsed,
            tokens_used=tokens
        )
        return response
    except Exception as e:
        logger.error(
            "agent_failed",
            session_id=session_id,
            error=str(e),
            traceback=traceback.format_exc()
        )
        raise
```

**2. Distributed Tracing**
```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Set up tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Trace agent execution
with tracer.start_as_current_span("agent_execution") as span:
    span.set_attribute("session_id", session_id)
    span.set_attribute("model", model_name)

    with tracer.start_as_current_span("tool_call"):
        result = tool.execute()

    with tracer.start_as_current_span("response_generation"):
        response = llm.generate()
```

**3. Metrics Collection**
```python
from prometheus_client import Counter, Histogram, Gauge

# Define metrics
agent_requests = Counter('agent_requests_total', 'Total agent requests')
agent_duration = Histogram('agent_duration_seconds', 'Agent execution time')
agent_cost = Counter('agent_cost_dollars', 'Agent cost in dollars')
active_sessions = Gauge('active_sessions', 'Number of active sessions')

# Instrument code
@agent_duration.time()
def run_agent(input: str):
    agent_requests.inc()
    response = agent.process(input)
    agent_cost.inc(calculate_cost(response))
    return response
```

#### Project 6.3: Alerting & Incident Response
Set up automated alerts:

**Alert Rules:**
```yaml
# Prometheus alerts
groups:
  - name: agent_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(agent_errors_total[5m]) > 0.05
        annotations:
          summary: "Agent error rate above 5%"

      - alert: HighCost
        expr: rate(agent_cost_dollars[1h]) > 10
        annotations:
          summary: "Agent cost exceeding $10/hour"

      - alert: SlowResponses
        expr: histogram_quantile(0.95, agent_duration_seconds) > 30
        annotations:
          summary: "95th percentile latency above 30s"
```

**Incident Response Playbook:**
```markdown
# Agent Down Playbook

## Detection
- Alert: "HighErrorRate" triggered
- Dashboard shows spike in errors

## Investigation
1. Check logs: `kubectl logs -f deployment/agent --tail=100`
2. Check traces: Open Jaeger, filter by last 10 minutes
3. Check external dependencies: Is OpenAI API down?

## Mitigation
- If OpenAI down: Switch to fallback provider (Anthropic)
- If database down: Use in-memory cache temporarily
- If bug introduced: Rollback to previous version

## Resolution
- Deploy fix
- Monitor for 30 minutes
- Mark incident resolved
```

#### Project 6.4: User-Facing Interfaces
Build 3 interfaces for your agent:

**1. Web Chat UI (Gradio/Streamlit)**
```python
import gradio as gr

def chat(message, history):
    response = agent.run(session_id, message)
    return response

gr.ChatInterface(chat).launch(
    server_name="0.0.0.0",
    server_port=7860,
    share=True
)
```

**2. REST API (FastAPI)**
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    response = agent.run(request.session_id, request.message)
    return {"response": response}
```

**3. Slack Bot**
```python
from slack_bolt import App

app = App(token=os.environ["SLACK_BOT_TOKEN"])

@app.message(".*")
def handle_message(message, say):
    user_input = message['text']
    session_id = message['user']
    response = agent.run(session_id, user_input)
    say(response)
```

#### Project 6.5: Capstone - Ship a Complete System
Build and deploy a production-ready agent system:

**Requirements:**
- ✅ 10+ production tools
- ✅ Persistent memory (choose backend)
- ✅ Quality evaluation (>80% pass rate on 100-case dataset)
- ✅ Deployed to cloud (choose platform)
- ✅ Observability (logs, traces, metrics)
- ✅ Alerting (error rate, cost, latency)
- ✅ User interface (web, API, or chat)
- ✅ Documentation (architecture, API docs, runbook)
- ✅ Cost analysis ($X per 1000 requests)

**Example Systems to Build:**
- Customer support bot (with ticket creation, escalation)
- Research assistant (with source tracking, citation generation)
- Code review agent (with PR comments, automated fixes)
- Content creation pipeline (research → outline → draft → edit → publish)
- Data analysis agent (SQL queries, chart generation, insights)

**Deliverables:**
- ✅ Deployed, working system (publicly accessible)
- ✅ ARCHITECTURE.md (design decisions, trade-offs)
- ✅ API.md (if REST API)
- ✅ RUNBOOK.md (deployment, monitoring, troubleshooting)
- ✅ Cost analysis spreadsheet
- ✅ Demo video (5 minutes showing system in action)
- ✅ Post-mortem (what went wrong, what you learned)

**Vibe Coding Practice:**
- Use ALL five modes across the project
- Full Session Architecture (Orient → Build → Checkpoint → Close)
- Maintain ARCHITECTURE.md throughout (not just at end)

**Learning Outcomes:**
- ✅ You can deploy production agents
- ✅ You can monitor and debug production issues
- ✅ You understand operational costs
- ✅ You have a portfolio piece to show employers/clients
- ✅ **You can ship complete AI systems, not just demos**

---

## COURSE DELIVERABLES

By the end of 6 weeks, you will have:

### **Code Artifacts:**
1. **Tool Library**: 20+ production-ready tools with tests
2. **Framework Comparisons**: Same agent in 3 frameworks with performance data
3. **Evaluation System**: 100-case dataset + automated testing pipeline
4. **Memory Implementations**: 3 backend implementations (SQLite, Postgres, Redis)
5. **Multi-Agent Systems**: 4 orchestration patterns implemented
6. **Deployed Agent**: Production system with monitoring

### **Documentation:**
1. **Framework Decision Guide**: When to use which framework
2. **Tool Documentation**: Each tool documented (purpose, limitations, examples)
3. **Architecture Docs**: ARCHITECTURE.md for all projects
4. **Runbook**: Deployment and operational procedures
5. **Post-Mortems**: Learning from every failure

### **Skills:**
1. ✅ Build production tools (not just design them)
2. ✅ Choose frameworks based on requirements
3. ✅ Implement quality evaluation systems
4. ✅ Build persistent memory systems
5. ✅ Orchestrate multi-agent systems
6. ✅ Deploy and monitor production agents
7. ✅ Debug production failures
8. ✅ Calculate and optimize costs

---

## HOW THIS INTEGRATES WITH AIARCH

### **The Learning Path:**

```
┌─────────────────────────────────────────────────────────────┐
│                   AIARCH CURRICULUM                         │
│                   (8 weeks - DESIGN)                        │
│                                                             │
│  You learn to THINK like an architect:                      │
│  - Design schemas and contracts                            │
│  - Make architectural decisions                            │
│  - Specify intent declaratively                            │
│  - Understand patterns that survive framework changes      │
│                                                             │
│  Deliverable: Architectural judgment + specification skills │
└─────────────────────────────────────────────────────────────┘
                            ↓
                   YOU ARE HERE
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              IMPLEMENTATION COURSE                          │
│                (6 weeks - BUILD)                            │
│                                                             │
│  You learn to SHIP like an engineer:                        │
│  - Build production systems                                 │
│  - Test, evaluate, iterate                                 │
│  - Deploy and monitor                                      │
│  - Handle failures gracefully                              │
│                                                             │
│  Deliverable: Working, deployed, production-ready agents   │
└─────────────────────────────────────────────────────────────┘
                            ↓
                     YOU EMERGE AS:
                            ↓
┌─────────────────────────────────────────────────────────────┐
│           COMPLETE AI SYSTEMS ARCHITECT                     │
│                                                             │
│  You can:                                                   │
│  ✅ Design systems (AIarch skills)                          │
│  ✅ Build systems (Implementation skills)                   │
│  ✅ Ship systems (Production skills)                        │
│  ✅ Maintain systems (Operational skills)                   │
│                                                             │
│  Your value: $150k-$250k+ annual salary                    │
└─────────────────────────────────────────────────────────────┘
```

### **Week-by-Week Mapping:**

| Implementation Week | AIarch Foundation | What You Apply |
|---------------------|-------------------|----------------|
| Week 1: Tool Arsenal | L05, L13, Phase 3 L01-L02 | Design schemas → Build real tools |
| Week 2: Agents | L15, L17, L14 | Understand ReAct → Implement in 3 frameworks |
| Week 3: Quality | L03, L16 | Design gates → Build evaluation pipelines |
| Week 4: Memory | L14, L02, Phase 3 L02 | Design memory → Implement persistence |
| Week 5: Multi-Agent | L17, Agent patterns | Design orchestration → Build coordination |
| Week 6: Production | All Tiers | Design system → Deploy and monitor |

### **The Vibe Coding Evolution:**

**AIarch Phase:**
- Learn the 5 modes
- Practice Constraint Sandwich
- Master Template Injection
- Build specification skills

**Implementation Phase:**
- **USE all 5 modes** in real projects
- Apply Constraint Sandwich to complex builds
- Inject your AIarch templates into production code
- Operate at Level 3-4 specification (contracts + test cases)

---

## PREREQUISITES

### **Hard Requirements:**
1. ✅ Completed AIarch Curriculum (all 8 weeks)
2. ✅ Read Vibe Coder's Field Manual
3. ✅ Comfortable with Python basics (you can read code)
4. ✅ API keys for OpenAI (or alternative provider)
5. ✅ GitHub account (for version control)

### **Recommended:**
- Cloud account (AWS/GCP/Azure free tier is sufficient)
- Basic terminal/command line comfort
- Text editor with AI assistance (Cursor, VS Code + Copilot)

### **Not Required:**
- ❌ Prior framework experience (you'll learn in Week 2)
- ❌ DevOps expertise (you'll learn in Week 6)
- ❌ Production experience (that's what this course teaches)

---

## SUCCESS METRICS

You've successfully completed this course when:

1. ✅ You have 20+ production tools in your library
2. ✅ You can choose frameworks based on requirements (not hype)
3. ✅ You have evaluation systems for all your agents (>80% pass rate)
4. ✅ You can implement persistent memory with any backend
5. ✅ You've built and deployed multi-agent systems
6. ✅ You have a production agent running 24/7
7. ✅ You can debug production failures using logs/traces/metrics
8. ✅ You understand your agent's cost ($X per 1000 requests)
9. ✅ You have a portfolio with 6 projects + documentation
10. ✅ **You can confidently say "I ship AI systems"**

---

## COST ESTIMATE

### **Platform Costs:**
- **OpenAI API**: $50-100 (if using GPT-4, less with GPT-4o-mini)
- **Alternative**: DeepSeek ($5-10) or Ollama (free, local)
- **Cloud deployment**: $0-20 (free tiers cover most usage)
- **Databases**: $0 (SQLite local, free tiers for Postgres/Redis)
- **Monitoring**: $0 (Prometheus + Grafana are free)

**Total: $0-100 depending on choices**

### **Time Investment:**
- **15-20 hours per week** (2-3 hours daily)
- Total: **90-120 hours** over 6 weeks
- Similar to a part-time course while working full-time

---

## TEACHING APPROACH

### **Structure:**
- **Monday**: New concept introduction (video/text)
- **Tuesday-Thursday**: Hands-on building (you code, I guide)
- **Friday**: Review, debugging, office hours
- **Weekend**: Optional challenge exercises

### **Support:**
- **Weekly office hours** (live Q&A)
- **Discord community** (peer support)
- **Code review** (I review your Week 6 capstone)
- **Debugging help** (when you get stuck)

### **Philosophy:**
- **You learn by building**, not watching
- **Failures are features** (we document every failure)
- **Ship ugly, iterate later** (perfection is the enemy of done)
- **Production experience >> Perfect code** (it's okay if it's messy, as long as it works)

---

## WHAT MAKES THIS DIFFERENT

### **vs. Other Implementation Courses:**

| Other Courses | This Course |
|---------------|-------------|
| "Here's how framework X works" | "Here's when to use framework X vs Y" |
| Build demos | Build production systems |
| Focus on happy path | Focus on failure handling |
| Theory-heavy | Build-heavy (80% coding) |
| No deployment | Deploy everything |
| No monitoring | Full observability stack |
| No cost analysis | Cost-conscious decisions |

### **vs. Agents Course (Edward Donner):**

| Agents Course | This Course |
|---------------|-------------|
| Survey of 5 frameworks | Deep dive into 3 frameworks + native |
| Breadth (touch many topics) | Depth (master production skills) |
| Beginner-friendly | Intermediate (requires AIarch) |
| Framework-focused | Architecture-focused (frameworks are tools) |
| Demo quality | Production quality |
| 6 weeks, all new material | 6 weeks, applying AIarch |

---

## GRADUATION: WHAT COMES NEXT

After completing both AIarch + Implementation:

### **Career Paths:**
1. **AI Engineer** ($120k-180k)
   - Build agents for companies
   - Integrate AI into existing products

2. **AI Architect** ($150k-250k+)
   - Design multi-agent systems
   - Make framework/platform decisions
   - Guide engineering teams

3. **Independent Consultant** ($150-500/hour)
   - Build custom agents for clients
   - Audit existing AI systems
   - Training and workshops

4. **Founder** (uncapped)
   - Build AI-powered products
   - Agent-as-a-service businesses
   - AI tooling companies

### **Continuing Education:**
- **Advanced Topics**: DSPy optimization, fine-tuning, RAG at scale
- **Specialization**: Healthcare AI, Legal AI, Financial AI
- **Leadership**: Managing AI engineering teams

---

## FINAL THOUGHTS

**AIarch taught you to think.**
**Implementation teaches you to ship.**

Together, you become **unstoppable**:
- You design systems with architectural clarity (AIarch)
- You build systems with production rigor (Implementation)
- You ship systems with confidence

**This is the complete package.**

Welcome to Implementation. Let's build.

---

*Course Version: 1.0*
*Last Updated: March 2026*
*Designed to complement: AIarch Curriculum (REVISED_CURRICULUM_MAP.md)*

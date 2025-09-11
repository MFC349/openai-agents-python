# OpenAI Agents SDK

The OpenAI Agents SDK is a lightweight yet powerful framework for building multi-agent workflows. It is provider-agnostic, supporting the OpenAI Responses and Chat Completions APIs, as well as 100+ other LLMs.

**✨ NEW: Legendary AI Training System** - Transform your agents with master-level capabilities across multiple domains of knowledge and expertise. [Learn more](#legendary-ai-training-system)

<img src="https://cdn.openai.com/API/docs/images/orchestration.png" alt="Image of the Agents Tracing UI" style="max-height: 803px;">

> [!NOTE]
> Looking for the JavaScript/TypeScript version? Check out [Agents SDK JS/TS](https://github.com/openai/openai-agents-js).

### Core concepts:

1. [**Agents**](https://openai.github.io/openai-agents-python/agents): LLMs configured with instructions, tools, guardrails, and handoffs
2. [**Legendary Training**](#legendary-ai-training-system): Transform agents with master-level capabilities across multiple domains
3. [**Handoffs**](https://openai.github.io/openai-agents-python/handoffs/): A specialized tool call used by the Agents SDK for transferring control between agents
4. [**Guardrails**](https://openai.github.io/openai-agents-python/guardrails/): Configurable safety checks for input and output validation
5. [**Sessions**](#sessions): Automatic conversation history management across agent runs
6. [**Tracing**](https://openai.github.io/openai-agents-python/tracing/): Built-in tracking of agent runs, allowing you to view, debug and optimize your workflows

Explore the [examples](examples) directory to see the SDK in action, and read our [documentation](https://openai.github.io/openai-agents-python/) for more details.

## Get started

To get started, set up your Python environment (Python 3.9 or newer required), and then install OpenAI Agents SDK package.

### venv

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install openai-agents
```

For voice support, install with the optional `voice` group: `pip install 'openai-agents[voice]'`.

### uv

If you're familiar with [uv](https://docs.astral.sh/uv/), using the tool would be even similar:

```bash
uv init
uv add openai-agents
```

For voice support, install with the optional `voice` group: `uv add 'openai-agents[voice]'`.

## Hello world example

```python
from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="You are a helpful assistant")

result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
print(result.final_output)

# Code within the code,
# Functions calling themselves,
# Infinite loop's dance.
```

(_If running this, ensure you set the `OPENAI_API_KEY` environment variable_)

(_For Jupyter notebook users, see [hello_world_jupyter.ipynb](examples/basic/hello_world_jupyter.ipynb)_)

## Handoffs example

```python
from agents import Agent, Runner
import asyncio

spanish_agent = Agent(
    name="Spanish agent",
    instructions="You only speak Spanish.",
)

english_agent = Agent(
    name="English agent",
    instructions="You only speak English",
)

triage_agent = Agent(
    name="Triage agent",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    handoffs=[spanish_agent, english_agent],
)


async def main():
    result = await Runner.run(triage_agent, input="Hola, ¿cómo estás?")
    print(result.final_output)
    # ¡Hola! Estoy bien, gracias por preguntar. ¿Y tú, cómo estás?


if __name__ == "__main__":
    asyncio.run(main())
```

## Functions example

```python
import asyncio

from agents import Agent, Runner, function_tool


@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny."


agent = Agent(
    name="Hello world",
    instructions="You are a helpful agent.",
    tools=[get_weather],
)


async def main():
    result = await Runner.run(agent, input="What's the weather in Tokyo?")
    print(result.final_output)
    # The weather in Tokyo is sunny.


if __name__ == "__main__":
    asyncio.run(main())
```

## Legendary AI Training System

The **Legendary AI Training System** transforms ordinary agents into masters with exceptional capabilities across multiple domains of human knowledge and expertise.

### Quick Start

```python
from agents import create_legendary_agent, get_training_profile, Runner

# Create a legendary sage agent with master-level capabilities
sage = create_legendary_agent(
    name="The Legendary Sage",
    profile=get_training_profile("legendary_sage")
)

# Ask a complex, multi-faceted question
result = Runner.run_sync(sage, """
    I need to transition my organization to sustainable practices while maintaining 
    profitability and employee satisfaction. The leadership team is divided, 
    stakeholders are resistant to change, and we have limited time and budget. 
    How would you approach this challenge?
""")

print(result.final_output)
# Provides comprehensive analysis with business strategy, change management,
# stakeholder engagement, and ethical considerations
```

### Available Training Profiles

| Profile | Focus | Capabilities |
|---------|-------|-------------|
| **legendary_sage** | Comprehensive | Master-level capabilities across all domains |
| **analytical_master** | Problem-solving | Advanced analytical thinking and reasoning |
| **communication_expert** | Interpersonal | Exceptional communication and collaboration |
| **innovation_genius** | Creative | Revolutionary thinking and innovation |
| **ethical_leader** | Principled | Strong moral reasoning and leadership |
| **balanced_expert** | Well-rounded | Advanced capabilities across key domains |

### Enhance Existing Agents

```python
from agents import Agent, apply_legendary_training

# Start with a basic agent
basic_agent = Agent(name="Assistant", instructions="You are helpful.")

# Apply legendary training
enhanced_agent = apply_legendary_training(
    basic_agent, 
    get_training_profile("communication_expert")
)

# Now the agent has master-level communication skills
```

### Custom Training Profiles

```python
from agents.training import TrainingProfile, TrainingIntensity, TrainingFocus

custom_profile = TrainingProfile(
    name="Research Specialist",
    description="Expert in academic research and knowledge synthesis",
    skill_domains={"problem_solving", "domain_expertise", "communication"},
    intensity=TrainingIntensity.LEGENDARY,
    focus=TrainingFocus.ANALYTICAL,
    custom_instructions="Focus on evidence-based analysis and citation..."
)

researcher = create_legendary_agent("Researcher", custom_profile)
```

### CLI Interface

The SDK includes a powerful CLI for interacting with legendary agents:

```bash
# List available training profiles
agents list-profiles

# Chat with a legendary agent
agents chat communication_expert -m "Explain AI to different audiences"

# Run interactive session
agents chat innovation_genius

# Run demonstrations
agents demo -p analytical_master

# Show system information
agents info
```

### API Server

Deploy a FastAPI server for legendary agents:

```bash
# Install API dependencies
pip install 'openai-agents[api]'

# Run the server
python -m agents.api.server --host 0.0.0.0 --port 8000

# Access API documentation at http://localhost:8000/docs
```

API endpoints:
- `GET /profiles` - List all training profiles
- `POST /chat` - Chat with legendary agents
- `POST /chat/stream` - Stream responses
- `GET /health` - Health check

### Training Capabilities

The legendary training system provides:

- **🧠 Master-level Problem Solving**: Advanced analytical thinking, systems reasoning, and creative solution generation
- **💬 Exceptional Communication**: Audience-adapted explanations, persuasive writing, and interpersonal excellence
- **🔬 Multi-Domain Expertise**: Deep knowledge across sciences, humanities, business, and technology
- **⚖️ Ethical Reasoning**: Sophisticated moral decision-making and principled leadership
- **🎨 Creative Innovation**: Out-of-the-box thinking and breakthrough solution development
- **👑 Leadership Excellence**: Inspirational vision, team development, and collaborative problem-solving

### No API Key? No Problem!

The system automatically uses intelligent stub models when no OpenAI API key is available, providing realistic legendary responses for demonstration and development:

```bash
# Works without API key - uses stub model
unset OPENAI_API_KEY
python -m examples.legendary_training.main
```

### Integration

Legendary training integrates seamlessly with all existing SDK features:
- **Tools**: Enhanced agents use tools more effectively
- **Handoffs**: Improved coordination between agents  
- **Guardrails**: Ethical reasoning enhances safety
- **Tracing**: Monitor legendary capabilities in action
- **Sessions**: Persistent legendary agent conversations

## The agent loop

When you call `Runner.run()`, we run a loop until we get a final output.

1. We call the LLM, using the model and settings on the agent, and the message history.
2. The LLM returns a response, which may include tool calls.
3. If the response has a final output (see below for more on this), we return it and end the loop.
4. If the response has a handoff, we set the agent to the new agent and go back to step 1.
5. We process the tool calls (if any) and append the tool responses messages. Then we go to step 1.

There is a `max_turns` parameter that you can use to limit the number of times the loop executes.

### Final output

Final output is the last thing the agent produces in the loop.

1.  If you set an `output_type` on the agent, the final output is when the LLM returns something of that type. We use [structured outputs](https://platform.openai.com/docs/guides/structured-outputs) for this.
2.  If there's no `output_type` (i.e. plain text responses), then the first LLM response without any tool calls or handoffs is considered as the final output.

As a result, the mental model for the agent loop is:

1. If the current agent has an `output_type`, the loop runs until the agent produces structured output matching that type.
2. If the current agent does not have an `output_type`, the loop runs until the current agent produces a message without any tool calls/handoffs.

## Common agent patterns

The Agents SDK is designed to be highly flexible, allowing you to model a wide range of LLM workflows including deterministic flows, iterative loops, and more. See examples in [`examples/agent_patterns`](examples/agent_patterns).

## Tracing

The Agents SDK automatically traces your agent runs, making it easy to track and debug the behavior of your agents. Tracing is extensible by design, supporting custom spans and a wide variety of external destinations, including [Logfire](https://logfire.pydantic.dev/docs/integrations/llms/openai/#openai-agents), [AgentOps](https://docs.agentops.ai/v1/integrations/agentssdk), [Braintrust](https://braintrust.dev/docs/guides/traces/integrations#openai-agents-sdk), [Scorecard](https://docs.scorecard.io/docs/documentation/features/tracing#openai-agents-sdk-integration), and [Keywords AI](https://docs.keywordsai.co/integration/development-frameworks/openai-agent). For more details about how to customize or disable tracing, see [Tracing](http://openai.github.io/openai-agents-python/tracing), which also includes a larger list of [external tracing processors](http://openai.github.io/openai-agents-python/tracing/#external-tracing-processors-list).

## Long running agents & human-in-the-loop

You can use the Agents SDK [Temporal](https://temporal.io/) integration to run durable, long-running workflows, including human-in-the-loop tasks. View a demo of Temporal and the Agents SDK working in action to complete long-running tasks [in this video](https://www.youtube.com/watch?v=fFBZqzT4DD8), and [view docs here](https://github.com/temporalio/sdk-python/tree/main/temporalio/contrib/openai_agents).

## Sessions

The Agents SDK provides built-in session memory to automatically maintain conversation history across multiple agent runs, eliminating the need to manually handle `.to_input_list()` between turns.

### Quick start

```python
from agents import Agent, Runner, SQLiteSession

# Create agent
agent = Agent(
    name="Assistant",
    instructions="Reply very concisely.",
)

# Create a session instance
session = SQLiteSession("conversation_123")

# First turn
result = await Runner.run(
    agent,
    "What city is the Golden Gate Bridge in?",
    session=session
)
print(result.final_output)  # "San Francisco"

# Second turn - agent automatically remembers previous context
result = await Runner.run(
    agent,
    "What state is it in?",
    session=session
)
print(result.final_output)  # "California"

# Also works with synchronous runner
result = Runner.run_sync(
    agent,
    "What's the population?",
    session=session
)
print(result.final_output)  # "Approximately 39 million"
```

### Session options

-   **No memory** (default): No session memory when session parameter is omitted
-   **`session: Session = DatabaseSession(...)`**: Use a Session instance to manage conversation history

```python
from agents import Agent, Runner, SQLiteSession

# Custom SQLite database file
session = SQLiteSession("user_123", "conversations.db")
agent = Agent(name="Assistant")

# Different session IDs maintain separate conversation histories
result1 = await Runner.run(
    agent,
    "Hello",
    session=session
)
result2 = await Runner.run(
    agent,
    "Hello",
    session=SQLiteSession("user_456", "conversations.db")
)
```

### Custom session implementations

You can implement your own session memory by creating a class that follows the `Session` protocol:

```python
from agents.memory import Session
from typing import List

class MyCustomSession:
    """Custom session implementation following the Session protocol."""

    def __init__(self, session_id: str):
        self.session_id = session_id
        # Your initialization here

    async def get_items(self, limit: int | None = None) -> List[dict]:
        # Retrieve conversation history for the session
        pass

    async def add_items(self, items: List[dict]) -> None:
        # Store new items for the session
        pass

    async def pop_item(self) -> dict | None:
        # Remove and return the most recent item from the session
        pass

    async def clear_session(self) -> None:
        # Clear all items for the session
        pass

# Use your custom session
agent = Agent(name="Assistant")
result = await Runner.run(
    agent,
    "Hello",
    session=MyCustomSession("my_session")
)
```

## Development (only needed if you need to edit the SDK/examples)

0. Ensure you have [`uv`](https://docs.astral.sh/uv/) installed.

```bash
uv --version
```

1. Install dependencies

```bash
make sync
```

2. (After making changes) lint/test

```
make check # run tests linter and typechecker
```

Or to run them individually:

```
make tests  # run tests
make mypy   # run typechecker
make lint   # run linter
make format-check # run style checker
```

## Acknowledgements

We'd like to acknowledge the excellent work of the open-source community, especially:

-   [Pydantic](https://docs.pydantic.dev/latest/) (data validation) and [PydanticAI](https://ai.pydantic.dev/) (advanced agent framework)
-   [LiteLLM](https://github.com/BerriAI/litellm) (unified interface for 100+ LLMs)
-   [MkDocs](https://github.com/squidfunk/mkdocs-material)
-   [Griffe](https://github.com/mkdocstrings/griffe)
-   [uv](https://github.com/astral-sh/uv) and [ruff](https://github.com/astral-sh/ruff)

We're committed to continuing to build the Agents SDK as an open source framework so others in the community can expand on our approach.

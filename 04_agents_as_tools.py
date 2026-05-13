"""
Pattern: Orchestrator-Worker
Specialist sub-agents exposed as tools via .as_tool();
Control returns to the orchestrator after each sub-agent completes.
"""
import asyncio
from agents import Runner, trace
from my_agents.research.research_assistant_orchestrator import research_assistant_orchestrator_agent
from utils import display_token_usage, generate_trace_id


async def main():
    trace_id = generate_trace_id()
    prompt = "Search for what's new in the OpenAI Agents SDK in 2026 and send me a summary email."

    print(f"User prompt: {prompt}")

    with trace(workflow_name="Agents as Tools Demo", trace_id=trace_id):
        result = await Runner.run(
            starting_agent=research_assistant_orchestrator_agent,
            input=prompt
        )

    print(f"Agent response: {result.final_output}")

    display_token_usage(result)


if __name__ == "__main__":
    asyncio.run(main())

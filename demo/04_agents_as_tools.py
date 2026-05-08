"""
Orchestration Worker workflow pattern
"""
import asyncio
from agents import Runner, trace
from demo.my_agents.research_assistant_orchestrator import research_assistant_orchestrator_agent
from demo.utils import display_token_usage


async def main():
    prompt = "Search for what's new in the OpenAI Agents SDK in 2026 and send me a summary email."
    print("=" * 100)
    print(f"User prompt: {prompt}\n")

    with trace("Agents as Tools Demo"):
        result = await Runner.run(research_assistant_orchestrator_agent, prompt, max_turns=6)

    print(f"Agent response:\n{result.final_output}")

    display_token_usage(result)


if __name__ == "__main__":
    asyncio.run(main())

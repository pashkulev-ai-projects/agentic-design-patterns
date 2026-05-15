"""
Concept: Single Agent
An Agent is configured with a name, a system prompt (instructions), and a model.
Runner.run() sends the user prompt to the agent and returns a RunResult.
The agent's reply is available as result.final_output (a plain string when no output_type is set).
"""
import asyncio
from agents import Runner, RunResult
from my_agents import devils_advocate_agent
from utils import display_token_usage


async def main():
    prompt = "AI agents will replace developers"
    result: RunResult = await Runner.run(
        starting_agent=devils_advocate_agent,
        input=prompt
    )

    print("=" * 100)
    print(f"User prompt: {prompt}")
    print(f"Agent response: {result.final_output}")

    display_token_usage(result)


if __name__ == "__main__":
    asyncio.run(main())

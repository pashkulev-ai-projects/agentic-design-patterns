import asyncio
from agents import Runner, RunResult
from my_agents import devils_advocate_agent
from utils import display_token_usage


async def main():
    prompt = "AI agents will replace developers"
    agent_response: RunResult = await Runner.run(starting_agent=devils_advocate_agent, input=prompt)

    print("=" * 100)
    print(f"User prompt: {prompt}")
    print(f"Agent response: {agent_response.final_output}")

    display_token_usage(agent_response)


if __name__ == "__main__":
    asyncio.run(main())

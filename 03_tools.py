import asyncio
from agents import Runner, trace, RunResult
from my_agents import research_assistant_agent
from utils import display_token_usage, generate_trace_id
from dotenv import load_dotenv

load_dotenv(override=True)


async def main():
    trace_id = generate_trace_id()
    prompt = "Search for the latest developments in AI agents and send me a summary email."

    print(f"User prompt: {prompt}")

    with trace(workflow_name="Research Assistant Demo", trace_id=trace_id):
        result: RunResult = await Runner.run(
            starting_agent=research_assistant_agent,
            input=prompt
        )

    print(f"Agent response: {result.final_output}")

    display_token_usage(result)


if __name__ == "__main__":
    asyncio.run(main())

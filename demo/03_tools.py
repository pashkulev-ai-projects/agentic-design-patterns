import asyncio
from agents import Runner, trace, RunResult
from demo.my_agents import research_assistant_agent
from demo.utils import display_token_usage, generate_trace_id
from dotenv import load_dotenv

load_dotenv(override=True)


async def main():
    trace_id = generate_trace_id()
    prompt = "Search for the latest developments in AI agents and send me a summary email."

    print(f"User prompt: {prompt}")

    with trace("Research Assistant Demo", trace_id=trace_id):
        agent_response: RunResult = await Runner.run(research_assistant_agent, prompt)

    print(f"Agent response: {agent_response.final_output}")

    display_token_usage(agent_response)


if __name__ == "__main__":
    asyncio.run(main())

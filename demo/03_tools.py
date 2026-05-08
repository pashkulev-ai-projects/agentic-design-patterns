import asyncio
from agents import Runner, gen_trace_id, trace, RunResult
from demo.my_agents import research_assistant_agent
from demo.utils import display_token_usage
from dotenv import load_dotenv

load_dotenv(override=True)


async def main():
    trace_id = gen_trace_id()
    print(f"Trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n")

    prompt = "Search for the latest developments in AI agents and send me a summary email."
    print("=" * 100)
    print(f"User prompt: {prompt}\n")

    with trace("Research Assistant Demo", trace_id=trace_id):
        agent_response: RunResult = await Runner.run(research_assistant_agent, prompt)

    print(f"Agent response:\n{agent_response.final_output}")

    display_token_usage(agent_response)


if __name__ == "__main__":
    asyncio.run(main())

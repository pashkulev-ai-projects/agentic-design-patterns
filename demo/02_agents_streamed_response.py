import asyncio
from agents import Runner, RawResponsesStreamEvent
from openai.types.responses import ResponseTextDeltaEvent
from demo.my_agents import devils_advocate_agent
from demo.utils import display_token_usage
from dotenv import load_dotenv

load_dotenv(override=True)


async def main():
    prompt = "On-site work is strictly better than remote work."
    agent_response = Runner.run_streamed(devils_advocate_agent, prompt)

    print("=" * 100)
    print(f"User prompt: {prompt}")

    async for event in agent_response.stream_events():
        if isinstance(event, RawResponsesStreamEvent) and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

    display_token_usage(agent_response)


if __name__ == "__main__":
    asyncio.run(main())

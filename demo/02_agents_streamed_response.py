import asyncio
from agents import Agent, Runner, RawResponsesStreamEvent
from dotenv import load_dotenv
from openai.types.responses import ResponseTextDeltaEvent

load_dotenv(override=True)


async def main():
    agent = Agent(
        name="Devil's Advocate",
        instructions="You are a professional sceptic. Whatever the user claims or proposes, find the "
                     "strongest possible counterargument in 2-3 sentences. Be sharp but not rude",
        model="gpt-4o-mini",
    )

    prompt = "On-site work is strictly better than remote work."
    agent_response = Runner.run_streamed(agent, prompt)

    print(f"User prompt: {prompt}")

    async for event in agent_response.stream_events():
        if isinstance(event, RawResponsesStreamEvent) and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

    token_usage = agent_response.context_wrapper.usage
    print(f"Usage: {token_usage.input_tokens} input tokens and {token_usage.output_tokens} output tokens. "
          f"{token_usage.total_tokens} total tokens.")


if __name__ == "__main__":
    asyncio.run(main())

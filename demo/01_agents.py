import asyncio
from agents import Agent, Runner
from dotenv import load_dotenv

load_dotenv(override=True)


async def main():
    agent = Agent(
        name="Devil's Advocate",
        instructions="You are a professional sceptic. Whatever the user claims or proposes, find the "
                     "strongest possible counterargument in 2-3 sentences. Be sharp but not rude",
        model="gpt-4o-mini",
    )

    prompt = "AI agents will replace developers"
    agent_response = await Runner.run(agent, prompt)

    print(f"User prompt: {prompt}")
    print(f"Agent response: {agent_response.final_output}")

    token_usage = agent_response.context_wrapper.usage
    print(f"Usage: {token_usage.input_tokens} input tokens and {token_usage.output_tokens} output tokens. "
          f"{token_usage.total_tokens} total tokens.")


if __name__ == "__main__":
    asyncio.run(main())

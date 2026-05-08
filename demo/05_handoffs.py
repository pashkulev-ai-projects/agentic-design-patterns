"""
Routing Workflow Pattern
"""
import asyncio
from agents import Runner, trace, RunResult
from demo.my_agents import triage_agent
from demo.utils import display_token_usage
from dotenv import load_dotenv

load_dotenv(override=True)
async def main():
    # Switch prompts to demo both routes:
    # prompt = "I was charged twice for my subscription this month. This is unacceptable."
    prompt = "I can't log into my account. I've reset my password three times and it still says invalid credentials."

    print("=" * 100)
    print(f"Customer: {prompt}\n")

    with trace("Handoffs Demo"):
        agent_response: RunResult = await Runner.run(triage_agent, prompt)

    print(f"\nFinal response:\n{agent_response}")

    display_token_usage(agent_response)


if __name__ == "__main__":
    asyncio.run(main())

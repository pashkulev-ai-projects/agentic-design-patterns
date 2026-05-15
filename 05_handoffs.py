"""
Pattern: Routing
Agents listed in handoffs=[...] are the destinations the router can permanently transfer control to.
When the router decides to hand off, the SDK transfers the conversation to the target agent —
the router is no longer involved. The specialist then runs to completion with its own tools and instructions.
Here: router_agent classifies intent on the very first message and immediately hands off
to either billing_agent or tech_support_agent, each equipped with domain-specific mock tools.
"""
import asyncio
from agents import Runner, trace, RunResult
from my_agents import router_agent
from utils import display_token_usage, generate_trace_id
from dotenv import load_dotenv

load_dotenv(override=True)
async def main():
    trace_id = generate_trace_id()
    # Switch prompts to demo both routes:
    prompt = "I was charged twice for my subscription this month. This is unacceptable."
    # prompt = "I can't log into my account. I've reset my password three times and it still says invalid credentials."

    print(f"Customer: {prompt}")

    with trace(workflow_name="Handoffs Demo", trace_id=trace_id):
        agent_response: RunResult = await Runner.run(router_agent, prompt)

    print(f"\nAgent Response: \n{agent_response.final_output}")

    display_token_usage(agent_response)


if __name__ == "__main__":
    asyncio.run(main())

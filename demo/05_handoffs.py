"""
Routing Workflow Pattern
"""
import asyncio
from agents import Runner, trace, RunResult
from demo.my_agents import router_agent
from demo.utils import display_token_usage, generate_trace_id
from dotenv import load_dotenv

load_dotenv(override=True)
async def main():
    trace_id = generate_trace_id()
    # Switch prompts to demo both routes:
    # prompt = "I was charged twice for my subscription this month. This is unacceptable."
    prompt = "I can't log into my account. I've reset my password three times and it still says invalid credentials."

    print(f"Customer: {prompt}")

    with trace(workflow_name="Handoffs Demo", trace_id=trace_id):
        agent_response: RunResult = await Runner.run(router_agent, prompt)

    print(f"\nAgent Response: \n{agent_response.final_output}")

    display_token_usage(agent_response)


if __name__ == "__main__":
    asyncio.run(main())

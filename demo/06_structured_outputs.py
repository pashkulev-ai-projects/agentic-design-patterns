"""
Prompt Chaining Workflow Pattern
"""
import asyncio
from pathlib import Path
from agents import Runner, trace
from demo.my_agents import code_reviewer_agent, frontend_developer_agent, email_sender_agent
from demo.utils import display_token_usage


async def review_file(file_name: str) -> None:
    code_review_dir = Path(__file__).parent / "assets" / "code_review"
    file_path = code_review_dir / file_name
    code = file_path.read_text()

    with trace("Code Review Demo"):
        # Review agent call
        review_agent_response = await Runner.run(code_reviewer_agent, code)
        print(f"Code Review Response type: {type(review_agent_response.final_output)}")
        display_token_usage(review_agent_response)

        # Frontend agent call
        code_review_json = review_agent_response.final_output.model_dump_json()
        frontend_agent_response = await Runner.run(frontend_developer_agent, code_review_json)
        display_token_usage(frontend_agent_response)

        # Send Email Agent call
        email_agent_response = await Runner.run(email_sender_agent, frontend_agent_response.final_output)
        display_token_usage(email_agent_response)

    print("=" * 100)
    print(email_agent_response.final_output)


async def main():
    # Switch files to demo both cases:
    await review_file("CleanBankAccount.java")
    # await review_file("buggy_python.py")


if __name__ == "__main__":
    asyncio.run(main())

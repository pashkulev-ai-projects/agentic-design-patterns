"""
Prompt Chaining Workflow Pattern
"""
import asyncio
from agents import Runner, trace
from demo.my_agents import code_reviewer_agent, frontend_developer_agent, email_sender_agent
from demo.my_agents.code_review.code_reviewer import CodeReview
from demo.utils import display_token_usage, generate_trace_id, get_source_code


async def review_file(file_name: str) -> None:
    trace_id = generate_trace_id()
    code = get_source_code(file_name)

    with trace(workflow_name="Code Review Demo", trace_id=trace_id):
        # Review agent call
        review_agent_response = await Runner.run(code_reviewer_agent, code)
        code_review: CodeReview = review_agent_response.final_output
        print(f"Code Review Response type: {type(code_review)}")
        display_token_usage(review_agent_response)

        # Frontend agent call
        code_review_json = code_review.model_dump_json()
        frontend_agent_response = await Runner.run(frontend_developer_agent, code_review_json)
        display_token_usage(frontend_agent_response)

        # Send Email Agent call
        html_content = frontend_agent_response.final_output
        email_agent_response = await Runner.run(email_sender_agent, html_content)
        display_token_usage(email_agent_response)

    print("=" * 100)
    print(email_agent_response.final_output)


async def main():
    # Switch files to demo both cases:
    await review_file("CleanBankAccount.java")
    # await review_file("buggy_python.py")


if __name__ == "__main__":
    asyncio.run(main())

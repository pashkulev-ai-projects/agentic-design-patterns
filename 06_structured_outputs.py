"""
Pattern: Prompt Chaining
Agents are called sequentially in code — each Runner.run() receives the previous agent's output as input.
Instead of returning free text, the Code Reviewer is configured with output_type=CodeReview — a Pydantic
model — so the SDK deserializes its response into a typed Python object automatically.
That object is then serialized to JSON and passed as input to the next agent in the chain.
Chain: Code Reviewer (CodeReview) → Frontend Developer (HTML) → Email Sender.
"""
import asyncio
from agents import Runner, trace
from my_agents import code_reviewer_agent, frontend_developer_agent, email_sender_agent
from my_agents.code_review.code_reviewer import CodeReview
from utils import display_token_usage, generate_trace_id, get_source_code


async def review_file(file_name: str) -> None:
    trace_id = generate_trace_id()
    code = get_source_code(file_name)

    with trace(workflow_name="Code Review Demo", trace_id=trace_id):
        # Review agent call
        review_agent_response = await Runner.run(
            starting_agent=code_reviewer_agent,
            input=code
        )
        code_review: CodeReview = review_agent_response.final_output
        print(f"Code Review Response type: {type(code_review)}")
        display_token_usage(review_agent_response)

        # Frontend agent call
        code_review_json = code_review.model_dump_json()
        frontend_agent_response = await Runner.run(
            starting_agent=frontend_developer_agent,
            input=code_review_json
        )
        display_token_usage(frontend_agent_response)

        # Send Email Agent call
        html_content = frontend_agent_response.final_output
        email_agent_response = await Runner.run(
            starting_agent=email_sender_agent,
            input=html_content
        )
        display_token_usage(email_agent_response)

    print("=" * 100)
    print(email_agent_response.final_output)


async def main():
    # Switch files to demo both cases:
    await review_file("buggy_python.py")
    # await review_file("CleanBankAccount.java")


if __name__ == "__main__":
    asyncio.run(main())

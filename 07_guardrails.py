"""
Pattern: Prompt Chaining with Guardrails
Input guardrail blocks prompt injection attempts;
Output guardrail blocks sensitive data leakage before output passes downstream.
"""
import asyncio
from agents import Runner, trace, InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered
from my_agents import frontend_developer_agent, email_sender_agent, guarded_reviewer_agent
from my_agents.code_review.code_reviewer import CodeReview
from utils import display_token_usage, get_source_code


async def run_pipeline(label: str, code: str) -> None:
    print(f"\n{'=' * 100}")
    print(f"Input: {label}")
    print("=" * 100)

    try:
        with trace("Guardrails Demo"):
            # Step 1 — Code Reviewer (guarded)
            review_response = await Runner.run(
                starting_agent=guarded_reviewer_agent,
                input=code
            )
            code_review: CodeReview = review_response.final_output
            display_token_usage(review_response)

            # Step 2 — Frontend Developer
            frontend_response = await Runner.run(
                starting_agent=frontend_developer_agent,
                input=code_review.model_dump_json()
            )
            display_token_usage(frontend_response)

            # Step 3 — Email Sender
            email_response = await Runner.run(
                starting_agent=email_sender_agent,
                input=frontend_response.final_output
            )
            display_token_usage(email_response)

        print(f"✓ Pipeline completed. Email sent successfully.")

    except InputGuardrailTripwireTriggered as e:
        check = e.guardrail_result.output.output_info
        print(f"🚨 INPUT GUARDRAIL TRIGGERED — Pipeline blocked.")
        print(f"   Attack pattern : {check.attack_pattern}")
        print(f"   Reason         : {check.reason}")

    except OutputGuardrailTripwireTriggered as e:
        check = e.guardrail_result.output.output_info
        print(f"🔒 OUTPUT GUARDRAIL TRIGGERED — Sensitive data leak prevented.")
        print(f"   Leaked fields  : {', '.join(check.leaked_fields)}")
        print(f"   Reason         : {check.reason}")


async def main():
    # Scenario 1: Prompt injection attempt embedded in code → input guardrail blocks
    code = get_source_code("injection_python.py")
    await run_pipeline("injection_python.py", code)

    # Scenario 2: Buggy code with hardcoded secrets → output guardrail blocks
    code = get_source_code("buggy_python.py")
    await run_pipeline("buggy_python.py", code)

    # Scenario 3: Clean code → both guardrails pass → email sent
    code = get_source_code("CleanBankAccount.java")
    await run_pipeline("CleanBankAccount.java", code)


if __name__ == "__main__":
    asyncio.run(main())

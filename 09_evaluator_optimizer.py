"""
Pattern: Evaluator-Optimizer
Two agents with different models form a feedback loop driven entirely by application code.
test_generator_agent (Deepseek R1:8b via Ollama, local) generates or improves unit tests.
test_evaluator_agent (mistral-large-latest via Mistral API, cloud) scores them and sets
approved=True on its TestEvaluation structured output when the quality threshold is met.
The loop runs until approved=True or MAX_ITERATIONS is reached; on each iteration the
evaluator's feedback and missing_cases are injected into the generator's next prompt.
"""
import asyncio
from agents import Runner, trace
from my_agents.unit_testing.test_generator import test_generator_agent
from my_agents.unit_testing.test_evaluator import test_evaluator_agent, TestEvaluation
from utils import display_token_usage, get_source_code, generate_trace_id

MAX_ITERATIONS = 3
SCORE_THRESHOLD = 9


async def run_evaluator_optimizer(file_name: str) -> None:
    trace_id = generate_trace_id()
    code = get_source_code(file_name)

    print(f"\n{'=' * 80}")
    print(f"Evaluator-Optimizer — {file_name}")
    print(f"Generator : Deepseek R1:8b (Ollama)")
    print(f"Evaluator : mistral-large-latest (Mistral)")
    print("=" * 80)

    tests: str | None = None
    evaluation: TestEvaluation | None = None

    with trace(workflow_name="Evaluator-Optimizer Demo", trace_id=trace_id):
        for iteration in range(1, MAX_ITERATIONS + 1):
            print(f"\n[Iteration {iteration}/{MAX_ITERATIONS}] Generating unit tests...")

            if tests is None:
                prompt = f"Generate basic JUnit 5 unit tests for this Java class covering only the happy path:\n\n{code}"
            else:
                prompt = (
                    f"Java class:\n\n{code}\n\n"
                    f"Previous tests (score: {evaluation.score}/10):\n\n{tests}\n\n"
                    f"Evaluator feedback: {evaluation.feedback}\n"
                    f"Missing cases: {', '.join(evaluation.missing_cases)}\n\n"
                    "Improve the tests to address all the feedback above."
                )

            # Run Unit Test Generator
            gen_response = await Runner.run(starting_agent=test_generator_agent, input=prompt)
            tests = gen_response.final_output
            display_token_usage(gen_response)
            print(f"  ✓ Tests generated ({len(tests.splitlines())} lines)")

            #  Run Unit Test Evaluator
            print(f"\n[Iteration {iteration}/{MAX_ITERATIONS}] Evaluating...")
            eval_input = f"Java class:\n\n{code}\n\nUnit tests:\n\n{tests}"
            eval_response = await Runner.run(test_evaluator_agent, eval_input)
            evaluation: TestEvaluation = eval_response.final_output
            display_token_usage(eval_response)

            print(f"  Score    : {evaluation.score}/10")
            print(f"  Approved : {'✓ Yes' if evaluation.approved else '✗ No'}")
            print(f"  Feedback : {evaluation.feedback}")
            if evaluation.missing_cases:
                print(f"  Missing  : {', '.join(evaluation.missing_cases)}")

            if evaluation.approved:
                print(f"\n✓ Quality threshold ({SCORE_THRESHOLD}/10) reached in {iteration} iteration(s)!")
                break

        else:
            print(f"\n⚠ Max iterations reached. Best score: {evaluation.score}/10")

    # Print final version of generated unit tests
    print(f"\n{'─' * 80}")
    print("FINAL GENERATED TESTS")
    print("─" * 80)
    print(tests)


async def main():
    await run_evaluator_optimizer("CleanBankAccount.java")


if __name__ == "__main__":
    asyncio.run(main())

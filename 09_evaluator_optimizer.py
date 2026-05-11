"""
Evaluator-Optimizer Pattern — Iterative unit test generation with multi-model pipeline
Generator : Deepseek R1:8b (local, Ollama)
Evaluator : mistral-large-latest (cloud, Mistral)
"""
import asyncio
from pathlib import Path
from agents import Runner, trace
from my_agents.unit_testing.test_generator import test_generator_agent
from my_agents.unit_testing.test_evaluator import test_evaluator_agent, TestEvaluation
from utils import display_token_usage

ASSETS_DIR = Path(__file__).parent / "assets" / "code_review"
MAX_ITERATIONS = 3
SCORE_THRESHOLD = 9


async def run_evaluator_optimizer(file_name: str) -> None:
    code = (ASSETS_DIR / file_name).read_text()

    print(f"\n{'=' * 80}")
    print(f"Evaluator-Optimizer — {file_name}")
    print(f"Generator : Deepseek R1:8b (Ollama)")
    print(f"Evaluator : mistral-large-latest (Mistral)")
    print("=" * 80)

    tests: str | None = None
    evaluation: TestEvaluation | None = None

    with trace("Evaluator-Optimizer Demo"):
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

            gen_response = await Runner.run(test_generator_agent, prompt)
            tests = gen_response.final_output
            display_token_usage(gen_response)
            print(f"  ✓ Tests generated ({len(tests.splitlines())} lines)")

            print(f"\n[Iteration {iteration}/{MAX_ITERATIONS}] Evaluating...")
            eval_input = f"Java class:\n\n{code}\n\nUnit tests:\n\n{tests}"
            eval_response = await Runner.run(test_evaluator_agent, eval_input)
            evaluation = eval_response.final_output
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

    print(f"\n{'─' * 80}")
    print("FINAL GENERATED TESTS")
    print("─" * 80)
    print(tests)


async def main():
    await run_evaluator_optimizer("CleanBankAccount.java")


if __name__ == "__main__":
    asyncio.run(main())

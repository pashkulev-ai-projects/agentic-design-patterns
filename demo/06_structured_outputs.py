import asyncio
from pathlib import Path
from typing import Literal

from agents import Agent, ModelSettings, Runner, gen_trace_id, trace
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv(override=True)

CODE_REVIEW_DIR = Path(__file__).parent / "code_review"


# --- Structured Output Schema ---

class Issue(BaseModel):
    code_snippet: str
    severity: Literal["critical", "warning", "suggestion"]
    description: str
    fix: str


class CodeReview(BaseModel):
    language: str
    overall_score: int  # 1-10
    summary: str
    issues: list[Issue]
    positive_aspects: list[str]
    verdict: Literal["approve", "request_changes", "reject"]


# --- Agent ---

reviewer = Agent(
    name="Code_Reviewer",
    instructions=(
        "You are a senior software engineer conducting thorough code reviews. "
        "Analyse the provided code carefully and return a structured review covering: "
        "language, an overall quality score from 1 to 10, a concise summary, "
        "a list of issues each with the exact problematic code snippet as context, severity, description and suggested fix, "
        "positive aspects of the code, and a final verdict. "
        "Severity guidelines: security vulnerabilities (SQL injection, plain text passwords, etc.) are always 'critical'; "
        "bad practices with side effects are 'warning'; style and minor improvements are 'suggestion'. "
        "You will receive the raw code to review directly as the message."
    ),
    output_type=CodeReview,
    model_settings=ModelSettings(temperature=0),
    model="gpt-4o-mini",
)


def print_review(file_name: str, review: CodeReview) -> None:
    print(f"\n{'=' * 60}")
    print(f"File:     {file_name}")
    print(f"Language: {review.language}")
    print(f"Score:    {review.overall_score}/10")
    print(f"Verdict:  {review.verdict.upper()}")
    print(f"\nSummary:\n{review.summary}")

    if review.positive_aspects:
        print(f"\nPositive aspects:")
        for point in review.positive_aspects:
            print(f"  + {point}")

    if review.issues:
        print(f"\nIssues found ({len(review.issues)}):")
        for issue in review.issues:
            print(f"  [{issue.severity.upper()}] `{issue.context}`: {issue.description}")
            print(f"    Fix: {issue.fix}")

    print(f"{'=' * 60}")


async def review_file(file_path: Path) -> None:
    code = file_path.read_text()

    trace_id = gen_trace_id()
    print(f"\nTrace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
    print(f"Reviewing: {file_path.name}")

    with trace("Code Review Demo", trace_id=trace_id):
        result = await Runner.run(reviewer, code)

    print_review(file_path.name, result.final_output)

    token_usage = result.context_wrapper.usage
    print(f"Usage: {token_usage.input_tokens} input tokens and {token_usage.output_tokens} output tokens. "
          f"{token_usage.total_tokens} total tokens.")


async def main():
    # Switch files to demo both cases:
    await review_file(CODE_REVIEW_DIR / "CleanBankAccount.java")
    await review_file(CODE_REVIEW_DIR / "buggy_python.py")


if __name__ == "__main__":
    asyncio.run(main())

"""
Parallelization Pattern — Multiple specialist my_agents running concurrently
"""
import asyncio
import json
import time
from pathlib import Path
from agents import Runner, trace
from demo.my_agents.code_review.specialist_reviewers import (
    security_reviewer_agent,
    performance_reviewer_agent,
    readability_reviewer_agent,
    SpecialistReview,
)
from demo.my_agents.code_review.review_aggregator import review_aggregator_agent, AggregatedReport
from demo.my_agents import frontend_developer_agent, email_sender_agent
from demo.utils import display_token_usage

ASSETS_DIR = Path(__file__).parent / "assets" / "code_review"


async def run_specialist(agent, code: str, label: str) -> SpecialistReview:
    print(f"  → [{label}] starting...")
    response = await Runner.run(agent, code)
    display_token_usage(response)
    print(f"  ✓ [{label}] done — score: {response.final_output.score}/10, issues: {len(response.final_output.issues)}")
    return response.final_output


async def review_parallel(file_name: str) -> None:
    code = (ASSETS_DIR / file_name).read_text()

    print(f"\n{'=' * 80}")
    print(f"File: {file_name}")
    print("=" * 80)

    with trace("Parallelization Demo"):
        # --- Parallel phase: 3 specialist reviewers run simultaneously ---
        print("\n[Parallel] Running Security, Performance, and Readability reviewers simultaneously...")
        t0 = time.perf_counter()

        security_review, performance_review, readability_review = await asyncio.gather(
            run_specialist(security_reviewer_agent, code, "Security"),
            run_specialist(performance_reviewer_agent, code, "Performance"),
            run_specialist(readability_reviewer_agent, code, "Readability"),
        )

        parallel_time = time.perf_counter() - t0
        print(f"\n  All 3 specialists completed in {parallel_time:.1f}s")

        # --- Sequential aggregation phase ---
        print("\n[Aggregator] Synthesising specialist reviews...")
        reviews_json = json.dumps([
            security_review.model_dump(),
            performance_review.model_dump(),
            readability_review.model_dump(),
        ])
        agg_response = await Runner.run(review_aggregator_agent, reviews_json)
        display_token_usage(agg_response)
        report: AggregatedReport = agg_response.final_output

        # --- Email phase ---
        print("\n[Email] Designing and sending full report...")
        full_report = json.dumps({
            "file": file_name,
            "aggregated": report.model_dump(),
            "specialists": {
                "security": security_review.model_dump(),
                "performance": performance_review.model_dump(),
                "readability": readability_review.model_dump(),
            }
        })
        frontend_response = await Runner.run(frontend_developer_agent, full_report)
        display_token_usage(frontend_response)

        email_response = await Runner.run(email_sender_agent, frontend_response.final_output)
        display_token_usage(email_response)

    # --- Console summary ---
    print(f"\n{'─' * 80}")
    print(f"AGGREGATED REPORT")
    print(f"{'─' * 80}")
    print(f"Overall Score  : {report.overall_score}/10")
    print(f"Verdict        : {report.verdict.upper()}")
    print(f"Security       : {report.security_score}/10")
    print(f"Performance    : {report.performance_score}/10")
    print(f"Readability    : {report.readability_score}/10")
    print(f"\nExecutive Summary:\n{report.executive_summary}")
    print(f"\nTop Issues:")
    for i, issue in enumerate(report.top_issues, 1):
        print(f"  {i}. {issue}")
    print(f"\nTotal wall-clock time (parallel phase): {parallel_time:.1f}s")
    print(f"Email sent successfully.")


async def main():
    await review_parallel("buggy_python.py")
    # await review_parallel("CleanBankAccount.java")


if __name__ == "__main__":
    asyncio.run(main())

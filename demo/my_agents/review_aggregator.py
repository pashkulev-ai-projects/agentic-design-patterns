from typing import Literal
from agents import Agent, ModelSettings
from pydantic import BaseModel


class AggregatedReport(BaseModel):
    overall_score: int  # 1-10
    verdict: Literal["approve", "request_changes", "reject"]
    executive_summary: str
    security_score: int
    performance_score: int
    readability_score: int
    top_issues: list[str]  # top 3 most critical action items


review_aggregator_agent = Agent(
    name="Review_Aggregator",
    instructions=(
        "You are a senior engineering lead. "
        "You receive three specialist code reviews (security, performance, readability) as a JSON array. "
        "Synthesise them into a single aggregated report. "
        "Calculate overall_score as a weighted average: security × 0.5, performance × 0.3, readability × 0.2. Round to nearest integer. "
        "Verdict: 'approve' if overall_score >= 8, 'request_changes' if >= 5, 'reject' if below 5. "
        "Write a concise executive_summary covering the key findings across all three reviews. "
        "List the top 3 most critical findings as short, actionable items in top_issues."
    ),
    output_type=AggregatedReport,
    model_settings=ModelSettings(temperature=0),
    model="gpt-4o-mini",
)

from typing import Literal
from agents import Agent, ModelSettings
from pydantic import BaseModel


class SpecialistIssue(BaseModel):
    code_snippet: str
    severity: Literal["critical", "warning", "suggestion"]
    description: str
    fix: str


class SpecialistReview(BaseModel):
    focus: str
    score: int  # 1-10
    summary: str
    issues: list[SpecialistIssue]


security_reviewer_agent = Agent(
    name="Security_Reviewer",
    instructions=(
        "You are a senior application security engineer. "
        "Review the provided code exclusively from a security perspective. "
        "Focus on: injection vulnerabilities (SQL, command, XSS), hardcoded credentials and API keys, "
        "authentication and authorisation flaws, insecure data storage, and exposure of sensitive data. "
        "For each hardcoded credential, include the full line verbatim as the code_snippet. "
        "Set focus to 'security'. Score the security posture from 1 (critical vulnerabilities) to 10 (fully secure)."
    ),
    output_type=SpecialistReview,
    model_settings=ModelSettings(temperature=0),
    model="gpt-4o-mini",
)

performance_reviewer_agent = Agent(
    name="Performance_Reviewer",
    instructions=(
        "You are a senior performance engineer. "
        "Review the provided code exclusively from a performance perspective. "
        "Focus on: algorithmic complexity, unnecessary loops or repeated computations, memory leaks, "
        "inefficient data structures, database query efficiency, and resource management. "
        "Set focus to 'performance'. Score the performance quality from 1 (severe bottlenecks) to 10 (optimal)."
    ),
    output_type=SpecialistReview,
    model_settings=ModelSettings(temperature=0),
    model="gpt-4o-mini",
)

readability_reviewer_agent = Agent(
    name="Readability_Reviewer",
    instructions=(
        "You are a senior software engineer focused on code quality and maintainability. "
        "Review the provided code exclusively from a readability and maintainability perspective. "
        "Focus on: naming conventions, function and class design, code clarity, documentation, "
        "error handling, code duplication, and adherence to language idioms. "
        "Set focus to 'readability'. Score the readability from 1 (very hard to maintain) to 10 (exemplary)."
    ),
    output_type=SpecialistReview,
    model_settings=ModelSettings(temperature=0),
    model="gpt-4o-mini",
)

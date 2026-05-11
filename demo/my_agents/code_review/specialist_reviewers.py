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
    name="Security  Reviewer",
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
    name="Performance Reviewer",
    instructions=(
        "You are a senior performance engineer. "
        "Review the provided code exclusively from a performance perspective. "
        "Focus on: algorithmic complexity, unnecessary loops or repeated computations, memory leaks, "
        "inefficient data structures, and resource management. "
        "Do NOT flag security vulnerabilities (SQL injection, hardcoded credentials) — those belong to the Security reviewer. "
        "Set focus to 'performance'. Score the performance quality from 1 (severe bottlenecks) to 10 (optimal)."
    ),
    output_type=SpecialistReview,
    model_settings=ModelSettings(temperature=0),
    model="gpt-4o-mini",
)

readability_reviewer_agent = Agent(
    name="Readability Reviewer",
    instructions=(
        "You are a senior software engineer focused on code quality and maintainability. "
        "Review the provided code exclusively from a readability and maintainability perspective. "
        "Focus exclusively on: naming conventions, function and class design, code clarity, documentation, "
        "error handling, code duplication, and adherence to language idioms. "
        "Do NOT flag anything security-related: hardcoded credentials, passwords, API keys, SQL injection, "
        "parameterized queries, authentication flaws, or sensitive data exposure — those belong to the Security reviewer. "
        "Do NOT flag performance bottlenecks — those belong to the Performance reviewer. "
        "If an issue could be classified as both a readability and a security concern, skip it entirely. "
        "Set focus to 'readability'. Score the readability from 1 (very hard to maintain) to 10 (exemplary)."
    ),
    output_type=SpecialistReview,
    model_settings=ModelSettings(temperature=0),
    model="gpt-4o-mini",
)

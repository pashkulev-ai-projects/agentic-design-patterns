from typing import Literal
from agents import Agent, ModelSettings
from pydantic import BaseModel


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

    def __str__(self):
        review_output = f"Language: {self.language}\n"
        review_output += f"Overall Score: {self.overall_score}\n"
        review_output += f"Verdict: {self.verdict.upper()}\n\n"
        review_output += f"Summary:\n"
        review_output += f"{self.summary}\n\n"

        if self.positive_aspects:
            review_output += f"Positive aspects:\n"
            for point in self.positive_aspects:
                review_output += f"  + {point}\n"

        if self.issues:
            f"\nIssues found ({len(self.issues)}):\n"
            for issue in self.issues:
                review_output += f"  [{issue.severity.upper()}] `{issue.code_snippet}`: {issue.description}\n"
                review_output += f"    Fix: {issue.fix}\n"

        return review_output


# --- Agent ---

code_reviewer_agent = Agent(
    name="Code_Reviewer",
    instructions=(
        "You are a senior software engineer conducting thorough code reviews. "
        "Analyse the provided code carefully and return a structured review covering: "
        "language, an overall quality score from 1 to 10, a concise summary, "
        "a list of issues each with the exact problematic code snippet as context, severity, description and suggested fix, "
        "positive aspects of the code, and a final verdict. "
        "Severity guidelines: security vulnerabilities (SQL injection, hardcoded credentials/API keys/secrets, plain text passwords, etc.) are always 'critical'; "
        "bad practices with side effects are 'warning'; style and minor improvements are 'suggestion'. "
        "For each hardcoded credential or secret, include the full line (variable name AND its literal value) verbatim as the code_snippet. "
        "Verdict: 'approve' when the code is ready to merge as-is, even if minor suggestions are noted; 'request_changes' when specific changes must be addressed before merging; 'reject' when critical issues are unresolved. "
        "You will receive the raw code to review directly as the message."
    ),
    output_type=CodeReview,
    model_settings=ModelSettings(temperature=0),
    model="gpt-4o-mini",
)
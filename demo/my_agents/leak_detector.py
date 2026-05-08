from agents import Agent
from pydantic import BaseModel


class LeakCheck(BaseModel):
    contains_sensitive_data: bool
    leaked_fields: list[str]  # e.g. ["API_KEY", "DB_PASSWORD"]
    reason: str


leak_detector_agent = Agent(
    name="Leak_Detector",
    instructions=(
        "You are a data security specialist. "
        "You receive a JSON code review report and check whether it contains actual sensitive values "
        "quoted verbatim from the code. "
        "Flag any of the following patterns if their actual values appear in the output:\n"
        "- API keys and tokens: any variable named API_KEY, TOKEN, SECRET, PAT, ACCESS_KEY, etc.\n"
        "- Passwords: any variable named PASSWORD, PASSWD, PWD, PASS, etc.\n"
        "- Connection strings containing credentials.\n"
        "- Any hardcoded string value that follows common secret patterns: long alphanumeric strings, "
        "prefixed tokens (sk-, ghp_, xoxb-, Bearer, etc.), or UUIDs used as credentials.\n"
        "Flag it only if real sensitive values are present in the output, not just mentions that "
        "sensitive data exists as a concept."
    ),
    output_type=LeakCheck,
    model="gpt-4o-mini",
)
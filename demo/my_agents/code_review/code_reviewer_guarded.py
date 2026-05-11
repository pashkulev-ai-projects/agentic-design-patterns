# Guarded code reviewer — same as base but with both guardrails attached
from agents import Agent, ModelSettings
from demo.my_agents.code_review.code_reviewer import code_reviewer_agent, CodeReview
from demo.guardrails import sensitive_data_leak_guardrail, prompt_injection_guardrail


guarded_reviewer_agent = Agent(
    name="Guarded Code Reviewer",
    instructions=code_reviewer_agent.instructions,
    output_type=CodeReview,
    model_settings=ModelSettings(temperature=0),
    model="gpt-4o-mini",
    input_guardrails=[prompt_injection_guardrail],
    output_guardrails=[sensitive_data_leak_guardrail],
)
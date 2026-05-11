from agents import (
    Agent,
    Runner,
    GuardrailFunctionOutput,
    RunContextWrapper,
    input_guardrail,
)
from my_agents.guardrails.injection_detector import injection_detector_agent


@input_guardrail
async def prompt_injection_guardrail(ctx: RunContextWrapper, agent: Agent, user_input: str) -> GuardrailFunctionOutput:
    result = await Runner.run(injection_detector_agent, user_input, context=ctx.context)
    check = result.final_output
    return GuardrailFunctionOutput(output_info=check, tripwire_triggered=check.is_injection)

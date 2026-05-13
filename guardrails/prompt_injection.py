from agents import (
    Agent,
    Runner,
    GuardrailFunctionOutput,
    RunContextWrapper,
    input_guardrail,
)
from my_agents.guardrails.injection_detector import injection_detector_agent, InjectionCheck


@input_guardrail
async def prompt_injection_guardrail(ctx: RunContextWrapper, agent: Agent, user_input: str) -> GuardrailFunctionOutput:
    result = await Runner.run(
        starting_agent=injection_detector_agent,
        input=user_input,
        context=ctx.context
    )
    check: InjectionCheck = result.final_output
    return GuardrailFunctionOutput(output_info=check, tripwire_triggered=check.is_injection)

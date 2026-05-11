from agents import (
    Agent,
    Runner,
    GuardrailFunctionOutput,
    RunContextWrapper,
    output_guardrail,
)
from my_agents.guardrails.leak_detector import leak_detector_agent


@output_guardrail
async def sensitive_data_leak_guardrail(
    ctx: RunContextWrapper, agent: Agent, output: object
) -> GuardrailFunctionOutput:
    output_json = output.model_dump_json() if hasattr(output, "model_dump_json") else str(output)
    result = await Runner.run(leak_detector_agent, output_json, context=ctx.context)
    check = result.final_output
    return GuardrailFunctionOutput(output_info=check, tripwire_triggered=check.contains_sensitive_data)

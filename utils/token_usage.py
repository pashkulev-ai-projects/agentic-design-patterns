from agents import RunResult, RunResultStreaming


def display_token_usage(agent_response: RunResult | RunResultStreaming):
    token_usage = agent_response.context_wrapper.usage
    print()
    print("=" * 100)
    print(f"Usage by {agent_response.last_agent.name}: {token_usage.input_tokens} input tokens and {token_usage.output_tokens} output tokens. "
          f"{token_usage.total_tokens} total tokens.")
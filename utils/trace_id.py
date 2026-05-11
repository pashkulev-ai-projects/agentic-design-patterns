from agents import gen_trace_id


def generate_trace_id():
    trace_id = gen_trace_id()
    print("=" * 100)
    print(f"Trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
    print("=" * 100)

    return trace_id
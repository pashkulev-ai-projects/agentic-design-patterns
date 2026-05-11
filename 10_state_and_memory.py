"""
State & Memory in Agentic Systems
Two approaches: in-thread (ephemeral) vs persistent SQLite (durable)
"""
import asyncio

from agents import Runner, trace
from my_agents import thread_assistant_agent
from my_agents.memory.memory_assistant import memory_assistant_agent
from utils import display_token_usage
from dotenv import load_dotenv

load_dotenv(override=True)
LINE_SEPARATOR = "=" * 80


def _log_output(prompt, response, turn):
    print(LINE_SEPARATOR)
    print(f"Turn {turn} → ")
    print(LINE_SEPARATOR)
    print(f"User Prompt: {prompt}")
    print(f"Agent Response: {response}")


# ─────────────────────────────────────────────────────────────────────────────
# Approach 1 — In-Thread State
# Context lives in the conversation history, dies when the session ends
# ─────────────────────────────────────────────────────────────────────────────

async def demo_in_thread_state() -> None:
    print(LINE_SEPARATOR)
    print("APPROACH 1 — In-Thread State (context lives within the session)")

    prompt1 = "My name is Ivan and I work in ICT Strypes."
    result1 = await Runner.run(thread_assistant_agent, prompt1)
    _log_output(prompt1, result1.final_output, 1)
    display_token_usage(result1)

    # Continue the thread — agent remembers Turn 1
    prompt2 = "What do you know about me?"
    context_history = result1.to_input_list() + [{"role": "user", "content": prompt2}]
    result2 = await Runner.run(starting_agent=thread_assistant_agent, input=context_history)
    _log_output(prompt2, result2.final_output, 2)
    display_token_usage(result2)

    # Fresh run — agent has no memory
    prompt3 = "What do you know about me?"
    result3 = await Runner.run(thread_assistant_agent, prompt3)
    _log_output(prompt3, result3.final_output, 3)
    display_token_usage(result3)


# ─────────────────────────────────────────────────────────────────────────────
# Approach 2 — Persistent SQLite Memory
# Facts survive across separate runs and sessions
# ─────────────────────────────────────────────────────────────────────────────

async def demo_persistent_memory() -> None:
    print("\n" + LINE_SEPARATOR)
    print("APPROACH 2 — Persistent SQLite Memory (survives across sessions)")
    print(LINE_SEPARATOR)
    print("\n--- Session 1: introducing ourselves ---")

    prompt1 = "Hi! My name is Ivan, I'm a DevOps Engineer at Strypes."
    result1 = await Runner.run(memory_assistant_agent, prompt1)
    _log_output(prompt1, result1.final_output, 1)
    display_token_usage(result1)

    print("\n--- Session 2: fresh run, agent remembers ---")
    prompt2 = "Hello again, do you remember me?"
    result2 = await Runner.run(memory_assistant_agent, prompt2)
    _log_output(prompt2, result2.final_output, 2)
    display_token_usage(result2)


async def main() -> None:
    with trace("State & Memory Demo"):
        await demo_in_thread_state()
        await demo_persistent_memory()


if __name__ == "__main__":
    asyncio.run(main())

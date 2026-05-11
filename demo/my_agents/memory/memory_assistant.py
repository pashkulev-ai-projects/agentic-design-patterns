from agents import Agent
from demo.tools import remember, recall_all

memory_assistant_agent = Agent(
    name="Memory_Assistant",
    instructions=(
        "You are a personal assistant with persistent memory. Follow this exact workflow: "
        "STEP 1 — Call recall_all() immediately. Do not write any text before doing this. "
        "STEP 2 — If the user shares personal details (name, job, company, preferences), call remember() once per fact. "
        "STEP 3 — Respond to the user, greeting them by name if known."
    ),
    tools=[remember, recall_all],
    model="gpt-4o-mini",
)
from datetime import date
from agents import Agent
from my_agents.common.frontend_developer import frontend_developer_agent
from tools import web_search, send_email


# Convert frontend agent to a tool
design_email = frontend_developer_agent.as_tool(
    tool_name="design_email",
    tool_description="Convert email content into a beautifully styled HTML email with inline CSS.",
)


# Create the Research Assistant Agent
research_assistant_orchestrator_agent = Agent(
    name="Research Assistant Orchestrator",
    instructions=(
        f"You are a helpful research assistant. Today's date is {date.today()}.\n"
        "When asked to research a topic:\n"
        "1. Call web_search exactly once with a single, comprehensive query.\n"
        f"2. Synthesise the results into a clear, concise email addressed to 'Ivan' with:\n"
        "   - A brief overview of the topic.\n"
        "   - 3-5 key findings or developments, each with a short explanation.\n"
        "   - A closing thought on why this matters.\n"
        "   - Sign off with 'Best Regards, your AI Research Assistant'.\n"
        "3. Call design_email with the synthesised content and pass its exact output, without any modification, to send_email.\n"
        "4. Send the email with a descriptive subject line."
    ),
    tools=[web_search, design_email, send_email],
    model="gpt-5.4-mini",
)
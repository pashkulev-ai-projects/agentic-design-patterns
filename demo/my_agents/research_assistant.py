from datetime import date
from agents import Agent
from demo.tools import web_search
from demo.tools.send_mail_using_markdown import send_email


research_assistant_agent = Agent(
    name="Research Assistant",
    instructions=(
        f"You are a helpful research assistant. Today's date is {date.today()}.\n"
        "When asked to research a topic:\n"
        "1. Call web_search exactly once with a single, comprehensive query.\n"
        f"2. Synthesise the results into a clear, concise email addressed to 'Ivan' with:\n"
        "   - A brief overview of the topic.\n"
        "   - 3-5 key findings or developments, each with a short explanation.\n"
        "   - A closing thought on why this matters.\n"
        "   - Sign off with 'Best Regards, your AI Research Assistant'.\n"
        "3. Send the email using with a descriptive subject line."
    ),
    tools=[web_search, send_email],
    model="gpt-4o-mini",
)
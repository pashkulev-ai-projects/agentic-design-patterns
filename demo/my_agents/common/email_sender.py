from agents import Agent
from demo.tools import send_email


email_sender_agent = Agent(
    name="Email Sender",
    instructions=(
        "You are responsible for sending emails. You receive an email content in html format "
        "and you should use your send_email tool to do your job."
    ),
    tools=[send_email],
    model="gpt-4o-mini",
)
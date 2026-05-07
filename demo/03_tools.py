import asyncio
import os
from datetime import date
import httpx
import markdown as md
import resend
from agents import Agent, Runner, function_tool, gen_trace_id, trace
from dotenv import load_dotenv

load_dotenv(override=True)
resend.api_key = os.environ["RESEND_API_KEY"]

FROM_EMAIL = "ivan@ivanpashkulev.com"
TO_EMAIL = "ivan.pashkulev@ict.eu"
first_name = TO_EMAIL.split(".")[0].capitalize()


@function_tool
def web_search(query: str) -> str:
    """Search the web for any topic and return a summary of the top results."""
    response = httpx.post(
        "https://google.serper.dev/search",
        headers={"X-API-KEY": os.environ["SERPER_API_KEY"], "Content-Type": "application/json"},
        json={"q": query, "num": 5},
        timeout=10,
    )
    response.raise_for_status()
    results = response.json().get("organic", [])
    return "\n\n".join(
        f"{r['title']}\n{r['link']}\n{r.get('snippet', '')}"
        for r in results
    )


@function_tool
def send_email(subject: str, content: str) -> str:
    """Send an email to the configured recipient with the given subject and content."""
    params: resend.Emails.SendParams = {
        "from": FROM_EMAIL,
        "to": [TO_EMAIL],
        "subject": subject,
        "html": md.markdown(content),
    }
    email = resend.Emails.send(params)
    return f"Email sent successfully. ID: {email['id']}"


async def main():
    agent = Agent(
        name="Research Assistant",
        instructions=(
            f"You are a helpful research assistant. Today's date is {date.today()}.\n"
            "When asked to research a topic:\n"
            "1. Call web_search with a well-crafted query to find the latest information.\n"
            f"2. Synthesise the results into a clear, concise email addressed to '{first_name}' with:\n"
            "   - A brief overview of the topic.\n"
            "   - 3-5 key findings or developments, each with a short explanation.\n"
            "   - A closing thought on why this matters.\n"
            "   - Sign off with 'Best Regards, your AI Research Assistant'.\n"
            "3. Send the email with a descriptive subject line."
        ),
        tools=[web_search, send_email],
        model="gpt-4o-mini",
    )

    prompt = "Search for the latest developments in AI agents and send me a summary email."

    trace_id = gen_trace_id()
    print(f"Trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n")
    print(f"User prompt: {prompt}\n")

    with trace("Research Assistant Demo", trace_id=trace_id):
        result = await Runner.run(agent, prompt)

    print(f"Agent response:\n{result.final_output}")

    token_usage = result.context_wrapper.usage
    print(f"\nUsage: {token_usage.input_tokens} input tokens and {token_usage.output_tokens} output tokens. "
          f"{token_usage.total_tokens} total tokens.")


if __name__ == "__main__":
    asyncio.run(main())

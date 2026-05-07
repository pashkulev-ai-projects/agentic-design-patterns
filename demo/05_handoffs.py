"""
Routing Pattern
"""
import asyncio
import os
from datetime import date
from agents import Agent, Runner, function_tool, gen_trace_id, trace
from dotenv import load_dotenv

load_dotenv(override=True)

COMPANY_NAME = "CloudDesk"
CURRENT_DATE = date.today()


# --- Mock Tools: Billing ---

@function_tool
def lookup_transaction(email: str) -> str:
    """Look up recent transactions for a customer account."""
    return (
        f"Account: {email}\n"
        f"Recent transactions:\n"
        f"  - {CURRENT_DATE}: $49.00 (Pro Plan - Monthly) — ref #TXN-88421\n"
        f"  - {CURRENT_DATE}: $49.00 (Pro Plan - Monthly) — ref #TXN-88422\n"
        f"  - 2026-04-01: $49.00 (Pro Plan - Monthly) — ref #TXN-81033\n"
        f"Account status: Active"
    )


@function_tool
def submit_refund(email: str, amount: float, reason: str) -> str:
    """Submit a refund request for a customer."""
    return (
        f"Refund request submitted successfully.\n"
        f"  Customer: {email}\n"
        f"  Amount: ${amount:.2f}\n"
        f"  Reason: {reason}\n"
        f"  Reference: REF-{abs(hash(email)) % 90000 + 10000}\n"
        f"  Processing time: 3-5 business days\n"
        f"  Confirmation will be sent to {email}"
    )


# --- Mock Tools: Tech Support ---

@function_tool
def check_system_status() -> str:
    """Check current CloudDesk system and service health."""
    return (
        "CloudDesk System Status — All systems operational.\n"
        "  - Authentication service: ✓ Online\n"
        "  - Dashboard: ✓ Online\n"
        "  - API: ✓ Online\n"
        "  - No active incidents reported."
    )


@function_tool
def reset_account_access(email: str) -> str:
    """Clear all active sessions and trigger a password reset email for the customer."""
    return (
        f"Account access reset for {email}.\n"
        f"  - All active sessions terminated.\n"
        f"  - Password reset email sent to {email}.\n"
        f"  - Account lock cleared (if applicable).\n"
        f"  - Customer may log in using the new password within 15 minutes."
    )


# --- Specialist Agents ---

billing_agent = Agent(
    name="Billing_Specialist",
    instructions=(
        f"You are a billing specialist at {COMPANY_NAME}, a SaaS project management platform. "
        f"Today's date is {CURRENT_DATE}.\n\n"
        "Your responsibilities and policies:\n"
        "- Always call lookup_transaction first to review the customer's recent charges before taking any action.\n"
        "- Double charges: apologise sincerely, submit an immediate refund for the duplicate amount.\n"
        "- Refund policy: full refunds within 30 days of charge, no questions asked.\n"
        "- Annual plans: pro-rated refunds only after the 30-day window.\n"
        "- Always provide the refund reference number and expected processing time.\n"
        "- Be empathetic, professional, and solution-focused. Never make the customer feel at fault.\n"
        "- End every interaction by asking if there is anything else you can help with."
    ),
    tools=[lookup_transaction, submit_refund],
    model="gpt-4o-mini",
)

tech_support_agent = Agent(
    name="Tech_Support_Specialist",
    instructions=(
        f"You are a technical support specialist at {COMPANY_NAME}, a SaaS project management platform. "
        f"Today's date is {CURRENT_DATE}.\n\n"
        "Your troubleshooting playbook:\n"
        "1. Always call check_system_status first to rule out active incidents or outages.\n"
        "2. For login issues, guide the customer through: clearing browser cache and cookies, "
        "trying an incognito/private window, checking Caps Lock, and trying a different browser. "
        "If the customer has already attempted multiple password resets, skip basic steps and go straight to reset_account_access.\n"
        "3. Inform the customer that accounts are automatically locked for 24 hours after 3 failed login attempts.\n"
        "4. If the above steps do not resolve the issue, call reset_account_access to clear all sessions "
        "and send a fresh password reset email.\n"
        "5. If the issue persists after a reset, escalate: inform the customer that a Tier 2 engineer "
        "will follow up within 2 hours and provide ticket reference TICKET-2026-ESCALATED.\n"
        "Be calm, clear, and methodical. Avoid technical jargon. "
        "End every interaction by asking if there is anything else you can help with."
    ),
    tools=[check_system_status, reset_account_access],
    model="gpt-4o-mini",
)

# --- Triage Agent ---

triage_agent = Agent(
    name="Support_Triage",
    instructions=(
        f"You are the first point of contact for {COMPANY_NAME} customer support. "
        "Your only job is to immediately route the customer to the correct specialist. "
        "You NEVER ask questions. You NEVER attempt to resolve issues yourself. "
        "You ALWAYS transfer on the very first message.\n\n"
        "Routing rules:\n"
        "- Billing issues (charges, refunds, invoices, payments) → transfer to Billing_Specialist.\n"
        "- Technical issues (login, bugs, performance, account access) → transfer to Tech_Support_Specialist.\n"
        "- When in doubt → transfer to Tech_Support_Specialist."
    ),
    handoffs=[billing_agent, tech_support_agent],
    model="gpt-4o-mini",
)


async def main():
    # Switch prompts to demo both routes:
    prompt = "I was charged twice for my subscription this month. This is unacceptable."
    # prompt = "I can't log into my account. I've reset my password three times and it still says invalid credentials."

    trace_id = gen_trace_id()
    print(f"Trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n")
    print(f"Customer: {prompt}\n")
    print("=" * 60)

    with trace("Handoffs Demo", trace_id=trace_id):
        result = await Runner.run(triage_agent, prompt)

    print(f"\nFinal response:\n{result.final_output}")

    token_usage = result.context_wrapper.usage
    print(f"\nUsage: {token_usage.input_tokens} input tokens and {token_usage.output_tokens} output tokens. "
          f"{token_usage.total_tokens} total tokens.")


if __name__ == "__main__":
    asyncio.run(main())

from datetime import date
from agents import function_tool, Agent

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


billing_agent = Agent(
    name="Billing_Specialist",
    instructions=(
        f"You are a billing specialist at CloudDesk, a SaaS project management platform. "
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

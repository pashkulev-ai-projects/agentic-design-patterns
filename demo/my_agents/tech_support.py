from datetime import date
from agents import function_tool, Agent


CURRENT_DATE = date.today()

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

COMPANY_NAME = "CloudDesk"

tech_support_agent = Agent(
    name="Tech_Support_Specialist",
    instructions=(
        f"You are a technical support specialist at CloudDesk, a SaaS project management platform. "
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

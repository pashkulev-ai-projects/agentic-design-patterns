import os
import resend
from agents import function_tool
from demo.utils.svg_assets import inject_svg_assets
from dotenv import load_dotenv

load_dotenv(override=True)

resend.api_key = os.environ["RESEND_API_KEY"]

FROM_EMAIL = "ivan@ivanpashkulev.com"
TO_EMAIL = "ivan.pashkulev@ict.eu"


@function_tool
def send_email(subject: str, content: str) -> str:
    """Send an email to the configured recipient with the given subject and content."""
    params: resend.Emails.SendParams = {
        "from": FROM_EMAIL,
        "to": [TO_EMAIL],
        "subject": subject,
        "html": inject_svg_assets(content)
    }
    email = resend.Emails.send(params)
    return f"Email sent successfully. ID: {email['id']}"
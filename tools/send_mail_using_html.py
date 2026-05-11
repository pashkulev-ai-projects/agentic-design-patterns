import os
import re
from pathlib import Path
import resend
from agents import function_tool
from dotenv import load_dotenv

load_dotenv(override=True)

resend.api_key = os.environ["RESEND_API_KEY"]

FROM_EMAIL = os.environ["EMAIL_FROM"]
TO_EMAIL = os.environ["EMAIL_TO"]

_IMAGES_DIR = Path(__file__).parent.parent / "assets" / "images"

_SVG_STYLES = {
    "logo_strypes.svg": "height:69px;",
    "header_angle.svg": "height:28px;max-width:150px;object-fit:contain;",
    "footer_line.svg":  "width:100%;display:block;",
}


def _inject_svg_assets(html: str) -> str:
    for filename, style in _SVG_STYLES.items():
        svg_content = (_IMAGES_DIR / filename).read_text()
        match = re.search(r'(?:xlink:href|href)=["\']([^"\']+)["\']', svg_content)
        if not match:
            continue
        replacement = f'<img src="{match.group(1)}" style="{style}">'
        pattern = rf'<img[^>]*src=["\'](?:images/)?{re.escape(filename)}["\'][^>]*/?>'
        html = re.sub(pattern, replacement, html)
    return html


@function_tool
def send_email(subject: str, content: str) -> str:
    """Send an email to the configured recipient with the given subject and content."""
    params: resend.Emails.SendParams = {
        "from": FROM_EMAIL,
        "to": [TO_EMAIL],
        "subject": subject,
        "html": _inject_svg_assets(content)
    }
    email = resend.Emails.send(params)
    return f"Email sent successfully. ID: {email['id']}"
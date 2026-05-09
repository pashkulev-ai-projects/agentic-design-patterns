import re
from pathlib import Path

_IMAGES_DIR = Path(__file__).parent.parent / "assets" / "images"

_SVG_STYLES = {
    "logo_strypes.svg":  "height:69px;",
    "header_angle.svg":  "height:28px;max-width:150px;object-fit:contain;",
    "footer_line.svg":   "width:100%;display:block;",
}


def _extract_data_uri(svg_content: str) -> str | None:
    """Extract the base64 data URI embedded inside an SVG <image> element."""
    match = re.search(r'(?:xlink:href|href)=["\']([^"\']+)["\']', svg_content)
    return match.group(1) if match else None


def inject_svg_assets(html: str) -> str:
    """Replace <img src="images/xxx.svg"> placeholders with <img src="data:image/png;base64,...">."""
    for filename, style in _SVG_STYLES.items():
        svg_content = (_IMAGES_DIR / filename).read_text()
        data_uri = _extract_data_uri(svg_content)
        if not data_uri:
            continue
        replacement = f'<img src="{data_uri}" style="{style}">'
        pattern = rf'<img[^>]*src=["\'](?:images/)?{re.escape(filename)}["\'][^>]*/?>'
        html = re.sub(pattern, replacement, html)
    return html

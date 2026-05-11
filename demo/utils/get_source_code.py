from pathlib import Path


def get_source_code(file_name: str) -> str:
    code_review_dir = Path(__file__).parent.parent / "assets" / "code_review"
    file_path = code_review_dir / file_name
    source_code = file_path.read_text()

    return source_code
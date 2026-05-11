import os
import httpx
from agents import function_tool
from dotenv import load_dotenv

load_dotenv(override=True)


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
        f"{result['title']}\n{result['link']}\n{result.get('snippet', '')}"
        for result in results
    )
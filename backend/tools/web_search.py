from langchain_core.tools import tool
from tavily import TavilyClient
import os

from dotenv import load_dotenv

load_dotenv()


@tool
def web_search(query: str) -> str:
    """
    Search the web for technical information when the OpsMind
    knowledge base does not contain enough information.

    The search can find official documentation, vendor documentation,
    Stack Overflow, GitHub, and other relevant technical sources.

    Returns search results including the title, URL, source, and content.
    """

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        return "Web search is unavailable because TAVILY_API_KEY is not configured."

    client = TavilyClient(api_key=api_key)

    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=5,
        include_answer=False
    )

    results = response.get("results", [])

    if not results:
        return "No useful web results were found."

    output = []

    for result in results:

        title = result.get("title", "")
        url = result.get("url", "")
        content = result.get("content", "")

        output.append(
            f"Title: {title}\n"
            f"URL: {url}\n"
            f"Content:\n{content}"
        )

    return "\n\n---\n\n".join(output)
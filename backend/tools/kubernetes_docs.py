import os
from urllib.parse import urlparse

from dotenv import load_dotenv
from tavily import TavilyClient
from langchain_core.tools import tool


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# TAVILY CLIENT
# ============================================================

tavily_client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


# ============================================================
# OFFICIAL KUBERNETES HOST CHECK
# ============================================================

def is_official_kubernetes_docs(url: str) -> bool:
    """
    Return True only for official Kubernetes documentation hosts.

    Allowed:
        kubernetes.io
        docs.kubernetes.io
        v1-33.docs.kubernetes.io
        v1-32.docs.kubernetes.io
        etc.

    Rejected:
        discuss.kubernetes.io
        blog.kubernetes.io
        other websites
    """

    if not url:
        return False

    hostname = (
        urlparse(url).hostname or ""
    ).lower()

    # Main Kubernetes domain
    if hostname == "kubernetes.io":
        return True

    # Official documentation subdomain
    if hostname == "docs.kubernetes.io":
        return True

    # Versioned documentation
    if hostname.endswith(".docs.kubernetes.io"):
        return True

    return False


# ============================================================
# KUBERNETES DOCUMENTATION SEARCH
# ============================================================

@tool
def search_kubernetes_docs(query: str) -> str:
    """
    Search the official Kubernetes documentation.

    USE THIS TOOL ONLY when the user's question is specifically about
    Kubernetes concepts, Kubernetes resources, Kubernetes behavior,
    Kubernetes configuration, Kubernetes commands, Kubernetes errors,
    Kubernetes Pods, Deployments, Services, or Kubernetes troubleshooting.

    DO NOT USE THIS TOOL for questions primarily about:
    - Redis
    - Docker
    - Linux
    - databases
    - general DevOps topics
    - applications unrelated to Kubernetes

    If the question is not specifically about Kubernetes, do not call
    this tool.
    """

    if not query or not query.strip():
        return (
            "No Kubernetes documentation query was provided."
        )

    try:

        response = tavily_client.search(
            query=query,
            include_domains=[
                "kubernetes.io"
            ],
            max_results=5,
            search_depth="advanced"
        )

    except Exception as error:

        return (
            "Unable to search the official Kubernetes "
            f"documentation: {error}"
        )

    results = response.get(
        "results",
        []
    )

    # --------------------------------------------------------
    # Filter official Kubernetes documentation
    # --------------------------------------------------------

    official_results = []

    for result in results:

        url = result.get(
            "url",
            ""
        )

        if is_official_kubernetes_docs(url):

            official_results.append(
                result
            )

    if not official_results:

        return (
            "No relevant information was found in the "
            "official Kubernetes documentation."
        )

    # --------------------------------------------------------
    # Format results
    # --------------------------------------------------------

    output = [
        "Official Kubernetes documentation:",
        ""
    ]

    for result in official_results:

        title = result.get(
            "title",
            "Untitled"
        )

        url = result.get(
            "url",
            ""
        )

        content = result.get(
            "content",
            ""
        ).strip()

        output.append(
            f"Title: {title}"
        )

        output.append(
            f"URL: {url}"
        )

        output.append(
            "Content:"
        )

        output.append(
            content
        )

        output.append("")
        output.append("---")
        output.append("")

    return "\n".join(output)
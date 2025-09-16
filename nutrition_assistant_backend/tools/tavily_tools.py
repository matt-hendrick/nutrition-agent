import os
from dotenv import load_dotenv

from tavily import TavilyClient

load_dotenv()

TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "")
if not TAVILY_API_KEY:
    raise RuntimeError("TAVILY_API_KEY environment variable not set.")

# see the Tavily docs for more details https://github.com/tavily-ai/tavily-python
# https://docs.tavily.com/documentation/api-reference/introduction
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)


def tavily_search(query: str):
    """Perform a simple Tavily search."""
    return tavily_client.search(query)

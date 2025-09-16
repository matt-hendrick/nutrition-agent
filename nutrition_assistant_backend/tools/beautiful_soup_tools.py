import requests
from bs4 import BeautifulSoup


def fetch_clean_text(url: str) -> str:
    """
    Fetches the HTML from a URL and extracts the main visible text content.
    Args:
        url (str): The URL to fetch.
    Returns:
        str: Cleaned text content from the page.
    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove non-visible elements
        for element in soup(["script", "style", "head", "meta"]):
            element.decompose()

        # Extract and clean text
        text = soup.get_text(separator="\n")
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = "\n".join(chunk for chunk in chunks if chunk)

        return clean_text

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        raise

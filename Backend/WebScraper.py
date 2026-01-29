import requests
from bs4 import BeautifulSoup
import trafilatura
import logging

def scrape_url(url, timeout=10):
    """
    Attempts to extract the main meaningful text from a URL.
    Uses trafilatura for high-quality content extraction.
    """
    try:
        # Standard headers to avoid bot detection
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=timeout)
        if response.status_code == 200:
            # Try trafilatura first as it's excellent at removing boilerplate
            downloaded = response.text
            result = trafilatura.extract(downloaded)
            
            if result:
                return result[:3000] # Limit to 3000 chars per site for LLM context
            
            # Fallback to BeautifulSoup if trafilatura fails
            soup = BeautifulSoup(downloaded, 'html.parser')
            # Remove scripts and styles
            for script in soup(["script", "style"]):
                script.decompose()
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            return text[:2000]
            
        return f"Failed to retrieve content from {url} (Status: {response.status_code})"
    except Exception as e:
        return f"Error scraping {url}: {str(e)}"

def research_topic(urls):
    """Scrapes multiple URLs and returns a consolidated context block."""
    context = ""
    # Only scrape the top 2-3 results to keep it fast and within token limits
    for url in urls[:3]:
        content = scrape_url(url)
        context += f"\n--- Source: {url} ---\n{content}\n"
    return context

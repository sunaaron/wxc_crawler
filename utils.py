from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
from bs4 import BeautifulSoup

from typing import Optional

async def fetch_page_content(url: str) -> Optional[str]:
    """Fetch HTML content from the given URL."""
    try:
        browser_config = BrowserConfig()
        run_config = CrawlerRunConfig()

        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(
                url=url,
                config=run_config
            )
            return result.html
    except Exception as e:
        print(f"Error fetching page content: {e}")
        return None

def parse_html_content(html_content: str) -> BeautifulSoup:
    """Parse HTML content using BeautifulSoup."""
    return BeautifulSoup(html_content, 'html.parser')

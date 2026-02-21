from crawl4ai import AsyncWebCrawler
from bs4 import BeautifulSoup

async def crawl_post(post_url: str):
    async with AsyncWebCrawler() as crawler:
        # Perform the crawl
        result = await crawler.arun(
            url=post_url
        )
        
        if result.success:
            print(f"Successfully crawled: {result.url}")
            
            # Using BeautifulSoup for robust extraction of WXC structure
            soup = BeautifulSoup(result.html, 'html.parser')
            
            # Extract main post content and title
            title_el = soup.select_one('h1.title')
            post_title = title_el.get_text(strip=True) if title_el else ""
            
            content_el = soup.select_one('#msgbodyContent')
            post_content = content_el.get_text(strip=True) if content_el else ""
            
            # Extract all comment titles from the thread container
            comment_els = soup.select('#comment a.post')
            comment_titles = [el.get_text(strip=True) for el in comment_els]
            
            # Format the final data structure
            return {
                "post_title": post_title,
                "post_content": post_content,
                "comments": comment_titles
            } 
        else:
            print(f"Failed to crawl: {result.url}")

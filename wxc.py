import asyncio
from index_crawler import crawl_index

async def main():
    """Main function to orchestrate the web scraping process."""
    # Crawl page 1
    print("Crawling page 1...")
    await crawl_index(1)

if __name__ == "__main__":
    asyncio.run(main())

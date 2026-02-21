import asyncio
from datetime import datetime, timedelta
from index_crawler import crawl_index
from utils import fetch_page_content, parse_html_content
from constants import ZNJY_BASE_URL, PAGE_PARAM, DEFAULT_PAGE_NUMBER
import re

async def get_posts_with_date_filter(pages_to_crawl: range, target_date_offset: int = 3):
    """
    Crawl index pages and filter posts by date.
    
    Args:
        pages_to_crawl: Range of page numbers to crawl (e.g., range(3, 11) for pages 3-10)
        target_date_offset: How many days back from today to filter for (default 3)
    """
    
    # Calculate the target date (today - offset days)
    target_date = datetime.now() - timedelta(days=target_date_offset)
    target_date_str = target_date.strftime("%m/%d/%Y")
    
    print(f"Target date for filtering: {target_date_str}")
    
    # Store all results
    all_results = {}
    
    # Crawl each page in the specified range
    for page_num in pages_to_crawl:
        print(f"\n--- Crawling page {page_num} ---")
        
        # Get results from crawl_index function
        result = await crawl_index(page_num)
        
        # Filter results by target date
        filtered_results = {}
        for date_str, href_list in result.items():
            if date_str == target_date_str:
                filtered_results[date_str] = href_list
                print(f"Found {len(href_list)} posts with date {date_str}")
        
        # Merge filtered results into all_results
        for date_str, href_list in filtered_results.items():
            if date_str not in all_results:
                all_results[date_str] = []
            all_results[date_str].extend(href_list)
    
    return all_results

async def main():
    """Main function to execute the date-filtered crawling."""
    
    # Define pages to crawl (3 to 10 inclusive)
    pages_to_crawl = range(3, 11)  # This creates [3, 4, 5, 6, 7, 8, 9, 10]
    
    # Get posts with date filter (3 days back from today)
    filtered_results = await get_posts_with_date_filter(pages_to_crawl, target_date_offset=3)
    
    # Display results
    print("\n=== FINAL RESULTS ===")
    if filtered_results:
        for date_str, href_list in filtered_results.items():
            print(f"\nPosts from {date_str}:")
            for i, href in enumerate(href_list, 1):
                print(f"  {i}. {href}")
    else:
        print("No posts found matching the date filter.")
    
    return filtered_results

if __name__ == "__main__":
    results = asyncio.run(main())
#!/usr/bin/env python3
"""
Main script to crawl index pages 3-10 and filter posts by date.
Today's date is when the main function is called.
Filter posts where date_str = today_date - 3
"""

import asyncio
from datetime import datetime, timedelta
from index_crawler import crawl_index

async def main():
    """Main function that implements the requirements."""
    
    # Calculate target date (3 days back from today)
    target_date = datetime.now() - timedelta(days=3)
    target_date_str = target_date.strftime("%m/%d/%Y")
    
    print(f"Today's date: {datetime.now().strftime('%m/%d/%Y')}")
    print(f"Target date (3 days back): {target_date_str}")
    
    # Crawl pages 3 to 10
    print("\n--- Crawling pages 3 to 10 ---")
    
    all_matching_posts = {}
    
    # Loop through pages 3 to 10
    for page_num in range(3, 11):  # Pages 3 through 10 inclusive
        print(f"\nCrawling page {page_num}...")
        
        # Get results from crawl_index function
        result = await crawl_index(page_num)
        
        # Filter for posts with target date
        matching_posts = {}
        for date_str, href_list in result.items():
            if date_str == target_date_str:
                matching_posts[date_str] = href_list
                print(f"Found {len(href_list)} posts with date {date_str}")
        
        # Add matching posts to overall results
        for date_str, href_list in matching_posts.items():
            if date_str not in all_matching_posts:
                all_matching_posts[date_str] = []
            all_matching_posts[date_str].extend(href_list)
    
    # Display final results
    print("\n=== FINAL RESULTS ===")
    if all_matching_posts:
        for date_str, href_list in all_matching_posts.items():
            print(f"\nPosts from {date_str}:")
            for i, href in enumerate(href_list, 1):
                print(f"  {i}. {href}")
    else:
        print("No posts found matching the date filter.")
    
    return all_matching_posts

if __name__ == "__main__":
    results = asyncio.run(main())
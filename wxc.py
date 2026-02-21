#!/usr/bin/env python3
"""
Main script to crawl index pages 1-10 and filter posts by date.
Today's date is when the main function is called.
Filter posts where date_str = today_date - 3
"""

import asyncio
from datetime import datetime, timedelta
import sys
from constants import ZNJY_CATEGORY
from index_crawler import crawl_index
from post_crawler import crawl_post
import mysql_writer

async def fetch_post_data(href_list, target_date_str):
    """Fetch detailed data for each post URL."""
    post_data_results = []
    
    for href in href_list:
        print(f"Fetching data for post: {href}")
        try:
            # Call the post_crawler to get post data
            post_data = await crawl_post(href)
            if len(post_data["comments"]) == 0:
                 print(f"Skipping empty post: {href}")
            elif post_data:
                post_data_results.append({
                    "url": href,
                    "data": post_data
                })
            else:
                print(f"Failed to fetch data for: {href}")
        except Exception as e:
            print(f"Error fetching data for {href}: {e}")
    
    return post_data_results

async def crawl_and_filter_posts(pages_to_crawl, target_date_str):
    """Crawl pages and filter posts by date."""
    all_matching_posts = {}
    
    # Loop through pages 1 to 10
    for page_num in pages_to_crawl:  # Pages 1 through 10 inclusive
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
    
    return all_matching_posts

async def main(target_date_str=None):
    """Main function that implements the requirements."""
    
    # If no date string provided, use default logic (today - 3 days)
    if target_date_str is None:
        # Calculate target date (3 days back from today)
        target_date = datetime.now() - timedelta(days=3)
        target_date_str = target_date.strftime("%m/%d/%Y")
        
        print(f"Today's date: {datetime.now().strftime('%m/%d/%Y')}")
        print(f"Target date (3 days back): {target_date_str}")
    else:
        # Use the provided date string
        print(f"Using provided target date: {target_date_str}")
    
    # Convert the target date to mmddyyyy format for storage
    # Extract month, day, year from the target_date_str (format mm/dd/yyyy)
    if "/" in target_date_str:
        parts = target_date_str.split("/")
        if len(parts) == 3:
            # Convert mm/dd/yyyy to mmddyyyy
            date_for_storage = parts[0] + parts[1] + parts[2]
        else:
            date_for_storage = "00000000"  # Default fallback
    else:
        date_for_storage = "00000000"  # Default fallback
    
    # Crawl pages 1 to 10 and filter by date
    print("\n--- Crawling pages 1 to 10 ---")
    
    pages_to_crawl = range(1, 11)  # Pages 1 through 10 inclusive
    all_matching_posts = await crawl_and_filter_posts(pages_to_crawl, target_date_str)
    
    # Display final results
    print("\n=== FINAL RESULTS ===")
    if all_matching_posts:
        for date_str, href_list in all_matching_posts.items():
            print(f"\nPosts from {date_str}:")
            for i, href in enumerate(href_list, 1):
                print(f"  {i}. {href}")
    else:
        print("No posts found matching the date filter.")
    
    # If we have results, fetch the actual post data for each href
    if all_matching_posts:
        print("\n--- Fetching Post Data ---")
        post_data_results = {}
        
        for date_str, href_list in all_matching_posts.items():

            post_data_results[date_str] = await fetch_post_data(href_list, target_date_str)
        
        # Store data in MySQL database
        print("\n--- Storing Data in MySQL ---")
        
        # Flatten all post data for database insertion
        all_post_data = []
        for date_str, posts in post_data_results.items():
            all_post_data.extend(posts)
        
        if all_post_data:
            # Insert all posts into database
            success_count = mysql_writer.insert_multiple_posts(all_post_data, ZNJY_CATEGORY, date_for_storage)
            print(f"Successfully stored {success_count} posts in MySQL database")
        else:
            print("No post data to store in database")
    
    return all_matching_posts

if __name__ == "__main__":
    # Check if a date string was provided as command line argument
    target_date_str = None
    if len(sys.argv) > 1:
        # Validate that the argument is in mmddyyyy format
        date_arg = sys.argv[1]
        if len(date_arg) == 8 and date_arg.isdigit():
            # Convert mmddyyyy to mm/dd/yyyy format
            try:
                month = date_arg[0:2]
                day = date_arg[2:4]
                year = date_arg[4:8]
                target_date_str = f"{month}/{day}/{year}"
            except:
                print("Invalid date format. Please use mmddyyyy format.")
                sys.exit(1)
        else:
            print("Invalid date format. Please use mmddyyyy format (e.g., 02212025).")
            sys.exit(1)
    
    results = asyncio.run(main(target_date_str))
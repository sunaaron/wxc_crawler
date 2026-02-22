import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
from bs4 import BeautifulSoup
import re
from typing import List, Optional, Tuple, Dict
import sys
from datetime import datetime, timedelta

# Import the helper functions from utils module
from utils import fetch_page_content, parse_html_content
from constants import ZNJY_BASE_URL, PAGE_PARAM, DEFAULT_PAGE_NUMBER

async def extract_div_elements(soup: BeautifulSoup) -> List:
    """Extract all div elements with class 'odd' or 'even'."""
    odd_divs = soup.find_all('div', class_='odd')
    even_divs = soup.find_all('div', class_='even')
    
    # Combine both lists
    div_elements = []
    div_elements.extend(odd_divs)
    div_elements.extend(even_divs)
    
    return div_elements

async def extract_anchor_hrefs(div_elements: List) -> List:
    """Extract anchor elements and their href attributes."""
    href_list = []
    
    for i, div in enumerate(div_elements):
        # Find the first <a> tag within this div
        first_a_tag = div.find('a')
        if first_a_tag:            
            # Extract href attribute and append to href_list
            href = first_a_tag.get('href')
            if href:
                href_list.append(href)
    
    return href_list

def extract_date_strings(div_elements: List) -> List:
    """Extract date strings in mm/dd/yyyy format from div elements, but store them in yyyy/mm/dd format."""
    date_strings = []
    
    for i, div in enumerate(div_elements):
        div_text = div.get_text()
        # Pattern to match mm/dd/yyyy format
        date_pattern = r'\b(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])/(\d{4})\b'
        match = re.search(date_pattern, div_text)
        if match:
            date_str = match.group(0)
            month = date_str[0:2]
            day = date_str[3:5]
            year = date_str[6:10]
            new_date_str = f"{year}/{month}/{day}"  
            date_strings.append(new_date_str)
            print(f"Div {i+1} - Date found: {new_date_str}")
        else:
            print(f"Div {i+1} - No date found")
    
    return date_strings

async def crawl_index(page_number: int) -> Dict[str, List[str]]:
    """Main function to orchestrate the web scraping process for a specific page.
    
    Returns:
        Dict[str, List[str]]: Dictionary mapping date strings to lists of hrefs
    """
    # Construct URL with page number
    if page_number <= DEFAULT_PAGE_NUMBER:
        url = ZNJY_BASE_URL
    else:
        url = f"{ZNJY_BASE_URL}{PAGE_PARAM}{page_number}"
    
    print(f"Scraping page {page_number} with URL: {url}")
    
    # Fetch HTML content
    html_content = await fetch_page_content(url)
    if not html_content:
        print("Failed to fetch HTML content")
        return {}
    
    # Parse HTML
    soup = parse_html_content(html_content)
    
    # Extract div elements
    div_elements = await extract_div_elements(soup)
    print(f"Found {len(div_elements)} div elements")
    
    # Extract hrefs
    href_list = await extract_anchor_hrefs(div_elements)
    
    # Extract date strings
    date_strings = extract_date_strings(div_elements)
    
    # Merge href_list and date_strings into a single dictionary
    result_dict = {}
    
    # For each date string, create an entry with the href list
    # This assumes that each date corresponds to a div element and its href
    for i, date_str in enumerate(date_strings):
        if date_str not in result_dict:
            result_dict[date_str] = []
        # Add the corresponding href if available
        if i < len(href_list):
            result_dict[date_str].append(ZNJY_BASE_URL + href_list[i].lstrip('./'))
    
    # Print results
    print(f"\nTotal hrefs found: {len(href_list)}")
    for i, href in enumerate(href_list):
        print(f"Href {i+1}: {href}")
    
    return result_dict

async def crawl_index_with_date_filter(pages_to_crawl: range, target_date_offset: int = 3) -> Dict[str, List[str]]:
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

if __name__ == "__main__":
    # Default to page 1 if no argument provided
    page_number = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PAGE_NUMBER
    result = asyncio.run(crawl_index(page_number))
    print(f"\nResult dictionary: {result}")

# Web Crawler with Date Filtering

This project provides a web crawler that can crawl index pages and filter posts by date.

## Features

1. **Default behavior**: When no arguments are provided, it crawls pages 3-10 and filters posts for the date that is 3 days back from today
2. **Custom date filtering**: When provided with a date string in `mmddyyyy` format, it filters posts for that specific date

## Usage

### Default behavior (3 days back from today)
```bash
python wxc.py
```

### Custom date filtering
```bash
python wxc.py 02212025
```

This will filter posts for February 21, 2025 (format mmddyyyy).

## Files

- `wxc.py`: Main script that implements the date filtering functionality
- `index_crawler.py`: Handles crawling of index pages and extracting date information
- `utils.py`: Utility functions for fetching page content and parsing HTML
- `constants.py`: Configuration constants like base URLs

## Requirements

- Python 3.7+
- crawl4ai>=0.8.0
- beautifulsoup4>=4.9.3

## How it works

1. The crawler visits pages 3 through 10 of the target website
2. It extracts date information from each post (in mm/dd/yyyy format)
3. It filters posts based on the specified date criteria:
   - If no argument provided: Filters for posts from 3 days ago
   - If argument provided: Filters for posts from the specified date

## Example Output

```
Today's date: 02242025
Target date (3 days back): 02212025

--- Crawling pages 3 to 10 ---

Crawling page 3...
Found 2 posts with date 02/21/2025
...
```
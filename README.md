# Web Crawler with Date Filtering

This project provides a web crawler that can crawl index pages and filter posts by date.

## Features

1. **Default behavior**: When no arguments are provided, it crawls pages 3-10 and filters posts for the date that is 3 days back from today
2. **Custom date filtering**: When provided with a date string in `mmddyyyy` format, it filters posts for that specific date
3. **Post data fetching**: For each matching post URL, it fetches the actual post content
4. **MySQL Database Storage**: Stores all crawled data in a remote MySQL database

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

## MySQL Database Setup

The crawler stores data in a remote MySQL instance at:
- Host: 192.168.86.55
- Port: 3306
- Database: wxc_crawler

### Table Structure
The crawler creates and uses one table named `wxc_posts` with the following columns:
- `id` (INT AUTO_INCREMENT PRIMARY KEY)
- `category` (VARCHAR(255))
- `post_url` (VARCHAR(500))
- `post_title` (VARCHAR(500))
- `post_body` (TEXT)
- `comments` (TEXT)
- `llm_summary` (TEXT)
- `created_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)

## Files

- `wxc.py`: Main script that implements the date filtering functionality and post data fetching
- `index_crawler.py`: Handles crawling of index pages and extracting date information
- `post_crawler.py`: Fetches detailed content for individual posts
- `mysql_writer.py`: Handles MySQL database connection and data storage
- `utils.py`: Utility functions for fetching page content and parsing HTML
- `constants.py`: Configuration constants like base URLs

## Requirements

- Python 3.7+
- crawl4ai>=0.8.0
- beautifulsoup4>=4.9.3
- mysql-connector-python>=8.0.0

## How it works

1. The crawler visits pages 3 through 10 of the target website
2. It extracts date information from each post (in mm/dd/yyyy format)
3. It filters posts based on the specified date criteria:
   - If no argument provided: Filters for posts from 3 days ago
   - If argument provided: Filters for posts from the specified date
4. For each matching post URL, it fetches the detailed content using `post_crawler.py`
5. All crawled data is stored in the MySQL database at 192.168.86.55:3306

## Example Output

```
Today's date: 02242025
Target date (3 days back): 02212025

--- Crawling pages 3 to 10 ---

Crawling page 3...
Found 2 posts with date 02/21/2025
...

=== FINAL RESULTS ===

Posts from 02/21/2025:
  1. https://bbs.wenxuecity.com/znjy/thread-12345.html
  2. https://bbs.wenxuecity.com/znjy/thread-12346.html

--- Fetching Post Data ---
Fetching data for post: https://bbs.wenxuecity.com/znjy/thread-12345.html

--- Storing Data in MySQL ---
wxc_posts table created successfully
Successfully inserted post: https://bbs.wenxuecity.com/znjy/thread-12345.html
Successfully inserted post: https://bbs.wenxuecity.com/znjy/thread-12346.html
Successfully stored 2 posts in MySQL database
```
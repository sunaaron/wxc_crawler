"""Constants used throughout the web scraping application."""

# Base URL for the target website
ZNJY_BASE_URL = "https://bbs.wenxuecity.com/znjy/"
ZNJY_CATEGORY = 'znjy'

TZLC_BASE_URL = "https://bbs.wenxuecity.com/tzlc/"
TZLC_CATEGORY = 'tzlc'

# Page parameter for pagination
PAGE_PARAM = "?page="

# Default page number
DEFAULT_PAGE_NUMBER = 1

# MySQL Database Configuration
MYSQL_HOST = '192.168.86.55'
MYSQL_PORT = 3306
MYSQL_DATABASE = 'wxc_crawler'
MYSQL_USER = 'crawler_admin'
MYSQL_PASSWORD = '123'

# Table Configuration
WXC_POSTS_TABLE = 'wxc_posts'

# Crawler Configuration
MIN_PAGE_NUMBER = 1
MAX_PAGE_NUMBER = 10

# Default Values
DEFAULT_CATEGORY = 'general'

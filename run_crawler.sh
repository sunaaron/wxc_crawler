#!/bin/bash

# Simple shell script to run the web crawler with different options

echo "Web Crawler with Date Filtering"
echo "================================"

if [ $# -eq 0 ]; then
    echo "No arguments provided. Running with default behavior (3 days back from today)."
    echo "Usage: ./run_crawler.sh [mmddyyyy]"
    echo ""
    echo "Examples:"
    echo "  ./run_crawler.sh                 # Use default (3 days back)"
    echo "  ./run_crawler.sh 02212025        # Filter for Feb 21, 2025"
    echo ""
    
    echo "Running default crawl..."
    python3 wxc.py
else
    echo "Running with custom date: $1"
    python3 wxc.py $1
fi
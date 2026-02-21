import asyncio
from index_crawler import crawl_index
from post_crawler import crawl_post 
from post_analyzer import analyze_with_llm

async def main():
    """Main function to orchestrate the web scraping process."""
    # # Crawl page 1
    # print("Crawling page 1...")
    # result_1 = await crawl_index(1)
    
    # # Crawl page 2
    # print("\nCrawling page 2...")
    # result_2 = await crawl_index(2)
    
    # Crawl page 3
    print("\nCrawling page 3...")
    result_3 = await crawl_index(3)
    
    # Process results by calling crawl_post for each href
    print("\n=== PROCESSING POSTS ===")
    
    # Process results from page 3
    if result_3:
        print("\nProcessing page 3 posts:")
        for date_str, href_list in result_3.items():
            print(f"Date: {date_str}")
            for href in href_list:
                print(f"  Processing post: {href}")
                try:
                    post_data = await crawl_post(href)
                    print(f"  Post data retrieved: {post_data}")
                    analyzesis_result = analyze_with_llm(post_data)
                    print(f"  Analysis result: {analyzesis_result}")
                    break
                except Exception as e:
                    print(f"  Error processing post {href}: {e}")
                break

if __name__ == "__main__":
    asyncio.run(main())

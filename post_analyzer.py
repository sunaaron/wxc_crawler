import asyncio
import json
from bs4 import BeautifulSoup
from crawl4ai import AsyncWebCrawler
from openai import OpenAI

def analyze_with_llm(post_data):
    """
    Analyze the extracted post data using a local LLM.
    
    Args:
        post_data: Dictionary containing post_title, post_content, and comments
    
    Returns:
        str: Analysis result from the LLM
    """
    # Initialize OpenAI client pointing to local LLM server
    client = OpenAI(
        base_url="http://127.0.0.1:1234/v1",
        api_key="not-needed"  # Local LLM doesn't require a real API key
    )
    
    # Format the post data for analysis
    prompt = f"""这是一个来自文学城子女教育的论坛帖子。请首先判断这个帖子是否与教育, 留学, 升学, 育儿, 择校, 职业规划, 心理健康等相关，如果不是，请直接返回“与教育无关”。如果是，请总结这篇论坛的帖子。根据原贴的题目和内容，以及回帖的内容，给出讨论的话题和结论。

题目: {post_data['post_title']}

内容: {post_data['post_content']}

回帖 ({len(post_data['comments'])} 条):
{chr(10).join(f"{i+1}. {comment}" for i, comment in enumerate(post_data['comments']))}
"""
    
    try:
        # Call the local LLM
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes forum posts and discussions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=65536
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error analyzing with LLM: {str(e)}"

def debug_analyze_with_llm(post_data):
    """
    Debug the analysis result, e.g., print it or save to a file.
    
    Args:
        post_data_dict: The final structured data dictionary from crawling and analysis
    """
    # Save the final structured data to a JSON file
    with open("wxc_data.json", "w", encoding="utf-8") as f:
        json.dump(post_data, f, indent=2, ensure_ascii=False)
    
    print(f"Extraction complete! Found {len(post_data['comments'])} comments.")
    print(f"Results saved to wxc_data.json")
    
    # Output a preview
    print("\nPreview of extracted data:")
    print(json.dumps(post_data, indent=2, ensure_ascii=False))
    
    # Analyze with local LLM
    print("\n" + "="*60)
    print("Analyzing with local LLM...")
    print("="*60)
    
    analysis = analyze_with_llm(post_data)
    
    # Save analysis to file
    with open("wxc_analysis.txt", "w", encoding="utf-8") as f:
        f.write(f"Analysis of: {post_data['post_title']}\n")
        f.write("="*60 + "\n\n")
        f.write(analysis)
    
    print("\nAnalysis saved to wxc_analysis.txt")
    print("\nAnalysis:")
    print(analysis)
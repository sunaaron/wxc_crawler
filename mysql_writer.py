#!/usr/bin/env python3
"""
MySQL writer to store crawled posts in the wxc_posts table.
"""

import mysql.connector
from mysql.connector import Error
import json
from datetime import datetime

def create_connection():
    """Create connection to MySQL database."""
    try:
        connection = mysql.connector.connect(
            host='192.168.86.55',
            port=3306,
            database='wxc_crawler',
            user='crawler_admin',  # Replace with actual username
            password='123'  # Replace with actual password
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_wxc_posts_table():
    """Create the wxc_posts table if it doesn't exist."""
    connection = create_connection()
    if connection is None:
        return False
    
    try:
        cursor = connection.cursor()
        
        create_table_query = """
        CREATE TABLE IF NOT EXISTS wxc_posts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            category VARCHAR(255),
            post_url VARCHAR(500),
            post_title VARCHAR(500),
            post_body TEXT,
            comments TEXT,
            llm_summary TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )"""
        
        cursor.execute(create_table_query)
        connection.commit()
        print("wxc_posts table created successfully")
        return True
        
    except Error as e:
        print(f"Error creating wxc_posts table: {e}")
        return False
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def insert_post_data(post_data, category="znjy"):
    """Insert post data into wxc_posts table."""
    connection = create_connection()
    if connection is None:
        return False
    
    try:
        cursor = connection.cursor()
        
        # Prepare the insert query
        insert_query = """
        INSERT INTO wxc_posts 
        (category, post_url, post_title, post_body, comments, llm_summary)
        VALUES (%s, %s, %s, %s, %s, %s)"""
        
        # Extract data from post_data structure
        category = category  # Use the passed category value
        post_url = post_data.get('url', '')
        post_title = post_data.get('data', {}).get('post_title', '')
        post_body = post_data.get('data', {}).get('post_content', '')
        comments = json.dumps(post_data.get('data', {}).get('comments', []))
        llm_summary = ""  # Empty for now, can be populated with LLM analysis
        
        # Execute the insert
        cursor.execute(insert_query, (
            category,
            post_url,
            post_title,
            post_body,
            comments,
            llm_summary
        ))
        
        connection.commit()
        print(f"Successfully inserted post: {post_url}")
        return True
        
    except Error as e:
        print(f"Error inserting post data: {e}")
        return False
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def insert_multiple_posts(post_data_list):
    """Insert multiple posts into the database."""
    success_count = 0
    
    for post_data in post_data_list:
        if insert_post_data(post_data):
            success_count += 1
    
    print(f"Successfully inserted {success_count} out of {len(post_data_list)} posts")
    return success_count

def test_database_connection():
    """Test if we can connect to the database."""
    connection = create_connection()
    if connection:
        print("Successfully connected to MySQL database")
        connection.close()
        return True
    else:
        print("Failed to connect to MySQL database")
        return False

# Example usage (can be called from main wxc.py)
if __name__ == "__main__":
    # Test the database connection
    print("Testing MySQL connection...")
    test_database_connection()
    
    # Create table if needed
    create_wxc_posts_table()

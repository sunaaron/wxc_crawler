#!/usr/bin/env python3
"""
MySQL writer to store crawled posts in the wxc_posts table.
"""

import mysql.connector
from mysql.connector import Error
import json
from datetime import datetime
from constants import MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD, WXC_POSTS_TABLE

def create_connection():
    """Create connection to MySQL database."""
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            database=MYSQL_DATABASE,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
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
        
        # First check if table exists and has the new structure
        cursor.execute(f"SHOW TABLES LIKE '{WXC_POSTS_TABLE}'")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            # Create new table with the updated schema
            create_table_query = f"""
            CREATE TABLE {WXC_POSTS_TABLE} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date_str CHAR(8),
                category VARCHAR(255),
                post_url VARCHAR(500),
                post_title VARCHAR(500),
                post_body TEXT,
                comments TEXT,
                llm_summary TEXT,
                is_useful BOOLEAN DEFAULT 0,
                has_tts BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_category_date (category, date_str)
            )"""
            
            cursor.execute(create_table_query)
            print(f"{WXC_POSTS_TABLE} table created successfully with new schema")                    
        connection.commit()
        return True
        
    except Error as e:
        print(f"Error creating/updating {WXC_POSTS_TABLE} table: {e}")
        return False
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def insert_post_data(post_data, category, date_str=None):
    """Insert post data into wxc_posts table."""
    connection = create_connection()
    if connection is None:
        return False
    
    try:
        cursor = connection.cursor()
        
        # Prepare the insert query
        insert_query = f"""
        INSERT INTO {WXC_POSTS_TABLE} 
        (date_str, category, post_url, post_title, post_body, comments, llm_summary, is_useful, has_tts)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        
        # Extract data from post_data structure
        # Use provided date_str or extract from post_data if available
        if date_str is None:
            # For now, we'll use a placeholder - in real implementation,
            # this would be determined by the actual crawled date
            date_str = "00000000"  # Default placeholder

        post_url = post_data.get('url', '')
        post_title = post_data.get('data', {}).get('post_title', '')
        post_body = post_data.get('data', {}).get('post_content', '')
        comments = json.dumps(post_data.get('data', {}).get('comments', []), ensure_ascii=False)
        llm_summary = ""  # Empty for now, can be populated with LLM analysis
        
        # Execute the insert
        cursor.execute(insert_query, (
            date_str,
            category,
            post_url,
            post_title,
            post_body,
            comments,
            llm_summary,
            0,  # is_useful defaults to 0 (not useful)
            0   # has_tts defaults to 0 (no TTS)
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

def insert_multiple_posts(post_data_list, category, date_str=None):
    """Insert multiple posts into the database."""
    success_count = 0
    
    for post_data in post_data_list:
        if insert_post_data(post_data, category, date_str):
            success_count += 1
    
    print(f"Successfully inserted {success_count} out of {len(post_data_list)} posts")
    return success_count

def read_max_date_by_category(category):
    """Return the maximum date_str for a given category."""
    connection = create_connection()
    if connection is None:
        return None
    
    try:
        cursor = connection.cursor()
        
        # Query to get the maximum date_str for a given category
        query = f"""
        SELECT MAX(date_str) 
        FROM {WXC_POSTS_TABLE} 
        WHERE category = %s
        """
        
        cursor.execute(query, (category,))
        result = cursor.fetchone()
        
        # Return the max date_str or None if no records found
        return result[0] if result and result[0] is not None else None
        
    except Error as e:
        print(f"Error reading max date by category: {e}")
        return None
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

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

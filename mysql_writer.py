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
        
        # First check if table exists and has the new structure
        cursor.execute("SHOW TABLES LIKE 'wxc_posts'")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            # Create new table with the updated schema
            create_table_query = """
            CREATE TABLE wxc_posts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date_str CHAR(8),
                category VARCHAR(255),
                post_url VARCHAR(500),
                post_title VARCHAR(500),
                post_body TEXT,
                comments TEXT,
                llm_summary TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_category_date (category, date_str)
            )"""
            
            cursor.execute(create_table_query)
            print("wxc_posts table created successfully with new schema")
        else:
            # Table exists, check and modify structure if needed
            # Check if date_str column exists
            cursor.execute("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = 'wxc_crawler' 
                AND TABLE_NAME = 'wxc_posts' 
                AND COLUMN_NAME = 'date_str'
            """)
            
            date_str_exists = cursor.fetchone()
            
            if not date_str_exists:
                # Add the date_str column
                alter_query = """
                ALTER TABLE wxc_posts 
                ADD COLUMN date_str CHAR(8) AFTER id
                """
                cursor.execute(alter_query)
                print("Added date_str column to wxc_posts table")
            
            # Check if the multi-index exists
            cursor.execute("""
                SELECT INDEX_NAME 
                FROM INFORMATION_SCHEMA.STATISTICS 
                WHERE TABLE_SCHEMA = 'wxc_crawler' 
                AND TABLE_NAME = 'wxc_posts' 
                AND INDEX_NAME = 'idx_category_date'
            """)
            
            index_exists = cursor.fetchone()
            
            if not index_exists:
                # Create the multi-index
                create_index_query = """
                CREATE INDEX idx_category_date ON wxc_posts (category, date_str)
                """
                cursor.execute(create_index_query)
                print("Created multi-index on category and date_str")
        
        connection.commit()
        return True
        
    except Error as e:
        print(f"Error creating/updating wxc_posts table: {e}")
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
        insert_query = """
        INSERT INTO wxc_posts 
        (date_str, category, post_url, post_title, post_body, comments, llm_summary)
        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        
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

def insert_multiple_posts(post_data_list, category, date_str=None):
    """Insert multiple posts into the database."""
    success_count = 0
    
    for post_data in post_data_list:
        if insert_post_data(post_data, category, date_str):
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

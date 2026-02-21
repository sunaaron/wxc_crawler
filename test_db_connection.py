#!/usr/bin/env python3
"""
Test script to verify database connection and table creation.
"""

import mysql_writer

def main():
    print("Testing database connection...")
    
    # Test basic connection
    if mysql_writer.test_database_connection():
        print("Database connection test PASSED")
        
        # Test table creation
        print("\nCreating wxc_posts table...")
        success = mysql_writer.create_wxc_posts_table()
        if success:
            print("Table creation test PASSED")
        else:
            print("Table creation test FAILED")
    else:
        print("Database connection test FAILED")

if __name__ == "__main__":
    main()
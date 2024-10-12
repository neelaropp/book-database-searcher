# HenryDAO.py

import mysql.connector
from mysql.connector import Error

class HenryDAO:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host='my_host',  # Update with your host
                user='my_user',       # Update with your MySQL user
                password='password',  # Update with your MySQL password
                database='henry_books'
            )
            self.cursor = self.connection.cursor()
        except Error as e:
            print(f"Error connecting to MySQL Database: {e}")
            self.connection = None
            self.cursor = None

    def get_author_data(self):
        """Retrieve all authors from the database."""
        try:
            query = "SELECT AUTHOR_NUM, AUTHOR_FIRST, AUTHOR_LAST FROM HENRY_AUTHOR"
            self.cursor.execute(query)
            return [(f"{first} {last}", num) for num, first, last in self.cursor.fetchall()]
        except Error as e:
            print(f"Error fetching author data: {e}")
            return []
    # HenryDAO.py

    def get_books_by_author(self, author_num):
        """Retrieve all books for a specific author from the database."""
        if self.cursor is None:
            print("Cursor is not available. Cannot fetch books by author.")
            return []

        try:
            query = """
            SELECT b.BOOK_CODE, b.TITLE, b.PRICE 
            FROM HENRY_BOOK b
            JOIN HENRY_WROTE w ON b.BOOK_CODE = w.BOOK_CODE
            WHERE w.AUTHOR_NUM = %s
            """
            self.cursor.execute(query, (author_num,))
            return self.cursor.fetchall()  # Should return a list of books 
        except Error as e:
            print(f"Error fetching books by author: {e}")
            return []
        
    def get_branch_data_by_book(self, book_code):
        """Retrieve branch information (branch name and on-hand count) for a specific book."""
        if self.cursor is None:
            print("Cursor is not available. Cannot fetch branch data by book.")
            return []

        try:
            query = """
            SELECT hb.BRANCH_NAME, hi.ON_HAND
            FROM HENRY_INVENTORY hi
            JOIN HENRY_BRANCH hb ON hi.BRANCH_NUM = hb.BRANCH_NUM
            WHERE hi.BOOK_CODE = %s
            """
            self.cursor.execute(query, (book_code,))
            return self.cursor.fetchall()  # Returns a list of branches and on-hand counts
        except Error as e:
            print(f"Error fetching branch data for book: {e}")
            return []

    def get_publisher_data(self):
        """Retrieve all publishers from the database."""
        try:
            query = "SELECT PUBLISHER_CODE, PUBLISHER_NAME FROM HENRY_PUBLISHER"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error fetching publisher data: {e}")
            return []

    def get_category_data(self):
        """Retrieve all book categories (types) from the database."""
        try:
            query = "SELECT DISTINCT TYPE FROM HENRY_BOOK"
            self.cursor.execute(query)
            return [row[0] for row in self.cursor.fetchall()]
        except Error as e:
            print(f"Error fetching category data: {e}")
            return []
        
    def get_books_by_category(self, category_type):
        """Retrieve all books for a specific category from the database."""
        if self.cursor is None:
            print("Cursor is not available. Cannot fetch books by category.")
            return []

        try:
            query = "SELECT BOOK_CODE, TITLE, PRICE FROM HENRY_BOOK WHERE TYPE = %s"
            self.cursor.execute(query, (category_type,))
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error fetching books by category: {e}")
            return []

    def get_books_by_publisher(self, publisher_code):
        """Retrieve all books for a specific publisher from the database."""
        if self.cursor is None:
            print("Cursor is not available. Cannot fetch books by publisher.")
            return []

        try:
            query = "SELECT BOOK_CODE, TITLE, PRICE FROM HENRY_BOOK WHERE PUBLISHER_CODE = %s"
            self.cursor.execute(query, (publisher_code,))
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error fetching books by publisher: {e}")
            return []

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()

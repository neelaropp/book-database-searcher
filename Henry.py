# Henry.py
import tkinter as tk
from tkinter import ttk
from henryDAO import HenryDAO
from mysql.connector import Error

class HenrySBA:
    def __init__(self, parent, dao):
        self.dao = dao
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Combobox for authors
        ttk.Label(self.frame, text="Select Author:").pack(anchor=tk.W)
        self.author_combobox = ttk.Combobox(self.frame)
        self.author_combobox.pack(fill=tk.X, padx=10, pady=5)
        self.author_combobox.bind("<<ComboboxSelected>>", self.on_author_selected)

        # Combobox for books
        ttk.Label(self.frame, text="Books:").pack(anchor=tk.W)
        self.book_combobox = ttk.Combobox(self.frame)
        self.book_combobox.pack(fill=tk.X, padx=10, pady=5)
        self.book_combobox.bind("<<ComboboxSelected>>", self.on_book_selected)

        # Label for showing price
        self.price_label = ttk.Label(self.frame, text="Price: ")
        self.price_label.pack(padx=10, pady=5)

        # TreeView for showing branch info
        self.tree = ttk.Treeview(self.frame, columns=("Branch", "On Hand"), show='headings')
        self.tree.heading("Branch", text="Branch")
        self.tree.heading("On Hand", text="On Hand")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Populate authors on start
        self.populate_authors()
    
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
            return self.cursor.fetchall()  # Should return a list of books (book_code, title, price)
        except Error as e:
            print(f"Error fetching books by author: {e}")
        return []


    def populate_authors(self):
        authors = self.dao.get_author_data()
        if authors:
            self.author_combobox['values'] = [author[0] for author in authors]
            self.authors = authors  # Store the author list for later use
        else:
            print("No authors found in the database.")

    def on_author_selected(self, event):
        selected_index = self.author_combobox.current()
        if selected_index >= 0:  # Ensure a valid author is selected
            selected_author = self.authors[selected_index]
            author_id = selected_author[1]
            books = self.dao.get_books_by_author(author_id)
            if books:
                self.book_combobox['values'] = [book[1] for book in books]
                self.books = books  # Store books for later use
                self.book_combobox.current(0)  # Automatically select the first book
                self.on_book_selected(None)  # Manual book selection
            else:
                print(f"No books found for author: {selected_author[0]}")
        else:
            print("Invalid author selection.")

    def on_book_selected(self, event):
        selected_index = self.book_combobox.current()
        if selected_index >= 0:  # Ensure a valid book is selected
            selected_book = self.books[selected_index]
            book_code = selected_book[0]
            self.price_label.config(text=f"Price: ${selected_book[2]:.2f}")
            branch_info = self.dao.get_branch_data_by_book(book_code)
            self.tree.delete(*self.tree.get_children())  # Clear old data
            for branch in branch_info:
                self.tree.insert('', 'end', values=branch)
        else:
            print("Invalid book selection.")


class HenrySBC:
    def __init__(self, parent, dao):
        self.dao = dao
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Category Combobox
        ttk.Label(self.frame, text="Select Category:").pack(anchor=tk.W)
        self.category_combobox = ttk.Combobox(self.frame)
        self.category_combobox.pack(fill=tk.X, padx=10, pady=5)
        self.category_combobox.bind("<<ComboboxSelected>>", self.on_category_selected)

        # Combobox for books
        ttk.Label(self.frame, text="Books:").pack(anchor=tk.W)
        self.book_combobox = ttk.Combobox(self.frame)
        self.book_combobox.pack(fill=tk.X, padx=10, pady=5)
        self.book_combobox.bind("<<ComboboxSelected>>", self.on_book_selected)

        # Label for showing price
        self.price_label = ttk.Label(self.frame, text="Price: ")
        self.price_label.pack(padx=10, pady=5)

        # TreeView for showing branch info
        self.tree = ttk.Treeview(self.frame, columns=("Branch", "On Hand"), show='headings')
        self.tree.heading("Branch", text="Branch")
        self.tree.heading("On Hand", text="On Hand")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Populate categories on start
        self.populate_categories()

    def populate_categories(self):
        categories = self.dao.get_category_data()
        if categories:
            self.category_combobox['values'] = categories
        else:
            print("No categories found in the database.")

    def on_category_selected(self, event):
        selected_category = self.category_combobox.get()
        books = self.dao.get_books_by_category(selected_category)
        if books:
            self.book_combobox['values'] = [book[1] for book in books]
            self.books = books
            self.book_combobox.current(0)
            self.on_book_selected(None)
        else:
            print(f"No books found for category: {selected_category}")
            self.book_combobox['values'] = []  # Clear 

    def on_book_selected(self, event):
        selected_index = self.book_combobox.current()
        if selected_index >= 0:
            selected_book = self.books[selected_index]
            book_code = selected_book[0]
            self.price_label.config(text=f"Price: ${selected_book[2]:.2f}")
            branch_info = self.dao.get_branch_data_by_book(book_code)
            self.tree.delete(*self.tree.get_children())  # Clear old data
            for branch in branch_info:
                self.tree.insert('', 'end', values=branch)

class HenrySBP:
    def __init__(self, parent, dao):
        self.dao = dao
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Publisher
        ttk.Label(self.frame, text="Select Publisher:").pack(anchor=tk.W)
        self.publisher_combobox = ttk.Combobox(self.frame)
        self.publisher_combobox.pack(fill=tk.X, padx=10, pady=5)
        self.publisher_combobox.bind("<<ComboboxSelected>>", self.on_publisher_selected)

        # books
        ttk.Label(self.frame, text="Books:").pack(anchor=tk.W)
        self.book_combobox = ttk.Combobox(self.frame)
        self.book_combobox.pack(fill=tk.X, padx=10, pady=5)
        self.book_combobox.bind("<<ComboboxSelected>>", self.on_book_selected)

        # Label for showing price
        self.price_label = ttk.Label(self.frame, text="Price: ")
        self.price_label.pack(padx=10, pady=5)

        # branch info
        self.tree = ttk.Treeview(self.frame, columns=("Branch", "On Hand"), show='headings')
        self.tree.heading("Branch", text="Branch")
        self.tree.heading("On Hand", text="On Hand")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Populate publishers on start
        self.populate_publishers()

    def populate_publishers(self):
        publishers = self.dao.get_publisher_data()
        if publishers:
            self.publisher_combobox['values'] = [publisher[1] for publisher in publishers]
            self.publishers = publishers
        else:
            print("No publishers found in the database.")

    def on_publisher_selected(self, event):
        selected_index = self.publisher_combobox.current()
        if selected_index >= 0:
            selected_publisher = self.publishers[selected_index]
            publisher_code = selected_publisher[0]
            books = self.dao.get_books_by_publisher(publisher_code)
            if books:
                self.book_combobox['values'] = [book[1] for book in books]
                self.books = books
                self.book_combobox.current(0)
                self.on_book_selected(None)
            else:
                print(f"No books found for publisher: {selected_publisher[1]}")
                self.book_combobox['values'] = []  # Clear 

    def on_book_selected(self, event):
        selected_index = self.book_combobox.current()
        if selected_index >= 0:
            selected_book = self.books[selected_index]
            book_code = selected_book[0]
            self.price_label.config(text=f"Price: ${selected_book[2]:.2f}")
            branch_info = self.dao.get_branch_data_by_book(book_code)
            self.tree.delete(*self.tree.get_children())  # Clear old data
            for branch in branch_info:
                self.tree.insert('', 'end', values=branch)


class HenryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bookstore Search")
        self.dao = HenryDAO()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.sba = HenrySBA(self.notebook, self.dao)
        self.sbc = HenrySBC(self.notebook, self.dao)
        self.sbp = HenrySBP(self.notebook, self.dao)

        self.notebook.add(self.sba.frame, text="Search by Author")
        self.notebook.add(self.sbc.frame, text="Search by Category")
        self.notebook.add(self.sbp.frame, text="Search by Publisher")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = HenryApp(root)
    app.run()

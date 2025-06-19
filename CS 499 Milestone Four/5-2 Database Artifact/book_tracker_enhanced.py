import sqlite3  # Import SQLite library for database interaction

# Function to create the books table if it doesn't exist
def create_table():
    conn = sqlite3.connect("books_enhanced.db")  # Connect to (or create) the database file
    c = conn.cursor()
    # Create the books table with title, author, genre, and year fields
    c.execute("CREATE TABLE IF NOT EXISTS books (title TEXT NOT NULL, author TEXT, genre TEXT, year INTEGER)")
    conn.commit()
    conn.close()

# Function to add a book entry to the database
def add_book(title, author, genre, year):
    # Simple validation to ensure the title field is not empty
    if not title:
        print("Title cannot be empty.")
        return

    conn = sqlite3.connect("books_enhanced.db")
    c = conn.cursor()
    # Use parameterized SQL to prevent SQL injection
    c.execute("INSERT INTO books VALUES (?, ?, ?, ?)", (title, author, genre, year))
    conn.commit()
    conn.close()

# Function to retrieve and return all books from the database
def view_books():
    conn = sqlite3.connect("books_enhanced.db")
    c = conn.cursor()
    c.execute("SELECT * FROM books")  # Fetch all records from the books table
    rows = c.fetchall()  # Store results in a list
    conn.close()
    return rows

# Function to delete a book based on title
def delete_book(title):
    conn = sqlite3.connect("books_enhanced.db")
    c = conn.cursor()
    # Use parameterized query to safely delete book
    c.execute("DELETE FROM books WHERE title = ?", (title,))
    conn.commit()
    conn.close()

# Function to search for books that contain a specific keyword in the title
def search_book(title):
    conn = sqlite3.connect("books_enhanced.db")
    c = conn.cursor()
    # Use wildcard with LIKE for flexible matching
    c.execute("SELECT * FROM books WHERE title LIKE ?", ('%' + title + '%',))
    rows = c.fetchall()
    conn.close()
    return rows

# Example usage block to demonstrate functionality
if __name__ == "__main__":
    create_table()  # Ensure the table exists before any operations
    
    # Add a sample book (this line can be modified or removed for actual use)
    add_book("Brave New World", "Aldous Huxley", "Sci-Fi", 1932)

    # Display all books in the database
    print("All Books:")
    print(view_books())

    # Demonstrate the search functionality
    print("\nSearch Results for 'Brave':")
    print(search_book("Brave"))

    # Delete the sample book (for cleanup purposes)
    delete_book("Brave New World")


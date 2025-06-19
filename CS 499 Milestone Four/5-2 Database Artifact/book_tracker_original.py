import sqlite3

def create_table():
    conn = sqlite3.connect("books.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS books (title TEXT, author TEXT, genre TEXT, year INTEGER)")
    conn.commit()
    conn.close()

def add_book(title, author, genre, year):
    conn = sqlite3.connect("books.db")
    c = conn.cursor()
    c.execute(f"INSERT INTO books VALUES ('{title}', '{author}', '{genre}', {year})")
    conn.commit()
    conn.close()

def view_books():
    conn = sqlite3.connect("books.db")
    c = conn.cursor()
    c.execute("SELECT * FROM books")
    rows = c.fetchall()
    conn.close()
    return rows

def delete_book(title):
    conn = sqlite3.connect("books.db")
    c = conn.cursor()
    c.execute(f"DELETE FROM books WHERE title='{title}'")
    conn.commit()
    conn.close()

# Example usage
create_table()
add_book("1984", "George Orwell", "Dystopian", 1949)
print(view_books())
delete_book("1984")

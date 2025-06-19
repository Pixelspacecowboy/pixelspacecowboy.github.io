# 📚 Book Collection Tracker – SQLite Console App

This project is a simple, Python-based console application that allows users to manage a personal book collection using an embedded SQLite database.

Originally built as part of **DAD 220: Introduction to Structured Database Environments**, this application was designed to demonstrate CRUD operations, relational schema design, and SQL query construction. It has since been enhanced to include secure coding practices and more robust functionality.

---

## 🚀 Features

### 🟡 Original Version
- Add books to the collection
- View all books in the database
- Delete a book by title
- Uses **string interpolation** for SQL (intentionally vulnerable to demonstrate risk)

### 🟢 Enhanced Version
- 🛡️ **SQL Injection Protection**  
  All SQL queries now use **parameterized statements** to prevent injection attacks.
  
- 🔍 **Search Functionality**  
  Added ability to search for books by partial title using SQL `LIKE` statements.

- 🧼 **Input Validation**  
  Prevents empty titles from being added to the database.

- 🧱 **Better Code Structure**  
  Refactored into reusable functions with clear commenting to improve readability and modularity.

- ✅ **Example Use Block**  
  Provides demonstration usage for each function when run as a script.

---

## 🗃️ Database Schema

The `books` table uses the following schema:

| Column | Type    | Description             |
|--------|---------|-------------------------|
| title  | TEXT    | Title of the book (required) |
| author | TEXT    | Author of the book      |
| genre  | TEXT    | Genre/category          |
| year   | INTEGER | Year of publication     |

---

## 🧪 How to Run

### Prerequisites
- Python 3 installed (any OS)
- No need to install any third-party libraries (uses built-in `sqlite3`)

### Setup and Execution

1. Clone or download this repository.
2. Open a terminal and navigate to the project directory.
3. Choose the version you want to run:
    ```bash
    python book_tracker_original.py
    ```
    or
    ```bash
    python book_tracker_enhanced.py
    ```

### Sample Output
When you run `book_tracker_enhanced.py`, it will:
- Create the `books_enhanced.db` file (if not already present)
- Add a sample book
- Print all books
- Search for “Brave”
- Delete the test entry

---

## 📂 Project Structure


import sqlite3
import os

DB_FILE = os.path.abspath("stock_bot.db")

def check_tables():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # List all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tables:", tables)

        # Check the companies table
        if ('companies',) in tables:
            cursor.execute("SELECT * FROM companies;")
            rows = cursor.fetchall()
            print("Companies Table:")
            for row in rows:
                print(row)
        else:
            print("No companies table found.")

        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")


def test_connection():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Run a simple query to test the connection
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        if tables:
            print("Connection successful. Tables found:", tables)
        else:
            print("Connection successful, but no tables found.")

        conn.close()  # Always close the connection
    except sqlite3.Error as e:
        print(f"Failed to connect to database: {e}")

def print_rows():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM companies")
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(row)
    print(f"Current companies in DB: {rows}")


if __name__ == "__main__":
    check_tables()
    test_connection()
    print_rows()

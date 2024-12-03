import sqlite3

import os

DB_FILE = os.path.abspath("stock_bot.db")


def get_connection():
    """Establish a connection to the SQLite database."""
    return sqlite3.connect(DB_FILE)

def create_database():
    """Initialize the database with the companies table."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Create the companies table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code TEXT UNIQUE NOT NULL
        );
        ''')
        conn.commit()

def create_company_records_table(code):
    """Create a records table for a given company code."""
    with get_connection() as conn:
        cursor = conn.cursor()
        table_name = f"records_{code}"
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            last_trade_price REAL,
            max_price REAL,
            min_price REAL,
            avg_price REAL,
            percent_change REAL,
            volume INTEGER,
            turnover_best_denars REAL,
            total_turnover_denars REAL
        );
        ''')
        conn.commit()

if __name__ == '__main__':
    create_database()

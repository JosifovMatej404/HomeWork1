import sqlite3
from src.database.db_handler import get_connection, create_company_records_table
import os

DB_FILE = os.path.abspath("stock_bot.db")

def insert_company(company):
    """Insert a Company object into the database without checking for uniqueness."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT OR REPLACE INTO  companies (code, name)
            VALUES (?, ?)
            """, (company.code, company.name))
        conn.commit()  # Ensure changes are committed
        print(f"Inserted company {company.name} with code {company.code}")
    except sqlite3.IntegrityError as e:
            print(f"Failed to insert {company}: {e}")


def insert_company_record(code, record):
    """
    Insert a new record into the company's records table.
    `record` is an instance of CompanyRecord.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        table_name = f"records_{code}"
        cursor.execute(f'''
        INSERT INTO {table_name} (
            date, last_trade_price, max_price, min_price, avg_price, percent_change,
            volume, turnover_best_denars, total_turnover_denars
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        ''', (
            record.date, record.last_trade_price, record.max, record.min,
            record.avg_price, record.percent_change, record.volume,
            record.turnover_best_denars, record.total_turnover_denars
        ))
        conn.commit()

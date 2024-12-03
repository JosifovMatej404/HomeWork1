from src.scraper import task
from src.database.db_handler import create_database


def main():
    print("Initializing database...")
    create_database()

    print("Starting web scraping task...")
    task()
    print("Scraping task completed.")


if __name__ == "__main__":
    main()

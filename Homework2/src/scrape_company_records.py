import sqlite3
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import concurrent.futures
from bs4 import BeautifulSoup
import os
import requests
from src.models import CompanyRecord

DB_FILE = "src/database/stock_bot.db"

# def get_company_codes():
#     """Fetch all company codes from the database."""
#     query = "SELECT code FROM companies"
#     with sqlite3.connect(DB_FILE) as conn:
#         cursor = conn.cursor()
#         cursor.execute(query)
#         codes = cursor.fetchall()
#     return [code[0] for code in codes]

def get_company_codes():
    url = "https://www.mse.mk/mk/issuers/free-market"
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        print(f"Failed to retrieve data from {url}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    # Assuming company data is in a table with specific structure (modify as needed)
    companies = []

    rows = soup.find_all('tr')

    for row in rows:
        columns = row.find_all('td')
        if len(columns) >= 2:  # Assuming the first column is the company name and the second is the code
            code = columns[0].text.strip()
            companies.append(code)

    return companies


def get_driver():
    """Set up the headless Selenium WebDriver."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def scrape_data_for_code(driver, code):
    """Scrape data for a given company code."""
    base_url = f"https://www.mse.mk/en/stats/symbolhistory/{code}"
    driver.get(base_url)

    current_year = time.localtime().tm_year

    for year in range(current_year, current_year - 10, -1):
        # Find the year input fields and set the dates
        year_input = driver.find_element(By.ID, "FromDate")
        year_input.clear()
        year_input.send_keys(f"01/01/{year-1}")

        year_output = driver.find_element(By.ID, "ToDate")
        year_output.clear()
        year_output.send_keys(f"01/01/{year}")

        # Submit the form or trigger the date change, depending on the page's behavior
        submit_button = driver.find_element(By.CLASS_NAME, "btn btn-primary-sm")
        submit_button.click()  # Ensure this triggers the data reload
        time.sleep(0.3)  # Wait for the page to load

        # Now use BeautifulSoup to parse the page source
        soup = BeautifulSoup(driver.page_source, "html.parser")


        # Loop through table rows and extract data
        for row in soup.find_all("tr"):  # Skip header row
            cols = row.find_all("td")
            if len(cols) > 1:  # Make sure it's a valid row
                # Extract data from the columns
                date = cols[0].text.strip()
                last_trade_price = cols[1].text.strip()
                max_price = cols[2].text.strip()
                min_price = cols[3].text.strip()
                avg_price = cols[4].text.strip()
                percent_change = cols[5].text.strip()
                volume = cols[6].text.strip()
                turnover_best_denars = cols[7].text.strip()
                total_turnover_denars = cols[8].text.strip()

                record = CompanyRecord(date,last_trade_price,max_price,min_price,avg_price,percent_change,volume,turnover_best_denars,total_turnover_denars)

                # Store the data in the database
                store_data_in_db(code,record)

def store_data_in_db(code, data):
    """Store the scraped data in the database."""
    query = """
    INSERT INTO company_records (company_code, date, last_trade_price, max, min, avg_price, percent_change, volume, turnover_best_denars, total_turnover_denars)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (code, *data))
        conn.commit()


def scrape_all_codes():
    """Scrape data for all company codes concurrently."""
    codes = get_company_codes()
    driver = get_driver()

    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        futures = [executor.submit(scrape_data_for_code, driver, code) for code in codes]

    driver.quit()  # Close the driver


if __name__ == "__main__":
    scrape_all_codes()

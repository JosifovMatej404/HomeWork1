import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../models")))


import requests
from bs4 import BeautifulSoup
from src.models import Company
from src.database.insert_data import insert_company


# Add the parent directory (project root) to sys.path so Python can find the 'database' module


def scrape_company_data(url):
    """
    Scrapes company data (name and code) from the given URL.
    This function assumes the data is in a table or other HTML structure.
    """
    
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
            name = columns[1].text.strip()
            companies.append((name, code))

    return companies

def task():
    url = "https://www.mse.mk/mk/issuers/free-market"
    companies = scrape_company_data(url)
    print(companies)
    for name, code in companies:
        company = Company(name,code)
        insert_company(company)


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import threading

class SeleniumWorker:
    def __init__(self):
        self.html = ""
        self.driver = None
        self.chrome_options = self.initialize_chrome()
        self.data = []


    def initialize_chrome(self):
        # Set up Chrome options for headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("disable-infobars")  # Disable infobars
        chrome_options.add_argument("--disable-extensions")  # Disable extensions
        return chrome_options

    def set_driver_url(self, key):
        # Initialize WebDriver each time to ensure a fresh instance
        
        self.driver = webdriver.Chrome(options=self.chrome_options)
        url = f"https://www.mse.mk/mk/stats/symbolhistory/{key}"
        self.driver.get(url)


    def is_date_older_than_today(self, date_str):
        # Convert the date string to a datetime object
        # Get the current date
        current_date = self.get_current_date()

        # Compare dates
        if date_str < current_date:
            return True
        else:
            return False
    
    def convert_from_name_to_date(self, date_str):
        # Split the string using the dash ("-")
        parts = date_str.split("-")
        
        # Ensure the parts are in the expected order (day, month, year)
        year, month, day = parts[0], parts[1], parts[2]
            
        # Format the date as dd.mm.yyyy
        formatted_date = f"{day}.{month}.{year}"
        return formatted_date
    
    def get_current_date(self):
        return datetime.now().strftime("%d.%m.%y")


    def merge_data(self, data):
        for item in data:
            self.data.append(item)

    def return_data(self):
        temp = self.data.copy()
        self.data.clear()
        return temp

    def fetch_data_with_dates_and_key(self, start_date, end_date, key):
        def task():
            try:
                self.set_driver_url(key)
                self.driver.delete_all_cookies()  # Clear cookies after setting the URL
            
                print("Waiting for date inputs to load...")

                # Wait until input elements are interactable
                WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.NAME, "FromDate"))
                )
                WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.NAME, "ToDate"))
                )

                # Set the start and end dates
                input_element1 = self.driver.find_element(By.NAME, "FromDate")
                input_element1.clear()
                input_element1.send_keys(start_date)

                input_element2 = self.driver.find_element(By.NAME, "ToDate")
                input_element2.clear()
                input_element2.send_keys(end_date)

                print("Triggering data fetch...")
                # Locate and trigger the button click
                button = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "btn-primary-sm"))
                )
                self.driver.execute_script("arguments[0].click();", button)

                print("Waiting for data to load...")
                # Wait for the data table to load
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, "td"))
                )

                # Get page source after data is fully loaded
                page_html = self.driver.page_source
                print("Data loaded successfully!")
                self.html = page_html

            except Exception as e:
                print(f"An error occurred: {e}")
                self.html = self.driver.page_source
                self.driver.quit()
            finally:
                if self.driver:
                    self.driver.quit()  # Ensure the driver is properly closed

        # Run the task in a separate thread
        thread = threading.Thread(target=task)
        thread.start()
        thread.join()  # Wait for the thread to finish before returning data

    def return_html(self):
        return self.html

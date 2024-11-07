from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import threading

class SeleniumWorker:
    def __init__(self):
        self.html = ""

    def get_current_date(self):
        return datetime.now().strftime("%d.%m.%y")

    def fetch_data_with_dates_and_key(self, start_date, end_date, key):
        def task():
            # Set up Chrome options for headless mode
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")

            # Set up the WebDriver with headless mode
            driver = webdriver.Chrome(options=chrome_options)

            try:
                print("Getting website...")
                # Construct the URL with the key
                url = f"https://www.mse.mk/mk/stats/symbolhistory/{key}"
                driver.get(url)

                print("Waiting for date inputs to load...")
                # Wait until input elements are interactable
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.NAME, "FromDate"))
                )
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.NAME, "ToDate"))
                )
                
                # Set the start and end date
                input_element1 = driver.find_element(By.NAME, "FromDate")
                input_element1.clear()
                input_element1.send_keys(start_date)

                input_element2 = driver.find_element(By.NAME, "ToDate")
                input_element2.clear()
                input_element2.send_keys(end_date)

                print("Triggering data fetch...")
                # Locate and trigger the button click
                button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "btn-primary-sm"))
                )
                driver.execute_script("arguments[0].click();", button)  # Use JavaScript to click

                print("Waiting for data to load...")
                # Wait for the data table to load
                WebDriverWait(driver, 20).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, "td"))
                )

                # Get page source after data is fully loaded
                page_html = driver.page_source
                print("Data loaded successfully!")

                self.html = page_html

            except Exception as e:
                print(f"An error occurred: {e}")
            finally:
                driver.quit()

        # Run the task in a separate thread
        thread = threading.Thread(target=task)
        thread.start()

    def return_html(self):
        return self.html
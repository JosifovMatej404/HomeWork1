from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import threading

class SeleniumWorker:
    def __init__(self, callback):
        self.callback = callback

    def get_current_date():
        return datetime.now().strftime("%m/%d/%Y")

    def fetch_data_with_dates_and_key(start_date, end_date, key, callback=None):
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
                url = f"https://www.mse.mk/en/stats/symbolhistory/{key}"
                driver.get(url)

                print("Waiting for buttons...")
                # Wait until input elements are interactable
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.NAME, "FromDate"))
                )
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.NAME, "ToDate"))
                )
                
                print("Clicking buttons...")
                # Set the start and end date
                input_element1 = driver.find_element(By.NAME, "FromDate")
                input_element1.clear()
                input_element1.send_keys(start_date)

                input_element2 = driver.find_element(By.NAME, "ToDate")
                input_element2.clear()
                input_element2.send_keys(end_date)

                # Locate and trigger the button click
                button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "btn-primary-sm"))
                )
                driver.execute_script("arguments[0].click();", button)  # Use JavaScript to click

                print("Waiting for results table...")
                
                # Optionally, wait for results to load if there’s a specific class or ID to check
                WebDriverWait(driver, 20).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, "td"))
                )

                print("Found results!")

                # Call the callback function with the driver instance if specified
                if callback:
                    callback(driver)

                print("Finished.")

            except Exception as e:
                print(f"An error occurred: {e}")
            finally:
                driver.quit()

        # Run the task in a separate thread
        thread = threading.Thread(target=task)
        thread.start()

    # Define a callback function to process the data
    def process_data(driver):
        # Example: Extract data from the page
        print("Processing data...")
        # Locate and extract the text or tables, then close the driver when done
        # data_element = driver.find_element(By.CLASS_NAME, "result-class")
        # print(data_element.text)
        # driver.quit()

    # Example usage
    #end_date = get_current_date()
    #fetch_data_with_dates_and_key("06.10.2024", end_date, "REPL", callback=process_data)

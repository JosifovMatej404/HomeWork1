from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import time

def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")

def fetch_data_with_dates_and_key(start_date, end_date, key):
    # Set up the WebDriver (use the path to your ChromeDriver)
    driver = webdriver.Chrome()

    # Construct the URL with the key
    url = f"https://www.mse.mk/en/stats/symbolhistory/{key}"
    driver.get(url)

    # Wait for the page to load
    time.sleep(5)  # Adjust the delay as needed to ensure the page is fully loaded

    try:
        # Locate the input elements and set their values
        input_element1 = driver.find_element(By.NAME, "FromDate")  # Use appropriate attribute
        input_element1.clear()
        input_element1.send_keys(start_date)

        input_element2 = driver.find_element(By.NAME, "ToDate")  # Use appropriate attribute
        input_element2.clear()
        input_element2.send_keys(end_date)

        # Locate and click the button
        button = driver.find_element(By.CLASS_NAME, "btn-primary-sm")
        button.click()
        print("Button clicked successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

    # Keep the browser open for a while to observe the changes
    time.sleep(30)

    # Close the browser
    driver.quit()
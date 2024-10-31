from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from mysql_database import MySQLDatabase

import pandas as pd
import time
import os

class FormAutomation:
    def __init__(self, driver_path, form_url):
        service = Service(driver_path)
        self.driver = webdriver.Chrome(service=service)
        self.form_url = form_url
        self.db = db

    def navigate_to_form(self):
        self.driver.get(self.form_url)

    def fill_and_submit_form(self, ad):
        try:
            title_input = self.driver.find_element(By.ID, 'title')
            price_input = self.driver.find_element(By.ID, 'price')

            title_input.send_keys(ad['Title'])

            # Clean the price input
            raw_price = ad['Price']
            cleaned_price = float(raw_price.replace('Rs ', '').replace(',', '').strip())

            price_input.send_keys(cleaned_price)

            # Assuming availability is a known column in your CSV
            availability = ad.get('Availability', 'In Stock')  # Default value

            # Call the insert function to store the data in the database
            self.db.insert_ad(ad['Title'], cleaned_price, availability)

            submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_button.click()

            # Wait for confirmation message
            time.sleep(2)
            confirmation_message = self.driver.find_element(By.ID, 'confirmation')
            if confirmation_message.is_displayed():
                print("Ad submitted successfully!")
        except Exception as e:
            print(f"An error occurred during form submission: {e}")


    def close(self):
        self.driver.quit()



# To use this automation
if __name__ == "__main__":
    # Load the ads data from CSV
    ads_data = pd.read_csv("C:/Users/Administrator/Documents/Sandali Fernando/ads_data.csv") 
    
    # Initialize MySQL Database
    db = MySQLDatabase(host='localhost', database='ad_data', user='root', password='innobot')

    form_automation = FormAutomation(
        driver_path="C:/webdrivers/chromedriver.exe",
        form_url = "file:///C:/Users/Administrator/Documents/Sandali Fernando/src/automation/form.html"

    )
    
    try:
        form_automation.navigate_to_form()
        for ad in ads_data.iterrows():
            form_automation.fill_and_submit_form(ad[1])  # ad[1] contains the ad data as a Series
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        time.sleep(2)  # Keep the browser open for a few seconds
        form_automation.close()
        db.close()  # Close the database connection
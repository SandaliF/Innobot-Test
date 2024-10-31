from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from ads_scraper import AdScraper
from page_checker import PageChecker
import time
import pandas as pd

class WebScraper:
    def __init__(self, driver_path, base_url):
        service = Service(driver_path)
        self.driver = webdriver.Chrome(service=service)
        self.base_url = base_url

    def navigate_to_page(self, url):
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'gtm-top-ad')))  # Wait for ads to load
        # time.sleep(2)  # Adjust based on loading time

    def extract_product_info(self):
        # Use page source with AdScraper to get ad data
        page_source = self.driver.page_source
        ad_scraper = AdScraper(page_source)
        ads_data = ad_scraper.extract_ads()
        print(f"Extracted {len(ads_data)} ads.")
        return ads_data

    def handle_pagination(self):
        all_ads = []
        while True:
            ads_data = self.extract_product_info()
            all_ads.extend(ads_data)

            # Use PageChecker to see if further pages exist
            page_checker = PageChecker(self.driver.page_source)
            if not page_checker.has_results():
                break
            
            # Try clicking the "Next" button
            try:
                # Get all page numbers
                page_numbers = self.driver.find_elements(By.CLASS_NAME, "page-number--2O3yQ")
                current_page = self.driver.find_element(By.XPATH, "//span[@class='active-desktop--3b3Ed']")  

                # Find next page number
                next_page_index = int(current_page.text)  # Assuming current page number is displayed
                next_page_number = next_page_index + 1

                # Click on the next page number
                for page_number in page_numbers:
                    if page_number.text == str(next_page_number):
                        print(f"Navigating to page {next_page_number}.")
                        page_number.click()
                        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'gtm-top-ad')))  # Wait for ads to load
                        time.sleep(2)  # Consider adjusting this if necessary
                        break


            except:
                print("Reached the last page.")
                break
        return all_ads

    def close(self):
        self.driver.quit()

# To use this scraper
if __name__ == "__main__":
    scraper = WebScraper(
        driver_path="C:\webdrivers\chromedriver.exe", 
        base_url="https://ikman.lk/en/ads/sri-lanka/electronics")
    
    try:
        scraper.navigate_to_page(scraper.base_url)  # Navigate to the initial page
        all_ads_data = scraper.handle_pagination()
        scraper.close()

        # Save the scraped data to a CSV file
        if all_ads_data:
            df = pd.DataFrame(all_ads_data)
            df.to_csv("ads_data.csv", index=False)
            print(f"Scraped {len(all_ads_data)} ads and saved to 'ads_data.csv'.")
        else:
            print("No ads were scraped.")

    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        
        time.sleep(2)  
        scraper.close()




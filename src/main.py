import sys
import os
import time
import pandas as pd
from automation.mysql_database import MySQLDatabase
from automation.form_automator import FormAutomation
from scraper.ads_scraper import AdScraper
from scraper.page_checker import PageChecker
from scraper.web_scraper import WebScraper
from reports.report_generator import ReportGenerator

# Add the src folder to the Python path if needed
src_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(src_path)

def main():
    # Database configuration
    db_config = {
        'host': 'localhost',
        'database': 'ad_data',
        'user': 'root',
        'password': 'innobot'
    }

    # Initialize MySQL Database
    db = MySQLDatabase(**db_config)

    # Set up Web Scraper
    driver_path = "C:/webdrivers/chromedriver.exe"  # Update this with your actual path
    base_url = "https://ikman.lk/en/ads/sri-lanka/electronics"

    web_scraper = WebScraper(driver_path, base_url)

    try:
        # Step 1: Scrape ads
        print("Starting the scraping process...")
        web_scraper.navigate_to_page(base_url)
        all_ads_data = web_scraper.handle_pagination()
        web_scraper.close()

        # Save ads data to CSV for form automation
        if all_ads_data:
            df = pd.DataFrame(all_ads_data)
            df.to_csv("ads_data.csv", index=False)
            print(f"Scraped {len(all_ads_data)} ads and saved to 'ads_data.csv'.")
        else:
            print("No ads were scraped.")
            return

        # Load ads data from CSV
        ads_data = pd.read_csv("ads_data.csv")

        # Step 2: Store the scraped data in the database
        print("Inserting scraped data into the database...")
        for ad in ads_data.iterrows():
            title = ad[1]['title']
            description = ad[1]['description']
            price = ad[1]['price']
            # Insert data into the database
            db.insert_product(title, description, price)  # Ensure this method exists in MySQLDatabase

        # Step 3: Automate the form submission process using the scraped data
        print("Starting the form submission automation...")
        form_automation = FormAutomation(
            driver_path=driver_path,
            form_url="file:///C:/Users/Administrator/Documents/Sandali Fernando/src/automation/form.html"
        )

        form_automation.navigate_to_form()

        for ad in ads_data.iterrows():
            form_automation.fill_and_submit_form(ad[1])  # Fill and submit the form for each ad

        # Step 4: Generate report
        report_gen = ReportGenerator(
            host="localhost",
            user="root",
            password="innobot",
            database="ad_data"
        )

        print("Generating the report...")
        report = report_gen.generate_report()
        print(report)  # Print the report to console
        report_gen.save_report(report, "C:/Users/Administrator/Documents/Sandali Fernando/src/reports/report.csv")
        report_gen.close()

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        time.sleep(2)  # Keep the browser open for a few seconds
        form_automation.close()  # Ensure the form automation is closed if opened
        db.close()  # Close the database connection

if __name__ == "__main__":
    main()

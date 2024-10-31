import re
from bs4 import BeautifulSoup

class AdScraper:
    def __init__(self, page_source):
        self.soup = BeautifulSoup(page_source, 'html.parser')

    def extract_ads(self):
        ads_data = []
        top_ads = self.soup.find_all('li', class_='gtm-top-ad')
        normal_ads = self.soup.find_all('li', class_='gtm-normal-ad')

        print(f"Found {len(top_ads)} top ads and {len(normal_ads)} normal ads.")  # Debugging line

        for ads in [top_ads, normal_ads]:
            for ad in ads:
                ad_info = self._parse_ad(ad)
                if ad_info:
                    ads_data.append(ad_info)
        return ads_data

    def _parse_ad(self, ad):
        try:
            # Extract title
            title_tag = ad.find('h2', class_=re.compile(r'^heading--'))
            title = title_tag.text.strip() if title_tag else 'No Title'

            # Extract price
            price_tag = ad.find('div', class_=re.compile(r'^price--'))
            price = price_tag.text.strip() if price_tag else 'No Price'

            # Extract location
            location_tag = ad.find('div', class_=re.compile(r'^description--'))
            location = location_tag.text.strip() if location_tag else 'No Location'

            # Extract seller badge
            seller_badge_tag = ad.find('div', class_=re.compile(r'^premium-member--'))
            seller_badge = seller_badge_tag.text.strip() if seller_badge_tag else 'No badge'

            return {
                "Title": title,
                "Price": price,
                "Location": location,
                "Seller Badge": seller_badge
            }

        except AttributeError as e:
            print(f"Error parsing ad: {e}")
            return None













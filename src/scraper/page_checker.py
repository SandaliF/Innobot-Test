import re
from bs4 import BeautifulSoup

class PageChecker:
    def __init__(self, page_source):
        self.soup = BeautifulSoup(page_source, 'html.parser')

    def has_results(self):
        no_results = self.soup.find('div', class_=re.compile(r'^no-result-text--'))
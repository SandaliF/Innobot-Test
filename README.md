# Web Scraper Project

This project is designed to scrape ads from a specified website (ikman.lk) and automate the form submission process. The data extracted can be stored in a MySQL database, and reports can be generated from the stored data.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Running the Project](#running-the-project)
- [Dependencies](#dependencies)
- [Usage](#usage)
- [License](#license)

## Features
- Scrapes ads from ikman.lk using Selenium and BeautifulSoup.
- Validates form submission with automated input using Selenium.
- Stores scraped data in a MySQL database.
- Generates CSV reports from the stored data.

## Technologies Used
- Python
- Selenium
- BeautifulSoup
- MySQL
- Pandas

## Setup Instructions

### Prerequisites
1. **Python**: Ensure Python 3.x is installed on your system.
2. **MySQL**: Install MySQL Server and set up a database to store scraped data.
3. **Chrome WebDriver**: Download and place the ChromeDriver executable in a suitable directory. Make sure the version matches your installed version of Chrome.

### Clone the Repository
```bash
git clone https://github.com/yourusername/Web_Scraper_Project.git
cd Web_Scraper_Project

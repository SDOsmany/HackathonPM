import requests
from bs4 import BeautifulSoup
import re

# from bs4.element import Tag # Not strictly needed for this code
import json
import concurrent.futures
import time  # Import time for potential delays

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

def find_devpost_links_dynamic(website_url):
    """
    Uses Selenium to fetch a webpage after JavaScript execution and finds
    anchor tags with the class "block-wrapper-link fade link-to-software".

    Args:
        website_url (str): The URL of the website to scrape.

    Returns:
        list: A list of URLs found in the href attributes of the matching anchor tags.
              Returns an empty list if no links are found or an error occurs.
    """
    found_urls = []
    # Configure Selenium (example for Chrome - you need ChromeDriver executable)
    # service = Service('/path/to/chromedriver') # Specify the path to your chromedriver executable
    # driver = webdriver.Chrome(service=service)

    # Simpler initialization if chromedriver is in your PATH
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless') # Run in headless mode (no browser window)
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)

        print(f"Loading page with Selenium: {website_url}")
        driver.get(website_url)

        # Wait for the links to potentially load. You might need to adjust the wait condition.
        # This waits up to 10 seconds for at least one element with the target class to appear.
        wait = WebDriverWait(driver, 10)
        target_class = "block-wrapper-link.fade.link-to-software" # Selenium CSS selector format
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'a.{target_class.replace(" ", ".")}')))
            print("Links with target class found (or waited for).")
        except TimeoutException:
            print("Timed out waiting for links with target class to appear.")
            # Continue anyway, as some might have loaded

        # Get the page source AFTER potential dynamic loading
        page_source = driver.page_source

        # Now use BeautifulSoup to parse the source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find all anchor tags with the specified classes using BeautifulSoup
        bs4_target_classes = ["block-wrapper-link", "fade", "link-to-software"]
        anchor_tags = soup.find_all('a', class_=bs4_target_classes)

        # Extract the href attribute
        for tag in anchor_tags:
            href = tag.get('href')
            if href:
                found_urls.append(href)

        print(f"Found {len(found_urls)} links with the specified class using Selenium+BeautifulSoup.")
        return found_urls

    except WebDriverException as e:
        print(f"Selenium WebDriver error occurred: {e}")
        print("Make sure you have a browser (like Chrome) and its driver (like ChromeDriver) installed and in your system's PATH.")
        return []
    except Exception as e:
        print(f"An error occurred during Selenium scraping: {e}")
        return []
    finally:
        # Always quit the driver
        if 'driver' in locals() and driver:
            driver.quit()

# --- Main part of the script for parallel execution ---

base_url = "https://devpost.com/software/popular"
# MAX_PAGE = 15701  # Be cautious with scraping this many pages rapidly!
# # Let's limit for a safer example:
# PAGES_TO_SCRAPE = 250  # Scrape the first 100 pages concurrently
MAX_PAGE = 10
PAGES_TO_SCRAPE = MAX_PAGE

urls_to_scrape = [
    # f"{base_url}?page={page_num}" for page_num in range(1, MAX_PAGE + 1)
    # f"https://devpost.com/software/search?query=is%3Afeatured+is%3Awinner&order_by=trending"
    f"https://devpost.com/software/search?order_by=trending&page={page_num}&query=is%3Afeatured+is%3Awinner"
    for page_num in range(1, MAX_PAGE + 1)
]

all_links = []
# Use ThreadPoolExecutor to manage threads
# The number of workers controls how many requests happen concurrently
# Adjust max_workers based on your system and network capabilities
# A common starting point is 5-32, but don't set it excessively high.
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    # Submit the find_devpost_links function for each URL
    # executor.map is a simple way to run a function on a list of inputs
    # It returns results in the order the inputs were submitted
    # We wrap it in list() to ensure all futures complete before proceeding
    results = list(executor.map(find_devpost_links_dynamic, urls_to_scrape))

    # Collect results from all threads
    for page_links in results:
        all_links.extend(page_links)

# Optional: Add a small delay between requests if needed to avoid overwhelming the server
# This is not needed when using ThreadPoolExecutor. It's more for sequential requests.
# If you encounter blocking, you might need to add delays *inside* the find_devpost_links function
# or between batches of concurrent requests.

print(f"\nTotal links found across {PAGES_TO_SCRAPE} pages: {len(all_links)}")

# Save all the collected links to a JSON file
output_filename = "dynamic_links.json"
with open(output_filename, "w") as file:
    json.dump(all_links, file, indent=4)

print(f"All links saved to {output_filename}")

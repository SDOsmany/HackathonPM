import requests
from bs4 import BeautifulSoup
import re

# from bs4.element import Tag # Not strictly needed for this code
import json
import concurrent.futures
import time  # Import time for potential delays


def find_devpost_links(website_url):
    """
    Fetches a webpage and finds all anchor tags with the class
    "block-wrapper-link fade link-to-software", extracting their href attributes.

    Args:
        website_url (str): The URL of the website to scrape.

    Returns:
        list: A list of URLs found in the href attributes of the matching anchor tags.
              Returns an empty list if no links are found or an error occurs.
    """
    found_urls = []
    try:
        # print(f"Fetching: {website_url}") # Optional: for tracking progress
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(website_url, headers=headers, timeout=15)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        soup = BeautifulSoup(response.content, "html.parser")

        target_class = ["block-wrapper-link", "fade", "link-to-software"]
        anchor_tags = soup.find_all("a", class_=target_class)

        for tag in anchor_tags:
            href = tag.get("href")
            if href:
                found_urls.append(href)

        print(f"Finished fetching {website_url}. Found {len(found_urls)} links.")
        return found_urls

    except requests.exceptions.Timeout:
        print(f"Timeout occurred while fetching {website_url}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching {website_url}: {e}")
        return []
    except Exception as e:
        print(f"An error occurred while parsing {website_url}: {e}")
        return []


# --- Main part of the script for parallel execution ---

base_url = "https://devpost.com/software/popular"
MAX_PAGE = 15701  # Be cautious with scraping this many pages rapidly!
# Let's limit for a safer example:
PAGES_TO_SCRAPE = 250  # Scrape the first 100 pages concurrently

urls_to_scrape = [
    f"{base_url}?page={page_num}" for page_num in range(1, PAGES_TO_SCRAPE + 1)
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
    results = list(executor.map(find_devpost_links, urls_to_scrape))

    # Collect results from all threads
    for page_links in results:
        all_links.extend(page_links)

# Optional: Add a small delay between requests if needed to avoid overwhelming the server
# This is not needed when using ThreadPoolExecutor. It's more for sequential requests.
# If you encounter blocking, you might need to add delays *inside* the find_devpost_links function
# or between batches of concurrent requests.

print(f"\nTotal links found across {PAGES_TO_SCRAPE} pages: {len(all_links)}")

# Save all the collected links to a JSON file
output_filename = "links.json"
with open(output_filename, "w") as file:
    json.dump(all_links, file, indent=4)

print(f"All links saved to {output_filename}")

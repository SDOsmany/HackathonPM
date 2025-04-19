import requests
from bs4 import BeautifulSoup
import re
from bs4.element import Tag  # Import Tag for type checking
import json

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
        # Fetch the webpage content
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(website_url, headers=headers, timeout=15) # Increased timeout slightly
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all anchor tags with the specified class
        # The class names are block-wrapper-link, fade, and link-to-software
        # Pass the classes as a list to find_all
        target_class = ["block-wrapper-link", "fade", "link-to-software"]
        anchor_tags = soup.find_all('a', class_=target_class)

        # Extract the href attribute from each found tag
        for tag in anchor_tags:
            href = tag.get('href')
            if href: # Make sure the href attribute exists
                found_urls.append(href)

        print(f"Found {len(found_urls)} links with the specified class on {website_url}")
        return found_urls

    except requests.exceptions.Timeout:
        print(f"Timeout occurred while fetching {website_url}")
        return [] # Return empty list on error
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching {website_url}: {e}")
        return [] # Return empty list on error
    except Exception as e:
        print(f"An error occurred while parsing {website_url}: {e}")
        return [] # Return empty list on error
    

url = "https://devpost.com/software/popular"
links = find_devpost_links(url)
MAX_PAGE = 15701
# for page_num in range(2, MAX_PAGE + 1):
for page_num in range(2, 10):
    # print(f"{page_num=}")
    url = "https://devpost.com/software/popular?page={page_num}"
    links.extend(find_devpost_links(url))

with open("links.py", "w") as file:
    json.dump(links, file, indent=4)
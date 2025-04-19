import requests
from bs4 import BeautifulSoup
import re
import random

# from bs4.element import Tag  # Still not strictly needed for this code
import json
import concurrent.futures
import time  # Import time for potential delays

MULT_BIAS = (
    10  # Increase this to go slower, but decrease likelihood of DevPost rate-limiting
)
DYNAMIC = True


def get_devpost_description(devpost_url):
    """
    Fetches and attempts to extract content from the div with id="app-details-left"
    on a Devpost project page.

    Args:
        devpost_url (str): The URL of the Devpost project page.

    Returns:
        dict or None: A dictionary {'url': devpost_url, 'content': extracted_text},
                      or None if it could not be fetched or the div was not found.
                      Returning a dict helps keep track of which URL belongs to which content.
    """
    sleep_duration = random.uniform(0.5 * MULT_BIAS, 2.5 * MULT_BIAS)
    time.sleep(sleep_duration)
    try:
        # print(f"Fetching description for: {devpost_url}") # Optional: for tracking progress
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(devpost_url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        soup = BeautifulSoup(response.content, "html.parser")

        description_container = soup.find("div", id="app-details-left")

        description_text = None
        if description_container:
            description_text = description_container.get_text(separator="\n").strip()
            print(
                f"Successfully extracted description for {devpost_url}"
            )  # Optional feedback
        else:
            print(
                f"Could not find div #app-details-left for {devpost_url}"
            )  # Feedback for missing container

        # Return a dictionary containing both the URL and the content
        return {
            "url": devpost_url,
            "content": (
                description_text
                if description_text
                else "Content not found or extracted."
            ),
        }

    except requests.exceptions.Timeout:
        print(f"Timeout occurred while fetching description for {devpost_url}")
        return {"url": devpost_url, "content": "Timeout occurred."}  # Return error info
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching description for {devpost_url}: {e}")
        return {
            "url": devpost_url,
            "content": f"Request error: {e}",
        }  # Return error info
    except Exception as e:
        print(f"An error occurred while parsing description for {devpost_url}: {e}")
        return {
            "url": devpost_url,
            "content": f"Parsing error: {e}",
        }  # Return error info


# --- Main part of the script ---

# 1. Load URLs from the JSON file

# Replace 'devpost_links.json' with the actual name of the JSON file
# created in the previous step that contains your list of Devpost URLs.
input_links_file = "dynamic_links.json" if DYNAMIC else "links.json"
output_filename = "dynamic_big_data.json" if DYNAMIC else "big_data.json"

# Check if the input file exists
try:
    with open(input_links_file, "r", encoding="utf-8") as f:
        # Assuming the JSON file contains a list of URL strings directly
        LINKS = list(json.load(f))
    print(f"Successfully loaded {len(LINKS)} links from {input_links_file}")

except FileNotFoundError:
    print(f"Error: Input links file not found at {input_links_file}")
    LINKS = []  # Initialize as empty list if file not found
except json.JSONDecodeError:
    print(
        f"Error: Could not decode JSON from {input_links_file}. Make sure it's a valid JSON file."
    )
    LINKS = []
except Exception as e:
    print(f"An unexpected error occurred while loading links: {e}")
    LINKS = []

# 2. Parallelize fetching descriptions

if LINKS:  # Only proceed if links were loaded
    devpost_data_list = []
    # Use ThreadPoolExecutor to manage threads for fetching descriptions
    # Adjust max_workers based on your system and network capabilities
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        # Submit the get_devpost_description function for each URL
        # executor.map is suitable here, it returns results in input order
        # We wrap in list() to wait for all futures to complete
        results = list(executor.map(get_devpost_description, LINKS))

        # Collect results. Results are already dictionaries from get_devpost_description
        devpost_data_list = results

    print(f"\nFinished fetching descriptions for {len(devpost_data_list)} links.")

    # 3. Save the data (URL and content) to a JSON file
    with open(output_filename, "w", encoding="utf-8") as file:
        json.dump(devpost_data_list, file, indent=4, ensure_ascii=False)

    print(f"All project data saved to {output_filename}")

else:
    print("No links were loaded, skipping description fetching.")

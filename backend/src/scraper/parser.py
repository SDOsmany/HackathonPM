import requests
from bs4 import BeautifulSoup
import re
from bs4.element import Tag  # Import Tag for type checking
import json


def get_readme_content(github_url):
    """
    Fetches the content of README.md from a public GitHub repository URL.
    Tries both 'main' and 'master' branches.

    Args:
        github_url (str): The standard GitHub repository URL (e.g., https://github.com/owner/repo).

    Returns:
        str or None: The content of the README.md file if found and fetched successfully,
                     otherwise returns None.
    """
    # Validate and parse the GitHub URL
    parts = github_url.strip("/").split("/")
    if len(parts) < 5 or parts[2] != "github.com":
        print(f"Warning: Invalid GitHub repository URL format: {github_url}")
        return None  # Return None for invalid URL format

    owner = parts[3]
    repo = parts[4]

    # Common default branches to try
    branches_to_try = ["main", "master"]
    raw_urls = [
        f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/README.md"
        for branch in branches_to_try
    ]

    # Attempt to fetch from the potential URLs
    for url in raw_urls:
        try:
            response = requests.get(url)
            # Check if the request was successful (status code 200)
            if not (response.ok):
                print(f"FAILED FOR THIS URL: {github_url}")
            if response.status_code == 200:
                # print(f"Successfully fetched README from: {url}") # Optional feedback
                return response.text  # Return the content immediately upon success
            # If not found (404), try the next URL
            elif response.status_code == 404:
                # print(f"README not found at: {url} - trying next branch...") # Optional feedback
                continue  # Continue to the next URL in the list
            else:
                # For other errors, print a warning and try next
                print(
                    f"Warning: Failed to fetch {url} with status code: {response.status_code}"
                )
                continue
        except requests.exceptions.RequestException as e:
            # Handle network or other request errors
            print(f"Warning: An error occurred while trying to fetch {url}: {e}")
            continue  # Continue to the next URL in the list

    # If none of the URLs worked after trying all branches
    print(
        f"Warning: Could not find README.md for repository: {github_url} on main or master branches."
    )
    return None  # Return None if README was not found after trying all options

def get_devpost_description(devpost_url):
    """
    Fetches and attempts to extract content from the div with id="app-details-left"
    on a Devpost project page.

    Args:
        devpost_url (str): The URL of the Devpost project page.

    Returns:
        str or None: The extracted text content from the specified div,
                     or None if it could not be fetched or the div was not found.
    """
    try:
        # Send a GET request to the Devpost URL
        # Added a User-Agent header to mimic a browser, as some sites block default requests
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(devpost_url, headers=headers, timeout=10) # Added a timeout and headers
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # --- Find the div with id="app-details-left" ---
        description_container = soup.find('div', id='app-details-left')

        description_text = None
        if description_container:
            # Extract text from the container, preserving line breaks where possible
            description_text = description_container.get_text(separator='\n').strip()
            print(f"Successfully found and extracted content from #app-details-left on {devpost_url}")
        else:
            print(f"Could not find div with id='app-details-left' for {devpost_url}. HTML structure might be different or content is missing.")

        return description_text

    except requests.exceptions.Timeout:
        print(f"Timeout occurred while fetching {devpost_url}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching {devpost_url}: {e}")
        return None
    except Exception as e:
        print(f"An error occurred while parsing {devpost_url}: {e}")
        return None

FILE_PATH = "data.json"
with open(FILE_PATH, "r") as file:
    d_list = json.load(file)

# These are for manually fixed url parsings
BANNED_GITHUB_URLS = ["https://github.com/graphhop"]
BANNED_DEVPOST_URLS = []

for d in d_list:
    if d.get("is_github_url", False):
        assert "github" in d["url"]
        # print(f"GitHub URL: {d['url']}")
        # Get README.md file
        github_url = d["url"]
        if github_url in BANNED_GITHUB_URLS:
            # print(f"Skipping banned GitHub URL: {github_url}")
            continue
        readme_content = get_readme_content(github_url)
        # print(f"{github_url}: {readme_content}")
        # assert "content" not in d
        d["content"] = readme_content
    else:
        assert d.get("is_devpost_url", False)
        assert "devpost" in d["url"]
        devpost_url = d["url"]
        if devpost_url in BANNED_DEVPOST_URLS:
            # print(f"Skipping banned Devpost URL: {devpost_url}")
            continue
        content = get_devpost_description(devpost_url)
        d["content"] = content
    
    # Now, using summary and content fields, make a request to OpenAI API
    # to create "gpt_summary" and "gpt_content" fields
    

# Save the updated list back to the JSON file
with open(FILE_PATH, "w") as file:
    json.dump(d_list, file, indent=4)

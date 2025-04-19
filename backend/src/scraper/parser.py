import json
import requests


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
    parts = github_url.strip('/').split('/')
    if len(parts) < 5 or parts[2] != 'github.com':
        print(f"Warning: Invalid GitHub repository URL format: {github_url}")
        return None # Return None for invalid URL format

    owner = parts[3]
    repo = parts[4]

    # Common default branches to try
    branches_to_try = ['main', 'master']
    raw_urls = [f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/README.md" for branch in branches_to_try]

    # Attempt to fetch from the potential URLs
    for url in raw_urls:
        try:
            response = requests.get(url)
            # Check if the request was successful (status code 200)
            if not (response.ok):
                print(f"FAILED FOR THIS URL: {url}")
            if response.status_code == 200:
                # print(f"Successfully fetched README from: {url}") # Optional feedback
                return response.text # Return the content immediately upon success
            # If not found (404), try the next URL
            elif response.status_code == 404:
                # print(f"README not found at: {url} - trying next branch...") # Optional feedback
                continue # Continue to the next URL in the list
            else:
                # For other errors, print a warning and try next
                print(f"Warning: Failed to fetch {url} with status code: {response.status_code}")
                continue
        except requests.exceptions.RequestException as e:
            # Handle network or other request errors
            print(f"Warning: An error occurred while trying to fetch {url}: {e}")
            continue # Continue to the next URL in the list

    # If none of the URLs worked after trying all branches
    print(f"Warning: Could not find README.md for repository: {github_url} on main or master branches.")
    return None # Return None if README was not found after trying all options

FILE_PATH = "data.json"
with open(FILE_PATH, "r") as file:
    d_list = json.load(file)

# These are for manually fixed url parsings
BANNED_GITHUB_URLS = [
    "https://github.com/graphhop"
]

for d in d_list:
    if d.get("is_github_url", False):
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

# Save the updated list back to the JSON file
with open(FILE_PATH, "w") as file:
    json.dump(d_list, file, indent=4)

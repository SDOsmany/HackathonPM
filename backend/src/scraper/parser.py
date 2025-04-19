import json
import requests


def get_readme_from_github(repo_url: str) -> str | None:
    # Step 1: Extract owner and repo name
    try:
        parts = repo_url.rstrip("/").split("/")
        owner, repo = parts[-2], parts[-1]
    except IndexError:
        print("Invalid GitHub URL.")
        return None

    # Step 2: Get default branch using GitHub API
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(api_url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch repo info: {response.status_code}")
        return None

    default_branch = response.json().get("default_branch", "main")

    # Step 3: Try fetching the raw README.md file
    raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{default_branch}/README.md"
    readme_response = requests.get(raw_url)

    if readme_response.status_code == 200:
        return readme_response.text
    else:
        print("README.md not found.")
        return None

FILE_PATH = "data.json"
with open(FILE_PATH, "r") as file:
    d_list = json.load(file)

for d in d_list:
    if d.get("is_github_url", False):
        print(f"GitHub URL: {d['url']}")
        # Get README.md file
        github_url = d["url"]
        readme_content = get_readme_from_github(github_url)
        print(f"{github_url}: {readme_content}")
        assert "content" not in d
        d["content"] = readme_content
    else:


# Save the updated list back to the JSON file
with open(FILE_PATH, "w") as file:
    json.dump(d_list, file, indent=4)
        

        



# # Example usage
# url = "https://github.com/openai/openai-python"
# readme_content = get_readme_from_github(url)

# if readme_content:
#     print("README.md contents:")
#     print(readme_content[:500])  # Print first 500 chars

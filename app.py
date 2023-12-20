import os
from dotenv import load_dotenv
import requests
from base64 import b64decode

# Load environment variables from .env file
load_dotenv()

def get_repository_info(repo_url, github_token):
    # Extract owner and repository name from the URL
    parts = repo_url.split('/')
    owner = parts[-2]
    repo_name = parts[-1].replace('.git', '')  # Remove .git if present

    # Construct headers with authentication
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Make the GET request to the GitHub API for repo details
    url = f"https://api.github.com/repos/{owner}/{repo_name}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching repository details: {response.status_code}")
        return None
    
    repository_info = response.json()

    # Fetch latest commits
    latest_commits_url = repository_info.get("commits_url", '').replace('{/sha}', '?per_page=5')
    commits_response = requests.get(latest_commits_url, headers=headers)
    latest_commits = commits_response.json() if commits_response.status_code == 200 else []

    # Fetch README for basic analysis
    readme_url = repository_info.get("contents_url", '').replace('{+path}', 'README.md')
    readme_response = requests.get(readme_url, headers=headers)
    readme_data = readme_response.json() if readme_response.status_code == 200 else {}

    readme_content = b64decode(readme_data.get("content", "")).decode('utf-8') if readme_data.get("content") else "README not available."

    return {
        "name": repository_info.get("name"),
        "description": repository_info.get("description"),
        "language": repository_info.get("language"),
        "clone_url": repository_info.get("clone_url"),
        "stars": repository_info.get("stargazers_count"),
        "forks": repository_info.get("forks_count"),
        "watchers": repository_info.get("watchers_count"),
        "size": repository_info.get("size"),
        "latest_commits": latest_commits,
        "readme": readme_content
    }

def main():
    # Prompt the user for their GitHub personal access token
    print("Please login to GitHub and paste your personal access token here.")
    github_token = input("GitHub Personal Access Token: ")

    repo_url = input("Enter the GitHub repository URL: ")
    repository_info = get_repository_info(repo_url, github_token)

    if repository_info:
        print(f"Name: {repository_info['name']}")
        print(f"Description: {repository_info['description']}")
        print(f"Language: {repository_info['language']}")
        print(f"Clone URL: {repository_info['clone_url']}")
        print(f"Stars: {repository_info['stars']}, Forks: {repository_info['forks']}, Watchers: {repository_info['watchers']}, Size: {repository_info['size']}KB")
        
        print("\nLatest Commits:")
        for commit in repository_info["latest_commits"]:
            print(f"- {commit['commit']['author']['date']}: {commit['commit']['message']}")

        print("\nREADME:")
        print(repository_info["readme"])
    else:
        print("Failed to fetch repository details or invalid token.")

if __name__ == "__main__":
    main()

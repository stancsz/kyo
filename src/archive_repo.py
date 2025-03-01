import requests
import datetime

# Configuration: Replace with your GitHub username and personal access token.
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

# GitHub API base URL
API_BASE = "https://api.github.com"

# Define how long since the last commit to consider a repo "stale"
STALE_THRESHOLD = datetime.timedelta(days=90)

def get_all_repos():
    repos = []
    page = 1
    while True:
        url = f"{API_BASE}/user/repos"
        # type=owner returns repos you own, including private repositories
        params = {"per_page": 100, "page": page, "type": "owner"}
        try:
            response = requests.get(url, params=params, auth=(GITHUB_USERNAME, GITHUB_TOKEN))
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching repositories on page {page}: {e}")
            sys.exit(1)
        
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos

def archive_repo(repo_full_name):
    url = f"{API_BASE}/repos/{repo_full_name}"
    payload = {"archived": True}
    try:
        response = requests.patch(url, json=payload, auth=(GITHUB_USERNAME, GITHUB_TOKEN))
        response.raise_for_status()
        print(f"Archived {repo_full_name}")
    except requests.exceptions.RequestException as e:
        print(f"Error archiving {repo_full_name}: {e}")

def main():
    repos = get_all_repos()
    print(f"Found {len(repos)} repositories.")
    
    now = datetime.datetime.utcnow()
    for repo in repos:
        repo_full_name = repo.get("full_name")
        owner_login = repo.get("owner", {}).get("login", "").lower()
        archived = repo.get("archived", False)
        pushed_at_str = repo.get("pushed_at")
        
        # Only process repos owned by 'stancsz'
        if owner_login != GITHUB_USERNAME.lower():
            print(f"Skipping {repo_full_name} as it is not owned by {GITHUB_USERNAME}.")
            continue
        
        if not repo_full_name or not pushed_at_str:
            print(f"Skipping {repo_full_name} due to missing commit date information.")
            continue
        
        try:
            last_commit_date = datetime.datetime.strptime(pushed_at_str, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError as e:
            print(f"Error parsing last commit date for {repo_full_name}: {e}")
            continue
        
        # Check if repo is already archived
        if archived:
            print(f"{repo_full_name} is already archived. Skipping.")
            continue
        
        # Archive the repo if the last commit was more than 90 days ago
        if now - last_commit_date > STALE_THRESHOLD:
            print(f"{repo_full_name} last pushed on {last_commit_date.date()} is stale. Archiving...")
            archive_repo(repo_full_name)
        else:
            print(f"{repo_full_name} last pushed on {last_commit_date.date()} is active. Skipping.")

if __name__ == "__main__":
    main()
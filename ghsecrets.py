import os
import requests

# Constants
GITHUB_API_URL = "https://api.github.com"
ORG_NAME = "wmgtech"
TOKEN = os.getenv('TEST')  # Fetch the 'TEST' secret from environment

if TOKEN is None:
    raise ValueError("The TEST environment variable is not set. Please set it and try again.")

# Headers for authentication
headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Step 1: Get repositories starting with "wcm-tango"
def get_repositories(org_name):
    url = f"{GITHUB_API_URL}/orgs/{org_name}/repos"
    repos = []
    params = {"per_page": 100}
    
    while url:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        repos.extend([repo for repo in response.json() if repo['name'].startswith('wcm-tango')])
        url = response.links.get('next', {}).get('url')
    
    print(f"Found {len(repos)} repositories starting with 'wcm-tango'")
    return repos

# Step 2: Get secret scanning alerts for each repository
def get_secret_scanning_alerts(repo_full_name):
    url = f"{GITHUB_API_URL}/repos/{repo_full_name}/secret-scanning/alerts"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 404:
        print(f"Secret scanning is not enabled for repository: {repo_full_name}")
        return []
    
    response.raise_for_status()
    return response.json()

# Main script
repositories = get_repositories(ORG_NAME)

# Open a file to write the results
with open('results.txt', 'w') as file:
    for repo in repositories:
        repo_name = repo['full_name']
        alerts = get_secret_scanning_alerts(repo_name)
        open_alerts = [alert for alert in alerts if alert['state'] == 'open']
        
        if open_alerts:
            file.write(f"Repository: {repo_name}\n")
            for alert in open_alerts:
                file.write(f"- Secret: {alert['secret_type']}, Created at: {alert['created_at']}, URL: {alert['html_url']}\n")
            file.write("\n")
            print(f"Written alerts for repository: {repo_name}")
        else:
            print(f"No open alerts for repository: {repo_name}")

print("Results have been written to results.txt")

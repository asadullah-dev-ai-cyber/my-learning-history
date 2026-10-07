import requests
from config import Config

BASE_URL = Config.GITHUB_BASE_URL


def get_headers() -> dict:
    """Constructs HTTP headers, including optional GitHub token for higher rate limits."""
    headers = {"User-Agent": Config.USER_AGENT}
    if Config.GITHUB_TOKEN:
        headers["Authorization"] = f"token {Config.GITHUB_TOKEN}"
    return headers


def get_user_profile(username: str) -> dict:
    url = f"{BASE_URL}/users/{username.strip()}"

    try:
        response = requests.get(
            url,
            headers=get_headers(),
            timeout=Config.REQUEST_TIMEOUT
        )

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return {"error": f"User '{username}' was not found on GitHub."}
        elif response.status_code == 403:
            return {"error": "GitHub API rate limit exceeded. Try adding a GITHUB_TOKEN to .env."}
        else:
            return {"error": f"GitHub API error (Status Code: {response.status_code})"}

    except requests.exceptions.Timeout:
        return {"error": "Request timed out. Please check your connection."}
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error occurred: {e}"}


def get_user_repos(username: str) -> list | dict:
    url = f"{BASE_URL}/users/{username.strip()}/repos"
    params = {
        "per_page": Config.MAX_REPOS_PER_PAGE,
        "sort": "updated"
    }

    try:
        response = requests.get(
            url,
            headers=get_headers(),
            params=params,
            timeout=Config.REQUEST_TIMEOUT
        )

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return {"error": "Repositories not found."}
        elif response.status_code == 403:
            return {"error": "GitHub API rate limit exceeded."}
        else:
            return {"error": f"GitHub API error ({response.status_code})"}

    except requests.exceptions.Timeout:
        return {"error": "Request timed out while fetching repositories."}
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {e}"}
import httpx

class UserNotFoundError(Exception):
    def __init__(self, message, partial_data):
        super().__init__(message)
        self.partial_data = partial_data

class GitHubServerError(Exception):
    def __init__(self, message, partial_data):
        super().__init__(message)
        self.partial_data = partial_data

class GenericError(Exception):
    def __init__(self, message, partial_data):
        super().__init__(message)
        self.partial_data = partial_data

def get_github_user(username: str):
    url = f"https://api.github.com/users/{username}"
    response = httpx.get(url)

    if response.status_code == 404:
        raise UserNotFoundError(f"User '{username}' not found.", {"status": response.status_code, "text": f"User '{username}' not found."})
    if response.status_code >= 500:
        raise GitHubServerError("Server error", {"status": response.status_code, "text": response.text})
    if response.status_code < 200 or response.status_code >= 300:
        raise GenericError("Generic error", {"status": response.status_code, "text": response.text})

    return response.json()

def get_user_public_repos(username: str):
    url = f"https://api.github.com/users/{username}/repos"
    response = httpx.get(url)
    
    if response.status_code == 404:
        raise UserNotFoundError(f"Key error", {"status": response.status_code, "text": f"User '{username}' not found."})
    if response.status_code >= 500:
        raise GitHubServerError("Server error", {"status": response.status_code, "text": response.text})
    if response.status_code < 200 or response.status_code >= 300:
        raise GenericError("Generic error", {"status": response.status_code, "text": response.text})

    return response.json()

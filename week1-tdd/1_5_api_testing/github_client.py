import httpx

class ValidationFailed(Exception):
    def __init__(self, message, partial_data):
        super().__init__(message)
        self.partial_data = partial_data

def get_github_user(username: str):
    url = f"https://api.github.com/users/{username}"
    response = httpx.get(url)
    try:
        if response.status_code == 404:
            raise ValidationFailed(f"Key error", {"status": response.status_code, "text": f"User '{username}' not found."})
        if response.status_code >= 500:
            raise ValidationFailed("Server error", {"status": response.status_code, "text": response.text})
        else:
            print(f"API Error: {response.status_code}: {response.text}")
    except httpx.HTTPStatusError as e:
        raise ValidationFailed(f"Failed to fetch user data", {"status": e.response.status_code, "text": e.response.text})
    return response

def get_user_public_repos(username: str):
    url = f"https://api.github.com/users/{username}/repos"
    response = httpx.get(url)
    try:
        if response.status_code == 404:
            raise ValidationFailed(f"Key error", {"status": response.status_code, "text": f"User '{username}' not found."})
        if response.status_code >= 500:
            raise ValidationFailed("Server error", {"status": response.status_code, "text": response.text})
        else:
            print(f"API Error: {response.status_code}: {response.text}")
    except httpx.HTTPStatusError as e:
        raise ValidationFailed(f"Failed to fetch public repos", {"status": e.response.status_code, "text": e.response.text})
    return response

# main

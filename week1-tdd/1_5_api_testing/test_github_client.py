import httpx, respx, pytest
import github_client as gh_client

# --- real integration test (hits GitHub) ---
@pytest.mark.integration
def test_gh_get_user_real():
    response = gh_client.get_github_user("octocat")
    assert response["login"] == "octocat"

@pytest.mark.integration
def test_gh_get_user_repos_real():
    response = gh_client.get_user_public_repos("octocat")
    assert isinstance(response, list)

# --- mocked test (no network) ---
@respx.mock
def test_gh_user_handle_404():
    respx.get("https://api.github.com/users/na").mock(
        return_value=httpx.Response(404, json={"text": "User not found"})
    )
    with pytest.raises(gh_client.UserNotFoundError) as exc_info:
        gh_client.get_github_user("na")
    assert exc_info.value.partial_data["status"] == 404

@respx.mock
def test_gh_user_handle_500():
    respx.get("https://api.github.com/users/octocat").mock(
        return_value=httpx.Response(500, json={"text": "Server not available"})
    )
    with pytest.raises(gh_client.GitHubServerError) as exc_info:
        gh_client.get_github_user("octocat")
    assert exc_info.value.partial_data["status"] == 500

@respx.mock
def test_gh_user_handle_400():
    respx.get("https://api.github.com/users/octocat").mock(
        return_value=httpx.Response(400, json={"text": "Bad request"})
    )
    with pytest.raises(gh_client.GenericError) as exc_info:
        gh_client.get_github_user("octocat")
    assert exc_info.value.partial_data["status"] == 400

@respx.mock
def test_gh_user_found():
    respx.get("https://api.github.com/users/octocat").mock(
        return_value=httpx.Response(200, json={"login": "octocat"})
    )
    response = gh_client.get_github_user("octocat")

    assert response["login"] == "octocat"

@respx.mock
def test_gh_user_repos_handle_404():
    respx.get("https://api.github.com/users/na/repos").mock(
        return_value=httpx.Response(404, json={"text": "User not found"})
    )
    with pytest.raises(gh_client.UserNotFoundError) as exc_info:
        gh_client.get_user_public_repos("na")
    assert exc_info.value.partial_data["status"] == 404

@respx.mock
def test_gh_user_repos_handle_500():
    respx.get("https://api.github.com/users/octocat/repos").mock(
        return_value=httpx.Response(500, json={"text": "Server not available"})
    )
    with pytest.raises(gh_client.GitHubServerError) as exc_info:
        gh_client.get_user_public_repos("octocat")
    assert exc_info.value.partial_data["status"] == 500

@respx.mock
def test_gh_user_repos_handle_400():
    respx.get("https://api.github.com/users/octocat/repos").mock(
        return_value=httpx.Response(400, json={"text": "Bad request"})
    )
    with pytest.raises(gh_client.GenericError) as exc_info:
        gh_client.get_user_public_repos("octocat")
    assert exc_info.value.partial_data["status"] == 400

@respx.mock
def test_gh_user_repos_found():
    respx.get("https://api.github.com/users/octocat/repos").mock(
        return_value=httpx.Response(200, json=[{"name": "Hello-World"}, {"name": "Spoon-Knife"}])
    )
    response = gh_client.get_user_public_repos("octocat")

    assert isinstance(response, list)
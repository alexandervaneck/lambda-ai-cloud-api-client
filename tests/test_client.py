import httpx

from lambda_ai_cloud_api_client.client import AuthenticatedClient, Client


def test_client_builds_and_reuses_httpx_instances():
    client = Client(base_url="https://api.example.com", timeout=1.5, verify_ssl=False)

    httpx_client = client.get_httpx_client()
    assert isinstance(httpx_client, httpx.Client)
    assert str(httpx_client.base_url) == "https://api.example.com"
    assert httpx_client.timeout.read == 1.5
    assert client._verify_ssl is False

    # reuse existing instances and ensure setters mutate them
    client.with_headers({"X-Test": "1"})
    client.with_cookies({"session": "abc"})
    assert httpx_client.headers["X-Test"] == "1"
    assert httpx_client.cookies["session"] == "abc"

    client.with_timeout(httpx.Timeout(2.0))
    assert httpx_client.timeout.read == 2.0


def test_client_context_manager():
    with Client(base_url="https://api.example.com") as client:
        assert isinstance(client.get_httpx_client(), httpx.Client)


def test_authenticated_client_sets_auth_header():
    auth_client = AuthenticatedClient(base_url="https://api.example.com", token="secret", prefix="Token")
    httpx_client = auth_client.get_httpx_client()
    assert httpx_client.headers["Authorization"] == "Token secret"


def test_authenticated_client_reuses_and_updates():
    auth_client = AuthenticatedClient(base_url="https://api.example.com", token="secret")
    async_client = auth_client.get_async_httpx_client()
    assert async_client.headers["Authorization"] == "Bearer secret"

    auth_client.with_headers({"X-Extra": "yes"})
    auth_client.with_cookies({"session": "123"})
    assert async_client.headers["X-Extra"] == "yes"
    assert async_client.cookies["session"] == "123"


def test_client_custom_httpx_instances():
    custom = httpx.Client(base_url="https://override.test")
    client = Client(base_url="https://api.example.com")
    client.set_httpx_client(custom)
    assert client.get_httpx_client() is custom

    async_custom = httpx.AsyncClient(base_url="https://override.test")
    client.set_async_httpx_client(async_custom)
    assert client.get_async_httpx_client() is async_custom


def test_authenticated_client_context_and_prefixless_token():
    auth_client = AuthenticatedClient(base_url="https://api.example.com", token="secret", prefix="")
    with auth_client as ctx:
        assert ctx.get_httpx_client().headers["Authorization"] == "secret"
    # timeout mutator should update both clients if present
    auth_client.set_async_httpx_client(httpx.AsyncClient())
    auth_client.with_timeout(httpx.Timeout(3.0))
    assert auth_client.get_async_httpx_client().timeout.read == 3.0

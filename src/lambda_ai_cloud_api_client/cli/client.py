import os
from functools import cache
from typing import TypeVar

from lambda_ai_cloud_api_client.client import AuthenticatedClient

DEFAULT_BASE_URL = os.getenv("LAMBDA_CLOUD_BASE_URL", "https://cloud.lambdalabs.com")
TOKEN_ENV_VARS = ("LAMBDA_CLOUD_TOKEN", "LAMBDA_CLOUD_API_TOKEN", "LAMBDA_API_TOKEN")

T = TypeVar("T")


def _load_token() -> str:
    for env_var in TOKEN_ENV_VARS:
        token = os.getenv(env_var)
        if token:
            return token
    raise RuntimeError(
        f"No API token provided. Supply --token or set one of: {', '.join(TOKEN_ENV_VARS)}",
    )


@cache
def auth_client() -> AuthenticatedClient:
    base_url = os.getenv("LAMBDA_CLOUD_BASE_URL", DEFAULT_BASE_URL)
    token = _load_token()
    verify_ssl = os.getenv("LAMBDA_CLOUD_VERIFY_SSL", True)

    client = AuthenticatedClient(
        base_url=base_url,
        token=token,
        verify_ssl=verify_ssl,
    )
    return client

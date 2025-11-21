"""Command line wrapper for the Lambda Cloud API client (click-based)."""

from __future__ import annotations

import os
import sys
from types import SimpleNamespace
from typing import TypeVar

from lambda_ai_cloud_api_client.client import AuthenticatedClient

DEFAULT_BASE_URL = os.getenv("LAMBDA_CLOUD_BASE_URL", "https://cloud.lambdalabs.com")
TOKEN_ENV_VARS = ("LAMBDA_CLOUD_TOKEN", "LAMBDA_CLOUD_API_TOKEN", "LAMBDA_API_TOKEN")

T = TypeVar("T")


def _load_token(explicit_token: str | None) -> str:
    if explicit_token:
        return explicit_token
    for env_var in TOKEN_ENV_VARS:
        token = os.getenv(env_var)
        if token:
            return token
    print(
        f"No API token provided. Supply --token or set one of: {', '.join(TOKEN_ENV_VARS)}",
        file=sys.stderr,
    )
    sys.exit(1)


def auth_client(args: SimpleNamespace) -> AuthenticatedClient:
    token = _load_token(args.token)
    client = AuthenticatedClient(
        base_url=args.base_url,
        token=token,
        verify_ssl=not args.insecure,
    )
    return client

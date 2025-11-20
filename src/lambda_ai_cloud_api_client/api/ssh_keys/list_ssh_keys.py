from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_ssh_keys_response_200 import ListSSHKeysResponse200
from ...models.list_ssh_keys_response_401 import ListSSHKeysResponse401
from ...models.list_ssh_keys_response_403 import ListSSHKeysResponse403
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/ssh-keys",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ListSSHKeysResponse200 | ListSSHKeysResponse401 | ListSSHKeysResponse403 | None:
    if response.status_code == 200:
        response_200 = ListSSHKeysResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ListSSHKeysResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ListSSHKeysResponse403.from_dict(response.json())

        return response_403

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ListSSHKeysResponse200 | ListSSHKeysResponse401 | ListSSHKeysResponse403]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[ListSSHKeysResponse200 | ListSSHKeysResponse401 | ListSSHKeysResponse403]:
    """List your SSH keys

     Retrieves a list of your SSH keys.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListSSHKeysResponse200 | ListSSHKeysResponse401 | ListSSHKeysResponse403]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> ListSSHKeysResponse200 | ListSSHKeysResponse401 | ListSSHKeysResponse403 | None:
    """List your SSH keys

     Retrieves a list of your SSH keys.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListSSHKeysResponse200 | ListSSHKeysResponse401 | ListSSHKeysResponse403
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[ListSSHKeysResponse200 | ListSSHKeysResponse401 | ListSSHKeysResponse403]:
    """List your SSH keys

     Retrieves a list of your SSH keys.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListSSHKeysResponse200 | ListSSHKeysResponse401 | ListSSHKeysResponse403]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> ListSSHKeysResponse200 | ListSSHKeysResponse401 | ListSSHKeysResponse403 | None:
    """List your SSH keys

     Retrieves a list of your SSH keys.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListSSHKeysResponse200 | ListSSHKeysResponse401 | ListSSHKeysResponse403
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed

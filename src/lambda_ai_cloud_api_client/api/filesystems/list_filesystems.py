from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_filesystems_response_200 import ListFilesystemsResponse200
from ...models.list_filesystems_response_401 import ListFilesystemsResponse401
from ...models.list_filesystems_response_403 import ListFilesystemsResponse403
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/file-systems",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ListFilesystemsResponse200 | ListFilesystemsResponse401 | ListFilesystemsResponse403 | None:
    if response.status_code == 200:
        response_200 = ListFilesystemsResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ListFilesystemsResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ListFilesystemsResponse403.from_dict(response.json())

        return response_403

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ListFilesystemsResponse200 | ListFilesystemsResponse401 | ListFilesystemsResponse403]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[ListFilesystemsResponse200 | ListFilesystemsResponse401 | ListFilesystemsResponse403]:
    """List filesystems

     Retrieves a list of your filesystems.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListFilesystemsResponse200 | ListFilesystemsResponse401 | ListFilesystemsResponse403]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> ListFilesystemsResponse200 | ListFilesystemsResponse401 | ListFilesystemsResponse403 | None:
    """List filesystems

     Retrieves a list of your filesystems.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListFilesystemsResponse200 | ListFilesystemsResponse401 | ListFilesystemsResponse403
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[ListFilesystemsResponse200 | ListFilesystemsResponse401 | ListFilesystemsResponse403]:
    """List filesystems

     Retrieves a list of your filesystems.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListFilesystemsResponse200 | ListFilesystemsResponse401 | ListFilesystemsResponse403]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> ListFilesystemsResponse200 | ListFilesystemsResponse401 | ListFilesystemsResponse403 | None:
    """List filesystems

     Retrieves a list of your filesystems.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListFilesystemsResponse200 | ListFilesystemsResponse401 | ListFilesystemsResponse403
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed

from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.filesystem_delete_response_200 import FilesystemDeleteResponse200
from ...models.filesystem_delete_response_400 import FilesystemDeleteResponse400
from ...models.filesystem_delete_response_401 import FilesystemDeleteResponse401
from ...models.filesystem_delete_response_403 import FilesystemDeleteResponse403
from ...models.filesystem_delete_response_404 import FilesystemDeleteResponse404
from ...types import Response


def _get_kwargs(
    id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": f"/api/v1/filesystems/{id}",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    FilesystemDeleteResponse200
    | FilesystemDeleteResponse400
    | FilesystemDeleteResponse401
    | FilesystemDeleteResponse403
    | FilesystemDeleteResponse404
    | None
):
    if response.status_code == 200:
        response_200 = FilesystemDeleteResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = FilesystemDeleteResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = FilesystemDeleteResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = FilesystemDeleteResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = FilesystemDeleteResponse404.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    FilesystemDeleteResponse200
    | FilesystemDeleteResponse400
    | FilesystemDeleteResponse401
    | FilesystemDeleteResponse403
    | FilesystemDeleteResponse404
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    FilesystemDeleteResponse200
    | FilesystemDeleteResponse400
    | FilesystemDeleteResponse401
    | FilesystemDeleteResponse403
    | FilesystemDeleteResponse404
]:
    """Delete filesystem

     Deletes the filesystem with the specified ID. The filesystem must not be mounted to any running
    instances at the time of deletion.

    Args:
        id (str): The unique identifier (ID) of the filesystem to delete Example:
            398578a2336b49079e74043f0bd2cfe8.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FilesystemDeleteResponse200 | FilesystemDeleteResponse400 | FilesystemDeleteResponse401 | FilesystemDeleteResponse403 | FilesystemDeleteResponse404]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient,
) -> (
    FilesystemDeleteResponse200
    | FilesystemDeleteResponse400
    | FilesystemDeleteResponse401
    | FilesystemDeleteResponse403
    | FilesystemDeleteResponse404
    | None
):
    """Delete filesystem

     Deletes the filesystem with the specified ID. The filesystem must not be mounted to any running
    instances at the time of deletion.

    Args:
        id (str): The unique identifier (ID) of the filesystem to delete Example:
            398578a2336b49079e74043f0bd2cfe8.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FilesystemDeleteResponse200 | FilesystemDeleteResponse400 | FilesystemDeleteResponse401 | FilesystemDeleteResponse403 | FilesystemDeleteResponse404
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    FilesystemDeleteResponse200
    | FilesystemDeleteResponse400
    | FilesystemDeleteResponse401
    | FilesystemDeleteResponse403
    | FilesystemDeleteResponse404
]:
    """Delete filesystem

     Deletes the filesystem with the specified ID. The filesystem must not be mounted to any running
    instances at the time of deletion.

    Args:
        id (str): The unique identifier (ID) of the filesystem to delete Example:
            398578a2336b49079e74043f0bd2cfe8.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FilesystemDeleteResponse200 | FilesystemDeleteResponse400 | FilesystemDeleteResponse401 | FilesystemDeleteResponse403 | FilesystemDeleteResponse404]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
) -> (
    FilesystemDeleteResponse200
    | FilesystemDeleteResponse400
    | FilesystemDeleteResponse401
    | FilesystemDeleteResponse403
    | FilesystemDeleteResponse404
    | None
):
    """Delete filesystem

     Deletes the filesystem with the specified ID. The filesystem must not be mounted to any running
    instances at the time of deletion.

    Args:
        id (str): The unique identifier (ID) of the filesystem to delete Example:
            398578a2336b49079e74043f0bd2cfe8.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FilesystemDeleteResponse200 | FilesystemDeleteResponse400 | FilesystemDeleteResponse401 | FilesystemDeleteResponse403 | FilesystemDeleteResponse404
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed

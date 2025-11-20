from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_ssh_key_response_200 import DeleteSSHKeyResponse200
from ...models.delete_ssh_key_response_400 import DeleteSSHKeyResponse400
from ...models.delete_ssh_key_response_401 import DeleteSSHKeyResponse401
from ...models.delete_ssh_key_response_403 import DeleteSSHKeyResponse403
from ...types import Response


def _get_kwargs(
    id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": f"/api/v1/ssh-keys/{id}",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DeleteSSHKeyResponse200 | DeleteSSHKeyResponse400 | DeleteSSHKeyResponse401 | DeleteSSHKeyResponse403 | None:
    if response.status_code == 200:
        response_200 = DeleteSSHKeyResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = DeleteSSHKeyResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = DeleteSSHKeyResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = DeleteSSHKeyResponse403.from_dict(response.json())

        return response_403

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[DeleteSSHKeyResponse200 | DeleteSSHKeyResponse400 | DeleteSSHKeyResponse401 | DeleteSSHKeyResponse403]:
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
) -> Response[DeleteSSHKeyResponse200 | DeleteSSHKeyResponse400 | DeleteSSHKeyResponse401 | DeleteSSHKeyResponse403]:
    """Delete an SSH key

     Deletes the specified SSH key.

    Args:
        id (str): The unique identifier (ID) of the SSH key to delete Example:
            ddf9a910ceb744a0bb95242cbba6cb50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteSSHKeyResponse200 | DeleteSSHKeyResponse400 | DeleteSSHKeyResponse401 | DeleteSSHKeyResponse403]
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
) -> DeleteSSHKeyResponse200 | DeleteSSHKeyResponse400 | DeleteSSHKeyResponse401 | DeleteSSHKeyResponse403 | None:
    """Delete an SSH key

     Deletes the specified SSH key.

    Args:
        id (str): The unique identifier (ID) of the SSH key to delete Example:
            ddf9a910ceb744a0bb95242cbba6cb50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteSSHKeyResponse200 | DeleteSSHKeyResponse400 | DeleteSSHKeyResponse401 | DeleteSSHKeyResponse403
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
) -> Response[DeleteSSHKeyResponse200 | DeleteSSHKeyResponse400 | DeleteSSHKeyResponse401 | DeleteSSHKeyResponse403]:
    """Delete an SSH key

     Deletes the specified SSH key.

    Args:
        id (str): The unique identifier (ID) of the SSH key to delete Example:
            ddf9a910ceb744a0bb95242cbba6cb50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteSSHKeyResponse200 | DeleteSSHKeyResponse400 | DeleteSSHKeyResponse401 | DeleteSSHKeyResponse403]
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
) -> DeleteSSHKeyResponse200 | DeleteSSHKeyResponse400 | DeleteSSHKeyResponse401 | DeleteSSHKeyResponse403 | None:
    """Delete an SSH key

     Deletes the specified SSH key.

    Args:
        id (str): The unique identifier (ID) of the SSH key to delete Example:
            ddf9a910ceb744a0bb95242cbba6cb50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteSSHKeyResponse200 | DeleteSSHKeyResponse400 | DeleteSSHKeyResponse401 | DeleteSSHKeyResponse403
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed

from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_instance_response_200 import GetInstanceResponse200
from ...models.get_instance_response_401 import GetInstanceResponse401
from ...models.get_instance_response_403 import GetInstanceResponse403
from ...models.get_instance_response_404 import GetInstanceResponse404
from ...types import Response


def _get_kwargs(
    id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/v1/instances/{id}",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GetInstanceResponse200 | GetInstanceResponse401 | GetInstanceResponse403 | GetInstanceResponse404 | None:
    if response.status_code == 200:
        response_200 = GetInstanceResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = GetInstanceResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = GetInstanceResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = GetInstanceResponse404.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GetInstanceResponse200 | GetInstanceResponse401 | GetInstanceResponse403 | GetInstanceResponse404]:
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
) -> Response[GetInstanceResponse200 | GetInstanceResponse401 | GetInstanceResponse403 | GetInstanceResponse404]:
    """Retrieve instance details

     Retrieves the details of a specific instance, including whether or not the instance is running.

    Args:
        id (str): The unique identifier (ID) of the instance Example:
            ddaedf1b7a0e41ac981711504493b242.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetInstanceResponse200 | GetInstanceResponse401 | GetInstanceResponse403 | GetInstanceResponse404]
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
) -> GetInstanceResponse200 | GetInstanceResponse401 | GetInstanceResponse403 | GetInstanceResponse404 | None:
    """Retrieve instance details

     Retrieves the details of a specific instance, including whether or not the instance is running.

    Args:
        id (str): The unique identifier (ID) of the instance Example:
            ddaedf1b7a0e41ac981711504493b242.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetInstanceResponse200 | GetInstanceResponse401 | GetInstanceResponse403 | GetInstanceResponse404
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
) -> Response[GetInstanceResponse200 | GetInstanceResponse401 | GetInstanceResponse403 | GetInstanceResponse404]:
    """Retrieve instance details

     Retrieves the details of a specific instance, including whether or not the instance is running.

    Args:
        id (str): The unique identifier (ID) of the instance Example:
            ddaedf1b7a0e41ac981711504493b242.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetInstanceResponse200 | GetInstanceResponse401 | GetInstanceResponse403 | GetInstanceResponse404]
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
) -> GetInstanceResponse200 | GetInstanceResponse401 | GetInstanceResponse403 | GetInstanceResponse404 | None:
    """Retrieve instance details

     Retrieves the details of a specific instance, including whether or not the instance is running.

    Args:
        id (str): The unique identifier (ID) of the instance Example:
            ddaedf1b7a0e41ac981711504493b242.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetInstanceResponse200 | GetInstanceResponse401 | GetInstanceResponse403 | GetInstanceResponse404
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed

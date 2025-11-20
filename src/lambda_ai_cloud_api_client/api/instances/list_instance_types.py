from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_instance_types_response_200 import ListInstanceTypesResponse200
from ...models.list_instance_types_response_401 import ListInstanceTypesResponse401
from ...models.list_instance_types_response_403 import ListInstanceTypesResponse403
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/instance-types",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ListInstanceTypesResponse200 | ListInstanceTypesResponse401 | ListInstanceTypesResponse403 | None:
    if response.status_code == 200:
        response_200 = ListInstanceTypesResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ListInstanceTypesResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ListInstanceTypesResponse403.from_dict(response.json())

        return response_403

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ListInstanceTypesResponse200 | ListInstanceTypesResponse401 | ListInstanceTypesResponse403]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[ListInstanceTypesResponse200 | ListInstanceTypesResponse401 | ListInstanceTypesResponse403]:
    """List available instance types

     Retrieves a list of the instance types currently offered on Lambda's public cloud, as well as
    details about each type. Details include resource specifications, pricing, and regional
    availability.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListInstanceTypesResponse200 | ListInstanceTypesResponse401 | ListInstanceTypesResponse403]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> ListInstanceTypesResponse200 | ListInstanceTypesResponse401 | ListInstanceTypesResponse403 | None:
    """List available instance types

     Retrieves a list of the instance types currently offered on Lambda's public cloud, as well as
    details about each type. Details include resource specifications, pricing, and regional
    availability.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListInstanceTypesResponse200 | ListInstanceTypesResponse401 | ListInstanceTypesResponse403
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[ListInstanceTypesResponse200 | ListInstanceTypesResponse401 | ListInstanceTypesResponse403]:
    """List available instance types

     Retrieves a list of the instance types currently offered on Lambda's public cloud, as well as
    details about each type. Details include resource specifications, pricing, and regional
    availability.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListInstanceTypesResponse200 | ListInstanceTypesResponse401 | ListInstanceTypesResponse403]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> ListInstanceTypesResponse200 | ListInstanceTypesResponse401 | ListInstanceTypesResponse403 | None:
    """List available instance types

     Retrieves a list of the instance types currently offered on Lambda's public cloud, as well as
    details about each type. Details include resource specifications, pricing, and regional
    availability.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListInstanceTypesResponse200 | ListInstanceTypesResponse401 | ListInstanceTypesResponse403
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed

from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.instance_modification_request import InstanceModificationRequest
from ...models.post_instance_response_200 import PostInstanceResponse200
from ...models.post_instance_response_400 import PostInstanceResponse400
from ...models.post_instance_response_401 import PostInstanceResponse401
from ...models.post_instance_response_403 import PostInstanceResponse403
from ...models.post_instance_response_404 import PostInstanceResponse404
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    body: InstanceModificationRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/v1/instances/{id}",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    PostInstanceResponse200
    | PostInstanceResponse400
    | PostInstanceResponse401
    | PostInstanceResponse403
    | PostInstanceResponse404
    | None
):
    if response.status_code == 200:
        response_200 = PostInstanceResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = PostInstanceResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = PostInstanceResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = PostInstanceResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = PostInstanceResponse404.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    PostInstanceResponse200
    | PostInstanceResponse400
    | PostInstanceResponse401
    | PostInstanceResponse403
    | PostInstanceResponse404
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
    body: InstanceModificationRequest,
) -> Response[
    PostInstanceResponse200
    | PostInstanceResponse400
    | PostInstanceResponse401
    | PostInstanceResponse403
    | PostInstanceResponse404
]:
    """Update instance details

     Updates the details of the specified instance.

    Args:
        id (str): The unique identifier (ID) of the instance Example:
            ddaedf1b7a0e41ac981711504493b242.
        body (InstanceModificationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostInstanceResponse200 | PostInstanceResponse400 | PostInstanceResponse401 | PostInstanceResponse403 | PostInstanceResponse404]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient,
    body: InstanceModificationRequest,
) -> (
    PostInstanceResponse200
    | PostInstanceResponse400
    | PostInstanceResponse401
    | PostInstanceResponse403
    | PostInstanceResponse404
    | None
):
    """Update instance details

     Updates the details of the specified instance.

    Args:
        id (str): The unique identifier (ID) of the instance Example:
            ddaedf1b7a0e41ac981711504493b242.
        body (InstanceModificationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostInstanceResponse200 | PostInstanceResponse400 | PostInstanceResponse401 | PostInstanceResponse403 | PostInstanceResponse404
    """

    return sync_detailed(
        id=id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    body: InstanceModificationRequest,
) -> Response[
    PostInstanceResponse200
    | PostInstanceResponse400
    | PostInstanceResponse401
    | PostInstanceResponse403
    | PostInstanceResponse404
]:
    """Update instance details

     Updates the details of the specified instance.

    Args:
        id (str): The unique identifier (ID) of the instance Example:
            ddaedf1b7a0e41ac981711504493b242.
        body (InstanceModificationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostInstanceResponse200 | PostInstanceResponse400 | PostInstanceResponse401 | PostInstanceResponse403 | PostInstanceResponse404]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
    body: InstanceModificationRequest,
) -> (
    PostInstanceResponse200
    | PostInstanceResponse400
    | PostInstanceResponse401
    | PostInstanceResponse403
    | PostInstanceResponse404
    | None
):
    """Update instance details

     Updates the details of the specified instance.

    Args:
        id (str): The unique identifier (ID) of the instance Example:
            ddaedf1b7a0e41ac981711504493b242.
        body (InstanceModificationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostInstanceResponse200 | PostInstanceResponse400 | PostInstanceResponse401 | PostInstanceResponse403 | PostInstanceResponse404
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed

from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.instance_terminate_request import InstanceTerminateRequest
from ...models.terminate_instance_response_200 import TerminateInstanceResponse200
from ...models.terminate_instance_response_401 import TerminateInstanceResponse401
from ...models.terminate_instance_response_403 import TerminateInstanceResponse403
from ...models.terminate_instance_response_404 import TerminateInstanceResponse404
from ...types import Response


def _get_kwargs(
    *,
    body: InstanceTerminateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/instance-operations/terminate",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    TerminateInstanceResponse200
    | TerminateInstanceResponse401
    | TerminateInstanceResponse403
    | TerminateInstanceResponse404
    | None
):
    if response.status_code == 200:
        response_200 = TerminateInstanceResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = TerminateInstanceResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = TerminateInstanceResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = TerminateInstanceResponse404.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    TerminateInstanceResponse200
    | TerminateInstanceResponse401
    | TerminateInstanceResponse403
    | TerminateInstanceResponse404
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: InstanceTerminateRequest,
) -> Response[
    TerminateInstanceResponse200
    | TerminateInstanceResponse401
    | TerminateInstanceResponse403
    | TerminateInstanceResponse404
]:
    """Terminate instances

     Terminates one or more instances.

    Args:
        body (InstanceTerminateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TerminateInstanceResponse200 | TerminateInstanceResponse401 | TerminateInstanceResponse403 | TerminateInstanceResponse404]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: InstanceTerminateRequest,
) -> (
    TerminateInstanceResponse200
    | TerminateInstanceResponse401
    | TerminateInstanceResponse403
    | TerminateInstanceResponse404
    | None
):
    """Terminate instances

     Terminates one or more instances.

    Args:
        body (InstanceTerminateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TerminateInstanceResponse200 | TerminateInstanceResponse401 | TerminateInstanceResponse403 | TerminateInstanceResponse404
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: InstanceTerminateRequest,
) -> Response[
    TerminateInstanceResponse200
    | TerminateInstanceResponse401
    | TerminateInstanceResponse403
    | TerminateInstanceResponse404
]:
    """Terminate instances

     Terminates one or more instances.

    Args:
        body (InstanceTerminateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TerminateInstanceResponse200 | TerminateInstanceResponse401 | TerminateInstanceResponse403 | TerminateInstanceResponse404]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: InstanceTerminateRequest,
) -> (
    TerminateInstanceResponse200
    | TerminateInstanceResponse401
    | TerminateInstanceResponse403
    | TerminateInstanceResponse404
    | None
):
    """Terminate instances

     Terminates one or more instances.

    Args:
        body (InstanceTerminateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TerminateInstanceResponse200 | TerminateInstanceResponse401 | TerminateInstanceResponse403 | TerminateInstanceResponse404
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed

from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.instance_launch_request import InstanceLaunchRequest
from ...models.launch_instance_response_200 import LaunchInstanceResponse200
from ...models.launch_instance_response_400 import LaunchInstanceResponse400
from ...models.launch_instance_response_401 import LaunchInstanceResponse401
from ...models.launch_instance_response_403 import LaunchInstanceResponse403
from ...models.launch_instance_response_404 import LaunchInstanceResponse404
from ...types import Response


def _get_kwargs(
    *,
    body: InstanceLaunchRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/instance-operations/launch",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    LaunchInstanceResponse200
    | LaunchInstanceResponse400
    | LaunchInstanceResponse401
    | LaunchInstanceResponse403
    | LaunchInstanceResponse404
    | None
):
    if response.status_code == 200:
        response_200 = LaunchInstanceResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = LaunchInstanceResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = LaunchInstanceResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = LaunchInstanceResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = LaunchInstanceResponse404.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    LaunchInstanceResponse200
    | LaunchInstanceResponse400
    | LaunchInstanceResponse401
    | LaunchInstanceResponse403
    | LaunchInstanceResponse404
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
    body: InstanceLaunchRequest,
) -> Response[
    LaunchInstanceResponse200
    | LaunchInstanceResponse400
    | LaunchInstanceResponse401
    | LaunchInstanceResponse403
    | LaunchInstanceResponse404
]:
    """Launch instances

     Launches a Lambda On-Demand Cloud instance.

    Args:
        body (InstanceLaunchRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[LaunchInstanceResponse200 | LaunchInstanceResponse400 | LaunchInstanceResponse401 | LaunchInstanceResponse403 | LaunchInstanceResponse404]
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
    body: InstanceLaunchRequest,
) -> (
    LaunchInstanceResponse200
    | LaunchInstanceResponse400
    | LaunchInstanceResponse401
    | LaunchInstanceResponse403
    | LaunchInstanceResponse404
    | None
):
    """Launch instances

     Launches a Lambda On-Demand Cloud instance.

    Args:
        body (InstanceLaunchRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        LaunchInstanceResponse200 | LaunchInstanceResponse400 | LaunchInstanceResponse401 | LaunchInstanceResponse403 | LaunchInstanceResponse404
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: InstanceLaunchRequest,
) -> Response[
    LaunchInstanceResponse200
    | LaunchInstanceResponse400
    | LaunchInstanceResponse401
    | LaunchInstanceResponse403
    | LaunchInstanceResponse404
]:
    """Launch instances

     Launches a Lambda On-Demand Cloud instance.

    Args:
        body (InstanceLaunchRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[LaunchInstanceResponse200 | LaunchInstanceResponse400 | LaunchInstanceResponse401 | LaunchInstanceResponse403 | LaunchInstanceResponse404]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: InstanceLaunchRequest,
) -> (
    LaunchInstanceResponse200
    | LaunchInstanceResponse400
    | LaunchInstanceResponse401
    | LaunchInstanceResponse403
    | LaunchInstanceResponse404
    | None
):
    """Launch instances

     Launches a Lambda On-Demand Cloud instance.

    Args:
        body (InstanceLaunchRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        LaunchInstanceResponse200 | LaunchInstanceResponse400 | LaunchInstanceResponse401 | LaunchInstanceResponse403 | LaunchInstanceResponse404
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed

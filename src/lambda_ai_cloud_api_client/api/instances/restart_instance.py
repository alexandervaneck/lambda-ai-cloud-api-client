from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.instance_restart_request import InstanceRestartRequest
from ...models.restart_instance_response_200 import RestartInstanceResponse200
from ...models.restart_instance_response_401 import RestartInstanceResponse401
from ...models.restart_instance_response_403 import RestartInstanceResponse403
from ...models.restart_instance_response_404 import RestartInstanceResponse404
from ...types import Response


def _get_kwargs(
    *,
    body: InstanceRestartRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/instance-operations/restart",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    RestartInstanceResponse200
    | RestartInstanceResponse401
    | RestartInstanceResponse403
    | RestartInstanceResponse404
    | None
):
    if response.status_code == 200:
        response_200 = RestartInstanceResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = RestartInstanceResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = RestartInstanceResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = RestartInstanceResponse404.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    RestartInstanceResponse200 | RestartInstanceResponse401 | RestartInstanceResponse403 | RestartInstanceResponse404
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
    body: InstanceRestartRequest,
) -> Response[
    RestartInstanceResponse200 | RestartInstanceResponse401 | RestartInstanceResponse403 | RestartInstanceResponse404
]:
    """Restart instances

     Restarts one or more instances.

    Args:
        body (InstanceRestartRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RestartInstanceResponse200 | RestartInstanceResponse401 | RestartInstanceResponse403 | RestartInstanceResponse404]
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
    body: InstanceRestartRequest,
) -> (
    RestartInstanceResponse200
    | RestartInstanceResponse401
    | RestartInstanceResponse403
    | RestartInstanceResponse404
    | None
):
    """Restart instances

     Restarts one or more instances.

    Args:
        body (InstanceRestartRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RestartInstanceResponse200 | RestartInstanceResponse401 | RestartInstanceResponse403 | RestartInstanceResponse404
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: InstanceRestartRequest,
) -> Response[
    RestartInstanceResponse200 | RestartInstanceResponse401 | RestartInstanceResponse403 | RestartInstanceResponse404
]:
    """Restart instances

     Restarts one or more instances.

    Args:
        body (InstanceRestartRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RestartInstanceResponse200 | RestartInstanceResponse401 | RestartInstanceResponse403 | RestartInstanceResponse404]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: InstanceRestartRequest,
) -> (
    RestartInstanceResponse200
    | RestartInstanceResponse401
    | RestartInstanceResponse403
    | RestartInstanceResponse404
    | None
):
    """Restart instances

     Restarts one or more instances.

    Args:
        body (InstanceRestartRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RestartInstanceResponse200 | RestartInstanceResponse401 | RestartInstanceResponse403 | RestartInstanceResponse404
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed

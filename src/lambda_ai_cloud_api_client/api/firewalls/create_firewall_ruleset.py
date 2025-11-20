from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_firewall_ruleset_response_200 import CreateFirewallRulesetResponse200
from ...models.create_firewall_ruleset_response_400 import CreateFirewallRulesetResponse400
from ...models.create_firewall_ruleset_response_401 import CreateFirewallRulesetResponse401
from ...models.create_firewall_ruleset_response_403 import CreateFirewallRulesetResponse403
from ...models.create_firewall_ruleset_response_409 import CreateFirewallRulesetResponse409
from ...models.firewall_ruleset_create_request import FirewallRulesetCreateRequest
from ...types import Response


def _get_kwargs(
    *,
    body: FirewallRulesetCreateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/firewall-rulesets",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    CreateFirewallRulesetResponse200
    | CreateFirewallRulesetResponse400
    | CreateFirewallRulesetResponse401
    | CreateFirewallRulesetResponse403
    | CreateFirewallRulesetResponse409
    | None
):
    if response.status_code == 200:
        response_200 = CreateFirewallRulesetResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = CreateFirewallRulesetResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = CreateFirewallRulesetResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = CreateFirewallRulesetResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 409:
        response_409 = CreateFirewallRulesetResponse409.from_dict(response.json())

        return response_409

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    CreateFirewallRulesetResponse200
    | CreateFirewallRulesetResponse400
    | CreateFirewallRulesetResponse401
    | CreateFirewallRulesetResponse403
    | CreateFirewallRulesetResponse409
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
    body: FirewallRulesetCreateRequest,
) -> Response[
    CreateFirewallRulesetResponse200
    | CreateFirewallRulesetResponse400
    | CreateFirewallRulesetResponse401
    | CreateFirewallRulesetResponse403
    | CreateFirewallRulesetResponse409
]:
    """Create firewall ruleset

     Creates a new firewall ruleset with the specified name and rules.

    Args:
        body (FirewallRulesetCreateRequest): Request to create a new firewall ruleset.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateFirewallRulesetResponse200 | CreateFirewallRulesetResponse400 | CreateFirewallRulesetResponse401 | CreateFirewallRulesetResponse403 | CreateFirewallRulesetResponse409]
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
    body: FirewallRulesetCreateRequest,
) -> (
    CreateFirewallRulesetResponse200
    | CreateFirewallRulesetResponse400
    | CreateFirewallRulesetResponse401
    | CreateFirewallRulesetResponse403
    | CreateFirewallRulesetResponse409
    | None
):
    """Create firewall ruleset

     Creates a new firewall ruleset with the specified name and rules.

    Args:
        body (FirewallRulesetCreateRequest): Request to create a new firewall ruleset.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateFirewallRulesetResponse200 | CreateFirewallRulesetResponse400 | CreateFirewallRulesetResponse401 | CreateFirewallRulesetResponse403 | CreateFirewallRulesetResponse409
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: FirewallRulesetCreateRequest,
) -> Response[
    CreateFirewallRulesetResponse200
    | CreateFirewallRulesetResponse400
    | CreateFirewallRulesetResponse401
    | CreateFirewallRulesetResponse403
    | CreateFirewallRulesetResponse409
]:
    """Create firewall ruleset

     Creates a new firewall ruleset with the specified name and rules.

    Args:
        body (FirewallRulesetCreateRequest): Request to create a new firewall ruleset.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateFirewallRulesetResponse200 | CreateFirewallRulesetResponse400 | CreateFirewallRulesetResponse401 | CreateFirewallRulesetResponse403 | CreateFirewallRulesetResponse409]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: FirewallRulesetCreateRequest,
) -> (
    CreateFirewallRulesetResponse200
    | CreateFirewallRulesetResponse400
    | CreateFirewallRulesetResponse401
    | CreateFirewallRulesetResponse403
    | CreateFirewallRulesetResponse409
    | None
):
    """Create firewall ruleset

     Creates a new firewall ruleset with the specified name and rules.

    Args:
        body (FirewallRulesetCreateRequest): Request to create a new firewall ruleset.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateFirewallRulesetResponse200 | CreateFirewallRulesetResponse400 | CreateFirewallRulesetResponse401 | CreateFirewallRulesetResponse403 | CreateFirewallRulesetResponse409
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed

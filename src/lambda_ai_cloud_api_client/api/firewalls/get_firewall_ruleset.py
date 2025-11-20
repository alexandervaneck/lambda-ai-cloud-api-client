from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_firewall_ruleset_response_200 import GetFirewallRulesetResponse200
from ...models.get_firewall_ruleset_response_401 import GetFirewallRulesetResponse401
from ...models.get_firewall_ruleset_response_403 import GetFirewallRulesetResponse403
from ...models.get_firewall_ruleset_response_404 import GetFirewallRulesetResponse404
from ...types import Response


def _get_kwargs(
    id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/v1/firewall-rulesets/{id}",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    GetFirewallRulesetResponse200
    | GetFirewallRulesetResponse401
    | GetFirewallRulesetResponse403
    | GetFirewallRulesetResponse404
    | None
):
    if response.status_code == 200:
        response_200 = GetFirewallRulesetResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = GetFirewallRulesetResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = GetFirewallRulesetResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = GetFirewallRulesetResponse404.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    GetFirewallRulesetResponse200
    | GetFirewallRulesetResponse401
    | GetFirewallRulesetResponse403
    | GetFirewallRulesetResponse404
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
    GetFirewallRulesetResponse200
    | GetFirewallRulesetResponse401
    | GetFirewallRulesetResponse403
    | GetFirewallRulesetResponse404
]:
    """Retrieve firewall ruleset details

     Retrieves the details of a specific firewall ruleset.

    Args:
        id (str): The unique identifier (ID) of the firewall ruleset Example:
            c4d291f47f9d436fa39f58493ce3b50d.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetFirewallRulesetResponse200 | GetFirewallRulesetResponse401 | GetFirewallRulesetResponse403 | GetFirewallRulesetResponse404]
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
    GetFirewallRulesetResponse200
    | GetFirewallRulesetResponse401
    | GetFirewallRulesetResponse403
    | GetFirewallRulesetResponse404
    | None
):
    """Retrieve firewall ruleset details

     Retrieves the details of a specific firewall ruleset.

    Args:
        id (str): The unique identifier (ID) of the firewall ruleset Example:
            c4d291f47f9d436fa39f58493ce3b50d.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetFirewallRulesetResponse200 | GetFirewallRulesetResponse401 | GetFirewallRulesetResponse403 | GetFirewallRulesetResponse404
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
    GetFirewallRulesetResponse200
    | GetFirewallRulesetResponse401
    | GetFirewallRulesetResponse403
    | GetFirewallRulesetResponse404
]:
    """Retrieve firewall ruleset details

     Retrieves the details of a specific firewall ruleset.

    Args:
        id (str): The unique identifier (ID) of the firewall ruleset Example:
            c4d291f47f9d436fa39f58493ce3b50d.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetFirewallRulesetResponse200 | GetFirewallRulesetResponse401 | GetFirewallRulesetResponse403 | GetFirewallRulesetResponse404]
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
    GetFirewallRulesetResponse200
    | GetFirewallRulesetResponse401
    | GetFirewallRulesetResponse403
    | GetFirewallRulesetResponse404
    | None
):
    """Retrieve firewall ruleset details

     Retrieves the details of a specific firewall ruleset.

    Args:
        id (str): The unique identifier (ID) of the firewall ruleset Example:
            c4d291f47f9d436fa39f58493ce3b50d.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetFirewallRulesetResponse200 | GetFirewallRulesetResponse401 | GetFirewallRulesetResponse403 | GetFirewallRulesetResponse404
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed

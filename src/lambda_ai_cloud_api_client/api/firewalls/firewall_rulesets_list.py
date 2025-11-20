from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.firewall_rulesets_list_response_200 import FirewallRulesetsListResponse200
from ...models.firewall_rulesets_list_response_401 import FirewallRulesetsListResponse401
from ...models.firewall_rulesets_list_response_403 import FirewallRulesetsListResponse403
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/firewall-rulesets",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> FirewallRulesetsListResponse200 | FirewallRulesetsListResponse401 | FirewallRulesetsListResponse403 | None:
    if response.status_code == 200:
        response_200 = FirewallRulesetsListResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = FirewallRulesetsListResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = FirewallRulesetsListResponse403.from_dict(response.json())

        return response_403

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[FirewallRulesetsListResponse200 | FirewallRulesetsListResponse401 | FirewallRulesetsListResponse403]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[FirewallRulesetsListResponse200 | FirewallRulesetsListResponse401 | FirewallRulesetsListResponse403]:
    """List firewall rulesets

     Retrieves a list of your firewall rulesets.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FirewallRulesetsListResponse200 | FirewallRulesetsListResponse401 | FirewallRulesetsListResponse403]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> FirewallRulesetsListResponse200 | FirewallRulesetsListResponse401 | FirewallRulesetsListResponse403 | None:
    """List firewall rulesets

     Retrieves a list of your firewall rulesets.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FirewallRulesetsListResponse200 | FirewallRulesetsListResponse401 | FirewallRulesetsListResponse403
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[FirewallRulesetsListResponse200 | FirewallRulesetsListResponse401 | FirewallRulesetsListResponse403]:
    """List firewall rulesets

     Retrieves a list of your firewall rulesets.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FirewallRulesetsListResponse200 | FirewallRulesetsListResponse401 | FirewallRulesetsListResponse403]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> FirewallRulesetsListResponse200 | FirewallRulesetsListResponse401 | FirewallRulesetsListResponse403 | None:
    """List firewall rulesets

     Retrieves a list of your firewall rulesets.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FirewallRulesetsListResponse200 | FirewallRulesetsListResponse401 | FirewallRulesetsListResponse403
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed

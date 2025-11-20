from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.global_firewall_ruleset_patch_request import GlobalFirewallRulesetPatchRequest
from ...models.update_global_firewall_ruleset_response_200 import UpdateGlobalFirewallRulesetResponse200
from ...models.update_global_firewall_ruleset_response_401 import UpdateGlobalFirewallRulesetResponse401
from ...models.update_global_firewall_ruleset_response_403 import UpdateGlobalFirewallRulesetResponse403
from ...models.update_global_firewall_ruleset_response_409 import UpdateGlobalFirewallRulesetResponse409
from ...types import Response


def _get_kwargs(
    *,
    body: GlobalFirewallRulesetPatchRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/api/v1/firewall-rulesets/global",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    UpdateGlobalFirewallRulesetResponse200
    | UpdateGlobalFirewallRulesetResponse401
    | UpdateGlobalFirewallRulesetResponse403
    | UpdateGlobalFirewallRulesetResponse409
    | None
):
    if response.status_code == 200:
        response_200 = UpdateGlobalFirewallRulesetResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = UpdateGlobalFirewallRulesetResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = UpdateGlobalFirewallRulesetResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 409:
        response_409 = UpdateGlobalFirewallRulesetResponse409.from_dict(response.json())

        return response_409

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    UpdateGlobalFirewallRulesetResponse200
    | UpdateGlobalFirewallRulesetResponse401
    | UpdateGlobalFirewallRulesetResponse403
    | UpdateGlobalFirewallRulesetResponse409
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
    body: GlobalFirewallRulesetPatchRequest,
) -> Response[
    UpdateGlobalFirewallRulesetResponse200
    | UpdateGlobalFirewallRulesetResponse401
    | UpdateGlobalFirewallRulesetResponse403
    | UpdateGlobalFirewallRulesetResponse409
]:
    """Update global firewall ruleset

     Updates the global firewall ruleset. This allows updating the rules only.

    Args:
        body (GlobalFirewallRulesetPatchRequest): Request to update the global firewall ruleset.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UpdateGlobalFirewallRulesetResponse200 | UpdateGlobalFirewallRulesetResponse401 | UpdateGlobalFirewallRulesetResponse403 | UpdateGlobalFirewallRulesetResponse409]
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
    body: GlobalFirewallRulesetPatchRequest,
) -> (
    UpdateGlobalFirewallRulesetResponse200
    | UpdateGlobalFirewallRulesetResponse401
    | UpdateGlobalFirewallRulesetResponse403
    | UpdateGlobalFirewallRulesetResponse409
    | None
):
    """Update global firewall ruleset

     Updates the global firewall ruleset. This allows updating the rules only.

    Args:
        body (GlobalFirewallRulesetPatchRequest): Request to update the global firewall ruleset.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UpdateGlobalFirewallRulesetResponse200 | UpdateGlobalFirewallRulesetResponse401 | UpdateGlobalFirewallRulesetResponse403 | UpdateGlobalFirewallRulesetResponse409
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: GlobalFirewallRulesetPatchRequest,
) -> Response[
    UpdateGlobalFirewallRulesetResponse200
    | UpdateGlobalFirewallRulesetResponse401
    | UpdateGlobalFirewallRulesetResponse403
    | UpdateGlobalFirewallRulesetResponse409
]:
    """Update global firewall ruleset

     Updates the global firewall ruleset. This allows updating the rules only.

    Args:
        body (GlobalFirewallRulesetPatchRequest): Request to update the global firewall ruleset.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UpdateGlobalFirewallRulesetResponse200 | UpdateGlobalFirewallRulesetResponse401 | UpdateGlobalFirewallRulesetResponse403 | UpdateGlobalFirewallRulesetResponse409]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: GlobalFirewallRulesetPatchRequest,
) -> (
    UpdateGlobalFirewallRulesetResponse200
    | UpdateGlobalFirewallRulesetResponse401
    | UpdateGlobalFirewallRulesetResponse403
    | UpdateGlobalFirewallRulesetResponse409
    | None
):
    """Update global firewall ruleset

     Updates the global firewall ruleset. This allows updating the rules only.

    Args:
        body (GlobalFirewallRulesetPatchRequest): Request to update the global firewall ruleset.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UpdateGlobalFirewallRulesetResponse200 | UpdateGlobalFirewallRulesetResponse401 | UpdateGlobalFirewallRulesetResponse403 | UpdateGlobalFirewallRulesetResponse409
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed

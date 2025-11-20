from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.firewall_ruleset_patch_request import FirewallRulesetPatchRequest
from ...models.update_firewall_ruleset_response_200 import UpdateFirewallRulesetResponse200
from ...models.update_firewall_ruleset_response_401 import UpdateFirewallRulesetResponse401
from ...models.update_firewall_ruleset_response_403 import UpdateFirewallRulesetResponse403
from ...models.update_firewall_ruleset_response_404 import UpdateFirewallRulesetResponse404
from ...models.update_firewall_ruleset_response_409 import UpdateFirewallRulesetResponse409
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    body: FirewallRulesetPatchRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": f"/api/v1/firewall-rulesets/{id}",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    UpdateFirewallRulesetResponse200
    | UpdateFirewallRulesetResponse401
    | UpdateFirewallRulesetResponse403
    | UpdateFirewallRulesetResponse404
    | UpdateFirewallRulesetResponse409
    | None
):
    if response.status_code == 200:
        response_200 = UpdateFirewallRulesetResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = UpdateFirewallRulesetResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = UpdateFirewallRulesetResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = UpdateFirewallRulesetResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = UpdateFirewallRulesetResponse409.from_dict(response.json())

        return response_409

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    UpdateFirewallRulesetResponse200
    | UpdateFirewallRulesetResponse401
    | UpdateFirewallRulesetResponse403
    | UpdateFirewallRulesetResponse404
    | UpdateFirewallRulesetResponse409
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
    body: FirewallRulesetPatchRequest,
) -> Response[
    UpdateFirewallRulesetResponse200
    | UpdateFirewallRulesetResponse401
    | UpdateFirewallRulesetResponse403
    | UpdateFirewallRulesetResponse404
    | UpdateFirewallRulesetResponse409
]:
    """Update firewall ruleset

     Updates a firewall ruleset. This is a partial update that allows updating either the name, rules, or
    both.

    Args:
        id (str): The unique identifier (ID) of the firewall ruleset Example:
            c4d291f47f9d436fa39f58493ce3b50d.
        body (FirewallRulesetPatchRequest): Request to partially update a firewall ruleset.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UpdateFirewallRulesetResponse200 | UpdateFirewallRulesetResponse401 | UpdateFirewallRulesetResponse403 | UpdateFirewallRulesetResponse404 | UpdateFirewallRulesetResponse409]
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
    body: FirewallRulesetPatchRequest,
) -> (
    UpdateFirewallRulesetResponse200
    | UpdateFirewallRulesetResponse401
    | UpdateFirewallRulesetResponse403
    | UpdateFirewallRulesetResponse404
    | UpdateFirewallRulesetResponse409
    | None
):
    """Update firewall ruleset

     Updates a firewall ruleset. This is a partial update that allows updating either the name, rules, or
    both.

    Args:
        id (str): The unique identifier (ID) of the firewall ruleset Example:
            c4d291f47f9d436fa39f58493ce3b50d.
        body (FirewallRulesetPatchRequest): Request to partially update a firewall ruleset.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UpdateFirewallRulesetResponse200 | UpdateFirewallRulesetResponse401 | UpdateFirewallRulesetResponse403 | UpdateFirewallRulesetResponse404 | UpdateFirewallRulesetResponse409
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
    body: FirewallRulesetPatchRequest,
) -> Response[
    UpdateFirewallRulesetResponse200
    | UpdateFirewallRulesetResponse401
    | UpdateFirewallRulesetResponse403
    | UpdateFirewallRulesetResponse404
    | UpdateFirewallRulesetResponse409
]:
    """Update firewall ruleset

     Updates a firewall ruleset. This is a partial update that allows updating either the name, rules, or
    both.

    Args:
        id (str): The unique identifier (ID) of the firewall ruleset Example:
            c4d291f47f9d436fa39f58493ce3b50d.
        body (FirewallRulesetPatchRequest): Request to partially update a firewall ruleset.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UpdateFirewallRulesetResponse200 | UpdateFirewallRulesetResponse401 | UpdateFirewallRulesetResponse403 | UpdateFirewallRulesetResponse404 | UpdateFirewallRulesetResponse409]
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
    body: FirewallRulesetPatchRequest,
) -> (
    UpdateFirewallRulesetResponse200
    | UpdateFirewallRulesetResponse401
    | UpdateFirewallRulesetResponse403
    | UpdateFirewallRulesetResponse404
    | UpdateFirewallRulesetResponse409
    | None
):
    """Update firewall ruleset

     Updates a firewall ruleset. This is a partial update that allows updating either the name, rules, or
    both.

    Args:
        id (str): The unique identifier (ID) of the firewall ruleset Example:
            c4d291f47f9d436fa39f58493ce3b50d.
        body (FirewallRulesetPatchRequest): Request to partially update a firewall ruleset.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UpdateFirewallRulesetResponse200 | UpdateFirewallRulesetResponse401 | UpdateFirewallRulesetResponse403 | UpdateFirewallRulesetResponse404 | UpdateFirewallRulesetResponse409
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed

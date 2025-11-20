import datetime
from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_audit_events_response_200 import GetAuditEventsResponse200
from ...models.get_audit_events_response_400 import GetAuditEventsResponse400
from ...models.get_audit_events_response_401 import GetAuditEventsResponse401
from ...models.get_audit_events_response_403 import GetAuditEventsResponse403
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    start: datetime.datetime | Unset = UNSET,
    end: datetime.datetime | Unset = UNSET,
    page_token: str | Unset = UNSET,
    resource_type: str | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_start: str | Unset = UNSET
    if not isinstance(start, Unset):
        json_start = start.isoformat()
    params["start"] = json_start

    json_end: str | Unset = UNSET
    if not isinstance(end, Unset):
        json_end = end.isoformat()
    params["end"] = json_end

    params["page_token"] = page_token

    params["resource_type"] = resource_type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/audit-events",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    GetAuditEventsResponse200 | GetAuditEventsResponse400 | GetAuditEventsResponse401 | GetAuditEventsResponse403 | None
):
    if response.status_code == 200:
        response_200 = GetAuditEventsResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = GetAuditEventsResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = GetAuditEventsResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = GetAuditEventsResponse403.from_dict(response.json())

        return response_403

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    GetAuditEventsResponse200 | GetAuditEventsResponse400 | GetAuditEventsResponse401 | GetAuditEventsResponse403
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
    start: datetime.datetime | Unset = UNSET,
    end: datetime.datetime | Unset = UNSET,
    page_token: str | Unset = UNSET,
    resource_type: str | Unset = UNSET,
) -> Response[
    GetAuditEventsResponse200 | GetAuditEventsResponse400 | GetAuditEventsResponse401 | GetAuditEventsResponse403
]:
    """Get audit events

     Retrieves a list of audit events that have occurred in your account. To view the full catalog of
    possible audit events, visit [Access and security > Audit logs](https://docs.lambda.ai/public-
    cloud/access-security#audit-logs) in the Lambda Cloud documentation.

    Args:
        start (datetime.datetime | Unset): An ISO 8601 timestamp defining the start of the time
            range to query, inclusive. If omitted, the response starts at the earliest available
            event. Example: 2025-09-01T10:30:45.123456Z.
        end (datetime.datetime | Unset): An ISO 8601 timestamp defining the end of the time range
            to query, inclusive. If omitted, the response ends at the most recent event. Example:
            2025-09-15T10:30:45.123456Z.
        page_token (str | Unset): The token returned by the previous API response to retrieve the
            next page of results. Example: abCdEFg0h1I2jKlm34n5O6Pq78r=.
        resource_type (str | Unset): The resource type to filter by. By default, all available
            resource types are retrieved. Example: cloud.api_key.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetAuditEventsResponse200 | GetAuditEventsResponse400 | GetAuditEventsResponse401 | GetAuditEventsResponse403]
    """

    kwargs = _get_kwargs(
        start=start,
        end=end,
        page_token=page_token,
        resource_type=resource_type,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    start: datetime.datetime | Unset = UNSET,
    end: datetime.datetime | Unset = UNSET,
    page_token: str | Unset = UNSET,
    resource_type: str | Unset = UNSET,
) -> (
    GetAuditEventsResponse200 | GetAuditEventsResponse400 | GetAuditEventsResponse401 | GetAuditEventsResponse403 | None
):
    """Get audit events

     Retrieves a list of audit events that have occurred in your account. To view the full catalog of
    possible audit events, visit [Access and security > Audit logs](https://docs.lambda.ai/public-
    cloud/access-security#audit-logs) in the Lambda Cloud documentation.

    Args:
        start (datetime.datetime | Unset): An ISO 8601 timestamp defining the start of the time
            range to query, inclusive. If omitted, the response starts at the earliest available
            event. Example: 2025-09-01T10:30:45.123456Z.
        end (datetime.datetime | Unset): An ISO 8601 timestamp defining the end of the time range
            to query, inclusive. If omitted, the response ends at the most recent event. Example:
            2025-09-15T10:30:45.123456Z.
        page_token (str | Unset): The token returned by the previous API response to retrieve the
            next page of results. Example: abCdEFg0h1I2jKlm34n5O6Pq78r=.
        resource_type (str | Unset): The resource type to filter by. By default, all available
            resource types are retrieved. Example: cloud.api_key.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetAuditEventsResponse200 | GetAuditEventsResponse400 | GetAuditEventsResponse401 | GetAuditEventsResponse403
    """

    return sync_detailed(
        client=client,
        start=start,
        end=end,
        page_token=page_token,
        resource_type=resource_type,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    start: datetime.datetime | Unset = UNSET,
    end: datetime.datetime | Unset = UNSET,
    page_token: str | Unset = UNSET,
    resource_type: str | Unset = UNSET,
) -> Response[
    GetAuditEventsResponse200 | GetAuditEventsResponse400 | GetAuditEventsResponse401 | GetAuditEventsResponse403
]:
    """Get audit events

     Retrieves a list of audit events that have occurred in your account. To view the full catalog of
    possible audit events, visit [Access and security > Audit logs](https://docs.lambda.ai/public-
    cloud/access-security#audit-logs) in the Lambda Cloud documentation.

    Args:
        start (datetime.datetime | Unset): An ISO 8601 timestamp defining the start of the time
            range to query, inclusive. If omitted, the response starts at the earliest available
            event. Example: 2025-09-01T10:30:45.123456Z.
        end (datetime.datetime | Unset): An ISO 8601 timestamp defining the end of the time range
            to query, inclusive. If omitted, the response ends at the most recent event. Example:
            2025-09-15T10:30:45.123456Z.
        page_token (str | Unset): The token returned by the previous API response to retrieve the
            next page of results. Example: abCdEFg0h1I2jKlm34n5O6Pq78r=.
        resource_type (str | Unset): The resource type to filter by. By default, all available
            resource types are retrieved. Example: cloud.api_key.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetAuditEventsResponse200 | GetAuditEventsResponse400 | GetAuditEventsResponse401 | GetAuditEventsResponse403]
    """

    kwargs = _get_kwargs(
        start=start,
        end=end,
        page_token=page_token,
        resource_type=resource_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    start: datetime.datetime | Unset = UNSET,
    end: datetime.datetime | Unset = UNSET,
    page_token: str | Unset = UNSET,
    resource_type: str | Unset = UNSET,
) -> (
    GetAuditEventsResponse200 | GetAuditEventsResponse400 | GetAuditEventsResponse401 | GetAuditEventsResponse403 | None
):
    """Get audit events

     Retrieves a list of audit events that have occurred in your account. To view the full catalog of
    possible audit events, visit [Access and security > Audit logs](https://docs.lambda.ai/public-
    cloud/access-security#audit-logs) in the Lambda Cloud documentation.

    Args:
        start (datetime.datetime | Unset): An ISO 8601 timestamp defining the start of the time
            range to query, inclusive. If omitted, the response starts at the earliest available
            event. Example: 2025-09-01T10:30:45.123456Z.
        end (datetime.datetime | Unset): An ISO 8601 timestamp defining the end of the time range
            to query, inclusive. If omitted, the response ends at the most recent event. Example:
            2025-09-15T10:30:45.123456Z.
        page_token (str | Unset): The token returned by the previous API response to retrieve the
            next page of results. Example: abCdEFg0h1I2jKlm34n5O6Pq78r=.
        resource_type (str | Unset): The resource type to filter by. By default, all available
            resource types are retrieved. Example: cloud.api_key.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetAuditEventsResponse200 | GetAuditEventsResponse400 | GetAuditEventsResponse401 | GetAuditEventsResponse403
    """

    return (
        await asyncio_detailed(
            client=client,
            start=start,
            end=end,
            page_token=page_token,
            resource_type=resource_type,
        )
    ).parsed

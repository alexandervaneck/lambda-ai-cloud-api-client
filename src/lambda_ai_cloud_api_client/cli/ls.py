import sys

from rich.console import Console
from rich.table import Table

from lambda_ai_cloud_api_client.api.instances.list_instances import sync_detailed as _list_instances
from lambda_ai_cloud_api_client.cli.client import auth_client
from lambda_ai_cloud_api_client.cli.response import print_response
from lambda_ai_cloud_api_client.models import (
    ListInstancesResponse200,
    ListInstancesResponse401,
    ListInstancesResponse403,
)
from lambda_ai_cloud_api_client.types import Response, Unset


def list_instances(
    base_url: str, token: str | None = None, insecure: bool = False
) -> Response[ListInstancesResponse200 | ListInstancesResponse401 | ListInstancesResponse403]:
    client = auth_client(base_url=base_url, token=token, insecure=insecure)
    instances: Response[ListInstancesResponse200] = _list_instances(client=client)
    return instances


def filter_instances(
    response: Response[ListInstancesResponse200 | ListInstancesResponse401 | ListInstancesResponse403],
    region: tuple[str, ...] | None = None,
    status: tuple[str, ...] | None = None,
) -> Response[ListInstancesResponse200 | ListInstancesResponse401 | ListInstancesResponse403]:
    if response.parsed and hasattr(response.parsed, "data"):
        filtered = response.parsed.data
        if region:
            allowed = set(region)
            filtered = [i for i in filtered if getattr(getattr(i, "region", None), "name", None) in allowed]
        if status:
            allowed = set(status)
            filtered = [i for i in filtered if getattr(i, "status", None) in allowed]

        response.parsed.data = filtered  # type: ignore[attr-defined]

    return response


def render_instances_table(
    response: Response[ListInstancesResponse200 | ListInstancesResponse401 | ListInstancesResponse403],
) -> None:
    status = int(response.status_code)
    if status < 200 or status >= 300 or response.parsed is None:
        print_response(response)
        sys.exit(1)

    parsed = response.parsed
    instances = getattr(parsed, "data", None)
    if not instances:
        Console().print("No instances found.")
        return

    table = Table(title="Instances", show_lines=False)
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("IP")
    table.add_column("Status")
    table.add_column("Region")
    table.add_column("GPU")
    table.add_column("Price ($/hr)")

    for instance in instances:
        inst_type = getattr(instance, "instance_type", None)
        price = getattr(inst_type, "price_cents_per_hour", 0) / 100
        ip = getattr(instance, "ip", "")
        if isinstance(ip, Unset):
            ip = ""

        table.add_row(
            getattr(instance, "id", ""),
            getattr(instance, "name", ""),
            ip,
            getattr(instance, "status", ""),
            getattr(getattr(instance, "region", None), "name", "") or "",
            getattr(inst_type, "gpu_description", "") or "",
            f"{price:.2f}",
        )

    Console().print(table)

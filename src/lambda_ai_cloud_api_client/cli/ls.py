from rich import print
from rich.table import Table

from lambda_ai_cloud_api_client.api.instances.list_instances import sync_detailed as _list_instances
from lambda_ai_cloud_api_client.cli.client import auth_client
from lambda_ai_cloud_api_client.models import (
    Instance,
)
from lambda_ai_cloud_api_client.types import Unset


def list_instances() -> list[Instance]:
    client = auth_client()
    response = _list_instances(client=client)
    response.raise_for_status()
    return response.parsed.data


def filter_instances(
    instances: list[Instance],
    region: tuple[str, ...] | None = None,
    status: tuple[str, ...] | None = None,
    id: tuple[str, ...] | None = None,
) -> list[Instance]:
    filtered_instances = []
    for instance in instances:
        if id and instance.id not in id:
            continue
        if region and instance.region.name not in region:
            continue
        if status and instance.status not in status:
            continue

        filtered_instances.append(instance)

    return filtered_instances


def render_instances_table(instances: list[Instance], title: str = "Instances") -> None:
    if not instances:
        print("No instances found.")
        return

    table = Table(title=title, show_lines=False)
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

    print(table)

import logging

from rich.console import Console
from rich.table import Table

from lambda_ai_cloud_api_client.api.instances.list_instance_types import sync_detailed as _list_instance_types
from lambda_ai_cloud_api_client.cli.client import auth_client
from lambda_ai_cloud_api_client.models import InstanceTypesItem

logger = logging.getLogger(__name__)


def list_instance_types() -> list[InstanceTypesItem]:
    client = auth_client()
    response = _list_instance_types(client=client)
    response.raise_for_status()
    return response.parsed.data.additional_properties.values()


def filter_instance_types(
    instance_types: list[InstanceTypesItem],
    instance_type: str | None,
    available: bool,
    cheapest: bool,
    region: tuple[str, ...],
    gpu: tuple[str, ...],
    min_gpus: int | None,
    min_vcpus: int | None,
    min_memory: int | None,
    min_storage: int | None,
    max_price: int | None,
) -> list[InstanceTypesItem]:
    filtered_instance_type_items: list[InstanceTypesItem] = []

    for item in instance_types:
        name = item.instance_type.name
        price_dollars_per_hour = item.instance_type.price_cents_per_hour / 100

        if instance_type and item.instance_type.name != instance_type:
            logger.debug(f"[filter] {name} skipped: wanted instance_type '{instance_type}'.")
            continue

        if available and not item.regions_with_capacity_available:
            # No regions with capacity = not available
            logger.debug(f"[filter] {name} skipped: no regions with capacity and --available requested.")
            continue

        if region and not any(r in item.regions_with_capacity_available for r in region):
            regions = ", ".join([r.name for r in item.regions_with_capacity_available]) or "none"
            wanted = ", ".join(region)
            logger.debug(f"[filter] {name} skipped: regions with capacity [{regions}] do not include [{wanted}].")
            continue

        if gpu and not any(g in item.instance_type.gpu_description for g in gpu):
            continue

        if min_gpus is not None and item.instance_type.specs.gpus < min_gpus:
            logger.debug(f"[filter] {name} skipped: gpus {item.instance_type.specs.gpus} < min_gpus {min_gpus}.")
            continue

        if min_vcpus is not None and item.instance_type.specs.vcpus < min_vcpus:
            logger.debug(f"[filter] {name} skipped: vcpus {item.instance_type.specs.vcpus} < min_vcpus {min_vcpus}.")
            continue

        if min_memory is not None and item.instance_type.specs.memory_gib < min_memory:
            logger.debug(
                f"[filter] {name} skipped: memory {item.instance_type.specs.memory_gib} < min_memory {min_memory}."
            )
            continue

        if min_storage is not None and item.instance_type.specs.storage_gib < min_storage:
            logger.debug(
                f"[filter] {name} skipped: storage {item.instance_type.specs.storage_gib} < min_storage {min_storage}."
            )
            continue

        if max_price is not None and item.instance_type.price_cents_per_hour > max_price * 100:
            logger.debug(f"[filter] {name} skipped: price ${price_dollars_per_hour}/hr > max_price ${max_price}/hr.")
            continue

        logger.debug(f"[filter] {name} kept (price ${price_dollars_per_hour}/hr).")
        filtered_instance_type_items.append(item)

    if cheapest and filtered_instance_type_items:
        sorted_items = sorted(filtered_instance_type_items, key=lambda x: x.instance_type.price_cents_per_hour)
        return [sorted_items[0]]

    return filtered_instance_type_items


def render_types_table(instance_types: list[InstanceTypesItem], title: str = "Instance Types") -> None:
    if not instance_types:
        Console().print("No instance types found.")
        return

    table = Table(title=title, show_lines=False)
    table.add_column("Name")
    table.add_column("GPU")
    table.add_column("vCPUs")
    table.add_column("Memory (GiB)")
    table.add_column("Storage (GiB)")
    table.add_column("GPUs")
    table.add_column("Price ($/hr)")
    table.add_column("Regions w/ Capacity")

    for item in instance_types:
        regions = "-"
        if item.regions_with_capacity_available:
            regions = ", ".join([r.name for r in item.regions_with_capacity_available])

        row = [
            item.instance_type.name,
            item.instance_type.gpu_description,
            str(item.instance_type.specs.vcpus),
            str(item.instance_type.specs.memory_gib),
            str(item.instance_type.specs.storage_gib),
            str(item.instance_type.specs.gpus),
            f"{item.instance_type.price_cents_per_hour / 100:.2f}",
            regions,
        ]
        table.add_row(*row)

    Console().print(table)

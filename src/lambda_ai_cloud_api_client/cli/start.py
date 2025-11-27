from pathlib import Path
from typing import Any

from lambda_ai_cloud_api_client.api.instances.launch_instance import sync_detailed as launch_instance
from lambda_ai_cloud_api_client.cli.client import auth_client
from lambda_ai_cloud_api_client.cli.response import print_json
from lambda_ai_cloud_api_client.cli.types import filter_instance_types, list_instance_types, render_types_table
from lambda_ai_cloud_api_client.models import (
    ImageSpecificationFamily,
    ImageSpecificationID,
    InstanceLaunchRequest,
    InstanceType,
    InstanceTypesItem,
    Region,
    RequestedTagEntry,
)


def _parse_image(
    image_id: str | None, image_family: str | None
) -> ImageSpecificationFamily | ImageSpecificationID | None:
    if image_id and image_family:
        raise RuntimeError("Use either --image-id or --image-family, not both.")
    if image_id:
        return ImageSpecificationID(id=image_id)
    if image_family:
        return ImageSpecificationFamily(family=image_family)
    return None


def _parse_tags(raw_tags: list[str] | None) -> list[RequestedTagEntry] | None:
    if not raw_tags:
        return None
    tags: list[RequestedTagEntry] = []
    for raw in raw_tags:
        if "=" not in raw:
            raise RuntimeError(f"Invalid tag '{raw}'. Use key=value format.")
        key, value = raw.split("=", 1)
        tags.append(RequestedTagEntry(key=key, value=value))
    return tags


def _read_user_data(user_data_path: str | None) -> str | None:
    if not user_data_path:
        return None
    path = Path(user_data_path)
    if not path.exists():
        raise RuntimeError(f"User-data file not found: {path}")
    return path.read_text()


def _resolve_type_and_region(
    instance_type: str | None = None,
    region: tuple[str, ...] = (),
    available: bool = False,
    cheapest: bool = False,
    gpu: tuple[str, ...] = (),
    min_gpus: int | None = None,
    min_vcpus: int | None = None,
    min_memory: int | None = None,
    min_storage: int | None = None,
    max_price: int | None = None,
) -> tuple[InstanceType, Region]:
    instance_types = list_instance_types()
    items = filter_instance_types(
        instance_types,
        instance_type=instance_type,
        available=available,
        cheapest=cheapest,
        region=region,
        gpu=gpu,
        min_gpus=min_gpus,
        min_vcpus=min_vcpus,
        min_memory=min_memory,
        min_storage=min_storage,
        max_price=max_price,
    )

    if not items:
        raise RuntimeError("No instance types match your filters.")

    if len(items) > 1:
        names = ", ".join([i.instance_type.name for i in items])
        raise RuntimeError(f"Multiple instance types match ({names}). Provide --instance-type or narrow filters.")

    available_regions = items[0].regions_with_capacity_available
    if region:
        available_regions = [r for r in available_regions if r.name.value in region]
    return items[0].instance_type, available_regions[0]


def start_instance(
    instance_type: str | None,
    region: tuple[str, ...],
    available: bool,
    cheapest: bool,
    gpu: tuple[str, ...],
    min_gpus: int | None,
    min_vcpus: int | None,
    min_memory: int | None,
    min_storage: int | None,
    max_price: float | None,
    ssh_key: tuple[str, ...],
    dry_run: bool,
    name: str | None,
    hostname: str | None,
    filesystem: tuple[str, ...],
    image_id: str | None,
    image_family: str | None,
    user_data_file: str | None,
    tag: tuple[str, ...],
    json: bool = False,
) -> list[str]:
    client = auth_client()
    instance_type, region = _resolve_type_and_region(
        instance_type=instance_type,
        region=region,
        available=available,
        cheapest=cheapest,
        gpu=gpu,
        min_gpus=min_gpus,
        min_vcpus=min_vcpus,
        min_memory=min_memory,
        min_storage=min_storage,
        max_price=max_price,
    )

    image = _parse_image(image_id, image_family)
    tags = _parse_tags(tag)
    user_data = _read_user_data(user_data_file)

    if not ssh_key:
        raise RuntimeError("--ssh-key is required to start an instance. Please provide the name of an SSH key.")

    request_params: dict[str, Any] = {
        "region_name": region.name,
        "instance_type_name": instance_type.name,
        "ssh_key_names": ssh_key,
    }

    if name:
        request_params["name"] = name
    if hostname:
        request_params["hostname"] = hostname
    if filesystem:
        request_params["file_system_names"] = filesystem
    if image:
        request_params["image"] = image
    if user_data:
        request_params["user_data"] = user_data
    if tags:
        request_params["tags"] = tags

    plan = {
        "instance_type_name": instance_type.name,
        "region_name": region.name.value,
    }

    if json and dry_run:
        print_json(plan)
        return

    if not json:
        render_types_table(
            [InstanceTypesItem(regions_with_capacity_available=[region], instance_type=instance_type)],
            title="Launch plan",
        )

    if dry_run:
        print("Dry-run, exiting without launching...")
        return

    response = launch_instance(client=client, body=InstanceLaunchRequest(**request_params))
    response.raise_for_status()
    return response.parsed.data.instance_ids

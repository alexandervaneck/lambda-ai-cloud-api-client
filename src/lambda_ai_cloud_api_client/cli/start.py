import sys
from pathlib import Path
from typing import Any

from lambda_ai_cloud_api_client.api.instances.launch_instance import sync_detailed as launch_instance
from lambda_ai_cloud_api_client.cli.client import auth_client
from lambda_ai_cloud_api_client.cli.types import filter_instance_types, list_instance_types
from lambda_ai_cloud_api_client.models import (
    ImageSpecificationFamily,
    ImageSpecificationID,
    InstanceLaunchRequest,
    LaunchInstanceResponse200,
    LaunchInstanceResponse400,
    LaunchInstanceResponse401,
    LaunchInstanceResponse403,
    LaunchInstanceResponse404,
    PublicRegionCode,
    RequestedTagEntry,
)
from lambda_ai_cloud_api_client.types import Response


def _parse_image(
    image_id: str | None, image_family: str | None
) -> ImageSpecificationFamily | ImageSpecificationID | None:
    if image_id and image_family:
        print("Use either --image-id or --image-family, not both.", file=sys.stderr)
        sys.exit(1)
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
            print(f"Invalid tag '{raw}'. Use key=value format.", file=sys.stderr)
            sys.exit(1)
        key, value = raw.split("=", 1)
        tags.append(RequestedTagEntry(key=key, value=value))
    return tags


def _read_user_data(user_data_path: str | None) -> str | None:
    if not user_data_path:
        return None
    path = Path(user_data_path)
    if not path.exists():
        print(f"User-data file not found: {path}", file=sys.stderr)
        sys.exit(1)
    return path.read_text()


def _resolve_type_and_region(
    instance_type: str | None,
    region: tuple[str, ...],
    available: bool,
    cheapest: bool,
    gpu: tuple[str, ...],
    min_gpus: int | None,
    min_vcpus: int | None,
    min_memory: int | None,
    min_storage: int | None,
    max_price: int | None,
    token: str | None,
    base_url: str,
    insecure: bool,
) -> tuple[str, PublicRegionCode]:
    response = list_instance_types(base_url, token, insecure)
    response = filter_instance_types(
        response,
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

    parsed = getattr(response, "parsed", None)
    data = getattr(parsed, "data", None) if parsed is not None else None
    items = getattr(data, "additional_properties", None)

    if not items:
        print("No instance types match your filters.", file=sys.stderr)
        sys.exit(1)

    selected_name = instance_type
    selected = None
    if selected_name:
        selected = items.get(selected_name)
        if not selected:
            print(f"Instance type '{selected_name}' did not match the filters.", file=sys.stderr)
            sys.exit(1)
    else:
        if len(items) == 1:
            selected_name, selected = next(iter(items.items()))
        else:
            names = ", ".join(sorted(items.keys()))
            print(
                f"Multiple instance types match ({names}). Provide --instance-type or narrow filters.", file=sys.stderr
            )
            sys.exit(1)

    allowed_regions = [getattr(r, "name", None) for r in getattr(selected, "regions_with_capacity_available", [])]
    chosen_region_name = None
    if region:
        for reg in region:
            if reg in allowed_regions:
                chosen_region_name = reg
                break
        if chosen_region_name is None:
            print(
                f"No requested region has capacity for '{selected_name}'. "
                f"Allowed regions: {', '.join(allowed_regions) or '-'}",
                file=sys.stderr,
            )
            sys.exit(1)
    else:
        if allowed_regions:
            chosen_region_name = allowed_regions[0]

    if not chosen_region_name:
        print(f"No regions with capacity for '{selected_name}'.", file=sys.stderr)
        sys.exit(1)

    try:
        chosen_region = PublicRegionCode(chosen_region_name)
    except ValueError:
        valid_regions = ", ".join([r.value for r in PublicRegionCode])
        print(f"Invalid region '{chosen_region_name}'. Choose one of: {valid_regions}", file=sys.stderr)
        sys.exit(1)

    return selected_name, chosen_region


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
    json: bool,
    token: str | None,
    base_url: str,
    insecure: bool,
) -> Response[
    LaunchInstanceResponse200
    | LaunchInstanceResponse400
    | LaunchInstanceResponse401
    | LaunchInstanceResponse403
    | LaunchInstanceResponse404
    | None
]:
    client = auth_client(base_url=base_url, token=token, insecure=insecure)
    instance_type_name, region = _resolve_type_and_region(
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
        token=token,
        base_url=base_url,
        insecure=insecure,
    )

    image = _parse_image(image_id, image_family)
    tags = _parse_tags(tag)
    user_data = _read_user_data(user_data_file)

    request_params: dict[str, Any] = {
        "region_name": region,
        "instance_type_name": instance_type_name,
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

    if dry_run:
        plan = {
            "instance_type_name": instance_type_name,
            "region_name": region.value,
        }
        if json:
            print(json.dumps(plan, indent=2))
        else:
            print(f"Dry run: would launch instance_type='{instance_type_name}' in region='{region.value}'")
        return None

    request = InstanceLaunchRequest(**request_params)
    return launch_instance(client=client, body=request)

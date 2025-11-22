import json
import sys
from pathlib import Path
from types import SimpleNamespace
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


def _parse_image(args: SimpleNamespace) -> ImageSpecificationFamily | ImageSpecificationID | None:
    if args.image_id and args.image_family:
        print("Use either --image-id or --image-family, not both.", file=sys.stderr)
        sys.exit(1)
    if args.image_id:
        return ImageSpecificationID(id=args.image_id)
    if args.image_family:
        return ImageSpecificationFamily(family=args.image_family)
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


def _resolve_type_and_region(args: SimpleNamespace) -> tuple[str, PublicRegionCode]:
    type_args = SimpleNamespace(
        token=args.token,
        base_url=args.base_url,
        insecure=args.insecure,
        available=args.available,
        cheapest=args.cheapest,
        region=args.region,
        gpu=args.gpu,
        min_gpus=args.min_gpus,
        min_vcpus=args.min_vcpus,
        min_memory=args.min_memory,
        min_storage=args.min_storage,
        max_price=args.max_price,
    )
    response = list_instance_types(type_args)
    response = filter_instance_types(response, type_args)

    parsed = getattr(response, "parsed", None)
    data = getattr(parsed, "data", None) if parsed is not None else None
    items = getattr(data, "additional_properties", None)

    if not items:
        print("No instance types match your filters.", file=sys.stderr)
        sys.exit(1)

    selected_name = args.instance_type
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
    if args.region:
        for reg in args.region:
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
    args: SimpleNamespace,
) -> Response[
    LaunchInstanceResponse200
    | LaunchInstanceResponse400
    | LaunchInstanceResponse401
    | LaunchInstanceResponse403
    | LaunchInstanceResponse404
    | None
]:
    client = auth_client(args)

    instance_type_name, region = _resolve_type_and_region(args)

    image = _parse_image(args)
    tags = _parse_tags(args.tag)
    user_data = _read_user_data(args.user_data_file)

    request_params: dict[str, Any] = {
        "region_name": region,
        "instance_type_name": instance_type_name,
        "ssh_key_names": args.ssh_key,
    }

    if args.name:
        request_params["name"] = args.name
    if args.hostname:
        request_params["hostname"] = args.hostname
    if args.filesystem:
        request_params["file_system_names"] = args.filesystem
    if image:
        request_params["image"] = image
    if user_data:
        request_params["user_data"] = user_data
    if tags:
        request_params["tags"] = tags

    if args.dry_run:
        plan = {
            "instance_type_name": instance_type_name,
            "region_name": region.value,
        }
        if args.json:
            print(json.dumps(plan, indent=2))
        else:
            print(f"Dry run: would launch instance_type='{instance_type_name}' in region='{region.value}'")
        return None

    request = InstanceLaunchRequest(**request_params)
    return launch_instance(client=client, body=request)

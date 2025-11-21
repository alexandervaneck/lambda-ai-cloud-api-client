import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from lambda_ai_cloud_api_client.api.instances.launch_instance import sync_detailed as launch_instance
from lambda_ai_cloud_api_client.cli.client import auth_client
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


def start_instance(
    args: SimpleNamespace,
) -> Response[
    LaunchInstanceResponse200
    | LaunchInstanceResponse400
    | LaunchInstanceResponse401
    | LaunchInstanceResponse403
    | LaunchInstanceResponse404
]:
    client = auth_client(args)
    try:
        region = PublicRegionCode(args.region)
    except ValueError:
        valid_regions = ", ".join([r.value for r in PublicRegionCode])
        print(f"Invalid region '{args.region}'. Choose one of: {valid_regions}", file=sys.stderr)
        sys.exit(1)

    image = _parse_image(args)
    tags = _parse_tags(args.tag)
    user_data = _read_user_data(args.user_data_file)

    request_params: dict[str, Any] = {
        "region_name": region,
        "instance_type_name": args.instance_type,
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

    request = InstanceLaunchRequest(**request_params)
    return launch_instance(client=client, body=request)

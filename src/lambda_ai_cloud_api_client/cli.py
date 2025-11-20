"""Command line wrapper for the Lambda Cloud API client."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

from . import AuthenticatedClient
from .api.images.list_images import sync_detailed as list_images
from .api.instances.get_instance import sync_detailed as get_instance
from .api.instances.launch_instance import sync_detailed as launch_instance
from .api.instances.list_instance_types import sync_detailed as list_instance_types
from .api.instances.list_instances import sync_detailed as list_instances
from .api.instances.terminate_instance import sync_detailed as terminate_instance
from .api.ssh_keys.list_ssh_keys import sync_detailed as list_ssh_keys
from .models.image_specification_family import ImageSpecificationFamily
from .models.image_specification_id import ImageSpecificationID
from .models.instance_launch_request import InstanceLaunchRequest
from .models.instance_terminate_request import InstanceTerminateRequest
from .models.public_region_code import PublicRegionCode
from .models.requested_tag_entry import RequestedTagEntry

DEFAULT_BASE_URL = os.getenv("LAMBDA_CLOUD_BASE_URL", "https://cloud.lambdalabs.com")
TOKEN_ENV_VARS = ("LAMBDA_CLOUD_TOKEN", "LAMBDA_CLOUD_API_TOKEN", "LAMBDA_API_TOKEN")


def _to_serializable(value: Any) -> Any:
    """Convert API models into JSON serializable structures."""
    if hasattr(value, "to_dict"):
        return _to_serializable(value.to_dict())
    if isinstance(value, dict):
        return {k: _to_serializable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_to_serializable(v) for v in value]
    return value


def _print_response(response) -> None:
    """Pretty-print responses and exit non-zero on errors."""
    status = int(response.status_code)
    parsed = response.parsed
    if 200 <= status < 300:
        payload = _to_serializable(parsed) if parsed is not None else {"status": status}
        print(json.dumps(payload, indent=2))
        return

    payload = parsed if parsed is not None else response.content.decode("utf-8", errors="replace")
    print(json.dumps({"status_code": status, "error": _to_serializable(payload)}, indent=2))
    sys.exit(1)


def _load_token(explicit_token: str | None) -> str:
    if explicit_token:
        return explicit_token
    for env_var in TOKEN_ENV_VARS:
        token = os.getenv(env_var)
        if token:
            return token
    print(
        f"No API token provided. Supply --token or set one of: {', '.join(TOKEN_ENV_VARS)}",
        file=sys.stderr,
    )
    sys.exit(1)


def _build_client(args: argparse.Namespace) -> AuthenticatedClient:
    token = _load_token(args.token)
    return AuthenticatedClient(
        base_url=args.base_url,
        token=token,
        verify_ssl=not args.insecure,
    )


def _cmd_list_instances(args: argparse.Namespace) -> None:
    client = _build_client(args)
    response = list_instances(client=client, cluster_id=args.cluster_id)
    _print_response(response)


def _cmd_get_instance(args: argparse.Namespace) -> None:
    client = _build_client(args)
    response = get_instance(id=args.id, client=client)
    _print_response(response)


def _cmd_list_instance_types(args: argparse.Namespace) -> None:
    client = _build_client(args)
    response = list_instance_types(client=client)
    if getattr(args, "available_only", False) and response.parsed is not None:
        parsed = response.parsed
        target = None
        if hasattr(parsed, "data"):
            target = parsed.data
        elif hasattr(parsed, "additional_properties"):
            target = parsed

        if target and hasattr(target, "additional_properties"):
            filtered = target.__class__()  # type: ignore[call-arg]
            filtered.additional_properties = {
                name: item
                for name, item in target.additional_properties.items()
                if item.regions_with_capacity_available
            }
            if hasattr(parsed, "data"):
                parsed.data = filtered  # type: ignore[attr-defined]
                response.parsed = parsed
            else:
                response.parsed = filtered
    _print_response(response)


def _cmd_list_images(args: argparse.Namespace) -> None:
    client = _build_client(args)
    response = list_images(client=client)
    _print_response(response)


def _cmd_list_ssh_keys(args: argparse.Namespace) -> None:
    client = _build_client(args)
    response = list_ssh_keys(client=client)
    _print_response(response)


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


def _parse_image(args: argparse.Namespace) -> ImageSpecificationFamily | ImageSpecificationID | None:
    if args.image_id and args.image_family:
        print("Use either --image-id or --image-family, not both.", file=sys.stderr)
        sys.exit(1)
    if args.image_id:
        return ImageSpecificationID(id=args.image_id)
    if args.image_family:
        return ImageSpecificationFamily(family=args.image_family)
    return None


def _cmd_launch_instance(args: argparse.Namespace) -> None:
    client = _build_client(args)
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
    response = launch_instance(client=client, body=request)
    _print_response(response)


def _cmd_terminate_instances(args: argparse.Namespace) -> None:
    client = _build_client(args)
    request = InstanceTerminateRequest(instance_ids=args.instance_id)
    response = terminate_instance(client=client, body=request)
    _print_response(response)


def _add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--token", help="API token. Defaults to env vars: " + ", ".join(TOKEN_ENV_VARS))
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help=f"API base URL (default: {DEFAULT_BASE_URL})",
    )
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Disable TLS verification (not recommended).",
    )


def _build_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    _add_common_args(common)

    parser = argparse.ArgumentParser(
        description="Interact with Lambda Cloud from the CLI.",
        parents=[common],
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    instances_parser = subparsers.add_parser("instances", help="Manage instances.", parents=[common])
    instances_sub = instances_parser.add_subparsers(dest="instances_command", required=True)

    ls_parser = instances_sub.add_parser("ls", help="List running instances.")
    ls_parser.add_argument("--cluster-id", help="Filter by cluster ID.", default=None)
    ls_parser.set_defaults(func=_cmd_list_instances)

    get_parser = instances_sub.add_parser("get", help="Get details for a single instance.")
    get_parser.add_argument("id", help="Instance ID.")
    get_parser.set_defaults(func=_cmd_get_instance)

    launch_parser = instances_sub.add_parser("launch", help="Launch a new instance.")
    launch_parser.add_argument("--region", required=True, help="Region code (e.g. us-east-1).")
    launch_parser.add_argument("--instance-type", required=True, help="Instance type name.")
    launch_parser.add_argument(
        "--ssh-key",
        required=True,
        action="append",
        help="SSH key name to inject (repeat for multiple).",
    )
    launch_parser.add_argument("--name", help="Instance name.")
    launch_parser.add_argument("--hostname", help="Hostname to assign.")
    launch_parser.add_argument(
        "--filesystem",
        action="append",
        help="Filesystem name to mount (repeat for multiple).",
    )
    launch_parser.add_argument("--image-id", help="Image ID to boot from.")
    launch_parser.add_argument("--image-family", help="Image family to boot from.")
    launch_parser.add_argument("--user-data-file", help="Path to cloud-init user-data file.")
    launch_parser.add_argument(
        "--tag",
        action="append",
        help="Tag to apply, formatted as key=value (repeat for multiple).",
    )
    launch_parser.set_defaults(func=_cmd_launch_instance)

    terminate_parser = instances_sub.add_parser("terminate", help="Terminate one or more instances.")
    terminate_parser.add_argument(
        "instance_id",
        nargs="+",
        help="Instance IDs to terminate.",
    )
    terminate_parser.set_defaults(func=_cmd_terminate_instances)

    instance_types_parser = subparsers.add_parser(
        "instance-types",
        help="List available instance types.",
        parents=[common],
    )
    instance_types_parser.add_argument(
        "--available-only",
        action="store_true",
        help="Show only instance types with available capacity.",
    )
    instance_types_parser.set_defaults(func=_cmd_list_instance_types)

    images_parser = subparsers.add_parser("images", help="List available images.", parents=[common])
    images_parser.set_defaults(func=_cmd_list_images)

    ssh_parser = subparsers.add_parser("ssh-keys", help="List SSH keys.", parents=[common])
    ssh_parser.set_defaults(func=_cmd_list_ssh_keys)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()

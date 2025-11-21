"""Command line wrapper for the Lambda Cloud API client (click-based)."""

from __future__ import annotations

import json
import os
import sys
from collections.abc import Callable
from pathlib import Path
from types import SimpleNamespace
from typing import Any, TypeVar

import click
from rich.console import Console
from rich.table import Table

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

T = TypeVar("T")


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


def _build_client(args: SimpleNamespace) -> AuthenticatedClient:
    token = _load_token(args.token)
    return AuthenticatedClient(
        base_url=args.base_url,
        token=token,
        verify_ssl=not args.insecure,
    )


def _cmd_list_instances(args: SimpleNamespace) -> None:
    client = _build_client(args)
    response = list_instances(client=client, cluster_id=args.cluster_id)
    _print_response(response)


def _render_instances_table(response) -> None:
    status = int(response.status_code)
    if status < 200 or status >= 300 or response.parsed is None:
        _print_response(response)
        return

    parsed = response.parsed
    instances = getattr(parsed, "data", None)
    if not instances:
        Console().print("No instances found.")
        return

    table = Table(title="Instances", show_lines=False)
    table.add_column("ID")
    table.add_column("Name", default="")
    table.add_column("Status")
    table.add_column("Type")
    table.add_column("Region")
    table.add_column("IP", default="")

    for inst in instances:
        inst_name = getattr(inst, "name", "") or ""
        inst_status = getattr(inst, "status", "") or ""
        inst_type = getattr(getattr(inst, "instance_type", None), "name", "") or ""
        inst_region = getattr(getattr(inst, "region", None), "name", "") or ""
        inst_ip = getattr(inst, "ip", "") or ""

        table.add_row(inst.id, inst_name, str(inst_status), inst_type, inst_region, inst_ip)

    Console().print(table)


def _cmd_get_instance(args: SimpleNamespace) -> None:
    client = _build_client(args)
    response = get_instance(id=args.id, client=client)
    _print_response(response)


def _cmd_list_instance_types(args: SimpleNamespace) -> None:
    client = _build_client(args)
    response = list_instance_types(client=client)
    if response.parsed is not None:
        parsed = response.parsed
        target = None
        if hasattr(parsed, "data"):
            target = parsed.data
        elif hasattr(parsed, "additional_properties"):
            target = parsed

        if target and hasattr(target, "additional_properties"):
            items = dict(target.additional_properties)

            if getattr(args, "available_only", False):
                items = {name: item for name, item in items.items() if item.regions_with_capacity_available}

            if getattr(args, "cheapest", False) and items:
                prices: dict[str, int] = {}
                for name, item in items.items():
                    price = getattr(getattr(item, "instance_type", None), "price_cents_per_hour", None)
                    if price is not None:
                        prices[name] = price
                if prices:
                    min_price = min(prices.values())
                    items = {name: item for name, item in items.items() if prices.get(name) == min_price}

            filtered = target.__class__()  # type: ignore[call-arg]
            filtered.additional_properties = items
            if hasattr(parsed, "data"):
                parsed.data = filtered  # type: ignore[attr-defined]
                response.parsed = parsed
            else:
                response.parsed = filtered
    _print_response(response)


def _cmd_list_images(args: SimpleNamespace) -> None:
    client = _build_client(args)
    response = list_images(client=client)
    _print_response(response)


def _cmd_list_ssh_keys(args: SimpleNamespace) -> None:
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


def _parse_image(args: SimpleNamespace) -> ImageSpecificationFamily | ImageSpecificationID | None:
    if args.image_id and args.image_family:
        print("Use either --image-id or --image-family, not both.", file=sys.stderr)
        sys.exit(1)
    if args.image_id:
        return ImageSpecificationID(id=args.image_id)
    if args.image_family:
        return ImageSpecificationFamily(family=args.image_family)
    return None


def _cmd_launch_instance(args: SimpleNamespace) -> None:
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


def _cmd_terminate_instances(args: SimpleNamespace) -> None:
    client = _build_client(args)
    request = InstanceTerminateRequest(instance_ids=args.instance_id)
    response = terminate_instance(client=client, body=request)
    _print_response(response)


def _common_options(func: Callable[..., T]) -> Callable[..., T]:
    func = click.option("--token", help="API token. Defaults to env vars: " + ", ".join(TOKEN_ENV_VARS))(func)
    func = click.option(
        "--base-url",
        default=DEFAULT_BASE_URL,
        show_default=True,
        help="API base URL.",
    )(func)
    func = click.option(
        "--insecure",
        is_flag=True,
        help="Disable TLS verification (not recommended).",
    )(func)
    return func


@click.group()
def main() -> None:
    """Interact with Lambda Cloud from the CLI."""


@main.command("ls", help="List running instances (shortcut for 'instances ls').")
@click.option("--cluster-id", default=None, help="Filter by cluster ID.")
@_common_options
def root_ls(cluster_id: str | None, token: str | None, base_url: str, insecure: bool) -> None:
    args = SimpleNamespace(cluster_id=cluster_id, token=token, base_url=base_url, insecure=insecure)
    client = _build_client(args)
    response = list_instances(client=client, cluster_id=args.cluster_id)
    _render_instances_table(response)


@main.group(help="Manage instances.")
def instances() -> None:
    """Instances commands."""


@instances.command(name="ls", help="List running instances.")
@click.option("--cluster-id", default=None, help="Filter by cluster ID.")
@_common_options
def instances_ls(cluster_id: str | None, token: str | None, base_url: str, insecure: bool) -> None:
    args = SimpleNamespace(cluster_id=cluster_id, token=token, base_url=base_url, insecure=insecure)
    _cmd_list_instances(args)


@instances.command(name="get", help="Get details for a single instance.")
@click.argument("id")
@_common_options
def instances_get(id: str, token: str | None, base_url: str, insecure: bool) -> None:
    args = SimpleNamespace(id=id, token=token, base_url=base_url, insecure=insecure)
    _cmd_get_instance(args)


@instances.command(name="launch", help="Launch a new instance.")
@click.option("--region", required=True, help="Region code (e.g. us-east-1).")
@click.option("--instance-type", required=True, help="Instance type name.")
@click.option("--ssh-key", required=True, multiple=True, help="SSH key name to inject (repeat for multiple).")
@click.option("--name", help="Instance name.")
@click.option("--hostname", help="Hostname to assign.")
@click.option("--filesystem", multiple=True, help="Filesystem name to mount (repeat for multiple).")
@click.option("--image-id", help="Image ID to boot from.")
@click.option("--image-family", help="Image family to boot from.")
@click.option("--user-data-file", help="Path to cloud-init user-data file.")
@click.option("--tag", multiple=True, help="Tag to apply, formatted as key=value (repeat for multiple).")
@_common_options
def instances_launch(
    region: str,
    instance_type: str,
    ssh_key: tuple[str, ...],
    name: str | None,
    hostname: str | None,
    filesystem: tuple[str, ...],
    image_id: str | None,
    image_family: str | None,
    user_data_file: str | None,
    tag: tuple[str, ...],
    token: str | None,
    base_url: str,
    insecure: bool,
) -> None:
    args = SimpleNamespace(
        region=region,
        instance_type=instance_type,
        ssh_key=list(ssh_key),
        name=name,
        hostname=hostname,
        filesystem=list(filesystem) if filesystem else None,
        image_id=image_id,
        image_family=image_family,
        user_data_file=user_data_file,
        tag=list(tag),
        token=token,
        base_url=base_url,
        insecure=insecure,
    )
    _cmd_launch_instance(args)


@instances.command(name="terminate", help="Terminate one or more instances.")
@click.argument("instance_id", nargs=-1, required=True)
@_common_options
def instances_terminate(instance_id: tuple[str, ...], token: str | None, base_url: str, insecure: bool) -> None:
    args = SimpleNamespace(instance_id=list(instance_id), token=token, base_url=base_url, insecure=insecure)
    _cmd_terminate_instances(args)


@main.command(name="instance-types", help="List available instance types.")
@click.option(
    "--available-only",
    is_flag=True,
    help="Show only instance types with available capacity.",
)
@click.option(
    "--cheapest",
    is_flag=True,
    help="Show only the cheapest instance type(s).",
)
@_common_options
def instance_types_cmd(available_only: bool, cheapest: bool, token: str | None, base_url: str, insecure: bool) -> None:
    args = SimpleNamespace(
        available_only=available_only, cheapest=cheapest, token=token, base_url=base_url, insecure=insecure
    )
    _cmd_list_instance_types(args)


@main.command(name="images", help="List available images.")
@_common_options
def images_cmd(token: str | None, base_url: str, insecure: bool) -> None:
    args = SimpleNamespace(token=token, base_url=base_url, insecure=insecure)
    _cmd_list_images(args)


@main.command(name="ssh-keys", help="List SSH keys.")
@_common_options
def ssh_keys_cmd(token: str | None, base_url: str, insecure: bool) -> None:
    args = SimpleNamespace(token=token, base_url=base_url, insecure=insecure)
    _cmd_list_ssh_keys(args)


if __name__ == "__main__":
    main()

"""Command line wrapper for the Lambda Cloud API client (click-based)."""

from __future__ import annotations

import json as _json
import os
import sys
from collections.abc import Callable
from types import SimpleNamespace
from typing import TypeVar

import click

from lambda_ai_cloud_api_client.cli.get import get_instance
from lambda_ai_cloud_api_client.cli.images import filter_images, list_images, render_images_table
from lambda_ai_cloud_api_client.cli.keys import filter_keys, list_keys, render_keys_table
from lambda_ai_cloud_api_client.cli.ls import filter_instances, list_instances, render_instances_table
from lambda_ai_cloud_api_client.cli.rename import rename_instance
from lambda_ai_cloud_api_client.cli.response import print_response
from lambda_ai_cloud_api_client.cli.restart import restart_instances
from lambda_ai_cloud_api_client.cli.ssh import ssh_into_instance
from lambda_ai_cloud_api_client.cli.start import start_instance
from lambda_ai_cloud_api_client.cli.stop import stop_instances
from lambda_ai_cloud_api_client.cli.types import filter_instance_types, list_instance_types, render_types_table

DEFAULT_BASE_URL = os.getenv("LAMBDA_CLOUD_BASE_URL", "https://cloud.lambdalabs.com")
TOKEN_ENV_VARS = ("LAMBDA_CLOUD_TOKEN", "LAMBDA_CLOUD_API_TOKEN", "LAMBDA_API_TOKEN")

T = TypeVar("T")


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


class OrderedGroup(click.Group):
    def list_commands(self, ctx):
        return self.commands


@click.group(cls=OrderedGroup)
def main() -> None:
    """Interact with Lambda Cloud from the CLI."""


@main.command("ls", help="List instances.")
@click.option("--status", multiple=True, help="Filter by status (repeat to include multiple).")
@click.option("--region", multiple=True, help="Filter by region (repeat to include multiple).")
@click.option("--json", is_flag=True, help="Output raw JSON instead of a table.")
@_common_options
def ls_cmd(
    status: tuple[str, ...], region: tuple[str, ...], json: bool, token: str | None, base_url: str, insecure: bool
) -> None:
    response = list_instances(base_url, token, insecure)
    filtered_response = filter_instances(response, region, status)

    if json:
        print_response(filtered_response)
        return

    render_instances_table(filtered_response)


@main.command(name="get", help="Get instance details.")
@click.argument("id")
@_common_options
def get_cmd(id: str, token: str | None, base_url: str, insecure: bool) -> None:
    response = get_instance(id=id, base_url=base_url, token=token, insecure=insecure)
    print_response(response)

    status = int(response.status_code)
    if status < 200 or status >= 300 or response.parsed is None:
        sys.exit(1)


@main.command(name="start", help="Start/launch a new instance.")
@click.option("--instance-type", help="Instance type name (optional if filters narrow to one).")
@click.option("--region", multiple=True, help="Region filter (repeat allowed).")
@click.option("--available", is_flag=True, help="Show only types with available capacity.")
@click.option("--cheapest", is_flag=True, help="Show only the cheapest type(s).")
@click.option("--gpu", multiple=True, help="Filter by GPU description substring (repeat allowed).")
@click.option("--min-gpus", type=int, default=None, help="Minimum GPUs.")
@click.option("--min-vcpus", type=int, default=None, help="Minimum vCPUs.")
@click.option("--min-memory", type=int, default=None, help="Minimum memory (GiB).")
@click.option("--min-storage", type=int, default=None, help="Minimum storage (GiB).")
@click.option("--max-price", type=float, default=None, help="Maximum price (cents/hour).")
@click.option("--ssh-key", required=True, multiple=True, help="SSH key name to inject (repeat for multiple).")
@click.option("--dry-run", is_flag=True, help="Resolve type/region and print the plan without launching.")
@click.option("--name", help="Instance name.")
@click.option("--hostname", help="Hostname to assign.")
@click.option("--filesystem", multiple=True, help="Filesystem name to mount (repeat for multiple).")
@click.option("--image-id", help="Image ID to boot from.")
@click.option("--image-family", help="Image family to boot from.")
@click.option("--user-data-file", help="Path to cloud-init user-data file.")
@click.option("--tag", multiple=True, help="Tag to apply, formatted as key=value (repeat for multiple).")
@click.option("--json", is_flag=True, help="Output raw JSON instead of a table.")
@_common_options
def start_cmd(
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
) -> None:
    args = SimpleNamespace(
        instance_type=instance_type,
        region=list(region),
        available=available,
        cheapest=cheapest,
        gpu=list(gpu),
        min_gpus=min_gpus,
        min_vcpus=min_vcpus,
        min_memory=min_memory,
        min_storage=min_storage,
        max_price=max_price,
        ssh_key=list(ssh_key),
        dry_run=dry_run,
        name=name,
        hostname=hostname,
        filesystem=list(filesystem) if filesystem else None,
        image_id=image_id,
        image_family=image_family,
        user_data_file=user_data_file,
        tag=list(tag),
        json=json,
        token=token,
        base_url=base_url,
        insecure=insecure,
    )
    response = start_instance(args)
    if args.dry_run:
        return

    status = int(response.status_code)
    if status < 200 or status >= 300 or response.parsed is None:
        print_response(response)
        sys.exit(1)

    instance_ids = response.parsed.data.instance_ids
    if json:
        print(_json.dumps(instance_ids, indent=2))
        return

    print(f"Started instances: {', '.join(instance_ids)}")


@main.command(name="stop", help="Stop/terminate one or more instances.")
@click.argument("id", nargs=-1, required=True)
@_common_options
def stop_cmd(id: tuple[str, ...], token: str | None, base_url: str, insecure: bool) -> None:
    args = SimpleNamespace(id=list(id), token=token, base_url=base_url, insecure=insecure)
    response = stop_instances(args)
    print_response(response)

    status = int(response.status_code)
    if status < 200 or status >= 300 or response.parsed is None:
        sys.exit(1)


@main.command(name="restart", help="Restart one or more instances.")
@click.argument("id", nargs=-1, required=True)
@_common_options
def restart_cmd(id: tuple[str, ...], token: str | None, base_url: str, insecure: bool) -> None:
    args = SimpleNamespace(id=list(id), token=token, base_url=base_url, insecure=insecure)
    response = restart_instances(args)
    print_response(response)

    status = int(response.status_code)
    if status < 200 or status >= 300 or response.parsed is None:
        sys.exit(1)


@main.command(name="rename", help="Rename an instance.")
@click.argument("id")
@click.argument("name")
@_common_options
def rename_cmd(id: str, name: str, token: str | None, base_url: str, insecure: bool) -> None:
    response = rename_instance(id, name, base_url, token, insecure)
    print_response(response)

    status = int(response.status_code)
    if status < 200 or status >= 300 or response.parsed is None:
        sys.exit(1)


@main.command(name="ssh", help="SSH into an instance by name or id.")
@click.argument("name_or_id")
@click.option(
    "--timeout-seconds",
    type=int,
    default=60 * 10,  # 10min
    show_default=True,
    help="Time to wait for an IP before giving up.",
)
@click.option(
    "--interval-seconds",
    type=int,
    default=5,
    show_default=True,
    help="Polling interval while waiting for the IP.",
)
@click.option(
    "--ssh-ready-timeout-seconds",
    type=int,
    default=120,
    show_default=True,
    help="Time to wait for SSH (port 22) to open after an IP is assigned.",
)
@_common_options
def ssh_cmd(
    name_or_id: str,
    timeout_seconds: int,
    interval_seconds: int,
    ssh_ready_timeout_seconds: int,
    token: str | None,
    base_url: str,
    insecure: bool,
) -> None:
    args = SimpleNamespace(
        name_or_id=name_or_id,
        timeout_seconds=max(timeout_seconds, 1),
        interval_seconds=max(interval_seconds, 1),
        ssh_ready_timeout_seconds=max(ssh_ready_timeout_seconds, 1),
        token=token,
        base_url=base_url,
        insecure=insecure,
    )
    ssh_into_instance(args)


@main.command(name="types", help="List instance types.")
@click.option("--available", is_flag=True, help="Show only types with available capacity.")
@click.option("--cheapest", is_flag=True, help="Show only the cheapest type(s).")
@click.option("--region", multiple=True, help="Filter by region (repeat allowed).")
@click.option("--gpu", multiple=True, help="Filter by GPU description substring (repeat allowed).")
@click.option("--min-gpus", type=int, default=None, help="Minimum GPUs.")
@click.option("--min-vcpus", type=int, default=None, help="Minimum vCPUs.")
@click.option("--min-memory", type=int, default=None, help="Minimum memory (GiB).")
@click.option("--min-storage", type=int, default=None, help="Minimum storage (GiB).")
@click.option("--max-price", type=float, default=None, help="Maximum price (cents/hour).")
@click.option("--json", is_flag=True, help="Output raw JSON instead of a table.")
@_common_options
def types_cmd(
    available: bool,
    cheapest: bool,
    region: tuple[str, ...],
    gpu: tuple[str, ...],
    min_gpus: int | None,
    min_vcpus: int | None,
    min_memory: int | None,
    min_storage: int | None,
    max_price: int | None,
    json: bool,
    token: str | None,
    base_url: str,
    insecure: bool,
) -> None:
    args = SimpleNamespace(
        token=token,
        base_url=base_url,
        insecure=insecure,
        available=available,
        cheapest=cheapest,
        region=list(region),
        gpu=gpu,
        min_gpus=min_gpus,
        min_vcpus=min_vcpus,
        min_memory=min_memory,
        min_storage=min_storage,
        max_price=max_price,
    )
    response = list_instance_types(args)
    filtered_response = filter_instance_types(response, args)

    if json:
        print_response(filtered_response)
        return

    render_types_table(filtered_response)


@main.command(name="images", help="List available images.")
@click.option(
    "--family",
    multiple=True,
    help="Filter images by family (repeat to include multiple).",
)
@click.option(
    "--version",
    multiple=True,
    help="Filter images by version (repeat to include multiple).",
)
@click.option(
    "--arch",
    multiple=True,
    help="Filter images by architecture (repeat to include multiple).",
)
@click.option(
    "--region",
    multiple=True,
    help="Filter images by region name (repeat to include multiple).",
)
@click.option(
    "--json",
    is_flag=True,
    help="Output raw JSON instead of a table.",
)
@_common_options
def images_cmd(
    family: tuple[str, ...],
    version: tuple[str, ...],
    arch: tuple[str, ...],
    region: tuple[str, ...],
    json: bool,
    token: str | None,
    base_url: str,
    insecure: bool,
) -> None:
    response = list_images(base_url, token, insecure)
    filtered_response = filter_images(response, family, version, arch, region)

    if json:
        print_response(filtered_response)
        return

    render_images_table(filtered_response)


@main.command(name="keys", help="List SSH keys.")
@click.option(
    "--id",
    multiple=True,
    help="Filter keys by id (repeat to include multiple).",
)
@click.option(
    "--name",
    multiple=True,
    help="Filter key by name (repeat to include multiple).",
)
@click.option(
    "--json",
    is_flag=True,
    help="Output raw JSON instead of a table.",
)
@_common_options
def ssh_keys_cmd(
    id: tuple[str, ...] | None,
    name: tuple[str, ...] | None,
    json: bool,
    token: str | None,
    base_url: str,
    insecure: bool,
) -> None:
    response = list_keys(base_url, token, insecure)
    filtered_response = filter_keys(response, id, name)

    if json:
        print_response(filtered_response)
        return

    render_keys_table(filtered_response)


if __name__ == "__main__":
    main()

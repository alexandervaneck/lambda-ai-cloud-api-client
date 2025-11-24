"""Command line wrapper for the Lambda Cloud API client (click-based)."""

from __future__ import annotations

import json as _json
import os
import sys
from collections.abc import Callable
from typing import TypeVar

import click

from lambda_ai_cloud_api_client.cli.get import get_instance
from lambda_ai_cloud_api_client.cli.images import filter_images, list_images, render_images_table
from lambda_ai_cloud_api_client.cli.keys import filter_keys, list_keys, render_keys_table
from lambda_ai_cloud_api_client.cli.ls import filter_instances, list_instances, render_instances_table
from lambda_ai_cloud_api_client.cli.rename import rename_instance
from lambda_ai_cloud_api_client.cli.response import print_response
from lambda_ai_cloud_api_client.cli.restart import restart_instances
from lambda_ai_cloud_api_client.cli.run import run_remote
from lambda_ai_cloud_api_client.cli.ssh import choose_instance, ssh_into_instance
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


def _instance_type_filter_options(func: Callable[..., T]) -> Callable[..., T]:
    func = click.option("--instance-type", help="Instance type name (optional if filters narrow to one).")(func)
    func = click.option("--available", is_flag=True, help="Show only types with available capacity.")(func)
    func = click.option("--cheapest", is_flag=True, help="Show only the cheapest type(s).")(func)
    func = click.option("--region", multiple=True, help="Filter by region (repeat allowed).")(func)
    func = click.option("--gpu", multiple=True, help="Filter by GPU description substring (repeat allowed).")(func)
    func = click.option("--min-gpus", type=int, default=None, help="Minimum GPUs.")(func)
    func = click.option("--min-vcpus", type=int, default=None, help="Minimum vCPUs.")(func)
    func = click.option("--min-memory", type=int, default=None, help="Minimum memory (GiB).")(func)
    func = click.option("--min-storage", type=int, default=None, help="Minimum storage (GiB).")(func)
    func = click.option("--max-price", type=float, default=None, help="Maximum price (cents/hour).")(func)
    return func


def _ssh_wait_options(func: Callable[..., T]) -> Callable[..., T]:
    func = click.option(
        "--timeout-seconds",
        type=int,
        default=60 * 10,  # 10min
        show_default=True,
        help="Time to wait before an IP address is assigned and until SSH (port 22) is open, individually.",
    )(func)
    func = click.option(
        "--interval-seconds",
        type=int,
        default=5,
        show_default=True,
        help="Polling interval while waiting for the IP.",
    )(func)
    return func


def _start_options(func: Callable[..., T]) -> Callable[..., T]:
    func = click.option(
        "--ssh-key", required=False, multiple=True, help="SSH key name to inject (repeat for multiple)."
    )(func)
    func = click.option("--dry-run", is_flag=True, help="Resolve type/region and print the plan without launching.")(
        func
    )
    func = click.option("--name", help="Instance name.")(func)
    func = click.option("--hostname", help="Hostname to assign.")(func)
    func = click.option("--filesystem", multiple=True, help="Filesystem name to mount (repeat for multiple).")(func)
    func = click.option("--image-id", help="Image ID to boot from.")(func)
    func = click.option("--image-family", help="Image family to boot from.")(func)
    func = click.option("--user-data-file", help="Path to cloud-init user-data file.")(func)
    func = click.option("--tag", multiple=True, help="Tag to apply, formatted as key=value (repeat for multiple).")(
        func
    )
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
@click.argument("id_or_name")
@_common_options
def get_cmd(id_or_name: str, token: str | None, base_url: str, insecure: bool) -> None:
    instances = list_instances(base_url, token, insecure)
    response = choose_instance(instances, id_or_name)
    response = get_instance(id=response.id, base_url=base_url, token=token, insecure=insecure)
    print_response(response)

    status = int(response.status_code)
    if status < 200 or status >= 300 or response.parsed is None:
        sys.exit(1)


@main.command(name="start", help="Start/launch a new instance.")
@_instance_type_filter_options
@_start_options
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
    response = start_instance(
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
        ssh_key=ssh_key,
        dry_run=dry_run,
        name=name,
        hostname=hostname,
        filesystem=filesystem,
        image_id=image_id,
        image_family=image_family,
        user_data_file=user_data_file,
        tag=tag,
        json=json,
        token=token,
        base_url=base_url,
        insecure=insecure,
    )
    if dry_run:
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
@click.argument("id_or_name", nargs=-1, required=True)
@_common_options
def stop_cmd(id_or_name: tuple[str, ...], token: str | None, base_url: str, insecure: bool) -> None:
    response = stop_instances(id_or_name, base_url, token, insecure)
    print_response(response)

    status = int(response.status_code)
    if status < 200 or status >= 300 or response.parsed is None:
        sys.exit(1)


@main.command(name="restart", help="Restart one or more instances.")
@click.argument("id_or_name", nargs=-1, required=True)
@_common_options
def restart_cmd(id_or_name: tuple[str, ...], token: str | None, base_url: str, insecure: bool) -> None:
    response = restart_instances(id_or_name, base_url, token, insecure)
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
@_ssh_wait_options
@_common_options
def ssh_cmd(
    name_or_id: str,
    timeout_seconds: int,
    interval_seconds: int,
    token: str | None,
    base_url: str,
    insecure: bool,
) -> None:
    ssh_into_instance(name_or_id, max(timeout_seconds, 1), max(interval_seconds, 1), base_url, token, insecure)


@main.command(name="run", help="Run a command on an instance over SSH.")
@click.argument("command", nargs=-1, required=True)
@_instance_type_filter_options
@_start_options
@click.option(
    "-e",
    "--env",
    "env_vars",
    multiple=True,
    help="Set environment variables (KEY=VALUE) on the remote command (repeatable).",
)
@click.option(
    "--env-file",
    multiple=True,
    help="Path to a file with KEY=VALUE lines to set as environment variables (repeatable).",
)
@click.option(
    "-v",
    "--volume",
    "volume",
    multiple=True,
    help="Bind a local path to a remote path with rsync before/after command (<local>:<remote>).",
)
@click.option(
    "--rm",
    "remove",
    is_flag=True,
    help="Remove the instance after the command executes, make sure to use --volumes to retrieve written out data.",
)
@_ssh_wait_options
@_common_options
def run_cmd(
    command: tuple[str, ...],
    env_vars: tuple[str, ...],
    env_file: tuple[str, ...],
    volume: tuple[str, ...],
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
    remove: bool,
    timeout_seconds: int,
    interval_seconds: int,
    token: str | None,
    base_url: str,
    insecure: bool,
) -> None:
    # The first word in the command may be an id or instance name.
    # If we haven't set filters then we assume the first arg is the name or id.
    name_or_id = None
    if not any(
        [instance_type, available, cheapest, region, gpu, min_gpus, min_vcpus, min_memory, min_storage, max_price]
    ):
        name_or_id = command[0]
        command = command[1:]

    if not name_or_id and not ssh_key:
        raise click.UsageError("Provide --ssh-key when launching a new instance.")

    if not name_or_id:
        response = start_instance(
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
            ssh_key=ssh_key,
            dry_run=dry_run,
            name=name,
            hostname=hostname,
            filesystem=filesystem,
            image_id=image_id,
            image_family=image_family,
            user_data_file=user_data_file,
            tag=tag,
            token=token,
            base_url=base_url,
            insecure=insecure,
        )
        name_or_id = response.parsed.data.instance_ids[0]
    run_remote(
        name_or_id=name_or_id,
        command=command,
        env_vars=env_vars,
        env_files=env_file,
        volumes=volume,
        timeout_seconds=max(timeout_seconds, 1),
        interval_seconds=max(interval_seconds, 1),
        token=token,
        base_url=base_url,
        insecure=insecure,
    )
    if remove:
        response = stop_instances(tuple([name_or_id]), base_url, token, insecure)
        print_response(response)


@main.command(name="types", help="List instance types.")
@_instance_type_filter_options
@click.option("--json", is_flag=True, help="Output raw JSON instead of a table.")
@_common_options
def types_cmd(
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
    json: bool,
    token: str | None,
    base_url: str,
    insecure: bool,
) -> None:
    response = list_instance_types(base_url, token, insecure)
    filtered_response = filter_instance_types(
        response,
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

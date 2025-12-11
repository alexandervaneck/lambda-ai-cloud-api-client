import os
from collections.abc import Callable
from functools import wraps
from http import HTTPStatus
from typing import TypeVar

import click
from click import UsageError

from lambda_ai_cloud_api_client.cli.get import get_instance
from lambda_ai_cloud_api_client.cli.images import filter_images, list_images, render_images_table
from lambda_ai_cloud_api_client.cli.keys import filter_keys, list_keys, render_keys_table
from lambda_ai_cloud_api_client.cli.ls import filter_instances, list_instances, render_instances_table
from lambda_ai_cloud_api_client.cli.rename import rename_instance
from lambda_ai_cloud_api_client.cli.response import print_json
from lambda_ai_cloud_api_client.cli.restart import restart_instances
from lambda_ai_cloud_api_client.cli.run import run_remote
from lambda_ai_cloud_api_client.cli.ssh import get_instance_by_name_or_id, ssh_into_instance
from lambda_ai_cloud_api_client.cli.start import start_instance
from lambda_ai_cloud_api_client.cli.stop import stop_instances
from lambda_ai_cloud_api_client.cli.types import filter_instance_types, list_instance_types, render_types_table
from lambda_ai_cloud_api_client.errors import HttpError

DEFAULT_BASE_URL = os.getenv("LAMBDA_CLOUD_BASE_URL", "https://cloud.lambdalabs.com")
TOKEN_ENV_VARS = ("LAMBDA_CLOUD_TOKEN", "LAMBDA_CLOUD_API_TOKEN", "LAMBDA_API_TOKEN")

T = TypeVar("T")


def raise_error_as_usage_error(f: Callable[..., T]) -> Callable[..., T]:
    @wraps(f)
    def wrapper(*args, **kwargs) -> T:
        try:
            return f(*args, **kwargs)
        except (HttpError, RuntimeError) as e:
            raise UsageError(str(e)) from e

    return wrapper


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
        type=float,
        default=60 * 10,  # 10min
        show_default=True,
        help="Time to wait before an IP address is assigned and until SSH (port 22) is open, individually.",
    )(func)
    func = click.option(
        "--interval-seconds",
        type=float,
        default=5,
        show_default=True,
        help="Polling interval while waiting for the IP.",
    )(func)
    return func


def _start_options(func: Callable[..., T]) -> Callable[..., T]:
    func = click.option(
        "--ssh-key", required=False, multiple=True, help="SSH key name to inject (repeat for multiple)."
    )(func)
    func = click.option(
        "--firewall-ruleset",
        "firewall_ruleset",
        multiple=True,
        help="Firewall ruleset ID to associate with the instance (repeat for multiple).",
    )(func)
    func = click.option("--dry-run", is_flag=True, help="Resolve type/region and print the plan without launching.")(
        func
    )
    func = click.option("--name", help="Instance name.")(func)
    func = click.option("--hostname", help="Hostname to assign.")(func)
    func = click.option("--filesystem", multiple=True, help="Filesystem name to mount (repeat for multiple).")(func)
    func = click.option(
        "--filesystem-mount",
        "filesystem_mount",
        multiple=True,
        help="Mount filesystem by id at a given path (<filesystem-id>:<absolute-mount-path>). Repeatable.",
    )(func)
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
@raise_error_as_usage_error
def ls_cmd(status: tuple[str, ...], region: tuple[str, ...], json: bool) -> None:
    instances = list_instances()
    filtered_instances = filter_instances(instances, region, status)

    if json:
        print_json([i.to_dict() for i in instances])
        return

    render_instances_table(filtered_instances)


@main.command(name="get", help="Get instance details.")
@click.argument("id_or_name")
@raise_error_as_usage_error
def get_cmd(id_or_name: str) -> None:
    try:
        instance = get_instance(id=id_or_name)  # if user sent an ID it'll work.
    except HttpError as e:
        if e.status_code not in (HTTPStatus.NOT_FOUND, HTTPStatus.BAD_REQUEST):
            raise
        # We have to look up the name
        instances = list_instances()
        instance = get_instance_by_name_or_id(instances, id_or_name)

    print_json(instance.to_dict())


@main.command(name="start", help="Start/launch a new instance.")
@_instance_type_filter_options
@_start_options
@click.option("--json", is_flag=True, help="Output raw JSON instead of a table.")
@raise_error_as_usage_error
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
    filesystem_mount: tuple[str, ...],
    image_id: str | None,
    image_family: str | None,
    user_data_file: str | None,
    tag: tuple[str, ...],
    firewall_ruleset: tuple[str, ...],
    json: bool,
) -> None:
    instance_ids = start_instance(
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
        filesystem_mount=filesystem_mount,
        image_id=image_id,
        image_family=image_family,
        user_data_file=user_data_file,
        tag=tag,
        firewall_ruleset=firewall_ruleset,
        json=json,
    )
    if dry_run:
        return

    instances = list_instances()
    filtered_instances = filter_instances(instances, id=tuple(instance_ids))
    instance = filtered_instances[0]

    if json:
        print_json(instance.to_dict())
        return

    render_instances_table([instance], title="Launched instance")


@main.command(name="restart", help="Restart one or more instances.")
@click.argument("id_or_name", nargs=-1, required=True)
@raise_error_as_usage_error
def restart_cmd(
    id_or_name: tuple[str, ...],
) -> None:
    instances = restart_instances(id_or_name)
    print_json([i.to_dict() for i in instances])


@main.command(name="stop", help="Stop/terminate one or more instances.")
@click.argument("id_or_name", nargs=-1, required=True)
@raise_error_as_usage_error
def stop_cmd(
    id_or_name: tuple[str, ...],
) -> None:
    instances = stop_instances(id_or_name)
    print_json([i.to_dict() for i in instances])


@main.command(name="rename", help="Rename an instance.")
@click.argument("id")
@click.argument("name")
@raise_error_as_usage_error
def rename_cmd(
    id: str,
    name: str,
) -> None:
    instance = rename_instance(id, name)
    print_json(instance.to_dict())


@main.command(name="ssh", help="SSH into an instance by name or id.")
@click.argument("name_or_id")
@_ssh_wait_options
@raise_error_as_usage_error
def ssh_cmd(
    name_or_id: str,
    timeout_seconds: float,
    interval_seconds: float,
) -> None:
    instances = list_instances()
    instance = get_instance_by_name_or_id(instances, name_or_id)
    render_instances_table([instance], title="Instance")
    ssh_into_instance(instance, timeout_seconds, interval_seconds)


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
@raise_error_as_usage_error
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
    filesystem_mount: tuple[str, ...],
    image_id: str | None,
    image_family: str | None,
    user_data_file: str | None,
    tag: tuple[str, ...],
    firewall_ruleset: tuple[str, ...],
    remove: bool,
    timeout_seconds: int,
    interval_seconds: int,
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
        instance_ids = start_instance(
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
            filesystem_mount=filesystem_mount,
            image_id=image_id,
            image_family=image_family,
            user_data_file=user_data_file,
            tag=tag,
            firewall_ruleset=firewall_ruleset,
        )
        name_or_id = instance_ids[0]

    instances = list_instances()
    instance = get_instance_by_name_or_id(instances=instances, name_or_id=name_or_id)
    render_instances_table([instance], title="Instance")

    run_remote(
        instance=instance,
        command=command,
        env_vars=env_vars,
        env_files=env_file,
        volumes=volume,
        timeout_seconds=max(timeout_seconds, 1),
        interval_seconds=max(interval_seconds, 1),
    )
    if remove:
        instances = stop_instances(tuple([instance.id]))
        print_json([i.to_dict() for i in instances])


@main.command(name="types", help="List instance types.")
@_instance_type_filter_options
@click.option("--json", is_flag=True, help="Output raw JSON instead of a table.")
@raise_error_as_usage_error
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
) -> None:
    instance_types = list_instance_types()
    instance_types = filter_instance_types(
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

    if json:
        print_json([i.to_dict() for i in instance_types])
        return

    render_types_table(instance_types)


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
@raise_error_as_usage_error
def images_cmd(
    family: tuple[str, ...],
    version: tuple[str, ...],
    arch: tuple[str, ...],
    region: tuple[str, ...],
    json: bool,
) -> None:
    images = list_images()
    images = filter_images(images, family, version, arch, region)

    if json:
        print_json([i.to_dict() for i in images])
        return

    render_images_table(images)


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
@raise_error_as_usage_error
def ssh_keys_cmd(
    id: tuple[str, ...] | None,
    name: tuple[str, ...] | None,
    json: bool,
) -> None:
    keys = list_keys()
    keys = filter_keys(keys, id, name)

    if json:
        print_json([i.to_dict() for i in keys])
        return

    render_keys_table(keys)


if __name__ == "__main__":
    main()

from __future__ import annotations

import os
import shlex
import socket
import sys
import time

from lambda_ai_cloud_api_client.cli.get import get_instance
from lambda_ai_cloud_api_client.models import Instance
from lambda_ai_cloud_api_client.types import Unset


def get_instance_by_name_or_id(instances: list[Instance], name_or_id: str) -> Instance:
    filtered_instances = []
    for instance in instances:
        if instance.id == name_or_id or instance.name == name_or_id:
            filtered_instances.append(instance)

    if len(filtered_instances) == 1:
        return filtered_instances[0]

    if len(filtered_instances) > 1:
        raise RuntimeError(f"Multiple instances share the name '{name_or_id}'.")

    raise RuntimeError(f"No instance found with name or id '{name_or_id}'.")


def _wait_for_ip(instance: Instance, timeout_seconds: float, interval_seconds: float) -> Instance | None:
    deadline = time.monotonic() + timeout_seconds
    while True:
        if instance.ip and not isinstance(instance.ip, Unset):
            return instance

        instance = get_instance(instance.id)

        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return None

        print(
            f"Waiting for IP on instance '{instance.name}' ({instance.id})... retrying in {interval_seconds:.2f}s",
            file=sys.stderr,
        )
        time.sleep(interval_seconds)


def _wait_for_ssh(instance: Instance, timeout_seconds: float, interval_seconds: float) -> bool:
    deadline = time.monotonic() + timeout_seconds
    while True:
        try:
            with socket.create_connection((instance.ip, 22), timeout=5):
                return True
        except OSError:
            pass

        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return False

        print(
            f"Waiting for SSH on instance '{instance.name}' ({instance.ip})... retrying in {interval_seconds:.2f}s",
            file=sys.stderr,
        )
        time.sleep(interval_seconds)


def wait_for_instance(
    instance: Instance,
    timeout_seconds: float,
    interval_seconds: float,
) -> Instance:
    name, id = instance.name, instance.id
    instance = _wait_for_ip(instance, timeout_seconds, interval_seconds)

    if instance is None or not instance.ip or isinstance(instance.ip, Unset):
        raise RuntimeError(f"Instance '{name}' ({id}) did not receive an IP within {timeout_seconds} seconds.")

    if not _wait_for_ssh(instance, timeout_seconds, interval_seconds):
        raise RuntimeError(f"Instance '{name}' ({id}) did not open SSH within {timeout_seconds} seconds.")

    return instance


def ssh_command(ip: str, command: tuple[str, ...], env_assignments: list[str] | None = None) -> list[str]:
    target = f"ubuntu@{ip}"
    ssh_args = [
        "ssh",
        "-o",
        "StrictHostKeyChecking=accept-new",
        "-o",
        "UserKnownHostsFile=/dev/null",
        target,
    ]
    if command:
        parts: list[str] = []
        if env_assignments:
            parts.extend(env_assignments)
        parts.extend(command)
        remote_cmd = " ".join(shlex.quote(p) for p in parts)
        ssh_args.append(remote_cmd)
    return ssh_args


def ssh_into_instance(
    instance: Instance,
    timeout_seconds: float,
    interval_seconds: float,
    *,
    command: tuple[str, ...] | None = None,
    env_assignments: list[str] | None = None,
) -> None:
    instance = wait_for_instance(
        instance,
        timeout_seconds,
        interval_seconds,
    )
    ssh_args = ssh_command(instance.ip, command, env_assignments)
    print(f"Executing: {' '.join(ssh_args)}")
    os.execvp("ssh", ssh_args)

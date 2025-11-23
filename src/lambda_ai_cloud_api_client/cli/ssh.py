from __future__ import annotations

import os
import socket
import sys
import time

from lambda_ai_cloud_api_client.cli.get import get_instance
from lambda_ai_cloud_api_client.cli.ls import list_instances
from lambda_ai_cloud_api_client.cli.response import print_response
from lambda_ai_cloud_api_client.models import Instance
from lambda_ai_cloud_api_client.types import Response, Unset


def _extract_ip(instance: Instance | None) -> str | None:
    if instance is None:
        return None

    ip = getattr(instance, "ip", None)
    if isinstance(ip, Unset) or not ip:
        return None
    return ip


def _choose_instance(response: Response, name_or_id: str) -> Instance:
    status = int(response.status_code)
    if status < 200 or status >= 300 or response.parsed is None:
        print_response(response)
        sys.exit(1)

    instances = getattr(response.parsed, "data", None) or []
    for inst in instances:
        if getattr(inst, "id", None) == name_or_id:
            return inst

    matches = [
        inst
        for inst in instances
        if not isinstance(getattr(inst, "name", None), Unset) and getattr(inst, "name", None) == name_or_id
    ]

    if not matches:
        print(f"No instance found with name or id '{name_or_id}'.", file=sys.stderr)
        sys.exit(1)

    if len(matches) > 1:
        ids = ", ".join(getattr(inst, "id", "") for inst in matches)
        print(
            f"Multiple instances share the name '{name_or_id}'. Choose by ID instead. Matches: {ids}", file=sys.stderr
        )
        sys.exit(1)

    return matches[0]


def _wait_for_ip(
    name_or_id: str,
    instance_id: str,
    timeout_seconds: int,
    interval_seconds: int,
    base_url: str,
    token: str | None = None,
    insecure: bool = False,
) -> str | None:
    deadline = time.monotonic() + timeout_seconds
    while True:
        response = get_instance(id=instance_id, base_url=base_url, token=token, insecure=insecure)
        status = int(response.status_code)
        if status < 200 or status >= 300 or response.parsed is None:
            print_response(response)
            sys.exit(1)

        ip = _extract_ip(getattr(response.parsed, "data", None))
        if ip:
            return ip

        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return None

        wait_seconds = min(interval_seconds, remaining)
        print(
            f"Waiting for IP on instance '{name_or_id}' ({instance_id})... retrying in {int(wait_seconds)}s",
            file=sys.stderr,
        )
        time.sleep(wait_seconds)


def _wait_for_ssh(name_or_id: str, ip: str, ssh_ready_timeout_seconds: int, interval_seconds: int) -> bool:
    deadline = time.monotonic() + ssh_ready_timeout_seconds
    while True:
        try:
            with socket.create_connection((ip, 22), timeout=5):
                return True
        except OSError:
            pass

        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return False

        wait_seconds = min(interval_seconds, remaining)
        print(
            f"Waiting for SSH on instance '{name_or_id}' ({ip})... retrying in {int(wait_seconds)}s",
            file=sys.stderr,
        )
        time.sleep(wait_seconds)


def ssh_into_instance(
    name_or_id: str,
    timeout_seconds: int,
    interval_seconds: int,
    base_url: str,
    token: str | None = None,
    insecure: bool = False,
) -> None:
    instances = list_instances(base_url, token, insecure)
    instance = _choose_instance(instances, name_or_id)

    ip = _extract_ip(instance)
    if not ip:
        ip = _wait_for_ip(
            name_or_id,
            instance.id,
            timeout_seconds,
            interval_seconds,
            base_url=base_url,
            token=token,
            insecure=insecure,
        )

    if not ip:
        print(
            f"Instance '{name_or_id}' ({instance.id}) did not receive an IP within {timeout_seconds} seconds.",
            file=sys.stderr,
        )
        sys.exit(1)

    if not _wait_for_ssh(name_or_id, ip, timeout_seconds, interval_seconds):
        print(
            f"Instance '{name_or_id}' ({instance.id}) did not open SSH within {timeout_seconds} seconds.",
            file=sys.stderr,
        )
        sys.exit(1)

    target = f"ubuntu@{ip}"
    print(f"Connecting to {target} ...")
    os.execvp("ssh", ["ssh", target])

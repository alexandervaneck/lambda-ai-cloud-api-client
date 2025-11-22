from __future__ import annotations

import os
import socket
import sys
import time
from types import SimpleNamespace

from lambda_ai_cloud_api_client.cli.get import get_instance as _get_instance
from lambda_ai_cloud_api_client.cli.ls import list_instances as _list_instances
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


def _wait_for_ip(instance_id: str, args: SimpleNamespace) -> str | None:
    deadline = time.monotonic() + args.timeout_seconds
    poll_args = SimpleNamespace(
        id=instance_id,
        token=args.token,
        base_url=args.base_url,
        insecure=args.insecure,
    )

    while True:
        response = _get_instance(poll_args)
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

        wait_seconds = min(args.interval_seconds, remaining)
        print(
            f"Waiting for IP on instance '{args.name_or_id}' ({instance_id})... retrying in {int(wait_seconds)}s",
            file=sys.stderr,
        )
        time.sleep(wait_seconds)


def _wait_for_ssh(ip: str, args: SimpleNamespace) -> bool:
    deadline = time.monotonic() + args.ssh_ready_timeout_seconds
    while True:
        try:
            with socket.create_connection((ip, 22), timeout=5):
                return True
        except OSError:
            pass

        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return False

        wait_seconds = min(args.interval_seconds, remaining)
        print(
            f"Waiting for SSH on instance '{args.name_or_id}' ({ip})... retrying in {int(wait_seconds)}s",
            file=sys.stderr,
        )
        time.sleep(wait_seconds)


def ssh_into_instance(args: SimpleNamespace) -> None:
    instances = _list_instances(args)
    instance = _choose_instance(instances, args.name_or_id)

    ip = _extract_ip(instance)
    if not ip:
        ip = _wait_for_ip(instance.id, args)

    if not ip:
        print(
            f"Instance '{args.name_or_id}' ({instance.id}) did not receive an IP within {args.timeout_seconds} seconds.",
            file=sys.stderr,
        )
        sys.exit(1)

    if not _wait_for_ssh(ip, args):
        print(
            f"Instance '{args.name_or_id}' ({instance.id}) did not open SSH within "
            f"{args.ssh_ready_timeout_seconds} seconds.",
            file=sys.stderr,
        )
        sys.exit(1)

    target = f"ubuntu@{ip}"
    print(f"Connecting to {target} ...")
    os.execvp("ssh", ["ssh", target])

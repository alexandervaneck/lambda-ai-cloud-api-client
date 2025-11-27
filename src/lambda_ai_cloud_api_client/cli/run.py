from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from dotenv import dotenv_values

from lambda_ai_cloud_api_client.cli.ssh import ssh_command, wait_for_instance
from lambda_ai_cloud_api_client.models import Instance


def _parse_env_vars(raw_env: list[str]) -> dict[str, str]:
    envs: dict[str, str] = {}
    for item in raw_env:
        if "=" not in item or item.startswith("="):
            raise RuntimeError(f"Invalid env var '{item}'. Use KEY=VALUE.")
        key, value = item.split("=", 1)
        envs[key] = value
    return envs


def _parse_env_file(path: Path) -> dict[str, str]:
    if not path.exists():
        raise RuntimeError(f"Env file not found: {path}")
    envs = dotenv_values(path)
    return {k: v for k, v in envs.items() if k is not None and v is not None}


def _parse_volumes(raw_volumes: tuple[str, ...]) -> list[tuple[str, str]]:
    volumes: list[tuple[str, str]] = []
    for spec in raw_volumes:
        if ":" not in spec:
            raise RuntimeError(f"Invalid volume '{spec}'. Use <local-path>:<remote-path>.")
        local, remote = spec.split(":", 1)
        if not Path(local).exists():
            raise RuntimeError(f"Local path not found for volume: {local}")
        volumes.append((local, remote))
    return volumes


def _rsync(local: str, remote: str, ip: str, reverse: bool = False) -> None:
    src, dst = (f"ubuntu@{ip}:{remote}", local) if reverse else (local, f"ubuntu@{ip}:{remote}")
    cmd = [
        "rsync",
        "-e",
        "ssh -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile=/dev/null",
        "-az",
        "--delete",
        src,
        dst,
    ]
    print(f"Rsync: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True, stdout=sys.stdout, stderr=sys.stderr)
    except FileNotFoundError as e:
        raise RuntimeError("rsync is not installed or not in PATH.") from e
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"rsync failed with code {e.returncode}") from e


def run_remote(
    instance: Instance,
    command: tuple[str, ...],
    env_vars: tuple[str, ...],
    env_files: tuple[str, ...],
    volumes: tuple[str, ...],
    timeout_seconds: int,
    interval_seconds: int,
) -> None:
    envs: dict[str, str] = {}
    envs.update(_parse_env_vars(list(env_vars)))
    for env_file in env_files:
        envs.update(_parse_env_file(Path(env_file)))
    env_assignments = [f"{k}={v}" for k, v in envs.items()]

    volume_pairs = _parse_volumes(volumes)

    instance = wait_for_instance(instance, timeout_seconds, interval_seconds)

    for local, remote in volume_pairs:
        _rsync(local, remote, instance.ip)

    ssh_args = ssh_command(instance.ip, command, env_assignments)
    print(f"Executing: {' '.join(ssh_args)}")

    try:
        result = subprocess.run(ssh_args)
    finally:
        for local, remote in volume_pairs:
            _rsync(local, remote, instance.ip, reverse=True)

    if result.returncode:
        sys.exit(result.returncode)

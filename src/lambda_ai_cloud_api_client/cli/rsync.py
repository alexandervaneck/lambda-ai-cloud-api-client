from __future__ import annotations

import subprocess
import sys
import click
from lambda_ai_cloud_api_client.models import Instance
from lambda_ai_cloud_api_client.cli.utils import get_rsync_ignore_args
from lambda_ai_cloud_api_client.cli.ls import list_instances
from lambda_ai_cloud_api_client.cli.ssh import get_instance_by_name_or_id

def rsync_instance(
    instance: Instance,
    src: str,
    dst: str,
    reverse: bool = False,
    additional_args: tuple[str, ...] = (),
    use_ignore: bool = True,
) -> None:
    """
    Rsync files to/from an instance.
    """
    if reverse:
        full_src = f"ubuntu@{instance.ip}:{src}"
        full_dst = dst
    else:
        full_src = src
        full_dst = f"ubuntu@{instance.ip}:{dst}"

    cmd = [
        "rsync",
        "-e",
        "ssh -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile=/dev/null",
        "-az",
    ]
    
    if use_ignore and not reverse:
        cmd.extend(get_rsync_ignore_args())

    cmd.extend(additional_args)
    cmd.extend([full_src, full_dst])

    from rich import print
    print(f"[bold blue]Rsync:[/bold blue] {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True, stdout=sys.stdout, stderr=sys.stderr)
    except FileNotFoundError as e:
        raise RuntimeError("rsync is not installed or not in PATH.") from e
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"rsync failed with code {e.returncode}") from e

def rsync_command(
    name_or_id: str,
    src: str,
    dst: str,
    reverse: bool,
    no_ignore: bool,
    args: tuple[str, ...],
) -> None:
    instances = list_instances()
    instance = get_instance_by_name_or_id(instances, name_or_id)
    
    rsync_instance(
        instance=instance,
        src=src,
        dst=dst,
        reverse=reverse,
        additional_args=args,
        use_ignore=not no_ignore,
    )

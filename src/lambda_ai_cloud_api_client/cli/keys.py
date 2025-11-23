import sys

from rich.console import Console
from rich.table import Table

from lambda_ai_cloud_api_client.api.ssh_keys.list_ssh_keys import sync_detailed as _list_keys
from lambda_ai_cloud_api_client.cli.client import auth_client
from lambda_ai_cloud_api_client.cli.response import print_response
from lambda_ai_cloud_api_client.models import ListSSHKeysResponse200
from lambda_ai_cloud_api_client.types import Response


def list_keys(base_url: str, token: str | None = None, insecure: bool = False) -> Response[ListSSHKeysResponse200]:
    client = auth_client(base_url=base_url, token=token, insecure=insecure)
    keys: Response[ListSSHKeysResponse200] = _list_keys(client=client)
    return keys


def filter_keys(
    response: Response[ListSSHKeysResponse200], id: str | None = None, name: str | None = None
) -> Response[ListSSHKeysResponse200]:
    if response.parsed and hasattr(response.parsed, "data"):
        filtered = response.parsed.data
        if id:
            allowed_id = set(id)
            filtered = [img for img in filtered if getattr(img, "id", None) in allowed_id]
        if name:
            allowed_name = set(name)
            filtered = [img for img in filtered if getattr(img, "name", None) in allowed_name]
        response.parsed.data = filtered  # type: ignore[attr-defined]

    return response


def render_keys_table(response) -> None:
    status = int(response.status_code)
    if status < 200 or status >= 300 or response.parsed is None:
        print_response(response)
        sys.exit(1)

    parsed = response.parsed
    keys = getattr(parsed, "data", None)
    if not keys:
        Console().print("No keys found.")
        return

    table = Table(title="Keys", show_lines=False, expand=True)
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Public key", overflow="fold")

    for img in keys:
        table.add_row(
            getattr(img, "id", ""),
            getattr(img, "name", ""),
            getattr(img, "public_key", ""),
        )

    Console().print(table)

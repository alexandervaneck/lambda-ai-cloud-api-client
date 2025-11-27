from rich import print
from rich.table import Table

from lambda_ai_cloud_api_client.api.ssh_keys.list_ssh_keys import sync_detailed as _list_keys
from lambda_ai_cloud_api_client.cli.client import auth_client
from lambda_ai_cloud_api_client.models import SSHKey


def list_keys() -> list[SSHKey]:
    client = auth_client()
    response = _list_keys(client=client)
    response.raise_for_status()
    return response.parsed.data


def filter_keys(keys: list[SSHKey], id: str | None = None, name: str | None = None) -> list[SSHKey]:
    filtered_keys = []
    for key in keys:
        if id and key.id not in id:
            continue
        if name and key.name not in name:
            continue
        filtered_keys.append(key)
    return filtered_keys


def render_keys_table(keys: list[SSHKey]) -> None:
    if not keys:
        print("No keys found.")
        return

    table = Table(title="Keys", show_lines=False, expand=True)
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Public key", overflow="fold")

    for key in keys:
        table.add_row(key.id, key.name, key.public_key)

    print(table)

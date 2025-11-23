from lambda_ai_cloud_api_client.api.instances.restart_instance import sync_detailed as restart_instance
from lambda_ai_cloud_api_client.cli.client import auth_client
from lambda_ai_cloud_api_client.cli.ls import list_instances
from lambda_ai_cloud_api_client.cli.ssh import choose_instance
from lambda_ai_cloud_api_client.models import (
    InstanceRestartRequest,
    RestartInstanceResponse200,
    RestartInstanceResponse401,
    RestartInstanceResponse403,
    RestartInstanceResponse404,
)
from lambda_ai_cloud_api_client.types import Response


def restart_instances(
    ids_or_name: tuple[str, ...], base_url: str, token: str | None = None, insecure: bool = False
) -> Response[
    RestartInstanceResponse200 | RestartInstanceResponse401 | RestartInstanceResponse403 | RestartInstanceResponse404
]:
    instance_ids = []
    for id_or_name in ids_or_name:
        instances = list_instances(base_url, token, insecure)
        instance = choose_instance(instances, id_or_name)
        instance_ids.append(instance.id)

    client = auth_client(base_url=base_url, token=token, insecure=insecure)
    request = InstanceRestartRequest(instance_ids=instance_ids)
    return restart_instance(client=client, body=request)

from lambda_ai_cloud_api_client.api.instances.restart_instance import sync_detailed as restart_instance
from lambda_ai_cloud_api_client.cli.client import auth_client
from lambda_ai_cloud_api_client.models import (
    InstanceRestartRequest,
    RestartInstanceResponse200,
    RestartInstanceResponse401,
    RestartInstanceResponse403,
    RestartInstanceResponse404,
)
from lambda_ai_cloud_api_client.types import Response


def restart_instances(
    id: tuple[str, ...], base_url: str, token: str | None = None, insecure: bool = False
) -> Response[
    RestartInstanceResponse200 | RestartInstanceResponse401 | RestartInstanceResponse403 | RestartInstanceResponse404
]:
    client = auth_client(base_url=base_url, token=token, insecure=insecure)
    request = InstanceRestartRequest(instance_ids=list(id))
    return restart_instance(client=client, body=request)

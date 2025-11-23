from types import SimpleNamespace

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
    args: SimpleNamespace,
) -> Response[
    RestartInstanceResponse200 | RestartInstanceResponse401 | RestartInstanceResponse403 | RestartInstanceResponse404
]:
    client = auth_client(base_url=args.base_url, token=args.token, insecure=args.insecure)
    request = InstanceRestartRequest(instance_ids=args.id)
    return restart_instance(client=client, body=request)

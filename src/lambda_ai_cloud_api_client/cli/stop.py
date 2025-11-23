from lambda_ai_cloud_api_client.api.instances.terminate_instance import sync_detailed as terminate_instance
from lambda_ai_cloud_api_client.cli.client import auth_client
from lambda_ai_cloud_api_client.cli.ls import list_instances
from lambda_ai_cloud_api_client.cli.ssh import choose_instance
from lambda_ai_cloud_api_client.models import (
    InstanceTerminateRequest,
    TerminateInstanceResponse200,
    TerminateInstanceResponse401,
    TerminateInstanceResponse403,
    TerminateInstanceResponse404,
)
from lambda_ai_cloud_api_client.types import Response


def stop_instances(
    ids_or_name: tuple[str, ...], base_url: str, token: str | None = None, insecure: bool = False
) -> Response[
    TerminateInstanceResponse200
    | TerminateInstanceResponse401
    | TerminateInstanceResponse403
    | TerminateInstanceResponse404
]:
    instance_ids = []
    for id_or_name in ids_or_name:
        instances = list_instances(base_url, token, insecure)
        instance = choose_instance(instances, id_or_name)
        instance_ids.append(instance.id)

    client = auth_client(base_url=base_url, token=token, insecure=insecure)
    request = InstanceTerminateRequest(instance_ids=instance_ids)
    return terminate_instance(client=client, body=request)

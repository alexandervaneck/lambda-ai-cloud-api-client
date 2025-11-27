from lambda_ai_cloud_api_client.api.instances.terminate_instance import sync_detailed as terminate_instance
from lambda_ai_cloud_api_client.cli.client import auth_client
from lambda_ai_cloud_api_client.cli.ls import list_instances
from lambda_ai_cloud_api_client.cli.ssh import get_instance_by_name_or_id
from lambda_ai_cloud_api_client.models import (
    Instance,
    InstanceTerminateRequest,
)


def stop_instances(ids_or_name: tuple[str, ...]) -> list[Instance]:
    instance_ids = []
    for id_or_name in ids_or_name:
        instances = list_instances()
        instance = get_instance_by_name_or_id(instances, id_or_name)
        instance_ids.append(instance.id)

    client = auth_client()
    response = terminate_instance(client=client, body=InstanceTerminateRequest(instance_ids=instance_ids))
    response.raise_for_status()
    return response.parsed.data.terminated_instances

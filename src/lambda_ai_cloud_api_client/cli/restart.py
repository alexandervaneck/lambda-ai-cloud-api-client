from lambda_ai_cloud_api_client.api.instances.restart_instance import sync_detailed as restart_instance
from lambda_ai_cloud_api_client.cli.client import auth_client
from lambda_ai_cloud_api_client.cli.ls import list_instances
from lambda_ai_cloud_api_client.cli.ssh import get_instance_by_name_or_id
from lambda_ai_cloud_api_client.models import (
    Instance,
    InstanceRestartRequest,
)


def restart_instances(ids_or_name: tuple[str, ...]) -> list[Instance]:
    instance_ids = []
    for id_or_name in ids_or_name:
        instances = list_instances()
        instance = get_instance_by_name_or_id(instances, id_or_name)
        instance_ids.append(instance.id)

    client = auth_client()
    response = restart_instance(client=client, body=InstanceRestartRequest(instance_ids=instance_ids))
    response.raise_for_status()
    return response.parsed.data.restarted_instances

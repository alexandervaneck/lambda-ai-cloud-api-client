from lambda_ai_cloud_api_client.api.instances.post_instance import sync_detailed as _post_instance
from lambda_ai_cloud_api_client.cli.client import auth_client
from lambda_ai_cloud_api_client.models import Instance, InstanceModificationRequest


def rename_instance(id: str, name: str) -> Instance:
    client = auth_client()
    response = _post_instance(client=client, id=id, body=InstanceModificationRequest(name=name))
    response.raise_for_status()
    return response.parsed.data

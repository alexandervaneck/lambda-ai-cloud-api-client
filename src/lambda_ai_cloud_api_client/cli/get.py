from lambda_ai_cloud_api_client.api.instances.get_instance import sync_detailed as _get_instance
from lambda_ai_cloud_api_client.cli.client import auth_client
from lambda_ai_cloud_api_client.models import Instance


def get_instance(id: str) -> Instance:
    client = auth_client()
    response = _get_instance(id, client=client)
    response.raise_for_status()
    return response.parsed.data

from lambda_ai_cloud_api_client.api.instances.get_instance import sync_detailed as _get_instance
from lambda_ai_cloud_api_client.cli.client import auth_client
from lambda_ai_cloud_api_client.models import GetInstanceResponse200
from lambda_ai_cloud_api_client.types import Response


def get_instance(
    id: str, base_url: str, token: str | None = None, insecure: bool = False
) -> Response[GetInstanceResponse200]:
    client = auth_client(base_url=base_url, token=token, insecure=insecure)
    instance: Response[GetInstanceResponse200] = _get_instance(id, client=client)
    return instance

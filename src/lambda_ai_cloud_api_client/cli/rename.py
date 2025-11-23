from lambda_ai_cloud_api_client.api.instances.post_instance import sync_detailed as _post_instance
from lambda_ai_cloud_api_client.cli.client import auth_client
from lambda_ai_cloud_api_client.models import InstanceModificationRequest, PostInstanceResponse200
from lambda_ai_cloud_api_client.types import Response


def rename_instance(
    id: str, name: str, base_url: str, token: str | None = None, insecure: bool = False
) -> Response[PostInstanceResponse200]:
    client = auth_client(base_url=base_url, token=token, insecure=insecure)
    instance: Response[PostInstanceResponse200] = _post_instance(
        client=client, id=id, body=InstanceModificationRequest(name=name)
    )
    return instance

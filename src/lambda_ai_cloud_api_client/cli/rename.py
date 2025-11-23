from types import SimpleNamespace

from lambda_ai_cloud_api_client.api.instances.post_instance import sync_detailed as _post_instance
from lambda_ai_cloud_api_client.cli.client import auth_client
from lambda_ai_cloud_api_client.models import InstanceModificationRequest, PostInstanceResponse200
from lambda_ai_cloud_api_client.types import Response


def rename_instance(args: SimpleNamespace) -> Response[PostInstanceResponse200]:
    client = auth_client(base_url=args.base_url, token=args.token, insecure=args.insecure)
    instance: Response[PostInstanceResponse200] = _post_instance(
        client=client, id=args.id, body=InstanceModificationRequest(name=args.name)
    )
    return instance

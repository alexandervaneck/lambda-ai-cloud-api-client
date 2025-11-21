from types import SimpleNamespace

from lambda_ai_cloud_api_client.api.instances.get_instance import sync_detailed as _get_instance
from lambda_ai_cloud_api_client.cli.client import auth_client
from lambda_ai_cloud_api_client.models import GetInstanceResponse200
from lambda_ai_cloud_api_client.types import Response


def get_instance(args: SimpleNamespace) -> Response[GetInstanceResponse200]:
    client = auth_client(args)
    instance: Response[GetInstanceResponse200] = _get_instance(client=client, id=args.id)
    return instance

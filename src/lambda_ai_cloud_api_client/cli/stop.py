from types import SimpleNamespace

from lambda_ai_cloud_api_client.api.instances.terminate_instance import sync_detailed as terminate_instance
from lambda_ai_cloud_api_client.cli.client import auth_client
from lambda_ai_cloud_api_client.models import (
    InstanceTerminateRequest,
    TerminateInstanceResponse200,
    TerminateInstanceResponse401,
    TerminateInstanceResponse403,
    TerminateInstanceResponse404,
)
from lambda_ai_cloud_api_client.types import Response


def stop_instances(
    args: SimpleNamespace,
) -> Response[
    TerminateInstanceResponse200
    | TerminateInstanceResponse401
    | TerminateInstanceResponse403
    | TerminateInstanceResponse404
]:
    client = auth_client(base_url=args.base_url, token=args.token, insecure=args.insecure)
    request = InstanceTerminateRequest(instance_ids=args.id)
    return terminate_instance(client=client, body=request)

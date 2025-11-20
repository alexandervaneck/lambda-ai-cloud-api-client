from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.add_ssh_key_request import AddSSHKeyRequest
from ...models.add_ssh_key_response_200 import AddSSHKeyResponse200
from ...models.add_ssh_key_response_400 import AddSSHKeyResponse400
from ...models.add_ssh_key_response_401 import AddSSHKeyResponse401
from ...models.add_ssh_key_response_403 import AddSSHKeyResponse403
from ...types import Response


def _get_kwargs(
    *,
    body: AddSSHKeyRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/ssh-keys",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AddSSHKeyResponse200 | AddSSHKeyResponse400 | AddSSHKeyResponse401 | AddSSHKeyResponse403 | None:
    if response.status_code == 200:
        response_200 = AddSSHKeyResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = AddSSHKeyResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = AddSSHKeyResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = AddSSHKeyResponse403.from_dict(response.json())

        return response_403

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[AddSSHKeyResponse200 | AddSSHKeyResponse400 | AddSSHKeyResponse401 | AddSSHKeyResponse403]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: AddSSHKeyRequest,
) -> Response[AddSSHKeyResponse200 | AddSSHKeyResponse400 | AddSSHKeyResponse401 | AddSSHKeyResponse403]:
    r""" Add an SSH key

     
    Add an SSH key to your Lambda Cloud account. You can upload an existing public
    key, or you can generate a new key pair.

    -  To use an existing key pair, set the `public_key` property in the request body
       to your public key.

    -  To generate a new key pair, omit the `public_key` property from the request
       body.

    :::note{type=\"attention\" title=\"Important\"}
    Lambda doesn't store your private key after it's been generated.
    If you generate a new key pair, make sure to save the resulting private key locally.
    :::

    For example, to generate a new key pair and associate it with a Lambda
    On-Demand Cloud instance:

    1. Generate the key pair. The command provided below automatically extracts and
        saves the returned private key to a new file called `key.pem`. Replace
        `<NEW-KEY-NAME>` with the name you want to assign to the SSH key:

        ```bash
        curl --request POST --url 'https://cloud.lambda.ai/api/v1/ssh-keys' \
        --fail \
        --user ${LAMBDA_API_KEY}: \
        --data '{\"name\": \"<NEW-KEY-NAME>\"}' \
        | jq -r '.data.private_key' > key.pem
        ```

    2. Next, set the private key's permissions to read-only:

        ```bash
        chmod 400 key.pem
        ```

    3. Launch a new instance. Replace `<NEW-KEY-NAME>` with the name you assigned
       to your SSH key.

        ```bash
        curl --request POST 'https://cloud.lambda.ai/api/v1/instance-operations/launch' \
        --fail \
        --user ${LAMBDA_API_KEY}: \
        --data '{\"region_name\":\"us-
    west-1\",\"instance_type_name\":\"gpu_1x_a10\",\"ssh_key_names\":[\"<NEW-KEY-
    NAME>\"],\"file_system_names\":[],\"quantity\":1,\"name\":\"My Instance\"}'
        ```

    4. From your local terminal, establish an SSH connection to the instance.
       Replace `<INSTANCE-IP>` with the public IP of the instance:

        ```bash
        ssh -i key.pem <INSTANCE-IP>
        ```

    Args:
        body (AddSSHKeyRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AddSSHKeyResponse200 | AddSSHKeyResponse400 | AddSSHKeyResponse401 | AddSSHKeyResponse403]
     """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: AddSSHKeyRequest,
) -> AddSSHKeyResponse200 | AddSSHKeyResponse400 | AddSSHKeyResponse401 | AddSSHKeyResponse403 | None:
    r""" Add an SSH key

     
    Add an SSH key to your Lambda Cloud account. You can upload an existing public
    key, or you can generate a new key pair.

    -  To use an existing key pair, set the `public_key` property in the request body
       to your public key.

    -  To generate a new key pair, omit the `public_key` property from the request
       body.

    :::note{type=\"attention\" title=\"Important\"}
    Lambda doesn't store your private key after it's been generated.
    If you generate a new key pair, make sure to save the resulting private key locally.
    :::

    For example, to generate a new key pair and associate it with a Lambda
    On-Demand Cloud instance:

    1. Generate the key pair. The command provided below automatically extracts and
        saves the returned private key to a new file called `key.pem`. Replace
        `<NEW-KEY-NAME>` with the name you want to assign to the SSH key:

        ```bash
        curl --request POST --url 'https://cloud.lambda.ai/api/v1/ssh-keys' \
        --fail \
        --user ${LAMBDA_API_KEY}: \
        --data '{\"name\": \"<NEW-KEY-NAME>\"}' \
        | jq -r '.data.private_key' > key.pem
        ```

    2. Next, set the private key's permissions to read-only:

        ```bash
        chmod 400 key.pem
        ```

    3. Launch a new instance. Replace `<NEW-KEY-NAME>` with the name you assigned
       to your SSH key.

        ```bash
        curl --request POST 'https://cloud.lambda.ai/api/v1/instance-operations/launch' \
        --fail \
        --user ${LAMBDA_API_KEY}: \
        --data '{\"region_name\":\"us-
    west-1\",\"instance_type_name\":\"gpu_1x_a10\",\"ssh_key_names\":[\"<NEW-KEY-
    NAME>\"],\"file_system_names\":[],\"quantity\":1,\"name\":\"My Instance\"}'
        ```

    4. From your local terminal, establish an SSH connection to the instance.
       Replace `<INSTANCE-IP>` with the public IP of the instance:

        ```bash
        ssh -i key.pem <INSTANCE-IP>
        ```

    Args:
        body (AddSSHKeyRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AddSSHKeyResponse200 | AddSSHKeyResponse400 | AddSSHKeyResponse401 | AddSSHKeyResponse403
     """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: AddSSHKeyRequest,
) -> Response[AddSSHKeyResponse200 | AddSSHKeyResponse400 | AddSSHKeyResponse401 | AddSSHKeyResponse403]:
    r""" Add an SSH key

     
    Add an SSH key to your Lambda Cloud account. You can upload an existing public
    key, or you can generate a new key pair.

    -  To use an existing key pair, set the `public_key` property in the request body
       to your public key.

    -  To generate a new key pair, omit the `public_key` property from the request
       body.

    :::note{type=\"attention\" title=\"Important\"}
    Lambda doesn't store your private key after it's been generated.
    If you generate a new key pair, make sure to save the resulting private key locally.
    :::

    For example, to generate a new key pair and associate it with a Lambda
    On-Demand Cloud instance:

    1. Generate the key pair. The command provided below automatically extracts and
        saves the returned private key to a new file called `key.pem`. Replace
        `<NEW-KEY-NAME>` with the name you want to assign to the SSH key:

        ```bash
        curl --request POST --url 'https://cloud.lambda.ai/api/v1/ssh-keys' \
        --fail \
        --user ${LAMBDA_API_KEY}: \
        --data '{\"name\": \"<NEW-KEY-NAME>\"}' \
        | jq -r '.data.private_key' > key.pem
        ```

    2. Next, set the private key's permissions to read-only:

        ```bash
        chmod 400 key.pem
        ```

    3. Launch a new instance. Replace `<NEW-KEY-NAME>` with the name you assigned
       to your SSH key.

        ```bash
        curl --request POST 'https://cloud.lambda.ai/api/v1/instance-operations/launch' \
        --fail \
        --user ${LAMBDA_API_KEY}: \
        --data '{\"region_name\":\"us-
    west-1\",\"instance_type_name\":\"gpu_1x_a10\",\"ssh_key_names\":[\"<NEW-KEY-
    NAME>\"],\"file_system_names\":[],\"quantity\":1,\"name\":\"My Instance\"}'
        ```

    4. From your local terminal, establish an SSH connection to the instance.
       Replace `<INSTANCE-IP>` with the public IP of the instance:

        ```bash
        ssh -i key.pem <INSTANCE-IP>
        ```

    Args:
        body (AddSSHKeyRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AddSSHKeyResponse200 | AddSSHKeyResponse400 | AddSSHKeyResponse401 | AddSSHKeyResponse403]
     """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: AddSSHKeyRequest,
) -> AddSSHKeyResponse200 | AddSSHKeyResponse400 | AddSSHKeyResponse401 | AddSSHKeyResponse403 | None:
    r""" Add an SSH key

     
    Add an SSH key to your Lambda Cloud account. You can upload an existing public
    key, or you can generate a new key pair.

    -  To use an existing key pair, set the `public_key` property in the request body
       to your public key.

    -  To generate a new key pair, omit the `public_key` property from the request
       body.

    :::note{type=\"attention\" title=\"Important\"}
    Lambda doesn't store your private key after it's been generated.
    If you generate a new key pair, make sure to save the resulting private key locally.
    :::

    For example, to generate a new key pair and associate it with a Lambda
    On-Demand Cloud instance:

    1. Generate the key pair. The command provided below automatically extracts and
        saves the returned private key to a new file called `key.pem`. Replace
        `<NEW-KEY-NAME>` with the name you want to assign to the SSH key:

        ```bash
        curl --request POST --url 'https://cloud.lambda.ai/api/v1/ssh-keys' \
        --fail \
        --user ${LAMBDA_API_KEY}: \
        --data '{\"name\": \"<NEW-KEY-NAME>\"}' \
        | jq -r '.data.private_key' > key.pem
        ```

    2. Next, set the private key's permissions to read-only:

        ```bash
        chmod 400 key.pem
        ```

    3. Launch a new instance. Replace `<NEW-KEY-NAME>` with the name you assigned
       to your SSH key.

        ```bash
        curl --request POST 'https://cloud.lambda.ai/api/v1/instance-operations/launch' \
        --fail \
        --user ${LAMBDA_API_KEY}: \
        --data '{\"region_name\":\"us-
    west-1\",\"instance_type_name\":\"gpu_1x_a10\",\"ssh_key_names\":[\"<NEW-KEY-
    NAME>\"],\"file_system_names\":[],\"quantity\":1,\"name\":\"My Instance\"}'
        ```

    4. From your local terminal, establish an SSH connection to the instance.
       Replace `<INSTANCE-IP>` with the public IP of the instance:

        ```bash
        ssh -i key.pem <INSTANCE-IP>
        ```

    Args:
        body (AddSSHKeyRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AddSSHKeyResponse200 | AddSSHKeyResponse400 | AddSSHKeyResponse401 | AddSSHKeyResponse403
     """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed

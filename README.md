# Lambda Cloud API - CLI

This project is a wrapper around the Lambda Cloud API with some additional Quality-of-Life additions.
The documentation of the API can be found here: https://docs-api.lambda.ai/api/cloud

## Installation

```bash
uv pip install lambda-ai-cloud-api-client
```

## Usage

1. Set up an API token and environment.

In your lambda.ai account go to https://cloud.lambda.ai/api-keys/cloud-api and generate a new Cloud AI Key.
Set this token as an environment variable in the terminal you've installed this project.

```bash
export LAMBDA_CLOUD_API_TOKEN=<your-token>
```
The project also accepts `LAMBDA_CLOUD_TOKEN` and `LAMBDA_API_TOKEN` if you prefer that naming.
Optionally you can set the api base url, `LAMBDA_CLOUD_BASE_URL`, the default is https://cloud.lambdalabs.com .

2. Using the CLI

To save on keystrokes I've named the command `lai` for lambda.ai. To see all available commands use:

```bash
lai --help
```

## Overview of features

- List instances: `lai ls`
- Get instance details: `lai get <instance-id>`
- Start an instance: `lai start --region us-east-1 --instance-type gpu_1x_a10 --ssh-key my-key --name demo`
- Start with filters (auto-selects type/region when narrowed to one): `lai start --available --cheapest --gpu H100 --ssh-key my-key`
- Dry run start resolution without launching: `lai start --dry-run --available --gpu H100 --ssh-key my-key`
- SSH into an instance by name or id (waits for IP and SSH availability): `lai ssh <name-or-id>`
- Stop instances: `lai stop <id-1> <id-2>`
- Restart instances: `lai restart <id-1> <id-2>`
- Rename an instance: `lai rename <instance-id> new-name`
- List instance types: `lai types --available --cheapest --region us-east-1`
  - --available shows only those instance types that are currently available
  - --cheapest finds the instance-type that is currently the cheapest $ per hour.
- List available images: `lai images --region us-east-1`
- List SSH keys: `lai keys`

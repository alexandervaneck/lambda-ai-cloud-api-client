# Lambda Cloud API - CLI

This repo contains the generated Python client for the Lambda Cloud API and a lightweight CLI wrapper so you can call it
directly from your terminal. The documentation for the api can be found here: https:/docs-api.lambda.ai/api/cloud

## Running the CLI locally

1. Set your API token via `LAMBDA_CLOUD_TOKEN` (or `LAMBDA_CLOUD_API_TOKEN` / `LAMBDA_API_TOKEN`), optionally
   `LAMBDA_CLOUD_BASE_URL` if you use a non-default endpoint.
2. Install this CLI: `uv pip install lambda-ai-cloud-api-client`.
3. Run commands: `lambda-ai <command> ...`

Examples:

- List instance types: `lambda-ai instance-types` (add `--available-only` to show only types with capacity, `--cheapest` to filter to the lowest price)
- List images: `lambda-ai images`
- List SSH keys: `lambda-ai ssh-keys`
- List instances: `lambda-ai instances ls`
- Shortcut table view: `lambda-ai ls` (renders a table; supports `--region` multiple times)
- Get one instance: `lambda-ai instances get <instance-id>`
- Launch an instance:
  `lambda-ai instances launch --region us-east-1 --instance-type gpu_1x_a10 --ssh-key my-key --name demo`
- Terminate instances: `lambda-ai instances terminate <id-1> <id-2>`

Flags:

- `--token` to override the token (instead of env vars)
- `--base-url` to target a specific control plane (defaults to `https://cloud.lambdalabs.com`)
- `--insecure` to skip TLS verification (only for debugging)

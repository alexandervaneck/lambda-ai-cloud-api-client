import sys
from types import SimpleNamespace

from rich.console import Console
from rich.table import Table

from lambda_ai_cloud_api_client.api.images.list_images import sync_detailed as _list_images
from lambda_ai_cloud_api_client.cli.client import auth_client
from lambda_ai_cloud_api_client.cli.response import print_response
from lambda_ai_cloud_api_client.models import ListImagesResponse200
from lambda_ai_cloud_api_client.types import Response


def list_images(args: SimpleNamespace) -> Response[ListImagesResponse200]:
    client = auth_client(base_url=args.base_url, token=args.token, insecure=args.insecure)
    images: Response[ListImagesResponse200] = _list_images(client=client)
    return images


def filter_images(response: Response[ListImagesResponse200], args: SimpleNamespace) -> Response[ListImagesResponse200]:
    if response.parsed and hasattr(response.parsed, "data"):
        filtered = response.parsed.data
        if args.family:
            allowed_family = set(args.family)
            filtered = [img for img in filtered if getattr(img, "family", None) in allowed_family]
        if args.version:
            allowed_version = set(args.version)
            filtered = [img for img in filtered if getattr(img, "version", None) in allowed_version]
        if args.arch:
            allowed_arch = set(args.arch)
            filtered = [img for img in filtered if getattr(img, "architecture", None) in allowed_arch]
        if args.region:
            allowed = set(args.region)
            filtered = [img for img in filtered if getattr(getattr(img, "region", None), "name", None) in allowed]

        response.parsed.data = filtered  # type: ignore[attr-defined]

    return response


def render_images_table(response) -> None:
    status = int(response.status_code)
    if status < 200 or status >= 300 or response.parsed is None:
        print_response(response)
        sys.exit(1)

    parsed = response.parsed
    images = getattr(parsed, "data", None)
    if not images:
        Console().print("No images found.")
        return

    table = Table(title="Images", show_lines=False, expand=True)
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Family")
    table.add_column("Version")
    table.add_column("Arch")
    table.add_column("Region")

    sorted_images = sorted(
        images,
        key=lambda img: (
            getattr(getattr(img, "region", None), "name", "") or "",
            getattr(img, "version", "") or "",
        ),
    )

    for img in sorted_images:
        region = getattr(img, "region", None)
        table.add_row(
            getattr(img, "id", ""),
            getattr(img, "name", ""),
            getattr(img, "family", ""),
            getattr(img, "version", ""),
            getattr(img, "architecture", ""),
            getattr(region, "name", "") if region else "",
        )

    Console().print(table)

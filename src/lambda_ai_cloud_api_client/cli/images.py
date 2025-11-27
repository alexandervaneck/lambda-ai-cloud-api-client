from rich import print
from rich.table import Table

from lambda_ai_cloud_api_client.api.images.list_images import sync_detailed as _list_images
from lambda_ai_cloud_api_client.cli.client import auth_client
from lambda_ai_cloud_api_client.models import Image


def list_images() -> list[Image]:
    client = auth_client()
    response = _list_images(client=client)
    response.raise_for_status()
    return response.parsed.data


def filter_images(
    images: list[Image],
    family: tuple[str, ...] | None = None,
    version: tuple[str, ...] | None = None,
    arch: tuple[str, ...] | None = None,
    region: tuple[str, ...] | None = None,
) -> list[Image]:
    filtered_images = []
    for image in images:
        if family and image.family not in family:
            continue
        if version and image.version not in version:
            continue
        if arch and image.architecture.value not in arch:
            continue
        if region and image.region.name not in region:
            continue
        filtered_images.append(image)
    return filtered_images


def render_images_table(images: list[Image]) -> None:
    if not images:
        print("No images found.")
        return

    table = Table(title="Images", show_lines=False, expand=True)
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Family")
    table.add_column("Version")
    table.add_column("Arch")
    table.add_column("Region")

    sorted_images = sorted(images, key=lambda image: (image.region.name, image.version))

    for image in sorted_images:
        table.add_row(
            image.id,
            image.name,
            image.family,
            image.version,
            image.architecture.value,
            image.region.name,
        )

    print(table)

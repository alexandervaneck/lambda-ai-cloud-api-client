import sys
from types import SimpleNamespace

from rich.console import Console
from rich.table import Table

from lambda_ai_cloud_api_client.api.instances.list_instance_types import sync_detailed as _list_instance_types
from lambda_ai_cloud_api_client.cli.client import auth_client
from lambda_ai_cloud_api_client.cli.response import print_response
from lambda_ai_cloud_api_client.models import ListInstanceTypesResponse200
from lambda_ai_cloud_api_client.types import Response


def list_instance_types(args: SimpleNamespace) -> Response[ListInstanceTypesResponse200]:
    client = auth_client(args)
    r: Response[ListInstanceTypesResponse200] = _list_instance_types(client=client)
    return r


def filter_instance_types(
    response: Response[ListInstanceTypesResponse200], args: SimpleNamespace
) -> Response[ListInstanceTypesResponse200]:
    parsed = response.parsed
    target = getattr(parsed, "data", parsed if hasattr(parsed, "additional_properties") else None)
    if not target or not hasattr(target, "additional_properties"):
        return response

    items = dict(target.additional_properties)

    if args.available:
        items = {name: item for name, item in items.items() if item.regions_with_capacity_available}

    if args.region:
        allowed_regions = set(args.region)
        items = {
            name: item
            for name, item in items.items()
            if any(getattr(reg, "name", None) in allowed_regions for reg in item.regions_with_capacity_available)
        }

    if args.gpu:
        items = {
            name: item
            for name, item in items.items()
            if getattr(getattr(item, "instance_type", None), "gpu_description", None)
            and any(term.lower() in getattr(item.instance_type, "gpu_description", "").lower() for term in args.gpu)
        }

    if args.min_gpus is not None:
        items = {
            name: item
            for name, item in items.items()
            if getattr(getattr(getattr(item, "instance_type", None), "specs", None), "gpus", 0) >= args.min_gpus
        }

    if args.min_vcpus is not None:
        items = {
            name: item
            for name, item in items.items()
            if getattr(getattr(getattr(item, "instance_type", None), "specs", None), "vcpus", 0) >= args.min_vcpus
        }

    if args.min_memory is not None:
        items = {
            name: item
            for name, item in items.items()
            if getattr(getattr(getattr(item, "instance_type", None), "specs", None), "memory_gib", 0) >= args.min_memory
        }

    if args.min_storage is not None:
        items = {
            name: item
            for name, item in items.items()
            if getattr(getattr(getattr(item, "instance_type", None), "specs", None), "storage_gib", 0)
            >= args.min_storage
        }

    if args.max_price is not None:
        items = {
            name: item
            for name, item in items.items()
            if getattr(getattr(item, "instance_type", None), "price_cents_per_hour", 0) <= args.max_price * 100
        }

    if args.cheapest and items:
        prices: dict[str, int] = {}
        for name, item in items.items():
            price = getattr(item, "instance_type", None).price_cents_per_hour
            prices[name] = price

        min_price = min(prices.values())
        items = {name: item for name, item in items.items() if prices.get(name) == min_price}

    response.parsed.data.additional_properties = items  # type: ignore[attr-defined]

    return response


def render_types_table(response: Response[ListInstanceTypesResponse200]) -> None:
    status = int(response.status_code)
    if status < 200 or status >= 300 or response.parsed is None:
        print_response(response)
        sys.exit(1)

    parsed = response.parsed
    types = getattr(parsed, "data", parsed if hasattr(parsed, "additional_properties") else None)
    if not types.to_dict() or not hasattr(types, "additional_properties"):
        Console().print("No instance types found.")
        return

    table = Table(title="Instance Types", show_lines=False)
    table.add_column("Name")
    table.add_column("GPU")
    table.add_column("vCPUs")
    table.add_column("Memory (GiB)")
    table.add_column("Storage (GiB)")
    table.add_column("GPUs")
    table.add_column("Price ($/hr)")
    table.add_column("Regions w/ Capacity")

    for name, item in types.additional_properties.items():
        inst_type = getattr(item, "instance_type", None)
        specs = getattr(inst_type, "specs", None)
        regions = ", ".join([getattr(r, "name", "") for r in item.regions_with_capacity_available]) or "-"
        price = getattr(inst_type, "price_cents_per_hour", 0) / 100
        table.add_row(
            name,
            getattr(inst_type, "gpu_description", "") or "",
            str(getattr(specs, "vcpus", "")),
            str(getattr(specs, "memory_gib", "")),
            str(getattr(specs, "storage_gib", "")),
            str(getattr(specs, "gpus", "")),
            f"{price:.2f}",
            regions,
        )

    Console().print(table)

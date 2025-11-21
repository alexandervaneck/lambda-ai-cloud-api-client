import json
import os
from collections.abc import Callable
from pathlib import Path

import pytest
from click.testing import Result

from lambda_ai_cloud_api_client.cli.client import DEFAULT_BASE_URL

DATA_FOLDER = Path(__file__).parent.parent / "data"
UPDATE_EXPECTED_DATA = os.environ.get("UPDATE_EXPECTED_DATA", "false").lower() == "true"


@pytest.fixture
def m_response() -> dict:
    f = DATA_FOLDER / "m_instance_types_response.json"
    return json.loads(f.read_text())


@pytest.mark.parametrize(
    "kwargs",
    (
        {},
        {"available": None},
        {"cheapest": None},
        {"region": "us-east-1"},
        {"gpu": "A10"},
        {"min-gpus": "2"},
        {"min-vcpus": "31"},
        {"min-memory": "500"},
        {"min-storage": "1000"},
        {"max-price": "1.00"},
        {"json": None},
    ),
    ids=(
        "",
        "available",
        "cheapest",
        "region",
        "gpu",
        "min-gpus",
        "min-vcpus",
        "min-memory",
        "min-storage",
        "max-price",
        "json",
    ),
)
def test_types(
    request,
    httpx_mock,
    m_response: dict,
    kwargs: dict,
    c_assert_cmd_kwargs_result_equals: Callable[[list[str], dict[str, str], Path], Result],
) -> None:
    # Arrange
    param_id = request.node.callspec.id
    httpx_mock.add_response(method="GET", url=f"{DEFAULT_BASE_URL}/api/v1/instance-types", json=m_response)
    # Act & Assert
    suffix = f"_{param_id}" if param_id else ""
    c_assert_cmd_kwargs_result_equals(["types"], kwargs, DATA_FOLDER / f"expected_types_output{suffix}.txt")


def test_types_empty(httpx_mock, c_assert_cmd_results_equals: Callable[[list[str], Path, int], Result]) -> None:
    # Arrange
    httpx_mock.add_response(
        method="GET", url=f"{DEFAULT_BASE_URL}/api/v1/instance-types", status_code=200, json={"data": {}}
    )
    # Act & Assert
    c_assert_cmd_results_equals(["types"], DATA_FOLDER / "expected_types_output_empty.txt")


def test_types_error(httpx_mock, c_assert_cmd_results_equals: Callable[[list[str], Path, int], Result]) -> None:
    # Arrange
    httpx_mock.add_response(method="GET", url=f"{DEFAULT_BASE_URL}/api/v1/instance-types", status_code=500, json={})
    # Act & Assert
    c_assert_cmd_results_equals(["types"], DATA_FOLDER / "expected_types_output_error.txt", expected_exit_code=1)

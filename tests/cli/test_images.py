import json
from collections.abc import Callable
from pathlib import Path

import pytest
from click.testing import Result

from lambda_ai_cloud_api_client.cli.client import DEFAULT_BASE_URL

DATA_FOLDER = Path(__file__).parent.parent / "data"


@pytest.fixture
def m_response() -> dict:
    f = DATA_FOLDER / "m_images_response.json"
    return json.loads(f.read_text())


@pytest.mark.parametrize(
    "kwargs",
    (
        {},
        {"region": "us-east-1"},
        {"arch": "arm64"},
        {"family": "lambda-stack-22-04"},
        {"version": "22.4.5-1459"},
        {"version": "22.4.5-1459", "family": "lambda-stack-22-04", "arch": "arm64"},
        {"json": None},
    ),
    ids=(
        "",
        "region",
        "arch",
        "family",
        "version",
        "combination",
        "json",
    ),
)
def test_images(
    request,
    httpx_mock,
    m_response: dict,
    kwargs: dict[str, str],
    c_assert_cmd_kwargs_result_equals: Callable[[list[str], dict[str, str], Path], Result],
) -> None:
    # Arrange
    param_id = request.node.callspec.id
    httpx_mock.add_response(method="GET", url=f"{DEFAULT_BASE_URL}/api/v1/images", json=m_response)
    # Act & Assert
    suffix = f"_{param_id}" if param_id else ""
    c_assert_cmd_kwargs_result_equals(["images"], kwargs, DATA_FOLDER / f"expected_images_output{suffix}.txt")


def test_images_empty(httpx_mock, c_assert_cmd_results_equals: Callable[[list[str], Path, int], Result]) -> None:
    # Arrange
    httpx_mock.add_response(method="GET", url=f"{DEFAULT_BASE_URL}/api/v1/images", status_code=200, json={"data": []})
    # Act & Assert
    c_assert_cmd_results_equals(["images"], DATA_FOLDER / "expected_images_output_empty.txt")


def test_images_error(httpx_mock, c_assert_cmd_results_equals: Callable[[list[str], Path, int], Result]) -> None:
    # Arrange
    httpx_mock.add_response(method="GET", url=f"{DEFAULT_BASE_URL}/api/v1/images", status_code=500, json={})
    # Act & Assert
    c_assert_cmd_results_equals(["images"], DATA_FOLDER / "expected_images_output_error.txt", expected_exit_code=1)

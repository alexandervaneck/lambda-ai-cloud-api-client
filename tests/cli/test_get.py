import json
from collections.abc import Callable
from pathlib import Path

import pytest
from click.testing import Result

from lambda_ai_cloud_api_client.cli.client import DEFAULT_BASE_URL

DATA_FOLDER = Path(__file__).parent.parent / "data"


@pytest.fixture
def m_response() -> dict:
    f = DATA_FOLDER / "m_instance_get_response.json"
    return json.loads(f.read_text())


def test_get_by_id(
    httpx_mock,
    m_response: dict,
    c_assert_cmd_results_equals: Callable[[list[str], Path], Result],
) -> None:
    # Arrange
    httpx_mock.add_response(
        method="GET",
        url=f"{DEFAULT_BASE_URL}/api/v1/instances",
        json=json.loads((DATA_FOLDER / "m_instances_response.json").read_text()),
    )
    httpx_mock.add_response(
        method="GET", url=f"{DEFAULT_BASE_URL}/api/v1/instances/0920582c7ff041399e34823a0be62549", json=m_response
    )
    cmd = ["get", "0920582c7ff041399e34823a0be62549"]

    # Act & Assert
    c_assert_cmd_results_equals(cmd, DATA_FOLDER / "expected_get_output_id.txt")


def test_get_by_name(
    httpx_mock,
    m_response: dict,
    c_assert_cmd_results_equals: Callable[[list[str], Path], Result],
) -> None:
    # Arrange
    httpx_mock.add_response(
        method="GET",
        url=f"{DEFAULT_BASE_URL}/api/v1/instances",
        json=json.loads((DATA_FOLDER / "m_instances_response.json").read_text()),
    )
    httpx_mock.add_response(
        method="GET", url=f"{DEFAULT_BASE_URL}/api/v1/instances/0920582c7ff041399e34823a0be62549", json=m_response
    )
    cmd = ["get", "My Instance"]

    # Act & Assert
    c_assert_cmd_results_equals(cmd, DATA_FOLDER / "expected_get_output_name.txt")


def test_get_error(httpx_mock, c_assert_cmd_results_equals: Callable[[list[str], Path, int], Result]) -> None:
    # Arrange
    httpx_mock.add_response(
        method="GET",
        url=f"{DEFAULT_BASE_URL}/api/v1/instances",
        json=json.loads((DATA_FOLDER / "m_instances_response.json").read_text()),
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{DEFAULT_BASE_URL}/api/v1/instances/0920582c7ff041399e34823a0be62549",
        status_code=500,
        json={},
    )
    cmd = ["get", "0920582c7ff041399e34823a0be62549"]
    # Act & Assert
    c_assert_cmd_results_equals(cmd, DATA_FOLDER / "expected_get_output_error.txt", 1)

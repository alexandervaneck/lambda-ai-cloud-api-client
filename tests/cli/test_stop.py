import json
from collections.abc import Callable
from pathlib import Path

import pytest
from click.testing import Result

from lambda_ai_cloud_api_client.cli.client import DEFAULT_BASE_URL

DATA_FOLDER = Path(__file__).parent.parent / "data"


@pytest.fixture
def m_response() -> dict:
    f = DATA_FOLDER / "m_stop_response.json"
    return json.loads(f.read_text())


def test_stop(
    httpx_mock,
    m_response: dict,
    c_assert_cmd_results_equals: Callable[[list[str], Path], Result],
) -> None:
    # Arrange
    httpx_mock.add_response(
        method="POST",
        url=f"{DEFAULT_BASE_URL}/api/v1/instance-operations/terminate",
        match_json={"instance_ids": ["0920582c7ff041399e34823a0be62549"]},
        json=m_response,
    )
    cmd = ["stop", "0920582c7ff041399e34823a0be62549"]

    # Act & Assert
    c_assert_cmd_results_equals(cmd, DATA_FOLDER / "expected_stop_output.txt")


def test_stop_error(httpx_mock, c_assert_cmd_results_equals: Callable[[list[str], Path, int], Result]) -> None:
    # Arrange
    httpx_mock.add_response(
        method="POST",
        url=f"{DEFAULT_BASE_URL}/api/v1/instance-operations/terminate",
        match_json={"instance_ids": ["0920582c7ff041399e34823a0be62549"]},
        status_code=500,
        json={},
    )
    cmd = ["stop", "0920582c7ff041399e34823a0be62549"]
    # Act & Assert
    c_assert_cmd_results_equals(cmd, DATA_FOLDER / "expected_stop_output_error.txt", 1)

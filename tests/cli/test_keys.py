import json
from collections.abc import Callable
from pathlib import Path

import pytest
from click.testing import Result

from lambda_ai_cloud_api_client.cli.client import DEFAULT_BASE_URL

DATA_FOLDER = Path(__file__).parent.parent / "data"


@pytest.fixture
def m_response() -> dict:
    f = DATA_FOLDER / "m_ssh_keys_response.json"
    return json.loads(f.read_text())


@pytest.mark.parametrize(
    "kwargs",
    (
        {},
        {"name": "yubikey"},
        {"id": "d02cb1eda8d4s47a927ebc5da267s9a4"},
        {"json": None},
    ),
    ids=(
        "",
        "name",
        "id",
        "json",
    ),
)
def test_keys(
    request,
    httpx_mock,
    m_response: dict,
    kwargs: dict[str, str],
    c_assert_cmd_kwargs_result_equals: Callable[[list[str], dict[str, str], Path], Result],
) -> None:
    # Arrange
    param_id = request.node.callspec.id
    httpx_mock.add_response(method="GET", url=f"{DEFAULT_BASE_URL}/api/v1/ssh-keys", json=m_response)
    # Act & Assert
    suffix = f"_{param_id}" if param_id else ""
    c_assert_cmd_kwargs_result_equals(["keys"], kwargs, DATA_FOLDER / f"expected_keys_output{suffix}.txt")


def test_key_empty(httpx_mock, c_assert_cmd_results_equals: Callable[[list[str], Path, int], Result]) -> None:
    # Arrange
    httpx_mock.add_response(method="GET", url=f"{DEFAULT_BASE_URL}/api/v1/ssh-keys", status_code=200, json={"data": []})
    # Act & Assert
    c_assert_cmd_results_equals(["keys"], DATA_FOLDER / "expected_keys_output_empty.txt")


def test_key_error(httpx_mock, c_assert_cmd_results_equals: Callable[[list[str], Path, int], Result]) -> None:
    # Arrange
    httpx_mock.add_response(method="GET", url=f"{DEFAULT_BASE_URL}/api/v1/ssh-keys", status_code=500, json={"data": []})
    # Act & Assert
    c_assert_cmd_results_equals(["keys"], DATA_FOLDER / "expected_keys_output_error.txt", 1)

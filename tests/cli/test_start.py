import json
from collections.abc import Callable
from pathlib import Path

import pytest
from click.testing import Result

from lambda_ai_cloud_api_client.cli.client import DEFAULT_BASE_URL

DATA_FOLDER = Path(__file__).parent.parent / "data"
REQUIRED_KWARGS = {
    "region": "us-east-1",
    "instance-type": "gpu_1x_a100",
    "ssh-key": "default-key",
}


@pytest.fixture
def m_response() -> dict:
    f = DATA_FOLDER / "m_start_response.json"
    return json.loads(f.read_text())


@pytest.mark.parametrize(
    "kwargs",
    (
        {},
        {"name": "demo-instance", "hostname": "demo-host", "filesystem": "demo-fs", "tag": "env=dev"},
        {"image-id": "l4-stack-123"},
        {"image-family": "lambda-stack-22-04", "user-data-file": "user-data.txt"},
        {"json": None},
    ),
    ids=(
        "",
        "with-metadata",
        "image-id",
        "image-family",
        "json",
    ),
)
def test_start(
    request,
    httpx_mock,
    m_response: dict,
    kwargs: dict[str, str],
    tmp_path: Path,
    c_assert_cmd_kwargs_result_equals: Callable[[list[str], dict[str, str], Path], Result],
) -> None:
    # Arrange
    param_id = request.node.callspec.id
    httpx_mock.add_response(method="POST", url=f"{DEFAULT_BASE_URL}/api/v1/instance-operations/launch", json=m_response)
    kwargs = {**REQUIRED_KWARGS, **kwargs}
    if user_data := kwargs.get("user-data-file"):
        user_data_path = tmp_path / user_data
        user_data_path.write_text("#cloud-config\n")
        kwargs["user-data-file"] = str(user_data_path)
    # Act & Assert
    suffix = f"_{param_id}" if param_id else ""
    c_assert_cmd_kwargs_result_equals(["start"], kwargs, DATA_FOLDER / f"expected_start_output{suffix}.txt")


def test_start_error(httpx_mock, c_assert_cmd_results_equals: Callable[[list[str], Path, int], Result]) -> None:
    # Arrange
    httpx_mock.add_response(
        method="POST", url=f"{DEFAULT_BASE_URL}/api/v1/instance-operations/launch", status_code=500, json={}
    )
    # Act & Assert
    cmd = [
        "start",
        "--region",
        REQUIRED_KWARGS["region"],
        "--instance-type",
        REQUIRED_KWARGS["instance-type"],
        "--ssh-key",
        REQUIRED_KWARGS["ssh-key"],
    ]
    c_assert_cmd_results_equals(cmd, DATA_FOLDER / "expected_start_output_error.txt", expected_exit_code=1)

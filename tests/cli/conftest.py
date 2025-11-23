import json
import os
from collections.abc import Callable, Iterable
from contextlib import nullcontext
from pathlib import Path

import pytest
from click.testing import CliRunner, Result

from lambda_ai_cloud_api_client import __main__ as cli
from lambda_ai_cloud_api_client.cli.client import DEFAULT_BASE_URL

DATA_FOLDER = Path(__file__).parent.parent / "data"
UPDATE_EXPECTED_DATA = os.environ.get("UPDATE_EXPECTED_DATA", "false").lower() == "true"


@pytest.fixture
def f_cli_runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def c_assert_cmd_results_equals(f_cli_runner: CliRunner) -> Callable[[list[str], Path, int | None], Result]:
    def _(command: Iterable[str], expected_file: Path, expected_exit_code: int = 0) -> Result:
        result = f_cli_runner.invoke(cli.main, command, env={"COLUMNS": "170", "LINES": "50"})

        assert result.exit_code == expected_exit_code, result.output
        if UPDATE_EXPECTED_DATA:
            expected_file.write_text(result.output)
        expected = expected_file.read_text()
        assert result.output == expected
        return result

    return _


@pytest.fixture
def c_assert_cmd_kwargs_result_equals(
    c_assert_cmd_results_equals: Callable[[tuple[str], Path], Result],
) -> Callable[[list[str], dict[str, str], Path], Result]:
    def _(command: list[str], kwargs: dict[str, str], expected: Path) -> Result:
        for k, v in kwargs.items():
            command.append(f"--{k}")
            if v is not None:
                command.append(v)

        return c_assert_cmd_results_equals(command, expected)

    return _


@pytest.fixture
def m_wait_for_ip(httpx_mock):
    # list instances returns one instance without an IP yet
    m_instances = json.loads((DATA_FOLDER / "m_instances_response.json").read_text())
    m_instances["data"][0].pop("ip", None)
    httpx_mock.add_response(method="GET", url=f"{DEFAULT_BASE_URL}/api/v1/instances", json=m_instances)

    # Subsequent get-instance polls: two without IP, then one with IP.
    instance_id = m_instances["data"][0]["id"]
    no_ip = {"data": dict(m_instances["data"][0])}
    no_ip["data"].pop("ip", None)
    with_ip = json.loads((DATA_FOLDER / "m_instance_get_response.json").read_text())
    httpx_mock.add_response(method="GET", url=f"{DEFAULT_BASE_URL}/api/v1/instances/{instance_id}", json=no_ip)
    httpx_mock.add_response(method="GET", url=f"{DEFAULT_BASE_URL}/api/v1/instances/{instance_id}", json=no_ip)
    httpx_mock.add_response(method="GET", url=f"{DEFAULT_BASE_URL}/api/v1/instances/{instance_id}", json=with_ip)


@pytest.fixture
def m_wait_for_ssh(monkeypatch):
    # Simulate SSH port not yet open, then available.
    attempts = {"count": 0}

    def _fake_create_connection(addr, timeout=None):
        attempts["count"] += 1
        if attempts["count"] < 2:
            raise OSError("connection refused")
        return nullcontext()

    monkeypatch.setattr("lambda_ai_cloud_api_client.cli.ssh.socket.create_connection", _fake_create_connection)
    monkeypatch.setattr("lambda_ai_cloud_api_client.cli.ssh.time.sleep", lambda *_args, **_kwargs: None)

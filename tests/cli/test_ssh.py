import json
from collections.abc import Callable
from pathlib import Path

import pytest
from click.testing import Result

from lambda_ai_cloud_api_client.cli.client import DEFAULT_BASE_URL

DATA_FOLDER = Path(__file__).parent.parent / "data"


def test_ssh_waits_for_port_then_execs(
    monkeypatch,
    c_assert_cmd_results_equals: Callable[[list[str], Path], Result],
    m_wait_for_ip,
    m_wait_for_ssh,
) -> None:
    captured_execvp: dict[str, tuple[str, list[str]]] = {}

    def _fake_execvp(file, args):
        captured_execvp["call"] = (file, args)
        return None

    monkeypatch.setattr("lambda_ai_cloud_api_client.cli.ssh.os.execvp", _fake_execvp)

    # Assert
    c_assert_cmd_results_equals(["ssh", "My Instance"], DATA_FOLDER / "expected_ssh_output.txt")
    assert captured_execvp["call"] == (
        "ssh",
        [
            "ssh",
            "-o",
            "StrictHostKeyChecking=accept-new",
            "-o",
            "UserKnownHostsFile=/dev/null",
            "ubuntu@198.51.100.2",
        ],
    )


@pytest.fixture
def m_wait_forever_ip(httpx_mock):
    # list instances returns one instance without an IP yet
    m_instances = json.loads((DATA_FOLDER / "m_instances_response.json").read_text())
    m_instances["data"][0].pop("ip", None)
    httpx_mock.add_response(method="GET", url=f"{DEFAULT_BASE_URL}/api/v1/instances", json=m_instances)

    # Subsequent get-instance polls: two without IP, then one with IP.
    instance_id = m_instances["data"][0]["id"]
    no_ip = {"data": dict(m_instances["data"][0])}
    httpx_mock.add_response(
        method="GET", url=f"{DEFAULT_BASE_URL}/api/v1/instances/{instance_id}", json=no_ip, is_reusable=True
    )


def test_ip_never_gets_assigned(
    c_assert_cmd_results_equals: Callable[[list[str], Path], Result],
    m_wait_forever_ip,
) -> None:
    # Assert
    c_assert_cmd_results_equals(
        ["ssh", "My Instance", "--timeout-seconds", "0.1"], DATA_FOLDER / "expected_ssh_ip_error_output.txt"
    )


@pytest.fixture
def m_wait_forever_ssh(monkeypatch):
    def _fake_create_connection(addr, timeout=None):
        raise OSError("connection refused")

    monkeypatch.setattr("lambda_ai_cloud_api_client.cli.ssh.socket.create_connection", _fake_create_connection)


def test_ssh_port_never_available(
    c_assert_cmd_results_equals: Callable[[list[str], Path], Result],
    m_wait_for_ip,
    m_wait_forever_ssh,
) -> None:
    # Assert
    c_assert_cmd_results_equals(
        ["ssh", "My Instance", "--timeout-seconds", "0.1", "--interval-seconds", "0.05"],
        DATA_FOLDER / "expected_ssh_connect_error_output.txt",
    )

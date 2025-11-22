import json
from collections.abc import Callable
from contextlib import nullcontext
from pathlib import Path

from click.testing import Result

from lambda_ai_cloud_api_client.cli.client import DEFAULT_BASE_URL

DATA_FOLDER = Path(__file__).parent.parent / "data"


def test_ssh_waits_for_port_then_execs(
    monkeypatch,
    httpx_mock,
    c_assert_cmd_results_equals: Callable[[list[str], Path], Result],
) -> None:
    # Arrange: list instances returns one instance without an IP yet
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

    # Simulate SSH port not yet open, then available.
    attempts = {"count": 0}

    def _fake_create_connection(addr, timeout=None):
        attempts["count"] += 1
        if attempts["count"] < 2:
            raise OSError("connection refused")
        return nullcontext()

    captured_execvp: dict[str, tuple[str, list[str]]] = {}

    def _fake_execvp(file, args):
        captured_execvp["call"] = (file, args)
        return None

    monkeypatch.setattr("lambda_ai_cloud_api_client.cli.ssh.socket.create_connection", _fake_create_connection)
    monkeypatch.setattr("lambda_ai_cloud_api_client.cli.ssh.time.sleep", lambda *_args, **_kwargs: None)
    monkeypatch.setattr("lambda_ai_cloud_api_client.cli.ssh.os.execvp", _fake_execvp)

    # Assert
    c_assert_cmd_results_equals(["ssh", "My Instance"], DATA_FOLDER / "expected_ssh_output.txt")
    assert captured_execvp["call"] == ("ssh", ["ssh", "ubuntu@198.51.100.2"])

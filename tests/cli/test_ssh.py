from collections.abc import Callable
from pathlib import Path

from click.testing import Result

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

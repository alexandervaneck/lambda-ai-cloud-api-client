import json
from collections.abc import Callable
from pathlib import Path

import pytest
from click.testing import Result

from lambda_ai_cloud_api_client.cli.client import DEFAULT_BASE_URL

DATA_FOLDER = Path(__file__).parent.parent / "data"


@pytest.fixture
def m_subprocess_run(monkeypatch) -> list[list[str]]:
    calls = []

    class FakeCompleted:
        def __init__(self, returncode=0):
            self.returncode = returncode

    def _fake_run(cmd, **kwargs):
        calls.append(cmd)
        return FakeCompleted()

    monkeypatch.setattr("lambda_ai_cloud_api_client.cli.run.subprocess.run", _fake_run)

    return calls


def test_run_execs_remote_command(
    c_assert_cmd_kwargs_result_equals: Callable[[list[str], dict[str, str], Path], Result],
    m_subprocess_run: list[list[str]],
    m_wait_for_ip,
    m_wait_for_ssh,
) -> None:
    c_assert_cmd_kwargs_result_equals(
        ["run", "My Instance", "echo", "hello", "world"], {}, DATA_FOLDER / "expected_run_output.txt"
    )
    assert m_subprocess_run[0] == [
        "ssh",
        "-o",
        "StrictHostKeyChecking=accept-new",
        "-o",
        "UserKnownHostsFile=/dev/null",
        "ubuntu@198.51.100.2",
        "echo hello world",
    ]


def test_run_execs_remote_command_with_filters(
    httpx_mock,
    c_assert_cmd_kwargs_result_equals: Callable[[list[str], dict[str, str], Path], Result],
    m_subprocess_run: list[list[str]],
    m_wait_for_ip,
    m_wait_for_ssh,
) -> None:
    httpx_mock.add_response(
        method="GET",
        url=f"{DEFAULT_BASE_URL}/api/v1/instance-types",
        json=json.loads((DATA_FOLDER / "m_instance_types_response.json").read_text()),
    )
    httpx_mock.add_response(
        method="POST",
        url=f"{DEFAULT_BASE_URL}/api/v1/instance-operations/launch",
        json=json.loads((DATA_FOLDER / "m_start_response.json").read_text()),
    )

    c_assert_cmd_kwargs_result_equals(
        ["run", "--cheapest", "--available", "--min-gpus", "1", "--ssh-key", "default-key", "echo", "hello", "world"],
        {},
        DATA_FOLDER / "expected_run_output_with_filters.txt",
    )
    assert m_subprocess_run[0] == [
        "ssh",
        "-o",
        "StrictHostKeyChecking=accept-new",
        "-o",
        "UserKnownHostsFile=/dev/null",
        "ubuntu@198.51.100.2",
        "echo hello world",
    ]


def test_run_with_env(
    tmp_path,
    c_assert_cmd_kwargs_result_equals: Callable[[list[str], dict[str, str], Path], Result],
    m_subprocess_run: list[list[str]],
    m_wait_for_ip,
    m_wait_for_ssh,
) -> None:
    env_file = tmp_path / "envfile"
    env_file.write_text(
        """
FOO=bar
# comment
BAZ=qux
"""
    )
    c_assert_cmd_kwargs_result_equals(
        ["run", "My Instance", "-e", "KEY=VALUE", "--env-file", str(env_file), "echo", "hi"],
        {},
        DATA_FOLDER / "expected_run_env_output.txt",
    )

    assert m_subprocess_run[0] == [
        "ssh",
        "-o",
        "StrictHostKeyChecking=accept-new",
        "-o",
        "UserKnownHostsFile=/dev/null",
        "ubuntu@198.51.100.2",
        "KEY=VALUE FOO=bar BAZ=qux echo hi",
    ]


def test_run_with_volume(
    c_assert_cmd_kwargs_result_equals: Callable[[list[str], dict[str, str], Path], Result],
    m_subprocess_run: list[list[str]],
    m_wait_for_ip,
    m_wait_for_ssh,
) -> None:
    c_assert_cmd_kwargs_result_equals(
        ["run", "My Instance", "-v", "./:/remote/path", "echo", "hi"],
        {},
        DATA_FOLDER / "expected_run_volume_output.txt",
    )

    assert m_subprocess_run[0] == [
        "rsync",
        "-e",
        "ssh -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile=/dev/null",
        "-az",
        "--delete",
        "./",
        "ubuntu@198.51.100.2:/remote/path",
    ]
    assert m_subprocess_run[-1] == [
        "rsync",
        "-e",
        "ssh -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile=/dev/null",
        "-az",
        "--delete",
        "ubuntu@198.51.100.2:/remote/path",
        "./",
    ]

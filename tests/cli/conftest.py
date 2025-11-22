import os
from collections.abc import Callable, Iterable
from pathlib import Path

import pytest
from click.testing import CliRunner, Result

from lambda_ai_cloud_api_client import __main__ as cli

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
        print(result.stderr)
        print(result.stdout)
        print(result.output)
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

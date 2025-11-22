from collections.abc import Callable
from pathlib import Path

from click.testing import Result

DATA_FOLDER = Path(__file__).parent.parent / "data"


def test_get(
    c_assert_cmd_results_equals: Callable[[list[str], Path], Result],
) -> None:
    # Arrange
    cmd = ["--help"]

    # Act & Assert
    c_assert_cmd_results_equals(cmd, DATA_FOLDER / "expected_help_output.txt")

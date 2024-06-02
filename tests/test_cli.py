from pathlib import Path  # Import Path from pathlib
from unittest.mock import MagicMock, patch

import click
from click.testing import CliRunner
from quick_python_project import cli


@patch("quick_python_project.project_generation.create_project")
def test_cli(mock_create_project):
    runner = CliRunner()
    result = runner.invoke(cli.cli, ["my_project", "my_command"])

    assert result.exit_code == 0
    mock_create_project.assert_called_once_with(
        "my_project", str(Path.home() / "code"), "my_command"
    )

    # Additional tests for default command_name
    result_default = runner.invoke(cli.cli, ["my_project"])
    assert result_default.exit_code == 0
    mock_create_project.assert_called_with("my_project", str(Path.home() / "code"), "cmd")

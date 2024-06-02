import os
import sys
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner

# Add the 'src' directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

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

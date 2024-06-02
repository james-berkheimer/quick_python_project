import os
import sys
import tempfile

from click.testing import CliRunner

# Add the 'src' directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from quick_python_project.cli import cli


def test_cli():
    with tempfile.TemporaryDirectory() as temp_dir:
        runner = CliRunner()
        result = runner.invoke(cli, ["my_project", "my_command", temp_dir])
        assert result.exit_code == 0

    result_no_args = runner.invoke(cli, ["my_project"])
    assert result_no_args.exit_code == 0

    result_help = runner.invoke(cli, ["--help"])
    assert result_help.exit_code == 0
    assert "This script creates a new Python project" in result_help.output

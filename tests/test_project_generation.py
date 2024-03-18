# FILEPATH: /home/james/code/quick_python_project/tests/test_main.py

import json
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

import pytest
from click.testing import CliRunner

# Add the 'src' directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from quick_python_project import main, project_generation


@patch("builtins.open", new_callable=mock_open)
def test_create_file_from_template_file_not_found(mock_file):
    path = "test_path"
    template_path = "template_path"
    replacements = {"PLACEHOLDER_NAME": "Test"}

    mock_file.side_effect = FileNotFoundError

    with pytest.raises(FileNotFoundError):
        project_generation.create_file_from_template(path, template_path, replacements)


@patch("builtins.open", new_callable=mock_open, read_data="PLACEHOLDER_NAME")
def test_create_file_from_template(mock_file):
    path = "test_path"
    template_path = "template_path"
    replacements = {"PLACEHOLDER_NAME": "Test"}

    project_generation.create_file_from_template(path, template_path, replacements)

    mock_file.assert_any_call(template_path, "r")
    mock_file.assert_any_call(path, "w")
    mock_file().write.assert_called_once_with("Test")


@patch("os.access", return_value=True)
@patch("quick_python_project.project_generation.create_file_from_template")
@patch("pathlib.Path.mkdir")
def test_generate_project_files(mock_mkdir, mock_create_file, mock_os_access):
    project_name = "test_project"
    project_root_path = "root_path"
    user_name = "test_user"
    user_email = "test_user@example.com"
    command_name = "test_command"
    package_type = "hatchling"
    min_python_version = "3.7"

    project_generation.generate_project_files(
        project_name,
        project_root_path,
        user_name,
        user_email,
        command_name,
        package_type,
        min_python_version,
    )

    mock_mkdir.assert_called()
    assert mock_create_file.call_count == 5
    mock_os_access.assert_called_once_with(project_root_path, os.W_OK)


@patch("quick_python_project.project_generation.create_project")
def test_create_project(mock_create_project):
    name = "test_project"
    path = "test_path"
    user_name = "test_user"
    user_email = "test_user@example.com"
    command_name = "test_command"
    package_type = "hatchling"
    save_defaults = True
    min_python_version = "3.7"

    project_generation.create_project(
        name,
        path,
        user_name,
        user_email,
        command_name,
        package_type,
        save_defaults,
        min_python_version,
    )

    mock_create_project.assert_called_once_with(
        name,
        path,
        user_name,
        user_email,
        command_name,
        package_type,
        save_defaults,
        min_python_version,
    )


@patch("builtins.open", new_callable=MagicMock)
@patch("os.access", return_value=True)
def test_get_default_value_exists(mock_access, mock_open):
    mock_open.return_value.__enter__.return_value = MagicMock()
    mock_open.return_value.__enter__.return_value.read.return_value = json.dumps({"key": "value"})

    result = main.get_default_value("key", "default")
    assert result == "value"


@patch("builtins.open", new_callable=MagicMock)
@patch("os.access", return_value=False)
def test_get_default_value_not_readable(mock_access, mock_open):
    result = main.get_default_value("key", "default")
    assert result == "default"


@patch("os.access", return_value=False)
def test_get_default_value_not_exists(mock_access):
    result = main.get_default_value("key", "default")
    assert result == "default"


@patch("quick_python_project.main.project_generation.create_project")
def test_main(mock_create_project):
    runner = CliRunner()
    result = runner.invoke(
        main.main,
        [
            "--name",
            "test_project",
            "--path",
            "/test/path",
            "--user-name",
            "Test User",
            "--user-email",
            "test@example.com",
            "--command-name",
            "test_command",
            "--package-type",
            "setuptools",
            "--min-python-version",
            "3.9",
            "--save-defaults",
            "--verbose",
        ],
    )

    assert result.exit_code == 0
    mock_create_project.assert_called_once_with(
        "test_project",
        "/test/path",
        "Test User",
        "test@example.com",
        "test_command",
        "setuptools",
        True,
        "3.9",
    )

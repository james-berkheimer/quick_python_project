from pathlib import Path
from unittest.mock import mock_open, patch

from quick_project import project_generation


@patch("builtins.open", new_callable=mock_open, read_data="PLACEHOLDER_NAME")
def test_create_file_from_template(mock_file):
    path = "test_path"
    template_path = "template_path"
    replacements = {"PLACEHOLDER_NAME": "Test"}

    project_generation.create_file_from_template(path, template_path, replacements)

    mock_file.assert_any_call(template_path, "r")
    mock_file.assert_any_call(path, "w")
    mock_file().write.assert_called_once_with("Test")


@patch("project_generation.create_file_from_template")
@patch("pathlib.Path.mkdir")
def test_generate_project_files(mock_mkdir, mock_create_file):
    project_name = "test_project"
    project_root_path = "root_path"
    user_name = "test_user"
    user_email = "test_user@example.com"
    command_name = "test_command"

    project_generation.generate_project_files(
        project_name, project_root_path, user_name, user_email, command_name
    )

    mock_mkdir.assert_called()
    assert mock_create_file.call_count == 5

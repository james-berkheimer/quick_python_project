from unittest import mock

import pytest
from quick_python_project import project_generation


@mock.patch("quick_python_project.project_generation.create_file_from_template")
@mock.patch("quick_python_project.project_generation.os.access", return_value=True)
@mock.patch("quick_python_project.project_generation.Path.mkdir")
@mock.patch("quick_python_project.project_generation.logger")
def test_generate_project_files_happy_path(
    mock_logger,
    mock_mkdir,
    mock_os_access,
    mock_create_file_from_template,
):
    with mock.patch("quick_python_project.project_generation.Path.exists") as mock_path_exists:
        mock_path_exists.return_value = False
        # Setup
        project_name = "test_project"
        project_root_path = "/path/to/project"
        command_name = "test_command"

        # Call the function under test
        project_generation.generate_project_files(
            project_name,
            project_root_path,
            command_name,
        )

    # Check if the function calls create_file_from_template correctly
    assert mock_create_file_from_template.call_count == 5
    mock_create_file_from_template.assert_any_call(mock.ANY, mock.ANY, mock.ANY)

    # Check if the logger is called correctly
    assert mock_logger.info.call_count == 2
    mock_logger.info.assert_any_call("Generating project files...")
    mock_logger.info.assert_any_call(
        f"Generated project files for '{project_name}' at '{project_root_path}'"
    )

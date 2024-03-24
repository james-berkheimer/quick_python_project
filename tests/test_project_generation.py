# FILEPATH: /home/james/code/quick_python_project/tests/test_project_generation.py
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from unittest.mock import MagicMock, call, mock_open, patch

import pytest

# Add the 'src' directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))


from quick_python_project import project_generation
from quick_python_project.project_generation import (
    create_file_from_template,
    create_project,
    generate_project_files,
)


class TestGenerateProjectFiles(unittest.TestCase):
    @mock.patch("quick_python_project.project_generation.create_file_from_template")
    @mock.patch("quick_python_project.project_generation.os.access")
    @mock.patch("quick_python_project.project_generation.Path.mkdir")
    @mock.patch("quick_python_project.project_generation.logger")
    def test_generate_project_files_happy_path(
        self,
        mock_logger,
        mock_mkdir,
        mock_os_access,
        mock_create_file_from_template,
    ):
        # Setup
        mock_os_access.return_value = True
        project_name = "test_project"
        project_root_path = "/path/to/project"
        user_name = "test_user"
        user_email = "test_user@example.com"
        command_name = "test_command"
        package_type = "test_package"
        min_python_version = "3.6"

        # Call the function under test
        project_generation.generate_project_files(
            project_name,
            project_root_path,
            user_name,
            user_email,
            command_name,
            package_type,
            min_python_version,
        )

        # Assert that the correct calls were made
        mock_os_access.assert_called_once_with(project_root_path, os.W_OK)
        mock_mkdir.assert_called()
        mock_create_file_from_template.assert_called()
        mock_logger.info.assert_called_with(
            f"Generated project files for '{project_name}' at '{project_root_path}'"
        )

    @mock.patch("quick_python_project.project_generation.create_file_from_template")
    @mock.patch("quick_python_project.project_generation.os.access")
    @mock.patch("quick_python_project.project_generation.Path.mkdir")
    @mock.patch("quick_python_project.project_generation.logger")
    def test_generate_project_files_permission_error(
        self,
        mock_logger,
        mock_mkdir,
        mock_os_access,
        mock_create_file_from_template,
    ):
        # Setup
        mock_os_access.return_value = False
        project_name = "test_project"
        project_root_path = "/path/to/project"
        user_name = "test_user"
        user_email = "test_user@example.com"
        command_name = "test_command"
        package_type = "test_package"
        min_python_version = "3.6"

        # Call the function under test and assert it raises a PermissionError
        with self.assertRaises(PermissionError):
            project_generation.generate_project_files(
                project_name,
                project_root_path,
                user_name,
                user_email,
                command_name,
                package_type,
                min_python_version,
            )

        # Assert that the correct calls were made
        mock_os_access.assert_called_once_with(project_root_path, os.W_OK)

    #######################################################################################

    def test_create_file_from_template(self):
        # Create a temporary file to use as the template
        with tempfile.NamedTemporaryFile(delete=False) as template:
            template.write(b"Hello, {name}!")
            template_path = template.name

        # Specify the path for the new file and the replacements
        path = tempfile.mktemp()
        replacements = {"{name}": "World"}

        # Call the function under test
        create_file_from_template(path, template_path, replacements)

        # Check that the new file was created and contains the expected content
        with open(path, "r") as file:
            content = file.read()
        assert content == "Hello, World!"

        # Clean up the temporary files
        os.remove(path)
        os.remove(template_path)

    def test_create_file_from_template_file_not_found(self):
        # Specify a non-existent template file
        template_path = "/path/to/nonexistent/template"

        # Specify the path for the new file and the replacements
        path = tempfile.mktemp()
        replacements = {"{name}": "World"}

        # Call the function under test and assert it raises a FileNotFoundError
        with pytest.raises(FileNotFoundError):
            create_file_from_template(path, template_path, replacements)

        # Clean up the temporary file if it exists
        if os.path.exists(path):
            os.remove(path)


class TestCreateProject(unittest.TestCase):
    @patch("quick_python_project.project_generation.generate_project_files")
    def test_create_project(self, mock_generate_project_files):
        # Arrange
        name = "test_project"
        path = tempfile.mkdtemp()  # Use a temporary directory
        user_name = "test_user"
        user_email = "test_user@example.com"
        command_name = "test_command"
        package_type = "test_package"
        save_prefs = False
        min_python_version = "3.6"

        # Act
        create_project(
            name,
            path,
            user_name,
            user_email,
            command_name,
            package_type,
            save_prefs,
            min_python_version,
        )

        # Assert
        mock_generate_project_files.assert_called_once_with(
            name,
            Path(path) / name,  # Convert the path to a Path object
            user_name,
            user_email,
            command_name,
            package_type,
            min_python_version,
        )


if __name__ == "__main__":
    unittest.main()

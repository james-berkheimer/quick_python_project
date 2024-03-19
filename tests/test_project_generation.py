# FILEPATH: /home/james/code/quick_python_project/tests/test_project_generation.py
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from unittest.mock import call, mock_open, patch

# Add the 'src' directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))


from quick_python_project.project_generation import (
    create_file_from_template,
    create_project,
    generate_project_files,
)


class TestCreateFileFromTemplate(unittest.TestCase):
    @patch("quick_python_project.project_generation.logger")
    @patch("builtins.open", new_callable=mock_open, read_data="placeholder")
    def test_create_file_from_template_happy_path(self, mock_open, mock_logger):
        replacements = {"placeholder": "value"}
        create_file_from_template("path", "template_path", replacements)
        calls = [call for call in mock_open.mock_calls if call[0] == ""]
        calls_expected = [call("template_path", "r"), call("path", "w")]
        self.assertEqual(calls, calls_expected)
        mock_logger.info.assert_called_once_with("Created file path from template template_path")

    @patch("quick_python_project.project_generation.logger")
    @patch("builtins.open", new_callable=mock_open, read_data="placeholder")
    def test_create_file_from_template_placeholder_not_found(self, mock_open, mock_logger):
        replacements = {"not_placeholder": "value"}
        create_file_from_template("path", "template_path", replacements)
        mock_logger.debug.assert_called_once_with(
            "Placeholder not_placeholder not found in template template_path"
        )

    @patch("quick_python_project.project_generation.logger")
    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_create_file_from_template_template_not_found(self, mock_open, mock_logger):
        replacements = {"placeholder": "value"}
        with self.assertRaises(FileNotFoundError):
            create_file_from_template("path", "template_path", replacements)
        mock_logger.error.assert_called_once_with("Template file template_path does not exist")

    @patch("quick_python_project.project_generation.logger")
    @patch("builtins.open", side_effect=Exception)
    def test_create_file_from_template_error_creating_file(self, mock_open, mock_logger):
        replacements = {"placeholder": "value"}
        with self.assertRaises(Exception):
            create_file_from_template("path", "template_path", replacements)
        mock_logger.error.assert_called_once_with(
            "Error creating file path from template template_path: "
        )


class TestGenerateProjectFiles(unittest.TestCase):
    @mock.patch("quick_python_project.project_generation.create_file_from_template")
    @mock.patch("quick_python_project.project_generation.os.access")
    @mock.patch("quick_python_project.project_generation.Path.mkdir")
    def test_generate_project_files(
        self,
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
        generate_project_files(
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
        calls = [
            call(
                Path(project_root_path) / "pyproject.toml",
                "templates/test_package_pyproject.toml",
                mock.ANY,
            ),
            call(Path(project_root_path) / ".gitignore", "templates/.gitignore", mock.ANY),
            call(Path(project_root_path) / ".README.md", "templates/README.md", mock.ANY),
            call(Path(project_root_path) / "LICENSE", "templates/LICENSE", mock.ANY),
            call(
                Path(project_root_path) / f"src/{project_name}/main.py",
                "templates/main.py",
                mock.ANY,
            ),
        ]
        mock_create_file_from_template.assert_has_calls(calls, any_order=True)

    @mock.patch("quick_python_project.project_generation.create_file_from_template")
    @mock.patch("quick_python_project.project_generation.os.access")
    @mock.patch("quick_python_project.project_generation.Path.mkdir")
    def test_generate_project_files_no_write_access(
        self,
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
            generate_project_files(
                project_name,
                project_root_path,
                user_name,
                user_email,
                command_name,
                package_type,
                min_python_version,
            )

    @mock.patch(
        "quick_python_project.project_generation.create_file_from_template",
        side_effect=Exception,
    )
    @mock.patch("quick_python_project.project_generation.os.access")
    @mock.patch("quick_python_project.project_generation.Path.mkdir")
    def test_generate_project_files_error_creating_file(
        self,
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

        # Call the function under test and assert it raises an Exception
        with self.assertRaises(Exception):
            generate_project_files(
                project_name,
                project_root_path,
                user_name,
                user_email,
                command_name,
                package_type,
                min_python_version,
            )


class TestCreateProject(unittest.TestCase):
    @mock.patch("quick_python_project.project_generation.generate_project_files")
    @mock.patch("quick_python_project.project_generation.create_file_from_template")
    def test_create_project(
        self,
        mock_create_file_from_template,
        mock_generate_project_files,
    ):
        # Setup
        name = "test_project"
        path = tempfile.mkdtemp()  # Use a temporary directory
        user_name = "test_user"
        user_email = "test_user@example.com"
        command_name = "test_command"
        package_type = "test_package"
        save_prefs = True
        min_python_version = "3.6"

        # Call the function under test
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

        # Assert that the correct calls were made
        mock_generate_project_files.assert_called_once_with(
            name,
            Path(path) / name,  # Convert the path to a PosixPath object
            user_name,
            user_email,
            command_name,
            package_type,
            min_python_version,
        )


if __name__ == "__main__":
    unittest.main()

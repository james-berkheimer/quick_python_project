# FILEPATH: /home/james/code/quick_python_project/tests/test_main.py
import json
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from unittest.mock import ANY, MagicMock, call, mock_open, patch

from click.testing import CliRunner

# Add the 'src' directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from quick_python_project.main import create_prefs_file, delete_prefs_file, get_saved_prefs, main

# print(f"Location: {os.path.dirname(main.__file__)}")


class TestPrefsFiles(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.cwd")
    def test_create_prefs_file(self, mock_cwd, mock_file):
        # Setup
        path = tempfile.mkdtemp()  # Use a temporary directory
        mock_cwd.return_value = Path(path)  # Mock Path.cwd() to return the temporary directory

        user_name = "test_user"
        user_email = "test_user@example.com"
        package_type = "test_package"
        min_python_version = "3.6"

        # Call the function under test
        create_prefs_file(path, user_name, user_email, package_type, min_python_version)

        # Assert that the file was opened in write mode
        mock_file.assert_called_once_with(Path(path) / "data" / "user_prefs.json", "w")

        # Get the mock file handle
        handle = mock_file()

        # Assert that the file was written with the correct JSON string
        expected_json = json.dumps(
            {
                "path": str(path),
                "user_name": user_name,
                "user_email": user_email,
                "package_type": package_type,
                "min_python_version": min_python_version,
            }
        )
        handle.write.assert_called_once_with(expected_json)

    @patch("os.path.exists")
    @patch("os.remove")
    @patch("quick_python_project.main.logger")
    def test_delete_prefs_file(self, mock_logger, mock_remove, mock_exists):
        # Test when file exists
        mock_exists.return_value = True
        delete_prefs_file()
        mock_remove.assert_called_once_with("user_prefs.json")
        mock_logger.info.assert_called_with("User preferences file deleted.")

        # Reset mocks
        mock_remove.reset_mock()
        mock_logger.reset_mock()

        # Test when file does not exist
        mock_exists.return_value = False
        delete_prefs_file()
        mock_remove.assert_not_called()
        mock_logger.info.assert_called_with("User preferences file does not exist.")

        # Reset mocks
        mock_logger.reset_mock()

        # Test when an error occurs
        mock_exists.side_effect = Exception("Test exception")
        delete_prefs_file()
        mock_logger.error.assert_called_with(
            "An error occurred while deleting the user preferences file: Test exception"
        )

    #########

    @patch.object(Path, "exists")
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.access")
    @patch("pathlib.Path.cwd")
    @patch("quick_python_project.main.logger")
    @patch("json.loads")
    def test_get_saved_prefs(
        self, mock_json_loads, mock_logger, mock_cwd, mock_access, mock_file, mock_exists
    ):
        # Setup
        path = tempfile.mkdtemp()  # Use a temporary directory
        mock_cwd.return_value = Path(path)  # Mock Path.cwd() to return the temporary directory
        prefs_path = Path(path) / "data" / "user_prefs.json"

        # Create a mock for the file object
        mock_file_obj = MagicMock()
        mock_file_obj.read.return_value = json.dumps({"key": "value"})

        # Set mock_file to return a mock that has `__enter__` method returning `mock_file_obj`
        mock_file.return_value.__enter__.return_value = mock_file_obj

        # Mock json.loads to return the dictionary
        mock_json_loads.return_value = {"key": "value"}

        # Test when the preferences file exists and is readable
        mock_access.return_value = True
        mock_exists.return_value = True

        # Call the function under test
        result = get_saved_prefs("key", "default")

        # Assert that the open function was called with the correct arguments
        mock_file.assert_called_once_with(prefs_path, "r")

        # Assert that the json.loads function was called with the mock file object
        mock_json_loads.assert_called_once_with(
            mock_file_obj.read.return_value,
            cls=ANY,
            object_hook=ANY,
            parse_float=ANY,
            parse_int=ANY,
            parse_constant=ANY,
            object_pairs_hook=ANY,
        )

        # Assert that the function returned the correct result
        self.assertEqual(result, "value")

        # Test when the preferences file does not exist or is not readable
        mock_access.return_value = False
        result = get_saved_prefs("key", "default")
        self.assertEqual(result, "default")
        mock_logger.debug.assert_called_with(
            f"The saved defaults file {prefs_path} is not readable or does not exist.  Using the provided default value."
        )


class TestMainFunction(unittest.TestCase):
    @patch("quick_python_project.main.create_prefs_file")
    @patch("quick_python_project.main.delete_prefs_file")
    @patch("quick_python_project.main.project_generation.create_project")
    def test_main(self, mock_create_project, mock_delete_prefs_file, mock_create_prefs_file):
        runner = CliRunner()
        result = runner.invoke(
            main,
            [
                "-n",
                "test_project",
                "-p",
                "/test/path",
                "-un",
                "test_user",
                "-ue",
                "test_user@example.com",
                "-cmd",
                "test_command",
                "-pt",
                "setuptools",
                "-mpv",
                "3.9",
                "-sp",
                "-v",
                "-dp",
            ],
        )

        # Print the output if the command failed
        if result.exit_code != 0:
            print(result.output)

        # Check that the command ran without errors
        self.assertEqual(result.exit_code, 0)

        # ... rest of the test

        # Check that the create_prefs_file function was called with the correct arguments
        mock_create_prefs_file.assert_called_once_with(
            "/test/path", "test_user", "test_user@example.com", "setuptools", "3.9"
        )

        # Check that the delete_prefs_file function was called
        mock_delete_prefs_file.assert_called_once()

        # Check that the create_project function was called with the correct arguments
        mock_create_project.assert_called_once_with(
            "test_project",
            "/test/path",
            "test_user",
            "test_user@example.com",
            "test_command",
            "setuptools",
            True,
            "3.9",
        )

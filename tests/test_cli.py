import json
import os
import stat
import sys
import unittest
from pathlib import Path
from unittest import mock
from unittest.mock import ANY, MagicMock, call, mock_open, patch

from click.testing import CliRunner

# Add the 'src' directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from quick_python_project.cli import (  # noqa: E402
    cli,
    create_prefs_file,
    create_project,
    delete_prefs_file,
    get_prefs_file_path,
    get_saved_prefs,
)

CONFIG_FILE_NAME = "config.json"


class TestGetPrefsFilePath(unittest.TestCase):
    @mock.patch("os.getenv")
    @mock.patch("pathlib.Path.home")
    def test_get_prefs_file_path_posix(self, mock_home, mock_getenv):
        # Arrange
        mock_home.return_value = Path("/home/user")
        mock_getenv.return_value = "C:\\Users\\user\\AppData\\Roaming"

        # Act & Assert
        self.assertEqual(
            str(get_prefs_file_path("posix")), str(Path("/home/user/.config/config.json"))
        )

    @mock.patch("os.getenv")
    @mock.patch("pathlib.Path.home")
    def test_get_prefs_file_path_nt(self, mock_home, mock_getenv):
        # Arrange
        mock_home.return_value = Path("/home/user")
        mock_getenv.return_value = "C:\\Users\\user\\AppData\\Roaming"

        # Act & Assert
        self.assertEqual(
            str(get_prefs_file_path("nt")),
            str(
                Path("C:\\Users\\user\\AppData\\Roaming")
                / "quick_python_project"
                / CONFIG_FILE_NAME
            ),
        )

    @mock.patch("os.getenv")
    @mock.patch("pathlib.Path.home")
    def test_get_prefs_file_path_unsupported(self, mock_home, mock_getenv):
        # Arrange
        mock_home.return_value = Path("/home/user")
        mock_getenv.return_value = "C:\\Users\\user\\AppData\\Roaming"

        # Act & Assert
        with self.assertRaises(NotImplementedError):
            get_prefs_file_path("unsupported")

    @mock.patch("quick_python_project.cli.open", new_callable=mock.mock_open)
    @mock.patch("quick_python_project.cli.os.chmod")
    def test_create_prefs_file_exception(self, mock_chmod, mock_open):
        # Arrange
        mock_open.side_effect = Exception("Test exception")
        project_path = "/path/to/project"
        user_name = "test_user"
        user_email = "test_user@example.com"
        package_type = "test_package"
        min_python_version = "3.7"

        # Act and Assert
        with self.assertRaises(Exception) as context:
            create_prefs_file(project_path, user_name, user_email, package_type, min_python_version)
        self.assertTrue("Test exception" in str(context.exception))

    @mock.patch("quick_python_project.cli.os.path.exists", return_value=True)
    @mock.patch("quick_python_project.cli.os.remove")
    def test_delete_prefs_file_exists(self, mock_remove, mock_exists):
        delete_prefs_file()
        mock_remove.assert_called_once()

    @mock.patch("quick_python_project.cli.os.path.exists", return_value=False)
    @mock.patch("quick_python_project.cli.os.remove")
    def test_delete_prefs_file_not_exists(self, mock_remove, mock_exists):
        delete_prefs_file()
        mock_remove.assert_not_called()

    @mock.patch("quick_python_project.cli.os.path.exists", return_value=True)
    @mock.patch("quick_python_project.cli.os.remove", side_effect=Exception("Test exception"))
    def test_delete_prefs_file_exception(self, mock_remove, mock_exists):
        with self.assertRaises(Exception) as context:
            delete_prefs_file()
        self.assertTrue("Test exception" in str(context.exception))


class TestPrefs(unittest.TestCase):
    @mock.patch("quick_python_project.cli.Path")
    @mock.patch("quick_python_project.cli.get_prefs_file_path")
    @mock.patch("quick_python_project.cli.json.dumps")
    @mock.patch("quick_python_project.cli.open", new_callable=mock.mock_open)
    @mock.patch("quick_python_project.cli.os.chmod")
    def test_create_prefs_file(
        self, mock_chmod, mock_open, mock_json_dumps, mock_get_prefs_file_path, mock_path
    ):
        # Arrange
        mock_get_prefs_file_path.return_value = "/path/to/prefs/file"
        mock_path.return_value.parent.mkdir.return_value = None
        mock_json_dumps.return_value = '{"key": "value"}'
        project_path = "/path/to/project"
        user_name = "test_user"
        user_email = "test_user@example.com"
        package_type = "test_package"
        min_python_version = "3.7"

        # Act
        create_prefs_file(project_path, user_name, user_email, package_type, min_python_version)

        # Assert
        mock_path.assert_called_once_with("/path/to/prefs/file")
        mock_path.return_value.parent.mkdir.assert_called_once_with(parents=True, exist_ok=True)
        mock_json_dumps.assert_called_once_with(
            {
                "project_path": project_path,
                "user_name": user_name,
                "user_email": user_email,
                "package_type": package_type,
                "min_python_version": min_python_version,
            }
        )
        mock_open.assert_called_once_with(mock_path.return_value, "w")
        mock_open.return_value.write.assert_called_once_with('{"key": "value"}')
        mock_chmod.assert_called_once_with(
            mock_path.return_value, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
        )

    @mock.patch("quick_python_project.cli.logger")
    @mock.patch("quick_python_project.cli.os.remove")
    @mock.patch("quick_python_project.cli.os.path.exists")
    @mock.patch("quick_python_project.cli.get_prefs_file_path")
    def test_delete_prefs_file(
        self, mock_get_prefs_file_path, mock_exists, mock_remove, mock_logger
    ):
        # Arrange
        mock_get_prefs_file_path.return_value = "/path/to/prefs/file"
        mock_exists.return_value = True

        # Act
        delete_prefs_file()

        # Assert
        mock_get_prefs_file_path.assert_called_once()
        mock_exists.assert_called_once_with("/path/to/prefs/file")
        mock_remove.assert_called_once_with("/path/to/prefs/file")
        mock_logger.info.assert_called_once_with(
            "User preferences file /path/to/prefs/file deleted."
        )

    class TestPrefs(unittest.TestCase):
        @patch("builtins.open", new_callable=MagicMock)
        @patch("src.quick_python_project.cli.get_prefs_file_path")
        def test_get_saved_prefs(self, mock_get_prefs_file_path, mock_open):
            # Test case where the preferences file exists and contains the key
            mock_get_prefs_file_path.return_value = MagicMock(
                spec=Path, exists=MagicMock(return_value=True), is_file=MagicMock(return_value=True)
            )
            mock_open.return_value.__enter__.return_value = MagicMock(spec=open)
            mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(
                {"key": "value"}
            )
            result = get_saved_prefs("key", "default_value")
            self.assertEqual(result, "value")

            # Test case where the preferences file exists but does not contain the key
            mock_open.return_value.__enter__.return_value.read.return_value = json.dumps({})
            result = get_saved_prefs("key", "default_value")
            self.assertEqual(result, "default_value")

            # Test case where the preferences file does not exist
            mock_get_prefs_file_path.return_value = MagicMock(
                spec=Path,
                exists=MagicMock(return_value=False),
                is_file=MagicMock(return_value=False),
            )
            result = get_saved_prefs("key", "default_value")
            self.assertEqual(result, "default_value")

    @mock.patch("quick_python_project.cli.get_prefs_file_path")
    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data='{"key": "value"}')
    def test_get_saved_prefs_exists(self, mock_open, mock_get_prefs_file_path):
        result = get_saved_prefs("key", "default_value")
        self.assertEqual(result, "value")

    @mock.patch("quick_python_project.cli.get_prefs_file_path")
    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data='{"key": "value"}')
    def test_get_saved_prefs_not_exists(self, mock_open, mock_get_prefs_file_path):
        result = get_saved_prefs("nonexistent_key", "default_value")
        self.assertEqual(result, "default_value")

    @mock.patch("quick_python_project.cli.get_prefs_file_path")
    def test_get_saved_prefs_file_not_exists(self, mock_get_prefs_file_path):
        # Test case where the preferences file does not exist
        mock_get_prefs_file_path.return_value = MagicMock(
            spec=Path, exists=MagicMock(return_value=False), is_file=MagicMock(return_value=False)
        )
        result = get_saved_prefs("key", "default_value")
        self.assertEqual(result, "default_value")

    @patch("builtins.open", new_callable=MagicMock)
    @patch("src.quick_python_project.cli.get_prefs_file_path")
    def test_get_saved_prefs_file_not_readable(self, mock_get_prefs_file_path, mock_open):
        # Test case where the preferences file exists but is not readable
        mock_get_prefs_file_path.return_value = MagicMock(
            spec=Path, exists=MagicMock(return_value=True), is_file=MagicMock(return_value=True)
        )
        mock_open.side_effect = OSError
        result = get_saved_prefs("key", "default_value")
        self.assertEqual(result, "default_value")


class TestCreateProject(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @patch("quick_python_project.cli.project_generation.create_project")
    def test_create_project(self, mock_create_project):
        # Make the mock return 0 (success)
        mock_create_project.return_value = 0

        result = self.runner.invoke(
            cli,
            [
                "create-project",
                "--name",
                "test_project",
                "--path",
                "/tmp",
                "--user-name",
                "test_user",
                "--user-email",
                "test_user@example.com",
                "--command",
                "test_command",
                "--package-type",
                "setuptools",
                "--min-python-version",
                "3.9",
                "--save-prefs",
                "--verbose",
            ],
        )

        # Check that the command did not return an error
        self.assertEqual(result.exit_code, 0)

        # Check that the create_project function was called with the correct arguments
        mock_create_project.assert_called_once_with(
            "test_project",
            "/tmp",
            "test_user",
            "test_user@example.com",
            "test_command",
            "setuptools",
            True,
            "3.9",
        )

    @patch("quick_python_project.cli.delete_prefs_file")
    def test_delete_prefs(self, mock_delete_prefs_file):
        # Make the mock return None (success)
        mock_delete_prefs_file.return_value = None

        result = self.runner.invoke(cli, ["delete-prefs"])

        # Check that the command did not return an error
        self.assertEqual(result.exit_code, 0)

        # Check that the delete_prefs_file function was called
        mock_delete_prefs_file.assert_called_once()


if __name__ == "__cli__":
    unittest.cli()

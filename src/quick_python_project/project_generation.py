import errno
import json
import logging
import os
import stat
from pathlib import Path

import colorlog

# Set up logging
handler = colorlog.StreamHandler()
handler.setFormatter(
    colorlog.ColoredFormatter("%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s")
)

logger = colorlog.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def create_file_from_template(path, template_path, replacements):
    """
    Create a new file based on a template file, replacing placeholders with specified values.

    Parameters:
    path (str): The path where the new file will be created.
    template_path (str): The path to the template file.
    replacements (dict): A dictionary mapping placeholders to their replacement values.

    Returns:
    None

    Raises:
    FileNotFoundError: If the template file does not exist.
    """
    try:
        with open(template_path, "r") as template:
            content = template.read()

        for placeholder, value in replacements.items():
            if placeholder not in content:
                logger.debug(f"Placeholder {placeholder} not found in template {template_path}")
            content = content.replace(placeholder, value)

        with open(path, "w") as file:
            file.write(content)
        logger.info(f"Created file {path} from template {template_path}")
    except FileNotFoundError:
        logger.error(f"Template file {template_path} does not exist")
        raise
    except Exception as e:
        logger.error(f"Error creating file {path} from template {template_path}: {e}")
        raise


def create_project(
    name, path, user_name, user_email, command_name, package_type, save_prefs, min_python_version
):
    """
    Create a new project with the specified name at the specified path.

    Parameters:
    name (str): The name of the project.
    path (str): The path where the project will be created.
    user_name (str): The name of the user.
    user_email (str): The email of the user.
    command_name (str): The name of the command.
    package_type (str): The type of the package.
    save_prefs (bool): Whether to save the current options as defaults.
    min_python_version (str): The minimum Python version required for the project.
    """
    logger.info("Creating project...")
    path = Path(path)
    project_root_path = path / name

    if project_root_path.exists():
        logger.error(
            f"Project directory {project_root_path} already exists. Please choose a different name or location."
        )
    else:
        project_root_path.mkdir(parents=True, exist_ok=True)

        try:
            generate_project_files(
                name,
                project_root_path,
                user_name,
                user_email,
                command_name,
                package_type,
                min_python_version,
            )
        except (PermissionError, IOError) as e:
            logger.error(f"Error: {e}")
            raise

        logger.info(f"Created '{name}' project at '{project_root_path}'")
        logger.info(f"User: '{user_name}' with email '{user_email}'")
        logger.info(f"Command: '{command_name}'")
        logger.info(f"Package type: '{package_type}'")
        logger.info(f"Minimum Python version: '{min_python_version}'")


def generate_project_files(
    project_name,
    project_root_path,
    user_name,
    user_email,
    command_name,
    package_type,
    min_python_version,
):
    """
    Generate the files for the new project based on templates.

    Parameters:
    project_name (str): The name of the project.
    project_root_path (str): The path where the project will be created.
    user_name (str): The name of the user.
    user_email (str): The email of the user.
    command_name (str): The name of the command.
    package_type (str): The type of the package.
    min_python_version (str): The minimum Python version required for the project.

    Raises:
    PermissionError: If the script does not have write access to the project root path.
    """
    if not os.access(project_root_path, os.W_OK):
        raise PermissionError(f"Cannot write to project root path {project_root_path}")

    logger.info("Generating project files...")
    replacements = {
        "PLACEHOLDER_NAME": project_name,
        "<USERNAME>": user_name,
        "<USERNAME@example>": user_email,
        "PLACEHOLDER_CMD": command_name,
        "PYTHON_VERSION": f">={min_python_version}",
    }

    script_dir = os.path.dirname(__file__)
    files_to_generate = [
        (
            "pyproject.toml",
            os.path.join(
                script_dir,
                f"templates/template_{package_type}_pyproject.toml",
            ),
        ),
        (
            ".gitignore",
            os.path.join(script_dir, "templates/template_.gitignore"),
        ),
        (
            ".README.md",
            os.path.join(script_dir, "templates/template_README.md"),
        ),
        (
            f"src/{project_name}/main.py",
            os.path.join(script_dir, "templates/template_main.py"),
        ),
        (
            f"src/{project_name}/__init__.py",
            os.path.join(script_dir, "templates/template___init__.py"),
        ),
    ]

    for file_name, template_name in files_to_generate:
        try:
            if file_name.endswith("_pyproject.toml"):
                file_path = Path(project_root_path) / "pyproject.toml"
            else:
                file_path = Path(project_root_path) / file_name
            file_path.parent.mkdir(parents=True, exist_ok=True)
            create_file_from_template(
                file_path, template_name.replace("templates_", ""), replacements
            )
        except (PermissionError, IOError) as e:
            logger.error(f"Error generating file {file_path}: {e}")
            raise

    logger.info(f"Generated project files for '{project_name}' at '{project_root_path}'")

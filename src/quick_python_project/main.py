import json
import logging
import os
import stat
from pathlib import Path

import click
import colorlog

from . import project_generation

# Set up logging
handler = colorlog.StreamHandler()
handler.setFormatter(
    colorlog.ColoredFormatter("%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s")
)

logger = colorlog.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def get_default_value(key, default):
    """
    Get the default value for a given key. If the key is not found in the default values file,
    the provided default value is returned.

    Parameters:
    key (str): The key for which to get the default value.
    default (str): The default value to return if the key is not found in the default values file.

    Returns:
    str: The default value for the given key.
    """
    defaults_path = Path.cwd() / "data" / "default_values.json"
    if defaults_path.exists() and os.access(defaults_path, os.R_OK):
        with open(defaults_path) as f:
            defaults = json.load(f)
            return defaults.get(key, default)
    elif defaults_path.exists():
        logger.warning(f"Defaults file {defaults_path} is not readable")
    return default


@click.command()
@click.option("--name", prompt="Project name", help="The name of the project.")
@click.option(
    "--path",
    prompt="Project path",
    default=get_default_value("path", str(Path.home() / "code")),
    help="The path where the project will be created.",
)
@click.option(
    "--user-name",
    default=get_default_value("user_name", "Default User"),
    help="The name of the user.",
)
@click.option(
    "--user-email",
    default=get_default_value("user_email", "user@example.com"),
    help="The email of the user.",
)
@click.option(
    "--command-name",
    default=get_default_value("command_name", "cmd"),
    help="The name of the command.",
)
@click.option(
    "--package-type",
    type=click.Choice(["setuptools", "hatchling", "poetry"], case_sensitive=False),
    default=get_default_value("package_type", "setuptools"),
    help="The type of the package.",
)
@click.option(
    "--min-python-version",
    type=click.Choice(
        ["3.9", "3.10", "3.11"],
        case_sensitive=False,
    ),
    default=get_default_value("min_python_version", "3.9"),
    help="The minimum Python version required for the project.",
)
@click.option("--save-defaults", is_flag=True, help="Save the current options as defaults.")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose logging (show debug logs).")
def main(
    name,
    path,
    user_name,
    user_email,
    command_name,
    package_type,
    save_defaults,
    min_python_version,
    verbose,
):
    """
    The main entry point for the script.
    """
    if verbose:
        logger.setLevel(logging.DEBUG)

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

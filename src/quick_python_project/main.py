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


def create_prefs_file(path, user_name, user_email, package_type, min_python_version):
    """_summary_

    Args:
        path (_type_): _description_
        user_name (_type_): _description_
        user_email (_type_): _description_
        package_type (_type_): _description_
        min_python_version (_type_): _description_
    """
    try:
        logger.info("Saving user preferences...")
        user_prefs_path = Path.cwd() / "data" / "user_prefs.json"
        user_prefs_path.parent.mkdir(parents=True, exist_ok=True)

        user_prefs = {
            "path": str(path),
            "user_name": user_name,
            "user_email": user_email,
            "package_type": package_type,
            "min_python_version": min_python_version,
        }

        # Convert the dictionary to a JSON string
        user_prefs_str = json.dumps(user_prefs)

        # Write the JSON string to the file
        with open(user_prefs_path, "w") as f:
            f.write(user_prefs_str)

        os.chmod(user_prefs_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
    except Exception as e:
        logger.error(f"An error occurred while creating the user preferences file: {e}")


def delete_prefs_file():
    """
    Deletes the user_prefs.json file if it exists.
    """
    try:
        if os.path.exists("user_prefs.json"):
            os.remove("user_prefs.json")
            logger.info("User preferences file deleted.")
        else:
            logger.info("User preferences file does not exist.")
    except Exception as e:
        logger.error(f"An error occurred while deleting the user preferences file: {e}")


def get_saved_prefs(key, default_argument):
    """
    Get the default value for a given key. If the key is not found in the default values file,
    the provided default value is returned.

    Parameters:
    key (str): The key for which to get the default value.
    default (str): The default value to return if the key is not found in the default values file.

    Returns:
    str: The default value for the given key.
    """
    prefs_path = Path.cwd() / "data" / "user_prefs.json"
    try:
        if prefs_path.exists() and os.access(prefs_path, os.R_OK):
            with open(prefs_path, "r") as prefs_file:
                defaults = json.load(prefs_file)
                return defaults.get(key, default_argument)
        else:
            logger.debug(
                f"The saved defaults file {prefs_path} is not readable or does not exist.  Using the provided default value."
            )
    except Exception as e:
        logger.error(f"An error occurred while getting the default value: {e}")
    return default_argument


@click.command()
@click.option("-n", "--name", prompt="Project name", help="The name of the project.")
@click.option(
    "-p",
    "--path",
    prompt="Project path",
    default=get_saved_prefs("path", str(Path.home() / "code")),
    help="The path where the project will be created.",
)
@click.option(
    "-un",
    "--user-name",
    default=get_saved_prefs("user_name", "Default User"),
    help="The name of the user.",
)
@click.option(
    "-ue",
    "--user-email",
    default=get_saved_prefs("user_email", "user@example.com"),
    help="The email of the user.",
)
@click.option(
    "-cmd",
    "--command",
    default=get_saved_prefs("command", "cmd"),
    help="The name of the command.",
)
@click.option(
    "-pt",
    "--package-type",
    type=click.Choice(["setuptools", "hatchling", "poetry"], case_sensitive=False),
    default=get_saved_prefs("package_type", "setuptools"),
    help="The type of the package.",
)
@click.option(
    "-mpv",
    "--min-python-version",
    type=click.Choice(
        ["3.9", "3.10", "3.11"],
        case_sensitive=False,
    ),
    default=get_saved_prefs("min_python_version", "3.9"),
    help="The minimum Python version required for the project.",
)
@click.option("-sp", "--save-prefs", is_flag=True, help="Save the current options as defaults.")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose logging (show debug logs).")
@click.option(
    "-dp", "--delete-prefs", is_flag=True, help="Delete the user preferences file if it exists."
)
def main(
    name,
    path,
    user_name,
    user_email,
    command,
    package_type,
    save_prefs,
    min_python_version,
    verbose,
    delete_prefs,  # add this parameter
):
    """
    The main entry point for the script.
    """
    if verbose:
        logger.setLevel(logging.DEBUG)

    if save_prefs:
        create_prefs_file(path, user_name, user_email, package_type, min_python_version)

    if delete_prefs:
        delete_prefs_file()

    project_generation.create_project(
        name,
        path,
        user_name,
        user_email,
        command,
        package_type,
        save_prefs,
        min_python_version,
    )

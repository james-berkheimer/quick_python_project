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


CONFIG_FILE_NAME = "user_prefs.json"

PLATFORM = os.name


def get_prefs_file_path(os_name=None):
    os_name = os_name or os.name
    if os_name == "posix":
        return Path.home() / ".config" / "config.json"
    elif os_name == "nt":
        return Path(os.getenv("APPDATA")) / "quick_python_project" / "config.json"
    else:
        raise NotImplementedError(f"OS '{os_name}' not supported")


def create_prefs_file(project_path, user_name, user_email, package_type, min_python_version):
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
        user_prefs_path = Path(get_prefs_file_path(PLATFORM))
        user_prefs_path.parent.mkdir(parents=True, exist_ok=True)

        user_prefs = {
            "project_path": project_path,
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

        logger.info(
            f"User preferences file created at {user_prefs_path}"
        )  # Log the path of the created file
    except Exception as e:
        logger.error(f"An error occurred while creating the user preferences file: {e}")
        raise


def delete_prefs_file():
    """
    Deletes the user_prefs.json file if it exists.
    """
    try:
        user_prefs_path = get_prefs_file_path(PLATFORM)
        if os.path.exists(user_prefs_path):
            os.remove(user_prefs_path)
            logger.info(f"User preferences file {user_prefs_path} deleted.")
        else:
            logger.warning(f"User preferences file {user_prefs_path} does not exist.")
    except Exception as e:
        logger.error(
            f"An error occurred while deleting the user preferences file {user_prefs_path}: {e}"
        )
        raise


prefs_file_read = False


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
    # Add a global variable to track if the prefs file has been read

    global prefs_file_read
    prefs_path = get_prefs_file_path(PLATFORM)
    try:
        if prefs_path.exists() and prefs_path.is_file():
            with open(prefs_path, "r") as prefs_file:
                defaults = json.load(prefs_file)
                if not prefs_file_read:
                    logger.info(f"Using preferences from {prefs_path}")
                    prefs_file_read = True
                return defaults.get(key, default_argument)
        else:
            logger.warning(
                f"The saved defaults file {prefs_path} is not readable or does not exist.  Using the provided default value."
            )
    except Exception as e:
        logger.error(f"An error occurred while getting the default value: {e}")
    return default_argument


def print_help(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(ctx.get_help(), color=ctx.color)
    ctx.exit()


@click.group(
    context_settings=dict(
        help_option_names=["-h", "--help"],
    )
)
@click.option("-h", "--help", is_flag=True, callback=print_help, expose_value=False, is_eager=True)
def cli():
    pass


@cli.command()
@click.option("-n", "--name", prompt="Project name", help="The name of the project.")
@click.option(
    "-p",
    "--path",
    prompt="Project path",
    default=str(Path.home() / "code"),
    help="The path where the project will be created.",
)
@click.option(
    "-un",
    "--user-name",
    default=None,
    help="The name of the user.",
)
@click.option(
    "-ue",
    "--user-email",
    default=None,
    help="The email of the user.",
)
@click.option(
    "-cmd",
    "--command",
    default=None,
    help="The name of the command.",
)
@click.option(
    "-pt",
    "--package-type",
    type=click.Choice(["setuptools", "hatchling", "poetry"], case_sensitive=False),
    default=None,
    help="The type of the package.",
)
@click.option(
    "-mpv",
    "--min-python-version",
    type=click.Choice(
        ["3.9", "3.10", "3.11"],
        case_sensitive=False,
    ),
    default=None,
    help="The minimum Python version required for the project.",
)
@click.option("-sp", "--save-prefs", is_flag=True, help="Save the current options as defaults.")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose logging (show debug logs).")
def create_project(
    name,
    path,
    user_name,
    user_email,
    command,
    package_type,
    save_prefs,
    min_python_version,
    verbose,
):
    """
    The main entry point for the script.
    """
    if verbose:
        logger.setLevel(logging.DEBUG)

    if path is None:
        path = click.prompt(
            "Please enter a project path",
            default=get_saved_prefs("path", str(Path.home() / "code")),
        )
    if user_name is None:
        user_name = get_saved_prefs("user_name", "Default User")
    if user_email is None:
        user_email = get_saved_prefs("user_email", "user@example.com")
    if command is None:
        command = get_saved_prefs("command", "cmd")
    if package_type is None:
        package_type = get_saved_prefs("package_type", "setuptools")
    if min_python_version is None:
        min_python_version = get_saved_prefs("min_python_version", "3.9")

    if save_prefs:
        create_prefs_file(path, user_name, user_email, package_type, min_python_version)

    try:
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
    except Exception as e:
        logger.error(f"An error occurred in create_project: {e}")
        raise


@cli.command()
def delete_prefs():
    """
    Deletes the user_prefs.json file if it exists.
    """
    delete_prefs_file()


@cli.command()
def summary():
    """Prints a summary of all commands and their options."""
    click.echo(click.style("Commands:", fg="green"))
    click.echo(click.style("  create-project", fg="blue"))
    click.echo("\tOptions:")
    click.echo(
        "\t" + click.style("-n, --name <TEXT>", fg="yellow") + "\t\t\t\t\tThe name of the project."
    )
    click.echo(
        "\t"
        + click.style("-p, --path <TEXT>", fg="yellow")
        + "\t\t\t\t\tThe path where the project will be created."
    )
    click.echo(
        "\t"
        + click.style("-un, --user-name <TEXT>", fg="yellow")
        + "\t\t\t\t\tThe name of the user."
    )
    click.echo(
        "\t"
        + click.style("-ue, --user-email <TEXT>", fg="yellow")
        + "\t\t\t\tThe email of the user."
    )
    click.echo(
        "\t"
        + click.style("-cmd, --command <TEXT>", fg="yellow")
        + "\t\t\t\t\tThe name of the command."
    )
    click.echo(
        "\t"
        + click.style("-pt, --package-type [setuptools|hatchling|poetry]", fg="yellow")
        + "\tThe type of the package."
    )
    click.echo(
        "\t"
        + click.style("-mpv, --min-python-version [3.9|3.10|3.11]", fg="yellow")
        + "\t\tThe minimum Python version required for the project."
    )
    click.echo(
        "\t"
        + click.style("-sp, --save-prefs", fg="yellow")
        + "\t\t\t\t\tSave the options as defaults:\n"
        + "\t\t\t\t\t\t\t\t\t[project path, user name, user email, package type, minimum Python version]"
    )
    click.echo(
        "\t"
        + click.style("-v, --verbose", fg="yellow")
        + "\t\t\t\t\t\tEnable verbose logging (show debug logs)."
    )
    click.echo(
        "\t" + click.style("-h, --help", fg="yellow") + "\t\t\t\t\t\tShow this message and exit."
    )
    click.echo(click.style("  delete-prefs", fg="blue"))
    click.echo("\tOptions:")
    click.echo(
        "\t" + click.style("-h, --help", fg="yellow") + "\t\t\t\t\t\tShow this message and exit."
    )


if __name__ == "__main__":
    cli()

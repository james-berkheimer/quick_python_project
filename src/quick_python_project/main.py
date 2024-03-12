import json
from pathlib import Path

import click

from . import project_generation


def get_default_value(key, default):
    defaults_path = Path.cwd() / "data" / "default_values.json"
    if defaults_path.exists():
        with open(defaults_path) as f:
            defaults = json.load(f)
            return defaults.get(key, default)
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
    default=get_default_value("command_name", "command"),
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
        ["3.0", "3.1", "3.2", "3.3", "3.4", "3.5", "3.6", "3.7", "3.8", "3.9", "3.10", "3.11"],
        case_sensitive=False,
    ),
    default=get_default_value("min_python_version", "3.9"),
    help="The minimum Python version required for the project.",
)
@click.option("--save-defaults", is_flag=True, help="Save the current options as defaults.")
def create_project(
    name, path, user_name, user_email, command_name, package_type, save_defaults, min_python_version
):
    """
    Create a new project with the specified name at the specified path.

    Parameters:
    ...
    min_python_version (str): The minimum Python version required for the project.
    """
    path = Path(path)
    project_root_path = path / name

    if save_defaults:
        defaults_path = Path.cwd() / "data" / "default_values.json"
        defaults_path.parent.mkdir(parents=True, exist_ok=True)
        with open(defaults_path, "w") as f:
            json.dump(
                {
                    "path": str(path),
                    "user_name": user_name,
                    "user_email": user_email,
                    "package_type": package_type,
                    "min_python_version": min_python_version,
                },
                f,
            )

    project_generation.generate_project_files(
        name,
        project_root_path,
        user_name,
        user_email,
        command_name,
        package_type,
        min_python_version,
    )
    click.echo(f"Created '{name}' project at '{project_root_path}'")
    click.echo(f"User: '{user_name}' with email '{user_email}'")
    click.echo(f"Command: '{command_name}'")
    click.echo(f"Package type: '{package_type}'")
    click.echo(f"Minimum Python version: '{min_python_version}'")

from pathlib import Path

import click

from . import project_generation


@click.command(
    help="""\b
    This script creates a new Python project with the specified name and command.

    Arguments:

        project_name: The name of the new project.

        command_name: The name of the command to launch the program. Default is 'cmd'.

        project_path: The path where the project will be created. Default is the user's home directory.

    Example:
    cli.py my_project my_command /path/to/project
    """
)
@click.argument("project_name")
@click.argument("command_name", default="cmd")
@click.argument("project_path", default=str(Path.home() / "code"))
def cli(project_name, command_name, project_path):
    """
    The main entry point for the script.
    """
    project_generation.create_project(project_name, command_name, project_path)


if __name__ == "__main__":
    cli()

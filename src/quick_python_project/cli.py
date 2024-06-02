from pathlib import Path

import click

from . import project_generation


@click.command(
    help="""\b
    This script creates a new Python project with the specified name and command.

    Arguments:

        project_name: The name of the new project.

        command_name: The name of the command to launch the program. Default is 'cmd'.

    Example:
    cli.py my_project my_command -d "requests" "numpy"
    """
)
@click.argument("project_name")
@click.argument("command_name", default="cmd")
def cli(project_name, command_name):
    """
    The main entry point for the script.
    """
    project_generation.create_project(project_name, str(Path.home() / "code"), command_name)


if __name__ == "__main__":
    cli()

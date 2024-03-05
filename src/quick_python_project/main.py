from pathlib import Path

import click

from quick_project import project_generation


@click.command()
@click.option("--name", prompt="Project name", help="The name of the project.")
@click.option(
    "--path",
    prompt="Project path",
    default=Path.home() / "code",
    help="The path where the project will be created.",
)
@click.option("--user-name", default="Default User", help="The name of the user.")
@click.option("--user-email", default="user@example.com", help="The email of the user.")
@click.option("--command-name", default="command", help="The name of the command.")
def create_project(name, path, user_name, user_email, command_name):
    """
    Create a new project with the specified name at the specified path.

    Parameters:
    name (str): The name of the project.
    path (str): The path where the project will be created.
    user_name (str): The name of the user.
    user_email (str): The email of the user.
    command_name (str): The name of the command.
    """
    project_root_path = path / name
    project_generation.create_directories(name, project_root_path)
    project_generation.generate_project_files(
        name, project_root_path, user_name, user_email, command_name
    )
    click.echo(f"Created '{name}' project at '{project_root_path}'")
    click.echo(f"User: '{user_name}' with email '{user_email}'")
    click.echo(f"Command: '{command_name}'")


def main():
    create_project()

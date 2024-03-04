import os

import click

from quick_project import project_generation


@click.command()
@click.option("--name", prompt="Project name", help="The name of the project.")
@click.option(
    "--path",
    prompt="Project path",
    default=os.path.join(os.getenv("HOME"), "code"),
    help="The path where the project will be created.",
)
def create_project(name, path):
    """This is a simple CLI that accepts a project name and path as options."""
    project_root_path = os.path.join(path, name)
    project_generation.create_directories(name, project_root_path)
    project_generation.generate_project_files(name, project_root_path)
    click.echo(f"Created '{name}' project at '{project_root_path}'")


def main():
    create_project()

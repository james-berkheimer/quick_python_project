import os
from pathlib import Path


def create_file_from_template(path, template_path, replacements):
    """
    Create a new file based on a template file, replacing placeholders with specified values.

    Parameters:
    path (str): The path where the new file will be created.
    template_path (str): The path to the template file.
    replacements (dict): A dictionary mapping placeholders to their replacement values.

    Returns:
    None
    """
    try:
        with open(template_path, "r") as template:
            content = template.read()

        for placeholder, value in replacements.items():
            content = content.replace(placeholder, value)

        with open(path, "w") as file:
            file.write(content)
    except Exception as e:
        print(f"Error creating file {path} from template {template_path}: {e}")


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
    Generate a set of project files based on templates, replacing placeholders with specified values.

    Parameters:
    project_name (str): The name of the project.
    project_root_path (str): The root path where the project files will be created.
    user_name (str): The user's name, used to replace placeholders in the templates.
    user_email (str): The user's email, used to replace placeholders in the templates.
    command_name (str): The command name, used to replace placeholders in the templates.
    package_type (str): The type of the package, used to select the appropriate pyproject.toml file.
    min_python_version (str): The minimum Python version required for the project.

    Returns:
    None
    """
    replacements = {
        "PLACEHOLDER_NAME": project_name,
        "<USERNAME>": user_name,
        "<USERNAME@example>": user_email,
        "PLACEHOLDER_CMD": command_name,
        "PYTHON_VERSION": f">={min_python_version}",
    }

    files_to_generate = [
        ("pyproject.toml", f"templates/{package_type}_pyproject.toml"),
        (".gitignore", "templates/.gitignore"),
        ("README.md", "templates/README.md"),
        ("LICENSE", "templates/LICENSE"),
        (f"src/{project_name}/main.py", "templates/main.py"),
    ]

    for file_name, template_name in files_to_generate:
        if file_name.endswith("_pyproject.toml"):
            file_path = Path(project_root_path) / "pyproject.toml"
        else:
            file_path = Path(project_root_path) / file_name
        file_path.parent.mkdir(parents=True, exist_ok=True)
        create_file_from_template(file_path, template_name, replacements)

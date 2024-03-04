import os


def create_directories(name, path):
    directories = [os.path.join(path, name), "src", name]
    root_path = ""
    for directory in directories:
        root_path = os.path.join(root_path, directory)
        os.makedirs(root_path, exist_ok=True)


def create_file_from_template(path, template_path, replacements):
    with open(template_path, "r") as template:
        content = template.read()

    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)

    with open(path, "w") as file:
        file.write(content)


def generate_project_files(project_name, project_root_path):
    # generate project_root_path/pyproject.toml file
    create_file_from_template(
        os.path.join(project_root_path, "pyproject.toml"),
        "templates/pyproject.toml",
        {"PLACEHOLDER_NAME": project_name},
    )

    # generate a python project_root_path/.gitignore file
    create_file_from_template(
        os.path.join(project_root_path, ".gitignore"),
        "templates/.gitignore",
        {"PLACEHOLDER_NAME": project_name},
    )

    # generate a project_root_path/README.md file
    create_file_from_template(
        os.path.join(project_root_path, "README.md"),
        "templates/README.md",
        {"PLACEHOLDER_NAME": project_name},
    )

    # generate a project_root_path/LICENSE file
    create_file_from_template(
        os.path.join(project_root_path, "LICENSE"),
        "templates/LICENSE",
        {"PLACEHOLDER_NAME": project_name},
    )

    # generate a project_root_path/src/project_name/main.py files in src/<name> directory
    os.makedirs(os.path.join(project_root_path, "src", project_name), exist_ok=True)
    create_file_from_template(
        os.path.join(project_root_path, "src", project_name, "main.py"),
        "templates/main.py",
        {"PLACEHOLDER_NAME": project_name},
    )

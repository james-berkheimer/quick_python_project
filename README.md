# Quick Python Project

## Description

Quick Python Project is a tool designed to streamline the creation and deployment of Python projects on PyPI. Originally conceived as a personal learning project, it aims to simplify the process of creating Python projects that can be quickly tested and run from the command line. The tool facilitates the creation of projects that utilize setuptools and a pyproject.toml file by default. Your feedback and suggestions for improvement are highly appreciated as I continue to enhance its functionality.

## Installation

```bash
pip install quick_python_project
```

## Usage

To create a new project using Quick Python Project, use the following command:

```bash
qpp create_project <project_name> <command_name> <project_path>
```

Replace `<project_name>` with the desired name of your project, `<command_name>` with the command that will be used to run your project, and optionally the path to the new project.  The default path will be /home/code

### Example:

```bash
qpp create_project my_project my_command /path/to/project
```

Once your project is created, you can navigate to its directory and run the specified command to execute it.

## Command Line Arguments

- `project_name`: The name of the new project.
- `command_name` (optional, default: 'cmd'): The name of the command to launch the program.
- `project_path` (optional, default: 'home/code'): The path to create the new project in.

### Example:

```bash
qpp create_project my_project my_command my_path
```

## Note

After creating your project, navigate to the project directory and follow these steps:

1. Set up a virtual environment:
```bash
python3 -m venv .venv
```

2. Activate the virtual environment:
```bash
source .venv/bin/activate
```

3. Perform an editable install of the project:
```bash
pip install -e .
```

4. Run the specified command:
```bash
my_command
```

This will execute your project, displaying any output to the console.

## Contributions

Contributions and feedback are welcome! If you have any suggestions or encounter any issues, please feel free to open an issue or submit a pull request on [GitHub](https://github.com/james-berkheimer/quick_python_project).

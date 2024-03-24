# Quick Python Project

## Description

This project is initially meant to be a learning process for how to build and deploy
a python project on PyPI.  I chose a project I have used to personally to creating
quick python projects that can be installed with pips editable install and run
by a command in a terminal in order to quickly test code.  I figured this might be usefull for others and I have done my best attempts to make
it more user friendly.  I will work on improving this as time allows with more features.

By default the projects use setuptools and a pyproject.toml.  But I have provided
defaults for Hatchling and Poetry.  Since I use neither of these, my defaults have
relied on reaserch and not experience.  Please feel free to propose any improvements.

## Installation

`pip install quick_python_project`

## Usage

Here's how you can use Quick Python Project:

```bash
qpp create_project --name MyProject --path ./my_project --user-name "Your Name" --user-email "your.email@example.com" --command myproject --package-type setuptools --min-python-version 3.9```
```

Here's what each option does:

- `--name`: The name of your project.
- `--path`: The directory where your project will be created.
- `--user-name`: Your name, which will be used in the project metadata.
- `--user-email`: Your email, which will be used in the project metadata.
- `--command`: The command that will be used to run your project.
- `--package-type`: The type of Python package to create. Can be `setuptools`, `hatchling`, or `poetry`.
- `--min-python-version`: The minimum Python version required for your project. Can be `3.9`, `3.10`, or `3.11`.

You can also save your preferences so you don't have to enter them every time:

```bash
qpp create_project --save-prefs --name MyProject --path ./my_project --user-name "Your Name" --user-email "your.email@example.com" --command myproject --package-type setuptools --min-python-version 3.9
```
And you can delete your saved preferences with the --delete-prefs option:
```bash
qpp delete_prefs
```

Once your project is created, you can navigate to the project directory and run your project with the command you specified:

```bash
cd my_project
# Install prefered virtual environment
python3 -m venv .venv
# Activate the virtual environment
source ./.venv/bin/activate
# Perform editable install of project
pip install -e .
# Run command
myproject
#This will print "Hello, world!" to the console.
```

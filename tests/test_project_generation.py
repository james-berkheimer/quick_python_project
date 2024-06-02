# FILEPATH: /home/james/code/quick_python_project/tests/test_project_generation.py
import os
import sys
import tempfile

import pytest

# Add the 'src' directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from quick_python_project.project_generation import create_file_from_template


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


def test_create_file_from_template(temp_dir):
    # Create a template file
    template_path = os.path.join(temp_dir, "template.txt")
    with open(template_path, "w") as template_file:
        template_file.write("Hello, {name}!")

    # Create a file from the template
    target_path = os.path.join(temp_dir, "output.txt")
    replacements = {"{name}": "World"}
    create_file_from_template(target_path, template_path, replacements)

    # Check if the file was created with the correct content
    assert os.path.exists(target_path)
    with open(target_path, "r") as output_file:
        content = output_file.read()
    assert content == "Hello, World!"


def test_create_file_from_template_nonexistent_template():
    with pytest.raises(FileNotFoundError):
        create_file_from_template("output.txt", "nonexistent_template.txt", {})


def test_create_file_from_template_replacements():
    # Create a template file
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_template:
        temp_template.write("Hello, {name}!")
        template_path = temp_template.name

    # Create a file from the template with replacements
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_output:
        output_path = temp_output.name
        replacements = {"{name}": "Universe"}
        create_file_from_template(output_path, template_path, replacements)

    # Check if the file was created with the correct content
    with open(output_path, "r") as output_file:
        content = output_file.read()
    assert content == "Hello, Universe!"

    # Clean up temporary files
    os.unlink(template_path)
    os.unlink(output_path)

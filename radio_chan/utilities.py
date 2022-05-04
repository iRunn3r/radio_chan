import os
from pathlib import Path


def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)


def write_to_file(message, path):
    absolute_path = Path(path)
    parent = absolute_path.parent.absolute()

    create_directory(parent)

    with open(path, "w") as f:
        f.write(message)

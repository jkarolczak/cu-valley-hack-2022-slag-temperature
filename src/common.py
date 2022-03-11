import os


def validate_path(file_path: str) -> None:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No such file or directory: {file_path}")

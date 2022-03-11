import os
from typing import List, Union


def validate_path(file_path: Union[str, List[str]]) -> None:
    if isinstance(file_path, str) and not os.path.exists(file_path):
        raise FileNotFoundError(f"No such file or directory: {file_path}")
    elif isinstance(file_path, list):
        for f in file_path:
            if not os.path.exists(f):
                raise FileNotFoundError(f"No such file or directory: {file_path}")

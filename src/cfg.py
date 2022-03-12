from typing import Dict

import yaml

from common import validate_path


def read(path: str) -> Dict:
    validate_path(path)
    with open(path) as fp:
        cfg = yaml.safe_load(fp)
    return cfg


def write(config: Dict, path: str) -> None:
    validate_path(path)
    with open(path, "w") as fp:
        yaml.dump(config, fp)

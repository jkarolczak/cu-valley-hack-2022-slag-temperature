from typing import Union, List, Dict

import neptune.new as neptune
import yaml

from common import validate_path


def get_run(secrets_path: str = "cfg/neptune.yaml", tags: Union[List[str], None] = None) -> neptune.Run:
    validate_path(secrets_path)
    with open(secrets_path) as fp:
        config = yaml.safe_load(fp)
    run = neptune.init(
        project=config["project"],
        api_token=config["api_token"],
        mode="async" if config["debug"] is False else "debug",
        tags=tags if tags is not None else []
    )
    return run


def model(run: neptune.Run, regressor: str, config: Dict) -> None:
    run["model/name"] = regressor
    for key, value in config.items():
        run[f"model/{key}"] = value


def dataset(run: neptune.Run, window_size: int, features: int) -> None:
    run["window_size"] = window_size
    run["features"] = features


def metrics(run: neptune.Run, metrics: Dict[str, float]) -> None:
    for key, value in metrics.items():
        run[key].log(value)

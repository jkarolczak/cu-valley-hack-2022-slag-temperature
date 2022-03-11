from typing import Dict

from .serialization import serialize
from ._xgboost import get_xgboost

MODELS = {
    "xgboost": get_xgboost
}


def get(model_name: str, config: Dict) -> object:
    if model_name not in MODELS.keys():
        raise KeyError(f"Invalid model name ({model_name})")
    regressor = MODELS[model_name](config)
    return regressor

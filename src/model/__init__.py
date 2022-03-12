from typing import Dict

from ._infer import infer
from ._lgbm import get_lgbm
from ._serialize import serialize
from ._sklearn import get_bayesian_ridge, get_lasso, get_random_forest, get_svr, get_tweedie_regressor, \
    get_decision_tree
from ._train import train
from ._xgboost import get_xgboost

MODELS = {
    "bayesianridge": get_bayesian_ridge,
    "lasso": get_lasso,
    "lgbm": get_lgbm,
    "randomforest": get_random_forest,
    "svr": get_svr,
    "decisiontree": get_decision_tree,
    "tweedieregressor": get_tweedie_regressor,
    "xgboost": get_xgboost
}


def get(model_name: str, config: Dict) -> object:
    model_name = model_name.lower().replace("_", "")
    if model_name not in MODELS.keys():
        raise KeyError(f"Invalid model name ({model_name})")
    regressor = MODELS[model_name](config)
    return regressor

from typing import Dict

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import BayesianRidge, Lasso, TweedieRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor


def get_bayesian_ridge(config: Dict) -> BayesianRidge:
    return BayesianRidge(**config)


def get_lasso(config: Dict) -> Lasso:
    return Lasso(**config)


def get_random_forest(config: Dict) -> RandomForestRegressor:
    return RandomForestRegressor(**config)


def get_svr(config: Dict) -> SVR:
    return SVR(**config)


def get_decision_tree(config: Dict) -> DecisionTreeRegressor:
    return DecisionTreeRegressor(**config)


def get_tweedie_regressor(config: Dict) -> TweedieRegressor:
    return TweedieRegressor(**config)

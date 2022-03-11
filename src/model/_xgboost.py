from typing import Dict

import xgboost as xgb


def get_xgboost(config: Dict) -> xgb.XGBRegressor:
    return xgb.XGBRegressor(**config)

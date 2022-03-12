from typing import Dict

import lightgbm as lgbm


def get_lgbm(config: Dict) -> lgbm.LGBMRegressor:
    return lgbm.LGBMRegressor(**config)

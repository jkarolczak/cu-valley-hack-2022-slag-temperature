import pickle
from typing import Dict

import pandas as pd
from sklearn.metrics import mean_absolute_error

from data import read_holdout


def infer(config: Dict) -> None:
    X, y, time = read_holdout(config)
    with open(config["model_path"], "rb") as fp:
        regressor = pickle.load(fp)

    predictions = pd.DataFrame({"czas": time, "temp": regressor.predict(X)})
    predictions.to_csv(config["predictions_path"], index=False)

    if config["show_metrics"]:
        mae = mean_absolute_error(predictions["temp"], y)
        print(f"MAE: {mae}")

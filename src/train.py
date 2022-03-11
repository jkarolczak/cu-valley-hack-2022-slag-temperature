from typing import Dict

from sklearn.metrics import mean_absolute_error

import cfg
import data
import model
import log


def train(config: Dict) -> None:
    model_name = config["model"]["name"]
    model_config = cfg.read(config["model"]["config_file"])
    regressor = model.get(model_name, model_config)

    run = log.get_run("../resources/cfg/neptune.yaml")
    log.model(run, model_name, model_config)

    X_train, X_test, y_train, y_test = data.read_datasets(config["dataset"])
    regressor.fit(X_train, y_train)
    model.serialize(regressor, model_name, directory=config["serialization"]["directory"])

    y_pred = regressor.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)

    log.mae(run, mae)

    run.stop()

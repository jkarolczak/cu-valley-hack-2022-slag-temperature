import argparse
import os
import pickle
import shutil
import sys
import zipfile

import pandas as pd
import xgboost as xgb

sys.path.append("src/")
from common import validate_path
from data import aggregate_inputs, read_inputs


def parse_input(archive_path: str) -> pd.DataFrame:
    validate_path(archive_path)
    with zipfile.ZipFile(archive_path, "r") as fp:
        fp.extractall(".tempdata")
    data_directory = os.path.join(".tempdata", os.listdir(".tempdata")[0])
    df_features, df_temperature = read_inputs(data_directory)
    df = aggregate_inputs(df_features, df_temperature, 30, mode="infer")
    if "temp" in df.columns:
        raise ValueError("Column temp wasn't removed from the input data")
    X = df.drop(columns=["czas"])
    time = df["czas"]
    return X, time


def unpickle_regressor() -> xgb.XGBRegressor:
    with open("static/model.pkl", "rb") as fp:
        model = pickle.load(fp)
    return model


def main(args: argparse.Namespace) -> None:
    X, time = parse_input(args.archive)
    regressor = unpickle_regressor()
    predictions = regressor.predict(X)
    df = pd.DataFrame({"czas": time, "temp": predictions})
    df.to_csv("predictions.csv", index=False)
    shutil.rmtree(".tempdata")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--archive', type=str, default="data.zip",
                        help="path to the input archive")
    arguments = parser.parse_args()
    main(arguments)

import gzip
import os
import re
from typing import Dict, Tuple

import pandas as pd
from sklearn.model_selection import train_test_split

import cfg
from common import validate_path


def gzip_to_dataframe(directory: str, file: str, time_col: str = "czas", sep: str = ",") -> pd.DataFrame:
    path = os.path.join(directory, file)
    validate_path(path)
    with gzip.open(path, "rb") as fp:
        df = pd.read_csv(fp, sep=sep)
    df[time_col] = pd.to_datetime(df[time_col], utc=True).dt.tz_convert(None)
    return df


def read_temp(directory: str, file: str = "temp_zuz.csv", time_col: str = "Czas", sep: str = ";") -> pd.DataFrame:
    path = os.path.join(directory, file)
    validate_path(path)
    df = pd.read_csv(path, sep=sep)
    df[time_col] = pd.to_datetime(df[time_col])
    df = df.rename(columns={"Czas": "czas"})
    return df


def read_inputs(directory_path: str = "resources/data") -> pd.DataFrame:
    validate_path(directory_path)
    all_files = os.listdir(directory_path)
    df_temperature = read_temp(directory_path)
    pattern = re.compile(r"avg_from.+\.gz")
    features_files = [f for f in all_files if pattern.match(f)]
    for idx, file_name in enumerate(features_files):
        df = gzip_to_dataframe(directory_path, file_name)
        if not idx:
            df_features = df.copy()
        else:
            df_features = pd.concat([df_features, df])
    df_features = df_features.reset_index()
    return df_features, df_temperature


def _rename(col):
    if isinstance(col, tuple):
        col = '_'.join(str(c) for c in col)
    return col


def window_statistics(df: pd.DataFrame) -> pd.DataFrame:
    df = df.groupby(lambda _: True).agg(['min', 'max', 'mean', 'std', 'skew', pd.DataFrame.kurt])
    df.columns = map(_rename, df.columns)
    return df


def aggregate_inputs(df_features: pd.DataFrame, df_temperature: pd.DataFrame, window_size: int) -> pd.DataFrame:
    feature_columns = set(df_features.columns).difference(set(["czas", "index"]))

    delta = pd.Timedelta(window_size, unit='m')
    for idx, row in enumerate(df_temperature.iterrows()):
        timestamp = row[1].czas
        window = df_features[(df_features["czas"] <= timestamp) & (timestamp - delta < df_features["czas"])]
        window_features = window[feature_columns]
        window_stats = window_statistics(window_features)
        window_stats.insert(0, "czas", [row[1].czas])
        window_stats.insert(1, "temp", [row[1].temp_zuz])
        if not idx:
            df_aggregated = window_stats
        else:
            df_aggregated = pd.concat([df_aggregated, window_stats])
    df_aggregated = df_aggregated.reset_index(drop=True).iloc[:-1]
    return df_aggregated


def read_datasets(config: Dict) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    train_path = os.path.join(config["directory"], config["filenames"]["train"])
    test_path = os.path.join(config["directory"], config["filenames"]["test"])

    validate_path([train_path, test_path])
    train, test = pd.read_csv(train_path), pd.read_csv(test_path)

    X_train = train.drop(columns=[config["columns"]["time"], config["columns"]["temperature"]])
    X_test = test.drop(columns=[config["columns"]["time"], config["columns"]["temperature"]])

    y_train = train[config["columns"]["temperature"]]
    y_test = test[config["columns"]["temperature"]]
    return X_train, X_test, y_train, y_test


def read_holdout(config: Dict) -> Tuple[pd.DataFrame, pd.DataFrame]:
    validate_path(config["holdout_path"])
    holdout = pd.read_csv(config["holdout_path"])

    y = holdout[config["columns"]["temperature"]]
    time = holdout[config["columns"]["time"]]
    X = holdout.drop(columns=[config["columns"]["time"], config["columns"]["temperature"]])

    return X, y, time


def split_dataset(config: Dict) -> None:
    if sum([v for v in config["sizes"].values()]) != 1:
        raise ValueError("Sizes of all datasets have to sum-up to 1.0")

    train_size = config["sizes"]["train"]
    test_size = config["sizes"]["test"] / (config["sizes"]["test"] + config["sizes"]["holdout"])

    df = pd.read_csv(config["paths"]["dataset"])

    df_train, df = train_test_split(df, train_size=train_size, shuffle=config["shuffle"])
    df_test, df_holdout = train_test_split(df, train_size=test_size, shuffle=config["shuffle"])

    os.makedirs(config["paths"]["output"], exist_ok=True)

    df_train.reset_index(drop=True).to_csv(os.path.join(config["paths"]["output"], config["filenames"]["train"]),
                                           index=False)
    df_test.reset_index(drop=True).to_csv(os.path.join(config["paths"]["output"], config["filenames"]["test"]),
                                          index=False)
    df_holdout.reset_index(drop=True).to_csv(os.path.join(config["paths"]["output"], config["filenames"]["holdout"]),
                                             index=False)


def select_variables(config: Dict) -> None:
    df_path = config["input_dataset_file"]
    validate_path(df_path)
    df = pd.read_csv(df_path)
    num_columns = df.shape[1] - (len(config["columns"]) + 2)
    df = df.drop(columns=config["columns"])
    df.to_csv(config["output_dataset_file"], index=False)

    validate_path(config["train_cfg"])
    train_cfg = cfg.read(config["train_cfg"])
    train_cfg["dataset"]["features"] = num_columns
    cfg.write(train_cfg, config["train_cfg"])

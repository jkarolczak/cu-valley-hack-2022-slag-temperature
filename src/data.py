import argparse
import gzip
import os
import re

import pandas as pd

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
    df_aggregated = df_aggregated.reset_index()
    return df_aggregated


def main(args) -> int:
    df_features, df_temperature = read_inputs(args.data_dir)
    aggregated = aggregate_inputs(df_features, df_temperature, window_size=args.window_size)
    aggregated.to_csv(args.output_file, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--window_size', type=int, default=60, help="window size")
    parser.add_argument('--data_dir', type=str, default="../resources/data",
                        help="path to the directory with the input files")
    parser.add_argument('--output_file', type=str, default="../resources/aggregated.csv",
                        help="path to the file to store the generated data")
    arguments = parser.parse_args()
    main(arguments)

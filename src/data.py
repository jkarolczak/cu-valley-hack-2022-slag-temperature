import gzip
import os
import re

import pandas as pd

from common import validate_path


def read_temp(directory: str, file: str = "temp_zuz.csv", time_col: str = "Czas", sep: str = ";") -> pd.DataFrame:
    path = os.path.join(directory, file)
    df = pd.read_csv(path, sep=sep)
    df[time_col] = pd.to_datetime(df[time_col])
    df.rename(columns={"Czas": "czas"})
    return df


def aggregate_inputs(directory_path: str = "resources/data") -> pd.DataFrame:
    validate_path(directory_path)
    all_files = os.listdir(directory_path)
    df_temperature = read_temp(directory_path)
    pattern = re.compile(r"avg_from.+\.gz")
    features_files = [f for f in all_files if pattern.match(f)]
    for file_name in features_files:
        file_path = os.path.join(directory_path, file_name)
        ...

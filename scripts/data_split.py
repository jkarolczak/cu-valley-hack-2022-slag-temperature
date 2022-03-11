import argparse
import os

import pandas as pd
from sklearn.model_selection import train_test_split

import cfg
from common import validate_path


def main(args: argparse.Namespace) -> None:
    path = args.dataset_cfg
    validate_path(path)
    config = cfg.read(path)
    if sum([v for v in config["sizes"].values()]) != 1:
        raise ValueError("Sizes of all datasets have to sum-up to 1.0")

    train_size = config["sizes"]["train"]
    test_size = config["sizes"]["test"] / (config["sizes"]["test"] + config["sizes"]["holdout"])

    df = pd.read_csv(config["paths"]["dataset"])

    df_train, df = train_test_split(df, train_size=train_size, shuffle=config["shuffle"])
    df_test, df_holdout = train_test_split(df, train_size=test_size, shuffle=config["shuffle"])

    os.makedirs(config["paths"]["output"], exist_ok=True)

    df_train.reset_index(drop=True).to_csv(os.path.join(config["paths"]["output"], config["filenames"]["train"]))
    df_test.reset_index(drop=True).to_csv(os.path.join(config["paths"]["output"], config["filenames"]["test"]))
    df_holdout.reset_index(drop=True).to_csv(os.path.join(config["paths"]["output"], config["filenames"]["holdout"]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_cfg', type=str, default="../resources/cfg/dataset.yaml",
                        help="path to the file containing dataset split configuration")
    arguments = parser.parse_args()
    main(arguments)

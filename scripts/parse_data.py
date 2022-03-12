import argparse

import cfg
from common import validate_path
from data import aggregate_inputs, read_inputs


def main(args: argparse.Namespace) -> None:
    config = cfg.read(args.cfg)

    validate_path(config["data_dir"])
    df_features, df_temperature = read_inputs(config["data_dir"])

    aggregated = aggregate_inputs(df_features, df_temperature, window_size=config["window_size"])
    aggregated.to_csv(config["output_file"], index=False)

    validate_path(config["train_cfg"])
    train_cfg = cfg.read(config["train_cfg"])
    train_cfg["dataset"]["window_size"] = config["window_size"]
    cfg.write(train_cfg, config["train_cfg"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg', type=str, default="../resources/cfg/parse_data.yaml",
                        help="path to the file containing data parsing configuration")
    arguments = parser.parse_args()
    main(arguments)

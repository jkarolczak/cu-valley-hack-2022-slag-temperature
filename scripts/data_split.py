import argparse

import cfg
from data import split_dataset


def main(args: argparse.Namespace) -> None:
    config = cfg.read(args.cfg)
    split_dataset(config)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg', type=str, default="../resources/cfg/dataset_split.yaml",
                        help="path to the file containing dataset split configuration")
    arguments = parser.parse_args()
    main(arguments)

import argparse

import cfg
from train import train
from common import validate_path


def main(args: argparse.Namespace) -> None:
    validate_path(args.train_cfg)
    config = cfg.read(args.train_cfg)
    train(config)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_cfg', type=str, default="../resources/cfg/train.yaml",
                        help="path to the file that contains training parameters")
    arguments = parser.parse_args()
    main(arguments)

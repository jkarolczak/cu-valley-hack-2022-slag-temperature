import argparse

import cfg
from model import infer


def main(args: argparse.Namespace) -> None:
    config = cfg.read(args.cfg)
    infer(config)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg', type=str, default="../resources/cfg/inference.yaml",
                        help="path to the file that contains inference configuration")
    arguments = parser.parse_args()
    main(arguments)

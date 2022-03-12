import argparse

import cfg
from data import select_variables


def main(args: argparse.Namespace) -> None:
    config = cfg.read(args.cfg)
    select_variables(config)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg', type=str, default="../resources/cfg/variable_selection.yaml",
                        help="path to the file that contains variable selection process configuration")
    arguments = parser.parse_args()
    main(arguments)

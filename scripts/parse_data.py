import argparse

from data import aggregate_inputs, read_inputs


def main(args: argparse.Namespace) -> None:
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

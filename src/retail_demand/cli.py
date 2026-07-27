import argparse
from collections.abc import Sequence
from pathlib import Path

from retail_demand.application.generate_demo import generate_and_save_demo_data
from retail_demand.data.generation import DemoDataParameters


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="retail-demand")
    commands = parser.add_subparsers(dest="command", required=True)
    generate = commands.add_parser("generate-data", help="generate synthetic retail datasets")
    generate.add_argument("--stores", type=_positive_integer, required=True)
    generate.add_argument("--products", type=_positive_integer, required=True)
    generate.add_argument("--days", type=_positive_integer, required=True)
    generate.add_argument("--seed", type=_non_negative_integer, required=True)
    generate.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args(argv)

    if arguments.command == "generate-data":
        parameters = DemoDataParameters(
            stores=arguments.stores,
            products=arguments.products,
            days=arguments.days,
            seed=arguments.seed,
        )
        summary = generate_and_save_demo_data(parameters, arguments.output)
        print(f"Synthetic data written to {summary.output}")
        for dataset, rows in summary.row_counts.items():
            print(f"{dataset}: {rows} rows")


def _positive_integer(value: str) -> int:
    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return parsed


def _non_negative_integer(value: str) -> int:
    parsed = int(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("must be at least 0")
    return parsed

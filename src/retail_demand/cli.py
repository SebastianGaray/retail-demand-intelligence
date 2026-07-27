import argparse
from collections.abc import Sequence
from pathlib import Path
from typing import cast

from retail_demand.application.generate_demo import generate_and_save_demo_data
from retail_demand.application.train import (
    evaluate_forecasters,
    save_champion_predictions,
    train_forecasters,
)
from retail_demand.artifacts.metadata import ForecastConfiguration
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

    train = commands.add_parser("train", help="train baselines and LightGBM")
    train.add_argument("--data", type=Path, required=True)
    train.add_argument("--output", type=Path, required=True)
    train.add_argument("--horizon", type=_positive_integer, default=28)
    train.add_argument("--seed", type=_non_negative_integer, default=42)

    evaluate = commands.add_parser("evaluate", help="evaluate a trained artifact")
    evaluate.add_argument("--data", type=Path, required=True)
    evaluate.add_argument("--artifact", type=Path, required=True)

    predictions = commands.add_parser("predictions", help="save champion test predictions")
    predictions.add_argument("--artifact", type=Path, required=True)
    arguments = parser.parse_args(argv)

    if arguments.command == "generate-data":
        parameters = DemoDataParameters(
            stores=cast(int, arguments.stores),
            products=cast(int, arguments.products),
            days=cast(int, arguments.days),
            seed=cast(int, arguments.seed),
        )
        summary = generate_and_save_demo_data(parameters, cast(Path, arguments.output))
        print(f"Synthetic data written to {summary.output}")
        for dataset, rows in summary.row_counts.items():
            print(f"{dataset}: {rows} rows")
    elif arguments.command == "train":
        metadata = train_forecasters(
            cast(Path, arguments.data),
            cast(Path, arguments.output),
            ForecastConfiguration(
                horizon=cast(int, arguments.horizon),
                seed=cast(int, arguments.seed),
            ),
        )
        print(f"Training artifact written to {arguments.output}")
        print(f"Champion: {metadata.champion_model}")
    elif arguments.command == "evaluate":
        metrics = evaluate_forecasters(
            cast(Path, arguments.data),
            cast(Path, arguments.artifact),
        )
        print(metrics[metrics["scope"] == "overall"].to_string(index=False))
    elif arguments.command == "predictions":
        output = save_champion_predictions(cast(Path, arguments.artifact))
        print(f"Predictions written to {output}")


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

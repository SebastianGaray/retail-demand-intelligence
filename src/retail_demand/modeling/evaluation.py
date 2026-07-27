from collections.abc import Sequence

import pandas as pd


def mae(actual: Sequence[float], predicted: Sequence[float]) -> float:
    pairs = list(zip(actual, predicted, strict=True))
    return sum(abs(observed - forecast) for observed, forecast in pairs) / len(pairs)


def wape(actual: Sequence[float], predicted: Sequence[float]) -> float | None:
    numerator = sum(
        abs(observed - forecast) for observed, forecast in zip(actual, predicted, strict=True)
    )
    denominator = sum(abs(observed) for observed in actual)
    return numerator / denominator if denominator else None


def mase(
    actual: Sequence[float],
    predicted: Sequence[float],
    training: Sequence[float],
    seasonality: int = 7,
) -> float | None:
    if len(training) <= seasonality:
        return None
    scale = sum(
        abs(training[index] - training[index - seasonality])
        for index in range(seasonality, len(training))
    ) / (len(training) - seasonality)
    return mae(actual, predicted) / scale if scale else None


def calculate_metrics(
    predictions: pd.DataFrame,
    training_history: pd.DataFrame,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for model, model_predictions in predictions.groupby("model", sort=False):
        rows.append(_metric_row("overall", "all", str(model), model_predictions, training_history))
        for field, scope in (("store_id", "store"), ("product_id", "product")):
            for identifier, group in model_predictions.groupby(field, sort=False):
                history = training_history[training_history[field] == identifier]
                rows.append(_metric_row(scope, str(identifier), str(model), group, history))
    return pd.DataFrame(rows)


def _metric_row(
    scope: str,
    identifier: str,
    model: str,
    predictions: pd.DataFrame,
    history: pd.DataFrame,
) -> dict[str, object]:
    actual = predictions["actual"].astype(float).tolist()
    predicted = predictions["prediction"].astype(float).tolist()
    training = history.sort_values(["store_id", "product_id", "date"])
    seasonal_errors = (
        training.groupby(["store_id", "product_id"], sort=False)["quantity"].diff(7).abs().dropna()
    )
    scale = float(seasonal_errors.mean()) if not seasonal_errors.empty else None
    absolute_error = mae(actual, predicted)
    return {
        "scope": scope,
        "identifier": identifier,
        "model": model,
        "mae": absolute_error,
        "wape": wape(actual, predicted),
        "mase": absolute_error / scale if scale else None,
        "observations": len(actual),
    }

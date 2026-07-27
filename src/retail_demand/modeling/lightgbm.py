from collections.abc import Callable, Sequence
from typing import cast

import pandas as pd
from lightgbm import LGBMRegressor
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder

from retail_demand.features.temporal import CATEGORICAL_FEATURES, FEATURE_COLUMNS


def build_model(seed: int) -> Pipeline:
    preprocessing = ColumnTransformer(
        [
            (
                "categories",
                OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1),
                CATEGORICAL_FEATURES,
            )
        ],
        remainder="passthrough",
    )
    regressor = LGBMRegressor(
        n_estimators=200,
        learning_rate=0.05,
        num_leaves=31,
        random_state=seed,
        n_jobs=1,
        verbosity=-1,
    )
    return Pipeline([("preprocessing", preprocessing), ("model", regressor)])


def fit_model(frame: pd.DataFrame, seed: int) -> Pipeline:
    model = build_model(seed)
    fit = cast(Callable[[pd.DataFrame, pd.Series], object], model.fit)  # pyright: ignore[reportUnknownMemberType]
    fit(frame[FEATURE_COLUMNS], frame["quantity"])
    return model


def predict(model: Pipeline, frame: pd.DataFrame) -> pd.Series:
    predictor = cast(Callable[[pd.DataFrame], Sequence[float]], model.predict)  # pyright: ignore[reportUnknownMemberType]
    values = predictor(frame[FEATURE_COLUMNS])
    return pd.Series(values, index=frame.index, dtype=float).clip(lower=0)

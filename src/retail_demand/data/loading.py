from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import pandas as pd
from pydantic import BaseModel, ValidationError

from retail_demand.data.schemas import DatasetContract
from retail_demand.domain.errors import DatasetValidationError, DatasetValidationIssue


def load_parquet[RecordT: BaseModel](
    path: Path, contract: DatasetContract[RecordT]
) -> tuple[RecordT, ...]:
    try:
        frame = pd.read_parquet(path)
    except (FileNotFoundError, OSError, ValueError) as error:
        raise DatasetValidationError(
            [DatasetValidationIssue(contract.name, "<file>", str(error))]
        ) from error

    records = frame.astype(object).where(pd.notna(frame), None).to_dict(orient="records")
    return validate_records(records, contract)


def validate_records[RecordT: BaseModel](
    records: Sequence[Mapping[Any, Any]], contract: DatasetContract[RecordT]
) -> tuple[RecordT, ...]:
    validated: list[RecordT] = []
    issues: list[DatasetValidationIssue] = []

    for row_number, record in enumerate(records):
        try:
            validated.append(contract.model.model_validate(record))
        except ValidationError as error:
            issues.extend(
                DatasetValidationIssue(
                    dataset=contract.name,
                    row=row_number,
                    field=".".join(str(part) for part in detail["loc"]) or "<row>",
                    problem=str(detail["msg"]),
                )
                for detail in error.errors()
            )

    if issues:
        raise DatasetValidationError(issues)

    _validate_unique_keys(validated, contract)
    return tuple(validated)


def _validate_unique_keys[RecordT: BaseModel](
    records: list[RecordT], contract: DatasetContract[RecordT]
) -> None:
    seen: dict[tuple[object, ...], int] = {}
    issues: list[DatasetValidationIssue] = []

    for row_number, record in enumerate(records):
        key = tuple(getattr(record, field) for field in contract.key)
        if key in seen:
            issues.append(
                DatasetValidationIssue(
                    dataset=contract.name,
                    row=row_number,
                    field=", ".join(contract.key),
                    problem=f"duplicate key; first seen at row {seen[key]}",
                )
            )
        else:
            seen[key] = row_number

    if issues:
        raise DatasetValidationError(issues)

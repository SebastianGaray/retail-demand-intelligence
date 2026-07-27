from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DatasetValidationIssue:
    dataset: str
    field: str
    problem: str
    row: int | None = None

    def __str__(self) -> str:
        location = f" row {self.row}" if self.row is not None else ""
        return f"{self.dataset}{location}, field '{self.field}': {self.problem}"


class DatasetValidationError(ValueError):
    def __init__(self, issues: list[DatasetValidationIssue]) -> None:
        self.issues = tuple(issues)
        super().__init__(". ".join(str(issue) for issue in issues))

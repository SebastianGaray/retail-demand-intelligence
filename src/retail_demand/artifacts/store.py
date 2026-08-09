import hashlib
import pickle
from pathlib import Path

from sklearn.pipeline import Pipeline

from retail_demand.artifacts.metadata import ArtifactMetadata


def save_model(model: Pipeline, path: Path) -> str:
    temporary = path.with_suffix(".tmp")
    temporary.write_bytes(pickle.dumps(model, protocol=pickle.HIGHEST_PROTOCOL))
    temporary.replace(path)
    return sha256(path)


def load_model(path: Path, expected_sha256: str) -> Pipeline:
    payload = path.read_bytes()
    actual_sha256 = hashlib.sha256(payload).hexdigest()
    if actual_sha256 != expected_sha256:
        raise ValueError(f"Model checksum mismatch for {path}")
    model: object = pickle.loads(payload)
    if not isinstance(model, Pipeline):
        raise ValueError(f"{path} does not contain a scikit-learn pipeline")
    return model


def save_metadata(metadata: ArtifactMetadata, path: Path) -> None:
    temporary = path.with_suffix(".tmp")
    temporary.write_text(metadata.model_dump_json(indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def load_metadata(path: Path) -> ArtifactMetadata:
    return ArtifactMetadata.model_validate_json(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

"""Pinned Imre acquisition; only verified local files become usable."""
from dataclasses import dataclass
import errno
import fcntl
import hashlib
import os
from pathlib import Path
import shutil
import tempfile
from typing import Callable
import urllib.error
import urllib.request


MODEL_REVISION = "cf910fb59f1d79ab3b625a63993a108751c6c25d"
MODEL_SOURCE = f"https://huggingface.co/rhasspy/piper-voices/tree/{MODEL_REVISION}/hu/hu_HU/imre/medium"


@dataclass(frozen=True)
class ModelArtifact:
    name: str
    sha256: str
    size: int


MODEL_ARTIFACTS = (
    ModelArtifact("hu_HU-imre-medium.onnx", "bcec8e6e5404baca0fcaf2895da4d02d414d3340b9f80bd94a2112b5c67061ae", 63221984),
    ModelArtifact("hu_HU-imre-medium.onnx.json", "760857edbd31947a853842df5833bd16aa1f660feabe11fbebb0a378bf8328c5", 5458),
    ModelArtifact("MODEL_CARD", "948c1d744bfe1431ad06bcc3aa1e8be2ff275b46c80dda7e8c5d05ae4722bf4c", 420),
)
DOWNLOAD_BYTES = sum(item.size for item in MODEL_ARTIFACTS)
DISK_BYTES = DOWNLOAD_BYTES * 2 + 1024 * 1024


def default_model_path() -> Path:
    override = os.environ.get("AUDIOBOOK_MODEL_PATH")
    return Path(override) if override else Path.home() / "Library/Application Support/HangosKonyv/models/piper-imre"


@dataclass(frozen=True)
class ModelStatus:
    state: str
    completed_bytes: int = 0
    total_bytes: int = DOWNLOAD_BYTES
    disk_bytes: int = DISK_BYTES
    source: str = MODEL_SOURCE
    license_source: str = MODEL_SOURCE.replace("/tree/", "/blob/") + "/MODEL_CARD"


class ModelError(Exception):
    """An actionable download or local-integrity failure."""


class ModelStore:
    def __init__(self, path: Path):
        self.path = path

    def status(self) -> ModelStatus:
        if not self.path.exists():
            return ModelStatus("model_missing")
        for artifact in MODEL_ARTIFACTS:
            path = self.path / artifact.name
            if path.is_symlink() or not path.is_file() or path.stat().st_size != artifact.size:
                return ModelStatus("model_damaged")
            with path.open("rb") as stream:
                if hashlib.file_digest(stream, "sha256").hexdigest() != artifact.sha256:
                    return ModelStatus("model_damaged")
        return ModelStatus("model_ready", DOWNLOAD_BYTES)

    def prepare(self, notify: Callable[[ModelStatus], None]) -> ModelStatus:
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with (self.path.parent / ".piper-imre-install.lock").open("a") as lock:
                try:
                    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except BlockingIOError as error:
                    raise ModelError("A modell letöltése egy másik alkalmazásban már folyamatban van. Próbáld újra később.") from error
                if self.status().state == "model_ready":
                    result = self.status()
                    notify(result)
                    return result
                if shutil.disk_usage(self.path.parent).free < DISK_BYTES:
                    raise ModelError("Nincs elég szabad tárhely a modell letöltéséhez. Szabadíts fel legalább 128 MB-ot, majd próbáld újra.")
                notify(ModelStatus("model_downloading"))
                with tempfile.TemporaryDirectory(dir=self.path.parent, prefix="piper-download-") as folder:
                    staged = Path(folder)
                    completed = 0
                    for artifact in MODEL_ARTIFACTS:
                        base = f"https://huggingface.co/rhasspy/piper-voices/resolve/{MODEL_REVISION}/hu/hu_HU/imre/medium/"
                        checksum = hashlib.sha256()
                        received = 0
                        with urllib.request.urlopen(base + artifact.name, timeout=30) as response, (staged / artifact.name).open("wb") as stream:
                            while chunk := response.read(256 * 1024):
                                received += len(chunk)
                                if received > artifact.size:
                                    raise ModelError("A letöltött modell mérete hibás. Próbáld újra a letöltést.")
                                stream.write(chunk)
                                checksum.update(chunk)
                                completed += len(chunk)
                                notify(ModelStatus("model_downloading", completed))
                        if received != artifact.size or checksum.hexdigest() != artifact.sha256:
                            raise ModelError("A letöltött Piper Imre modell sérült vagy hiányos. Próbáld újra a letöltést.")
                    self.path.mkdir(exist_ok=True)
                    for artifact in MODEL_ARTIFACTS:
                        (staged / artifact.name).replace(self.path / artifact.name)
                result = self.status()
                if result.state != "model_ready":
                    raise ModelError("A modell ellenőrzése sikertelen. Próbáld újra a letöltést.")
                notify(result)
                return result
        except (urllib.error.URLError, TimeoutError) as error:
            raise ModelError("Nem sikerült a modell letöltése. Ellenőrizd a hálózatot, és próbáld újra.") from error
        except OSError as error:
            message = ("Elfogyott a tárhely a modell letöltése közben. Szabadíts fel helyet és próbáld újra."
                       if error.errno == errno.ENOSPC else "A modell nem menthető. Ellenőrizd a tárhelyet és a mappa hozzáférését, majd próbáld újra.")
            raise ModelError(message) from error

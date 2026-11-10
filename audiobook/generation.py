"""The public file-to-MP3 generation boundary used by the Mac app."""
from dataclasses import dataclass
from pathlib import Path
import os
import hashlib
import shutil
import subprocess
import tempfile
import unicodedata
from typing import Callable


@dataclass(frozen=True)
class SourcePreview:
    text: str
    digest: str


@dataclass(frozen=True)
class JobEvent:
    state: str


@dataclass(frozen=True)
class GenerationResult:
    output: Path


SpeechRenderer = Callable[[str, Path, Callable[[str], None]], None]


class GenerationError(Exception):
    """An actionable error safe to display in the application."""


class GenerationService:
    def __init__(self, speech_renderer: SpeechRenderer | None = None, model_path: Path | None = None):
        from .speech import MlxSpeechRenderer

        self.speech_renderer = speech_renderer or MlxSpeechRenderer(
            model_path or Path(__file__).resolve().parents[1] / ".local/models/OmniVoice-bfloat16"
        )

    def preview(self, source: Path) -> SourcePreview:
        if source.suffix.lower() != ".txt":
            raise GenerationError("Ebben a változatban TXT-fájlt válassz.")
        try:
            with source.open("rb") as stream:
                data = stream.read(2404)
            if len(data) > 2403:
                raise GenerationError("Ez a fejlesztői változat legfeljebb 600 karakteres TXT-fájlt kezel.")
            text = data.decode("utf-8-sig").strip()
        except UnicodeError as error:
            raise GenerationError("A fájl nem érvényes UTF-8 szöveg. Mentsd UTF-8 kódolással.") from error
        except OSError as error:
            raise GenerationError("A szövegfájl nem olvasható. Ellenőrizd a fájlt és a hozzáférést.") from error
        if len(text) > 600:
            raise GenerationError("Ez a fejlesztői változat legfeljebb 600 karakteres TXT-fájlt kezel.")
        if not text:
            raise GenerationError("A kiválasztott fájl üres.")
        if any(unicodedata.category(c) == "Cc" and c not in "\n\r\t" for c in text):
            raise GenerationError("A fájl szöveg helyett bináris vezérlőjeleket tartalmaz.")
        return SourcePreview(text, hashlib.sha256(text.encode("utf-8")).hexdigest())

    def generate(
        self, source: Path, output: Path, *, notify: Callable[[JobEvent], None] = lambda event: None,
        expected_digest: str | None = None,
    ) -> GenerationResult:
        try:
            return self._generate(source, output, notify=notify, expected_digest=expected_digest)
        except GenerationError:
            notify(JobEvent("failed"))
            raise
        except (OSError, subprocess.CalledProcessError) as error:
            notify(JobEvent("failed"))
            raise GenerationError(
                "Nem sikerült elkészíteni vagy menteni az MP3-at. Ellenőrizd a szabad tárhelyet, "
                "a célmappa jogosultságát és a hangkódoló elérhetőségét."
            ) from error

    def _generate(
        self, source: Path, output: Path, *, notify: Callable[[JobEvent], None],
        expected_digest: str | None,
    ) -> GenerationResult:
        preview = self.preview(source)
        if expected_digest is not None and expected_digest != preview.digest:
            raise GenerationError("A forrásszöveg megváltozott az előnézet óta. Válaszd ki újra a fájlt.")
        if output.exists() or output.is_symlink():
            raise GenerationError("A célfájl már létezik. Válassz másik nevet.")
        notify(JobEvent("preparing"))
        with tempfile.TemporaryDirectory(dir=output.parent, prefix=".hangoskonyv-") as folder:
            wav = Path(folder) / "speech.wav"
            encoded = Path(folder) / "speech.mp3"
            self.speech_renderer(preview.text, wav, lambda state: notify(JobEvent(state)))
            notify(JobEvent("encoding"))
            subprocess.run([
                shutil.which("ffmpeg") or "ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error",
                "-n", "-i", str(wav), "-ac", "1", "-ar", "24000", "-codec:a", "libmp3lame",
                "-b:a", "96k", str(encoded),
            ], check=True, capture_output=True)
            try:
                os.link(encoded, output)
            except FileExistsError as error:
                raise GenerationError("A célfájl már létezik. Válassz másik nevet.") from error
        notify(JobEvent("completed"))
        return GenerationResult(output)

"""The public file-to-MP3 generation boundary used by the Mac app."""
from dataclasses import dataclass
from pathlib import Path
import os
import hashlib
import math
import shutil
import subprocess
import tempfile
import unicodedata
import wave

from .text import speech_parts
from .audio import append_speech_part
from typing import Callable


@dataclass(frozen=True)
class SourcePreview:
    text: str
    digest: str


@dataclass(frozen=True)
class JobEvent:
    state: str
    completed_characters: int = 0
    total_characters: int = 0


@dataclass(frozen=True)
class GenerationResult:
    output: Path
    audio_seconds: float
    peak_temporary_audio_bytes: int


SpeechRenderer = Callable[[str, Path, Callable[[str], None]], None]


class GenerationError(Exception):
    """An actionable error safe to display in the application."""


class GenerationService:
    def __init__(self, speech_renderer: SpeechRenderer | None = None, model_path: Path | None = None,
                 *, engine: str = "omnivoice"):
        from .speech import MlxSpeechRenderer
        from .vibevoice import VibeVoiceSpeechRenderer

        if engine not in {"omnivoice", "vibevoice"}:
            raise GenerationError("Ismeretlen helyi beszédmotor.")
        root = Path(__file__).resolve().parents[1] / ".local/models"
        if engine == "vibevoice":
            self.speech_renderer = speech_renderer or VibeVoiceSpeechRenderer(
                model_path or root / "VibeVoice_7B_hun_v2-mlx-4bit"
            )
        else:
            self.speech_renderer = speech_renderer or MlxSpeechRenderer(model_path or root / "OmniVoice-bfloat16")

    def preview(self, source: Path) -> SourcePreview:
        if source.suffix.lower() != ".txt":
            raise GenerationError("Ebben a változatban TXT-fájlt válassz.")
        try:
            text = source.read_text(encoding="utf-8-sig").strip()
        except UnicodeError as error:
            raise GenerationError("A fájl nem érvényes UTF-8 szöveg. Mentsd UTF-8 kódolással.") from error
        except OSError as error:
            raise GenerationError("A szövegfájl nem olvasható. Ellenőrizd a fájlt és a hozzáférést.") from error
        if not text:
            raise GenerationError("A kiválasztott fájl üres.")
        if any(unicodedata.category(c) == "Cc" and c not in "\n\r\t" for c in text):
            raise GenerationError("A fájl szöveg helyett bináris vezérlőjeleket tartalmaz.")
        return SourcePreview(text, hashlib.sha256(text.encode("utf-8")).hexdigest())

    def generate(
        self, source: Path, output: Path, *, notify: Callable[[JobEvent], None] = lambda event: None,
        expected_digest: str | None = None, speed: float = 1.0,
    ) -> GenerationResult:
        try:
            return self._generate(source, output, notify=notify, expected_digest=expected_digest, speed=speed)
        except GenerationError:
            notify(JobEvent("failed"))
            raise
        except (OSError, subprocess.CalledProcessError, wave.Error, EOFError) as error:
            notify(JobEvent("failed"))
            raise GenerationError(
                "Nem sikerült elkészíteni vagy menteni az MP3-at. Ellenőrizd a szabad tárhelyet, "
                "a célmappa jogosultságát és a hangkódoló elérhetőségét."
            ) from error

    def _generate(
        self, source: Path, output: Path, *, notify: Callable[[JobEvent], None],
        expected_digest: str | None, speed: float,
    ) -> GenerationResult:
        if not math.isfinite(speed) or not 0.75 <= speed <= 1.5:
            raise GenerationError("A felolvasási tempó 0,75 és 1,5 közé állítható.")
        preview = self.preview(source)
        if expected_digest is not None and expected_digest != preview.digest:
            raise GenerationError("A forrásszöveg megváltozott az előnézet óta. Válaszd ki újra a fájlt.")
        if output.exists() or output.is_symlink():
            raise GenerationError("A célfájl már létezik. Válassz másik nevet.")
        total = len(preview.text)
        completed = 0
        notify(JobEvent("preparing", completed, total))
        with tempfile.TemporaryDirectory(dir=output.parent, prefix=".hangoskonyv-") as folder:
            wav = Path(folder) / "part.wav"
            pcm = Path(folder) / "speech.pcm"
            encoded = Path(folder) / "speech.mp3"
            peak_temporary = 0
            with pcm.open("wb") as assembled:
                for part in speech_parts(preview.text):
                    self.speech_renderer(part, wav, lambda state: notify(JobEvent(state, completed, total)))
                    append_speech_part(wav, assembled)
                    peak_temporary = max(peak_temporary, assembled.tell() + wav.stat().st_size)
                    wav.unlink()
                    completed += len(part)
                    notify(JobEvent("generating", completed, total))
            notify(JobEvent("encoding", completed, total))
            subprocess.run([
                shutil.which("ffmpeg") or "ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error",
                "-n", "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", str(pcm), "-codec:a", "libmp3lame",
                *(["-af", f"atempo={speed}"] if speed != 1.0 else []),
                "-b:a", "96k", str(encoded),
            ], check=True, capture_output=True)
            pcm_bytes = pcm.stat().st_size
            peak_temporary = max(peak_temporary, pcm_bytes + encoded.stat().st_size)
            try:
                os.link(encoded, output)
            except FileExistsError as error:
                raise GenerationError("A célfájl már létezik. Válassz másik nevet.") from error
        notify(JobEvent("completed", total, total))
        return GenerationResult(output, pcm_bytes / 48000 / speed, peak_temporary)

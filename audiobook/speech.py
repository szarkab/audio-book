"""The user-approved Hungarian Piper Imre voice, entirely local."""
import hashlib
from pathlib import Path
import shutil
import subprocess
from typing import Any, Callable
import wave

from .settings import NarrationSettings


MODEL_REVISION = "cf910fb59f1d79ab3b625a63993a108751c6c25d"
MODEL_FILES = {
    "hu_HU-imre-medium.onnx": "bcec8e6e5404baca0fcaf2895da4d02d414d3340b9f80bd94a2112b5c67061ae",
    "hu_HU-imre-medium.onnx.json": "760857edbd31947a853842df5833bd16aa1f660feabe11fbebb0a378bf8328c5",
}


class PiperSpeechRenderer:
    def __init__(self, model_path: Path):
        self.model_path = model_path
        self._voice: Any = None

    def __call__(self, text: str, destination: Path, notify: Callable[[str], None], settings: NarrationSettings) -> None:
        from .generation import GenerationError

        if self._voice is None:
            for name, expected in MODEL_FILES.items():
                path = self.model_path / name
                if not path.is_file():
                    raise GenerationError("Hiányzik a Piper Imre modell. Ellenőrizd a modell telepítését.")
                with path.open("rb") as stream:
                    actual = hashlib.file_digest(stream, "sha256").hexdigest()
                if actual != expected:
                    raise GenerationError("A Piper Imre modell sérült vagy másik hangra cserélődött.")
            from piper import PiperVoice

            notify("loading_model")
            self._voice = PiperVoice.load(self.model_path / "hu_HU-imre-medium.onnx", use_cuda=False)
        notify("generating")
        from piper.config import SynthesisConfig

        synthesis = SynthesisConfig(length_scale=settings.length_scale, noise_scale=settings.noise_scale,
                                    noise_w_scale=settings.noise_w_scale, normalize_audio=settings.normalize_audio)
        native = destination.with_suffix(".native.wav")
        try:
            with wave.open(str(native), "wb") as audio:
                rate = self._voice.config.sample_rate
                audio.setnchannels(1)
                audio.setsampwidth(2)
                audio.setframerate(rate)
                first = True
                for chunk in self._voice.synthesize(text, syn_config=synthesis):
                    if not first and settings.sentence_silence:
                        audio.writeframes(bytes(round(settings.sentence_silence * rate) * 2))
                    audio.writeframes(chunk.audio_int16_bytes)
                    first = False
            # Piper's original 22,050 Hz PCM is resampled without changing tempo
            # for the application's existing 24 kHz lossless assembly path.
            subprocess.run([
                shutil.which("ffmpeg") or "ffmpeg", "-nostdin", "-v", "error", "-n",
                "-i", str(native), "-ar", "24000", "-ac", "1", "-c:a", "pcm_s16le", str(destination),
            ], check=True, capture_output=True)
        finally:
            native.unlink(missing_ok=True)

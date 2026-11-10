"""Offline MLX adapter for the approved male narrator."""
import os
import json
import hashlib
from pathlib import Path
from typing import Any, Callable


REFERENCE_TEXT = (
    "Az esti fény lassan elhalványult a dombok mögött. Júlia becsukta a könyvet, "
    "és az ablakhoz lépett. A kertben csend volt, csak a szél mozgatta a diófa "
    "leveleit. Úgy érezte, most végre van ideje nyugodtan végiggondolni a történteket."
)


class MlxSpeechRenderer:
    def __init__(self, model_path: Path):
        self.model_path = model_path
        self._model: Any = None
        self._reference_tokens: Any = None
        self._reference_text = ""

    def __call__(self, text: str, destination: Path, notify: Callable[[str], None]) -> None:
        from .generation import GenerationError

        required = ["config.json", "model.safetensors", "tokenizer.json",
                    "audio_tokenizer/config.json", "audio_tokenizer/model.safetensors"]
        if not all((self.model_path / item).is_file() for item in required):
            raise GenerationError("Hiányzik vagy hiányos a helyi beszédmodell. Ellenőrizd a modell telepítését.")
        os.environ["HF_HUB_OFFLINE"] = "1"
        os.environ["TRANSFORMERS_OFFLINE"] = "1"
        os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
        import mlx.core as mx
        import numpy as np
        from mlx_audio.audio_io import write as audio_write
        from mlx_audio.tts.models.omnivoice.duration import RuleDurationEstimator
        from mlx_audio.tts.utils import load_model
        from mlx_audio.tts.models.omnivoice.utils import create_voice_clone_prompt

        if not mx.metal.is_available():
            raise GenerationError("Az Apple GPU nem érhető el. Indítsd újra az alkalmazást a Macen.")
        mx.set_default_device(mx.gpu)
        if self._model is None:
            notify("loading_model")
            reference = Path(__file__).resolve().parents[1] / "assets/voices/male-reference.wav"
            metadata = reference.with_suffix(".json")
            if not reference.is_file() or not metadata.is_file():
                raise GenerationError("Hiányzik a férfi narrátor hangreferenciája. Ellenőrizd az alkalmazásfájlokat.")
            info = json.loads(metadata.read_text())
            if hashlib.sha256(reference.read_bytes()).hexdigest() != info["reference_wav_sha256"]:
                raise GenerationError("A narrátor hangreferenciája sérült.")
            model = load_model(str(self.model_path))
            tokens = create_voice_clone_prompt(
                str(reference), tokenizer=model.audio_tokenizer,
                ref_text=info["text"], preprocess=False,
            )
            mx.eval(tokens)
            self._model = model
            self._reference_tokens = tokens
            self._reference_text = info["text"]
        model = self._model
        duration = max(3.0, RuleDurationEstimator().estimate_duration(
            text, REFERENCE_TEXT, 23.0, low_threshold=None,
        ))
        mx.random.seed(42)
        notify("generating")
        result = next(model.generate(
            text=text, language="hu", instruct="male, middle-aged, low pitch",
            duration_s=duration, num_steps=64,
            ref_tokens=self._reference_tokens, ref_text=self._reference_text,
        ))
        mx.eval(result.audio)
        audio = np.asarray(result.audio, dtype=np.float32).reshape(-1)
        if not audio.size or not np.all(np.isfinite(audio)) or np.sqrt(np.mean(audio ** 2)) < 1e-5:
            raise GenerationError("A modell nem adott használható hangot. Próbáld újra a generálást.")
        peak = float(np.abs(audio).max())
        audio = audio * min(1.0, 0.95 / peak)
        audio_write(str(destination), audio, result.sample_rate)
        del result, audio
        mx.clear_cache()

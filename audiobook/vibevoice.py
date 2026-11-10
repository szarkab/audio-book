"""Offline adapter for the complete Hungarian non-streaming VibeVoice model."""
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any, Callable


class VibeVoiceSpeechRenderer:
    def __init__(self, model_path: Path):
        self.model_path = model_path
        self._model: Any = None

    def __call__(self, text: str, destination: Path, notify: Callable[[str], None]) -> None:
        from .generation import GenerationError

        required = ["config.json", "tokenizer.json", "tokenizer_config.json", "preparation.json",
                    "model.safetensors.index.json"]
        if not all((self.model_path / name).is_file() for name in required):
            raise GenerationError("Hiányzik vagy hiányos a helyi magyar VibeVoice-modell. Ellenőrizd az előkészítését.")
        index = json.loads((self.model_path / "model.safetensors.index.json").read_text())
        if not index.get("weight_map") or not all(
            (self.model_path / name).is_file() for name in set(index["weight_map"].values())
        ):
            raise GenerationError("A helyi VibeVoice-modell súlyfájljai hiányosak.")
        preparation = json.loads((self.model_path / "preparation.json").read_text())
        if (preparation.get("source") != "Cseti/VibeVoice_7B_hun_v2"
                or preparation.get("source_revision") != "22434d6f261e2f231b3c358563bdf2d2e8caab57"):
            raise GenerationError("Ez nem a kiválasztott magyar VibeVoice-modell rögzített változata.")
        os.environ["HF_HUB_OFFLINE"] = "1"
        os.environ["TRANSFORMERS_OFFLINE"] = "1"
        os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
        import mlx.core as mx
        import numpy as np
        from mlx_audio.audio_io import write as audio_write
        from mlx_audio.tts.models.vibevoice import Model, ModelConfig
        from mlx_audio.utils import apply_quantization, load_weights
        from transformers import AutoTokenizer

        if not mx.metal.is_available():
            raise GenerationError("Az Apple GPU nem érhető el. A VibeVoice-próbához indítsd az alkalmazást a Macen.")
        mx.set_default_device(mx.gpu)
        reference = Path(__file__).resolve().parents[1] / "assets/voices/male-reference.wav"
        metadata = reference.with_suffix(".json")
        if not reference.is_file() or not metadata.is_file():
            raise GenerationError("Hiányzik a férfi narrátor hangreferenciája.")
        info = json.loads(metadata.read_text())
        if hashlib.sha256(reference.read_bytes()).hexdigest() != info["reference_wav_sha256"]:
            raise GenerationError("A férfi narrátor hangreferenciája sérült.")
        if self._model is None:
            notify("loading_model")
            config = json.loads((self.model_path / "config.json").read_text())
            if config.get("model_type") != "vibevoice":
                raise GenerationError("Ez nem a kiválasztott magyar VibeVoice-modell formátuma.")
            model = Model(ModelConfig.from_dict(config))
            weights = model.sanitize(load_weights(self.model_path))
            apply_quantization(model, config, weights)
            model.load_weights(list(weights.items()), strict=True)
            del weights
            mx.eval(model.parameters())
            model.eval()
            # The generic upstream post-load hook may resolve a remote tokenizer.
            # This adapter deliberately loads only the paired local tokenizer.
            model.tokenizer = AutoTokenizer.from_pretrained(str(self.model_path), local_files_only=True)
            self._model = model
        mx.random.seed(42)
        notify("generating")
        limit = max(384, len(text) * 4)
        result = next(self._model.generate(
            text=text, ref_audio=str(reference), cfg_scale=1.3, ddpm_steps=20,
            max_tokens=limit, do_sample=False, verbose=False,
        ))
        budget = min(limit, self._model.config.decoder_config.max_position_embeddings - result.prompt["tokens"])
        if result.token_count - result.prompt["tokens"] >= budget:
            raise GenerationError("A VibeVoice elérte a biztonsági korlátot. A hang nem jelölhető teljesnek.")
        mx.eval(result.audio)
        audio = np.asarray(result.audio, dtype=np.float32).reshape(-1)
        if not audio.size or not np.all(np.isfinite(audio)) or np.sqrt(np.mean(audio ** 2)) < 1e-5:
            raise GenerationError("A VibeVoice nem adott használható hangot. Próbáld újra a generálást.")
        if result.sample_rate != 24000:
            raise GenerationError("A VibeVoice váratlan mintavételű hangot adott.")
        peak = float(np.abs(audio).max())
        audio *= min(1.0, 0.95 / peak)
        audio_write(str(destination), audio, result.sample_rate)
        print(json.dumps({"engine": "vibevoice", "peak_mlx_memory_bytes": mx.get_peak_memory(),
                          "audio_seconds": audio.size / result.sample_rate}), file=sys.stderr, flush=True)
        del result, audio
        mx.clear_cache()

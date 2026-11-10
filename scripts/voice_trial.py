"""Reproducible, offline Hungarian listening samples; not the application backend."""
import os
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

import argparse
from datetime import datetime, timezone
from importlib.metadata import version
import json
from pathlib import Path
import subprocess
import time

import mlx.core as mx
import numpy as np
from mlx_audio.audio_io import write as audio_write
from mlx_audio.tts.utils import load_model

ROOT = Path(__file__).resolve().parents[1]
MODEL_ID = "mlx-community/OmniVoice-bfloat16"
REVISION = "6119f7072580cc30c3cbdf496269216b03ad9742"
VOICES = {
    "male": {"instruct": "male, middle-aged, low pitch", "seed": 42},
    "female": {"instruct": "female, middle-aged, moderate pitch", "seed": 42},
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, default=ROOT / "samples/hu-narration.txt")
    parser.add_argument("--voices", nargs="+", choices=VOICES, default=list(VOICES))
    parser.add_argument("--steps", type=int, default=64)
    parser.add_argument("--duration", type=float, default=23.0)
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts/voice-trial")
    args = parser.parse_args()
    if args.steps < 1 or args.duration <= 0:
        parser.error("Steps and duration must be positive")
    text = args.text.read_text(encoding="utf-8").strip()
    if not text:
        parser.error("Source text is empty")
    model_path = ROOT / ".local/models/OmniVoice-bfloat16"
    args.output.mkdir(parents=True, exist_ok=True)
    if any((args.output / f"{voice}.json").exists() for voice in args.voices):
        parser.error("Output already contains a trial; choose another directory")
    if not mx.metal.is_available():
        raise RuntimeError("Apple Metal GPU is unavailable")
    mx.set_default_device(mx.gpu)
    print("Loading model locally on Metal GPU", flush=True)
    start = time.perf_counter()
    model = load_model(str(model_path))
    load_seconds = time.perf_counter() - start
    print(f"Model loaded in {load_seconds:.2f}s", flush=True)
    for voice in args.voices:
        settings = VOICES[voice]
        mx.random.seed(settings["seed"])
        mx.reset_peak_memory()
        print(f"Generating {voice}: {args.steps} steps, {args.duration}s target", flush=True)
        start = time.perf_counter()
        result = next(model.generate(
            text=text, language="hu", instruct=settings["instruct"],
            duration_s=args.duration, num_steps=args.steps,
        ))
        mx.eval(result.audio)
        audio = np.asarray(result.audio, dtype=np.float32).reshape(-1)
        generation_seconds = time.perf_counter() - start
        if audio.size == 0 or not np.all(np.isfinite(audio)):
            raise RuntimeError("Invalid generated waveform")
        rms = float(np.sqrt(np.mean(audio ** 2)))
        if rms < 1e-5:
            raise RuntimeError("Generated waveform is effectively silent")
        raw_peak = float(np.abs(audio).max())
        gain = min(1.0, 0.95 / raw_peak)
        audio = audio * gain
        rms = float(np.sqrt(np.mean(audio ** 2)))
        wav = args.output / f"{voice}.wav"
        audio_write(str(wav), audio, result.sample_rate)
        exports = {}
        for bitrate in (64, 96):
            mp3 = args.output / f"{voice}-{bitrate}k.mp3"
            subprocess.run([
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-n", "-i", str(wav),
                "-codec:a", "libmp3lame", "-b:a", f"{bitrate}k", str(mp3),
            ], check=True)
            exports[mp3.name] = mp3.stat().st_size
        report = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "model": MODEL_ID, "revision": REVISION,
            "packages": {p: version(p) for p in ("mlx", "mlx-audio", "transformers")},
            "device": "Apple Metal GPU", "network": "HF and Transformers offline mode",
            "text": text, "language": "hu", "voice_design": settings,
            "steps": args.steps, "requested_duration_seconds": args.duration,
            "audio_duration_seconds": audio.size / result.sample_rate,
            "sample_rate": result.sample_rate, "model_load_seconds": load_seconds,
            "generation_seconds": generation_seconds,
            "generation_time_per_audio_second": generation_seconds / (audio.size / result.sample_rate),
            "peak_mlx_memory_gb": mx.get_peak_memory() / 1e9,
            "rms": rms, "raw_peak_amplitude": raw_peak, "output_gain": gain,
            "peak_amplitude": float(np.abs(audio).max()),
            "wav_bytes": wav.stat().st_size, "mp3_bytes": exports,
            "listening_status": "pending user listening; waveform validation is not quality approval",
        }
        (args.output / f"{voice}.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps(report, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()

"""Validate and level one bounded speech part before streaming it to disk."""
from pathlib import Path
from typing import BinaryIO
import math
import wave

import numpy as np


def append_speech_part(source: Path, destination: BinaryIO, *, normalize_audio: bool = True, volume: float = 1.0) -> None:
    from .generation import GenerationError

    with wave.open(str(source), "rb") as audio:
        if (audio.getnchannels(), audio.getsampwidth(), audio.getframerate()) != (1, 2, 24000):
            raise GenerationError("A beszédmodell nem támogatott hangformátumot adott.")
        if audio.getnframes() == 0:
            raise GenerationError("A beszédmodell üres hangrészt adott. Nem mentettünk hiányos MP3-at.")
        expected_bytes = audio.getnframes() * 2
        copied_bytes = 0
        energies: list[tuple[float, int]] = []
        peak = 0.0
        # 20 ms frames distinguish speech from inter-sentence silence.
        while frames := audio.readframes(480):
            samples = np.frombuffer(frames, dtype="<i2").astype(np.float64)
            energies.append((float(np.dot(samples, samples)), len(samples)))
            peak = max(peak, float(np.max(np.abs(samples))))
            copied_bytes += len(frames)
        if copied_bytes != expected_bytes:
            raise GenerationError("A hangrész sérült vagy hiányos. Nem mentettünk csonka MP3-at.")
        threshold = max(energy / count for energy, count in energies) * 0.01
        active = [(energy, count) for energy, count in energies if energy / count >= threshold]
        rms = math.sqrt(sum(energy for energy, _ in active) / sum(count for _, count in active))
        if rms < 1 or peak < 1:
            raise GenerationError("A modell néma hangrészt adott. Nem mentettünk hiányos MP3-at.")
        # Equal speech RMS across parts, with a conservative peak ceiling.
        gain = min(3276.8 / rms, 31128.0 / peak) if normalize_audio else 1.0
        gain = min(gain * volume, 32767.0 / peak)
        audio.rewind()
        while frames := audio.readframes(4096):
            samples = np.frombuffer(frames, dtype="<i2").astype(np.float64)
            normalized = np.rint(samples * gain).astype("<i2")
            destination.write(normalized.tobytes())

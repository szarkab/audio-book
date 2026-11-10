"""Opt-in real Piper file-to-MP3 integration check.

This verifies audible, correctly timed output, not subjective pronunciation or
transcript accuracy. The selected model's hashes are verified by the adapter.
"""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

import numpy as np

from audiobook.generation import GenerationService
from audiobook.settings import NarrationSettings


@unittest.skipUnless(os.environ.get("AUDIOBOOK_REAL_PIPER_TEST") == "1", "Requires the local Piper Imre model")
class PiperIntegration(unittest.TestCase):
    def test_the_real_imre_voice_produces_audible_correctly_timed_mp3(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as folder:
            result = GenerationService().generate(root / "samples/hu-narration.txt", Path(folder) / "actual.mp3")
            decoded = np.frombuffer(subprocess.check_output([
                "ffmpeg", "-v", "error", "-i", str(result.output), "-ar", "24000", "-ac", "1",
                "-f", "f32le", "-",
            ]), dtype="<f4")
            self.assertTrue(np.all(np.isfinite(decoded)))
            self.assertGreater(float(np.sqrt(np.mean(decoded ** 2))), 0.01)
            self.assertAlmostEqual(len(decoded) / 24000, result.audio_seconds, delta=0.05)
            self.assertGreater(result.audio_seconds, 8)
            self.assertLess(result.audio_seconds, 45)

    def test_extra_sentence_pause_covers_internal_and_part_boundaries(self):
        import onnxruntime
        text = "Júlia belépett. A kertben csend volt. Péter elindult. A nap kisütött."
        durations = []
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "mondatok.txt"
            source.write_text(text)
            for index, silence in enumerate([0.0, 0.25]):
                onnxruntime.set_seed(42)
                result = GenerationService().generate(
                    source, Path(folder) / f"{index}.mp3",
                    settings=NarrationSettings(sentence_silence=silence),
                )
                durations.append(result.audio_seconds)
        self.assertAlmostEqual(durations[1] - durations[0], 0.75, delta=0.02)


if __name__ == "__main__":
    unittest.main()

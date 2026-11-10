"""Opt-in full-job content regression with the local M5 speech models.

A byte-identical waveform is no longer expected after the requested two-sentence
partitioning, fixed speaker conditioning, and level normalization.
"""
import difflib
import os
from pathlib import Path
import re
import tempfile
import unicodedata
import unittest

from audiobook.generation import GenerationService


@unittest.skipUnless(os.environ.get("AUDIOBOOK_REAL_MODEL_TEST") == "1" or
                     os.environ.get("AUDIOBOOK_REAL_VIBEVOICE_TEST") == "1", "Requires the local M5 models")
class NarrationContentRegression(unittest.TestCase):
    def test_generated_narration_preserves_the_source_content(self):
        from mlx_audio.stt import load
        root = Path(__file__).resolve().parents[1]
        vibevoice = os.environ.get("AUDIOBOOK_REAL_VIBEVOICE_TEST") == "1"
        source = root / ("samples/hu-vibevoice-trial.txt" if vibevoice else "samples/hu-narration.txt")
        with tempfile.TemporaryDirectory() as folder:
            result = GenerationService(engine="vibevoice" if vibevoice else "omnivoice").generate(
                source, Path(folder) / "actual.mp3"
            )
            import mlx.core as mx
            mx.clear_cache()
            transcriber = load(str(root / ".local/models/whisper-large-v3-turbo-asr-fp16"))
            transcript = transcriber.generate(str(result.output), language="hu", temperature=0.0,
                                               condition_on_previous_text=False, verbose=None).text
            def normalized(text):
                return "".join(re.findall(r"\w+", unicodedata.normalize("NFKC", text).casefold()))
            match = difflib.SequenceMatcher(None, normalized(source.read_text()), normalized(transcript), autojunk=False)
            self.assertGreaterEqual(match.ratio(), 0.97, transcript)


if __name__ == "__main__":
    unittest.main()

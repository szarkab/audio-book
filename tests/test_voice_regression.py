"""Opt-in M5 regression against the narrator sample the user accepted.

This checks identity of a known-good sample, not general speech naturalness.
"""
import hashlib
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

from audiobook.generation import GenerationService


@unittest.skipUnless(os.environ.get("AUDIOBOOK_REAL_MODEL_TEST") == "1", "Requires the local M5 model")
class ApprovedVoiceRegression(unittest.TestCase):
    def test_known_good_narration_is_preserved(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as folder:
            result = GenerationService().generate(root / "samples/hu-narration.txt", Path(folder) / "actual.mp3")
            def decoded_hash(path):
                pcm = subprocess.check_output([
                    "ffmpeg", "-v", "error", "-i", str(path), "-f", "s16le", "-acodec", "pcm_s16le", "-",
                ])
                return hashlib.sha256(pcm).hexdigest()
            self.assertEqual(
                decoded_hash(result.output), decoded_hash(root / "tests/fixtures/approved-male.mp3"),
                "The known-good male sample changed; this does not approve the new voice quality.",
            )


if __name__ == "__main__":
    unittest.main()

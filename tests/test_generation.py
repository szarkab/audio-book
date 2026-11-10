import json
import math
from pathlib import Path
import struct
import subprocess
import tempfile
import unittest
import wave

from audiobook.generation import GenerationError, GenerationService


def reference_speech(text, destination, notify):
    """Replace only the external speech model; encode a real waveform."""
    notify("generating")
    with wave.open(str(destination), "wb") as stream:
        stream.setnchannels(1)
        stream.setsampwidth(2)
        stream.setframerate(24000)
        stream.writeframes(b"".join(
            struct.pack("<h", int(4000 * math.sin(2 * math.pi * 220 * i / 24000)))
            for i in range(6000)
        ))


class GenerationTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name)
        self.source = self.root / "szöveg.txt"
        self.source.write_text("Júlia az ablakhoz lépett. A kertben csend volt.", encoding="utf-8")
        self.service = GenerationService(speech_renderer=reference_speech)

    def test_selected_text_becomes_one_playable_mp3(self):
        preview = self.service.preview(self.source)
        self.assertEqual(preview.text, "Júlia az ablakhoz lépett. A kertben csend volt.")
        events = []
        result = self.service.generate(self.source, self.root / "hang.mp3", notify=events.append)
        info = json.loads(subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries", "stream=codec_name,channels:format=duration",
            "-of", "json", str(result.output),
        ], text=True))
        self.assertEqual(info["streams"][0]["codec_name"], "mp3")
        self.assertEqual(info["streams"][0]["channels"], 1)
        self.assertGreater(float(info["format"]["duration"]), 0.2)
        self.assertEqual(events[-1].state, "completed")
        self.assertEqual(list(self.root.glob("*.mp3")), [result.output])

    def test_invalid_sources_fail_without_creating_an_mp3(self):
        cases = [("üres.txt", b"  \n"), ("sérült.txt", b"\xff\xfe"),
                 ("bináris.txt", b"hello\x00world"), ("nem-szöveg.md", b"hello")]
        for name, data in cases:
            with self.subTest(name=name):
                source = self.root / name
                source.write_bytes(data)
                events = []
                with self.assertRaises(GenerationError):
                    self.service.generate(source, self.root / "hiba.mp3", notify=events.append)
                self.assertFalse((self.root / "hiba.mp3").exists())
                self.assertEqual(events[-1].state, "failed")

    def test_existing_mp3_is_preserved_and_failure_is_explained(self):
        output = self.root / "korábbi.mp3"
        output.write_bytes(b"previous audiobook")
        with self.assertRaisesRegex(GenerationError, "létezik"):
            self.service.generate(self.source, output)
        self.assertEqual(output.read_bytes(), b"previous audiobook")

    def test_missing_model_is_an_actionable_job_failure(self):
        service = GenerationService(model_path=self.root / "missing-model")
        events = []
        with self.assertRaisesRegex(GenerationError, "modell"):
            service.generate(self.source, self.root / "hang.mp3", notify=events.append)
        self.assertFalse((self.root / "hang.mp3").exists())
        self.assertEqual(events[-1].state, "failed")

    def test_a_file_created_during_generation_is_not_reported_as_our_result(self):
        output = self.root / "hang.mp3"
        def concurrent_speech(text, destination, notify):
            reference_speech(text, destination, notify)
            output.write_bytes(b"another job finished first")
        service = GenerationService(speech_renderer=concurrent_speech)
        with self.assertRaisesRegex(GenerationError, "létezik"):
            service.generate(self.source, output)
        self.assertEqual(output.read_bytes(), b"another job finished first")

    def test_save_or_encoding_failure_never_leaves_a_finished_mp3(self):
        def broken_speech(text, destination, notify):
            raise OSError("disk full")
        def invalid_speech(text, destination, notify):
            destination.write_bytes(b"not audio")
        for renderer in [broken_speech, invalid_speech]:
            with self.subTest(renderer=renderer.__name__):
                service = GenerationService(speech_renderer=renderer)
                output = self.root / "hiba.mp3"
                events = []
                with self.assertRaises(GenerationError):
                    service.generate(self.source, output, notify=events.append)
                self.assertFalse(output.exists())
                self.assertEqual(events[-1].state, "failed")

    def test_source_changed_after_preview_requires_selecting_it_again(self):
        preview = self.service.preview(self.source)
        self.source.write_text("Ez már egy másik szöveg.")
        with self.assertRaisesRegex(GenerationError, "megváltozott"):
            self.service.generate(self.source, self.root / "hang.mp3", expected_digest=preview.digest)
        self.assertFalse((self.root / "hang.mp3").exists())

    def test_unsupported_long_text_is_explained_instead_of_truncated(self):
        self.source.write_text("á" * 601, encoding="utf-8")
        with self.assertRaisesRegex(GenerationError, "600"):
            self.service.generate(self.source, self.root / "hang.mp3")
        self.assertFalse((self.root / "hang.mp3").exists())


if __name__ == "__main__":
    unittest.main()

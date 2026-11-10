import json
from dataclasses import replace
import math
from pathlib import Path
import struct
import subprocess
import tempfile
import unittest
import wave
import numpy as np

from audiobook.generation import GenerationError, GenerationService
from audiobook.settings import NarrationSettings


def reference_speech(text, destination, notify, settings=None):
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

    def test_clear_ordinals_in_preview_are_exactly_the_spoken_text(self):
        original = "1. fejezet. 2. próba. A 15. versenyző és a 21. hely. A 100. alkalom."
        expected = "első fejezet. második próba. A tizenötödik versenyző és a huszonegyedik hely. A századik alkalom."
        self.source.write_text(original)
        received = []
        def capture(text, destination, notify, settings):
            received.append(text)
            reference_speech(text, destination, notify)
        service = GenerationService(speech_renderer=capture)
        preview = service.preview(self.source)
        self.assertEqual(preview.text, expected)
        result = service.generate(self.source, self.root / "sorszámok.mp3", expected_digest=preview.digest)
        self.assertEqual("".join(received), expected)
        self.assertEqual(self.source.read_text(), original)
        self.assertTrue(result.output.is_file())

    def test_even_a_source_change_with_identical_spoken_text_requires_new_preview(self):
        self.source.write_text("1. fejezet")
        preview = self.service.preview(self.source)
        self.source.write_text(" 1. fejezet\n")
        self.assertEqual(self.service.preview(self.source).text, preview.text)
        output = self.root / "megváltozott.mp3"
        with self.assertRaisesRegex(GenerationError, "megváltozott"):
            self.service.generate(self.source, output, expected_digest=preview.digest)
        self.assertFalse(output.exists())

    def test_ambiguous_dotted_numbers_are_preserved_in_preview_and_audio(self):
        original = ("2026. 11. 10. fejezet: keltezési példa. 2026. november 10. "
                    "Dr. Kovács a Fő utca 12. sz. alatt lakik. Verzió: v1.2.3. "
                    "A 1.2. fejezet verziócímke. Érték: 3,14 és 1.5. "
                    "A darabszám 1. Ez egy mondat. A 101. fejezet. 01. fejezet. "
                    "A darabszám 1. Próba következik. Az eredmény 2. Hely már nincs.")
        self.source.write_text(original)
        received = []
        def capture(text, destination, notify, settings):
            received.append(text)
            reference_speech(text, destination, notify)
        service = GenerationService(speech_renderer=capture)
        preview = service.preview(self.source)
        self.assertEqual(preview.text, original)
        service.generate(self.source, self.root / "kivételek.mp3", expected_digest=preview.digest)
        self.assertEqual("".join(received), original)

    def test_the_selected_narration_settings_reach_every_speech_part(self):
        self.source.write_text("Júlia belépett. A kertben csend volt. Péter tovább olvasott.")
        selected = NarrationSettings(length_scale=1.2, noise_scale=0.3, noise_w_scale=0.2,
                                     volume=0.7, normalize_audio=False, sentence_silence=0.15)
        received = []
        def capture(text, destination, notify, settings):
            received.append(settings)
            reference_speech(text, destination, notify)
        result = GenerationService(speech_renderer=capture).generate(
            self.source, self.root / "egyéni.mp3", settings=selected,
        )
        self.assertGreater(len(received), 1)
        self.assertTrue(all(settings == selected for settings in received))
        self.assertTrue(result.output.is_file())

    def test_invalid_narration_values_fail_before_synthesis(self):
        cases = [dict(length_scale=0), dict(noise_scale=-0.1), dict(noise_w_scale=2),
                 dict(volume=float("nan")), dict(sentence_silence=-1), dict(normalize_audio="yes")]
        for index, changes in enumerate(cases):
            with self.subTest(changes=changes):
                output = self.root / f"érvénytelen-{index}.mp3"
                events = []
                with self.assertRaises(GenerationError):
                    self.service.generate(self.source, output, settings=replace(NarrationSettings(), **changes),
                                          notify=events.append)
                self.assertFalse(output.exists())
                self.assertEqual(events[-1].state, "failed")

    def test_output_volume_survives_normalization_and_the_toggle_changes_levels(self):
        levels = {}
        for name, settings in [
            ("normal", NarrationSettings()),
            ("quiet", NarrationSettings(volume=0.5)),
            ("raw", NarrationSettings(normalize_audio=False)),
        ]:
            result = self.service.generate(self.source, self.root / f"{name}.mp3", settings=settings)
            pcm = np.frombuffer(subprocess.check_output([
                "ffmpeg", "-v", "error", "-i", str(result.output), "-f", "f32le", "-",
            ]), dtype="<f4")
            levels[name] = float(np.sqrt(np.mean(pcm ** 2)))
        self.assertAlmostEqual(levels["quiet"] / levels["normal"], 0.5, delta=0.03)
        self.assertLess(levels["raw"], levels["normal"] * 0.95)

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
        with self.assertRaisesRegex(GenerationError, "Imre"):
            service.generate(self.source, self.root / "hang.mp3", notify=events.append)
        self.assertFalse((self.root / "hang.mp3").exists())
        self.assertEqual(events[-1].state, "failed")

    def test_a_different_voice_cannot_silently_replace_imre(self):
        model = self.root / "wrong-voice"
        model.mkdir()
        (model / "hu_HU-imre-medium.onnx").write_bytes(b"a different voice")
        (model / "hu_HU-imre-medium.onnx.json").write_text("{}")
        output = self.root / "wrong.mp3"
        with self.assertRaisesRegex(GenerationError, "Imre.*sérült|sérült.*Imre"):
            GenerationService(model_path=model).generate(self.source, output)
        self.assertFalse(output.exists())

    def test_a_file_created_during_generation_is_not_reported_as_our_result(self):
        output = self.root / "hang.mp3"
        def concurrent_speech(text, destination, notify, settings=None):
            reference_speech(text, destination, notify)
            output.write_bytes(b"another job finished first")
        service = GenerationService(speech_renderer=concurrent_speech)
        with self.assertRaisesRegex(GenerationError, "létezik"):
            service.generate(self.source, output)
        self.assertEqual(output.read_bytes(), b"another job finished first")

    def test_save_or_encoding_failure_never_leaves_a_finished_mp3(self):
        def broken_speech(text, destination, notify, settings=None):
            raise OSError("disk full")
        def invalid_speech(text, destination, notify, settings=None):
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



if __name__ == "__main__":
    unittest.main()

import json
import numpy as np
from pathlib import Path
import subprocess
import tempfile
import unittest
import wave

from audiobook.generation import GenerationError, GenerationService
from test_generation import reference_speech


class LongGenerationTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name)
        self.source = self.root / "könyv.txt"

    def test_long_source_reaches_the_speech_model_in_full_and_produces_one_mp3(self):
        text = (
            "Júlia az ablakhoz lépett. A kertben csend volt. "
            "A diófa alatt Péter egy régi könyvet olvasott.\n\n"
        ) * 20
        self.source.write_text(text, encoding="utf-8")
        spoken = []
        def bounded_speech(part, destination, notify):
            if len(part) > 600:
                raise RuntimeError("The external speech model accepts bounded inputs")
            spoken.append(part)
            reference_speech(part, destination, notify)
        service = GenerationService(speech_renderer=bounded_speech)
        result = service.generate(self.source, self.root / "könyv.mp3")
        self.assertEqual("".join(spoken), text.strip())
        self.assertEqual(list(self.root.glob("*.mp3")), [result.output])
        info = json.loads(subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries", "stream=codec_name,channels",
            "-of", "json", str(result.output),
        ], text=True))
        self.assertEqual(info["streams"][0]["codec_name"], "mp3")
        self.assertEqual(info["streams"][0]["channels"], 1)

    def test_progress_covers_the_source_and_encoding_is_not_reported_as_finished(self):
        text = "A könyvtárban csend volt. Júlia tovább olvasott. " * 30
        self.source.write_text(text, encoding="utf-8")
        output = self.root / "hang.mp3"
        events = []
        def observe(event):
            events.append(event)
            if event.state == "encoding":
                self.assertFalse(output.exists())
        GenerationService(speech_renderer=reference_speech).generate(self.source, output, notify=observe)
        self.assertEqual(events[-1].completed_characters, len(text.strip()))
        self.assertEqual(events[-1].total_characters, len(text.strip()))
        progress = [e.completed_characters for e in events]
        self.assertEqual(progress, sorted(progress))
        self.assertIn("encoding", [e.state for e in events])
        self.assertEqual([e.state for e in events].count("completed"), 1)

    def test_hungarian_abbreviations_dates_and_quoted_sentences_stay_intact(self):
        contexts = [
            "Dr. Kovács Ágnes belépett a könyvtárba.",
            "A találkozó 2026. november 10-én kezdődött.",
            "K. Ágnes nyugodtan folytatta az olvasást.",
            "„Eljössz holnap?” – kérdezte Júlia.",
        ]
        for number, sentence in enumerate(contexts):
            with self.subTest(sentence=sentence):
                # Move each interesting punctuation mark near a potential model-input boundary.
                for offset in [370, 380, 390, 394, 398, 402]:
                    prefix = "A " + "a" * offset + ". "
                    self.source.write_text(prefix + sentence + " A történet folytatódott.")
                    spoken = []
                    def capture(part, destination, notify):
                        spoken.append(part)
                        reference_speech(part, destination, notify)
                    output = self.root / f"próba-{number}-{offset}.mp3"
                    GenerationService(speech_renderer=capture).generate(self.source, output)
                    self.assertTrue(any(sentence in part for part in spoken), (sentence, spoken))
                    output.unlink()

    def test_paragraphs_without_terminal_punctuation_also_generate_automatically(self):
        text = ("Ez egy önálló bekezdés amelynek nincs lezáró írásjele " * 4 + "\n\n") * 12
        self.source.write_text(text, encoding="utf-8")
        spoken = []
        def bounded_speech(part, destination, notify):
            if len(part) > 600:
                raise RuntimeError("The external speech model accepts bounded inputs")
            spoken.append(part)
            reference_speech(part, destination, notify)
        result = GenerationService(speech_renderer=bounded_speech).generate(self.source, self.root / "bekezdés.mp3")
        self.assertEqual("".join(spoken), text.strip())
        self.assertTrue(result.output.is_file())

    def test_an_empty_later_audio_part_cannot_become_a_successful_partial_book(self):
        text = "Első " + "szó " * 80 + "vége. " + "Második " + "szó " * 80 + "vége."
        self.source.write_text(text, encoding="utf-8")
        def incomplete_speech(part, destination, notify):
            if part.startswith("Első"):
                reference_speech(part, destination, notify)
            else:
                with wave.open(str(destination), "wb") as audio:
                    audio.setnchannels(1)
                    audio.setsampwidth(2)
                    audio.setframerate(24000)
                    audio.writeframes(b"")
        output = self.root / "hiányos.mp3"
        events = []
        with self.assertRaises(GenerationError):
            GenerationService(speech_renderer=incomplete_speech).generate(self.source, output, notify=events.append)
        self.assertFalse(output.exists())
        self.assertEqual(events[-1].state, "failed")

    def test_completed_job_reports_audio_duration_and_temporary_disk_usage(self):
        self.source.write_text("Júlia tovább olvasott.", encoding="utf-8")
        result = GenerationService(speech_renderer=reference_speech).generate(self.source, self.root / "mérés.mp3")
        self.assertAlmostEqual(result.audio_seconds, 0.25)
        self.assertGreater(result.peak_temporary_audio_bytes, result.output.stat().st_size)

    def test_truncated_audio_part_is_not_accepted_as_a_complete_book(self):
        self.source.write_text("Júlia tovább olvasott.", encoding="utf-8")
        def truncated_speech(part, destination, notify):
            reference_speech(part, destination, notify)
            with destination.open("r+b") as audio:
                audio.truncate(destination.stat().st_size - 100)
        output = self.root / "csonka.mp3"
        with self.assertRaises(GenerationError):
            GenerationService(speech_renderer=truncated_speech).generate(self.source, output)
        self.assertFalse(output.exists())

    def test_address_number_abbreviation_does_not_split_a_sentence(self):
        sentence = "A találkozót a Kossuth utca 12. sz. alatt tartották meg."
        text = "A " + "a" * 341 + ". " + sentence
        self.source.write_text(text, encoding="utf-8")
        spoken = []
        def capture(part, destination, notify):
            spoken.append(part)
            reference_speech(part, destination, notify)
        GenerationService(speech_renderer=capture).generate(self.source, self.root / "cím.mp3")
        self.assertTrue(any(sentence in part for part in spoken), spoken)
        self.assertEqual("".join(spoken), text)

    def test_lowercase_continuations_and_company_abbreviations_stay_in_the_sentence(self):
        cases = [
            (342, "A találkozót a Margit krt. egyik házában tartották meg."),
            (341, "A Szikra Kft. munkatársai közösen olvasták el a könyvet."),
            (350, "A Szikra Kft. Budapesti Irodája ma nyitva maradt."),
            (350, "A jegyzetben a ritka röv. magyarázata is szerepelt."),
        ]
        for index, (length, sentence) in enumerate(cases):
            with self.subTest(sentence=sentence):
                text = "A " + "a" * length + ". " + sentence
                self.source.write_text(text, encoding="utf-8")
                spoken = []
                def capture(part, destination, notify):
                    spoken.append(part)
                    reference_speech(part, destination, notify)
                GenerationService(speech_renderer=capture).generate(self.source, self.root / f"rövidítés-{index}.mp3")
                self.assertTrue(any(sentence in part for part in spoken), spoken)
                self.assertEqual("".join(spoken), text)

    def test_each_internal_speech_input_contains_at_most_two_sentences(self):
        sentences = [
            "Júlia az ablakhoz lépett.", "A kertben csend volt.",
            "Péter kinyitotta a könyvet.", "A szél megmozgatta a leveleket.",
            "A történet az erdőben folytatódott.", "Lassan beesteledett.",
        ]
        text = " ".join(sentences)
        self.source.write_text(text, encoding="utf-8")
        spoken = []
        def capture(part, destination, notify):
            spoken.append(part)
            reference_speech(part, destination, notify)
        GenerationService(speech_renderer=capture).generate(self.source, self.root / "két-mondat.mp3")
        self.assertTrue(all(sum(sentence in part for sentence in sentences) <= 2 for part in spoken), spoken)
        self.assertEqual("".join(spoken), text)

    def test_numbers_at_sentence_ends_do_not_hide_the_two_sentence_limit(self):
        sentences = ["Az első szám a 12.", "A második szám a 13.",
                     "A harmadik szám a 14.", "Ez a felsorolás vége."]
        text = " ".join(sentences)
        self.source.write_text(text, encoding="utf-8")
        spoken = []
        def capture(part, destination, notify):
            spoken.append(part)
            reference_speech(part, destination, notify)
        GenerationService(speech_renderer=capture).generate(self.source, self.root / "számok.mp3")
        self.assertTrue(all(sum(sentence in part for sentence in sentences) <= 2 for part in spoken), spoken)
        self.assertEqual("".join(spoken), text)
        date_sentence = "A dátum 2026. 11. 10. volt."
        self.source.write_text("A " + "a" * 380 + ". " + date_sentence)
        spoken.clear()
        GenerationService(speech_renderer=capture).generate(self.source, self.root / "dátum.mp3")
        self.assertTrue(any(date_sentence in part for part in spoken), spoken)

    def test_quiet_and_loud_model_parts_are_assembled_at_a_consistent_level(self):
        self.source.write_text("Júlia kilépett. A kertben csend volt. Péter olvasott. A nap kisütött.", encoding="utf-8")
        def varying_volume(part, destination, notify):
            reference_speech(part, destination, notify)
            with wave.open(str(destination), "rb") as audio:
                params = audio.getparams()
                pcm = np.frombuffer(audio.readframes(audio.getnframes()), dtype="<i2").astype(np.float64)
            pcm *= 0.1 if part.startswith("Júlia") else 2.0
            with wave.open(str(destination), "wb") as audio:
                audio.setparams(params)
                audio.writeframes(pcm.astype("<i2").tobytes())
        result = GenerationService(speech_renderer=varying_volume).generate(self.source, self.root / "hangerő.mp3")
        decoded = np.frombuffer(subprocess.check_output([
            "ffmpeg", "-v", "error", "-i", str(result.output), "-f", "f32le", "-acodec", "pcm_f32le", "-",
        ]), dtype="<f4")
        levels = [float(np.sqrt(np.mean(decoded[start:start+3000] ** 2))) for start in [1500, 7500]]
        self.assertLess(max(levels) / min(levels), 1.4, levels)


if __name__ == "__main__":
    unittest.main()

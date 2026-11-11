"""Opt-in file-to-MP3 check of the actual self-contained app worker."""
import json
import hashlib
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


@unittest.skipUnless(os.environ.get("AUDIOBOOK_PACKAGED_APP"), "Requires the built standalone app")
class PackagedAppIntegration(unittest.TestCase):
    def test_packaged_worker_generates_without_development_tools(self):
        app = Path(os.environ["AUDIOBOOK_PACKAGED_APP"])
        worker = app / "Contents/Resources/worker/HangosKonyvWorker"
        environment = {key: value for key, value in os.environ.items()
                       if not key.startswith(("PYTHON", "DYLD_", "AUDIOBOOK_"))}
        environment["PATH"] = "/usr/bin:/bin"
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "szöveg.txt"
            source.write_text(("Az 1. fejezet elkezdődött. A kertben csend volt. " * 30).strip())
            def run(*arguments):
                result = subprocess.run([str(worker), *arguments], cwd=folder, env=environment,
                                        text=True, capture_output=True, timeout=90)
                self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
                return [json.loads(line) for line in result.stdout.splitlines()]
            preview = run("preview", str(source))[-1]
            self.assertEqual(preview["text"], ("Az első fejezet elkezdődött. A kertben csend volt. " * 30).strip())
            output = Path(folder) / "hang.mp3"
            events = run("generate", str(source), "--output", str(output), "--expected-digest", preview["digest"])
            self.assertEqual(events[-1]["state"], "completed")
            self.assertGreater(events[-1]["audio_seconds"], 1)
            self.assertGreater(output.stat().st_size, 1000)
            progress = [event["completed_characters"] for event in events if "completed_characters" in event]
            self.assertEqual(progress[-1], len(preview["text"]))
            before = hashlib.sha256(output.read_bytes()).hexdigest()
            source.write_text("Péter becsukta a könyvet. A második történet véget ért.")
            second_preview = run("preview", str(source))[-1]
            second = run("generate", str(source), "--output", str(Path(folder) / "második.mp3"),
                         "--expected-digest", second_preview["digest"])
            self.assertEqual(second[-1]["state"], "completed")
            self.assertEqual(hashlib.sha256(output.read_bytes()).hexdigest(), before)

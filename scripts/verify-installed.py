#!/usr/bin/env python3
"""Check the installed worker with a short representative input, without network."""
import argparse
import hashlib
import json
import os
import plistlib
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--app", type=Path, default=Path.home() / "Applications/HangosKonyv.app")
parser.add_argument("--repetitions", type=int, default=1)
parser.add_argument("--output-dir", type=Path, required=True)
args = parser.parse_args()
if not 1 <= args.repetitions <= 3:
    parser.error("repetitions must be between 1 and 3")
folder = args.output_dir.resolve()
if folder.exists():
    parser.error("Choose a new output directory; existing results are preserved")
folder.mkdir(parents=True)
app = args.app.resolve()
worker = app / "Contents/Resources/worker/HangosKonyvWorker"
ffmpeg = app / "Contents/Resources/tools/ffmpeg"
environment = {key: value for key, value in os.environ.items() if not key.startswith(("PYTHON", "DYLD_", "AUDIOBOOK_"))}
environment["PATH"] = "/usr/bin:/bin"
# Only the children are restricted. Global network/security settings are unchanged.
profile = ('(version 1)(allow default)(deny network*)'
           '(deny file-read* (subpath ' + json.dumps(str(ROOT)) + ') (subpath "/opt/homebrew")'
           ' (subpath ' + json.dumps(str(Path.home() / ".local/share/uv")) + '))')
prefix = ["/usr/bin/sandbox-exec", "-p", profile]

def call(executable, *arguments, timeout=900):
    return subprocess.run([*prefix, str(executable), *map(str, arguments)], cwd=tempfile.gettempdir(),
                          env=environment, capture_output=True, text=True, timeout=timeout, check=True)


def file_hash(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def job(source, output):
    preview = json.loads(call(worker, "preview", source).stdout.splitlines()[-1])
    run = call(worker, "generate", source, "--output", output, "--expected-digest", preview["digest"])
    events = [json.loads(line) for line in run.stdout.splitlines()]
    if events[-1]["state"] != "completed":
        raise RuntimeError("The worker did not finish the job")
    progress = [e["completed_characters"] for e in events if "completed_characters" in e]
    if progress != sorted(progress) or progress[-1] != len(preview["text"]):
        raise RuntimeError("Source coverage/progress is incomplete")
    metrics = next(json.loads(line.removeprefix("GENERATION_METRICS ")) for line in run.stderr.splitlines()
                   if line.startswith("GENERATION_METRICS "))
    call(ffmpeg, "-nostdin", "-v", "error", "-i", output, "-f", "null", "-")
    return {"source_characters": len(preview["text"]), "source_digest": preview["digest"],
            "mp3_sha256": file_hash(output), **metrics}

story = (ROOT / "samples/hu-long-narration.txt").read_text().strip()
source = folder / "book.txt"
source.write_text((story + "\n\n") * args.repetitions)
first = folder / "book.mp3"
print("Representative narration job started", flush=True)
book = job(source, first)
print(json.dumps(book), flush=True)
second_source = folder / "next.txt"
second_source.write_text("Péter becsukta a könyvet. A következő történet külön feladatban készül el.")
next_result = job(second_source, folder / "next.mp3")
if file_hash(first) != book["mp3_sha256"]:
    raise RuntimeError("The next job modified the first MP3")
duration = book["audio_seconds"]
excerpts = []
for label, start in [("eleje", 0.0), ("kozepe", duration / 2), ("vege", max(0.0, duration - 8))]:
    output = folder / f"{label}.mp3"
    call(ffmpeg, "-nostdin", "-v", "error", "-n", "-ss", f"{start:.3f}", "-i", first,
         "-t", "8", "-c:a", "copy", output)
    excerpts.append({"label": label, "start_seconds": start, "path": output.name})
report = {"app_version": plistlib.loads((app / "Contents/Info.plist").read_bytes())["CFBundleShortVersionString"], "repetitions": args.repetitions,
          "network_and_development_paths_denied": True, "book": book, "next_job": next_result,
          "first_mp3_preserved": True, "full_mp3_decode": "passed", "excerpts": excerpts,
          "speech_content_and_naturalness": "Requires human listening; progress and decoding do not prove spoken accuracy"}
(folder / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print("All technical checks passed; listening remains separate", flush=True)

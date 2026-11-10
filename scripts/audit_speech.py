"""Local diagnostic transcription; a text match does not prove natural prosody."""
import os
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

import argparse
import difflib
import json
from pathlib import Path
import re
import time
import unicodedata

from mlx_audio.stt import load


def words(text):
    return re.findall(r"\w+", unicodedata.normalize("NFKC", text).casefold())


def edit_distance(expected, actual):
    row = list(range(len(actual) + 1))
    for i, left in enumerate(expected, 1):
        next_row = [i]
        for j, right in enumerate(actual, 1):
            next_row.append(min(next_row[-1] + 1, row[j] + 1, row[j - 1] + (left != right)))
        row = next_row
    return row[-1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", nargs=3, action="append", metavar=("LABEL", "AUDIO", "SOURCE"), required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--threshold", type=float, default=0.03)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    model = load(str(root / ".local/models/whisper-large-v3-turbo-asr-fp16"))
    reports = []
    for label, audio, source in args.case:
        started = time.perf_counter()
        result = model.generate(audio, language="hu", temperature=0.0,
                                condition_on_previous_text=False, verbose=None)
        expected_text = Path(source).read_text(encoding="utf-8-sig").strip()
        expected, actual = words(expected_text), words(result.text)
        errors = edit_distance(expected, actual)
        expected_letters, actual_letters = "".join(expected), "".join(actual)
        character_errors = edit_distance(expected_letters, actual_letters)
        changes = [{"expected": " ".join(expected[a:b]), "transcribed": " ".join(actual[c:d])}
                   for tag, a, b, c, d in difflib.SequenceMatcher(None, expected, actual, autojunk=False).get_opcodes()
                   if tag != "equal"]
        report = {"label": label, "expected_words": len(expected), "transcribed_words": len(actual),
                  "word_edit_rate": errors / max(1, len(expected)),
                  "character_edit_rate": character_errors / max(1, len(expected_letters)), "changes": changes,
                  "transcription": result.text, "seconds": time.perf_counter() - started,
                  "asr_model": "mlx-community/whisper-large-v3-turbo-asr-fp16",
                  "asr_revision": "624c19c9af5603fa73b83bce14d4aeea96156d18"}
        reports.append(report)
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(reports, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps({k: report[k] for k in ("label", "expected_words", "transcribed_words", "word_edit_rate", "character_edit_rate", "seconds")}, ensure_ascii=False), flush=True)
    raise SystemExit(1 if any(r["character_edit_rate"] > args.threshold for r in reports) else 0)


if __name__ == "__main__":
    main()

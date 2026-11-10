#!/usr/bin/env python3
"""One-time developer download of the exact approved Imre voice."""
import hashlib
from pathlib import Path
import sys
import tempfile
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from audiobook.speech import MODEL_FILES, MODEL_REVISION


def prepare():
    target = ROOT / ".local/models/piper-imre"
    if target.exists():
        for name, expected in MODEL_FILES.items():
            path = target / name
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                raise SystemExit("The existing Imre model is incomplete or damaged.")
        print("Piper Imre is ready.")
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    base = f"https://huggingface.co/rhasspy/piper-voices/resolve/{MODEL_REVISION}/hu/hu_HU/imre/medium/"
    with tempfile.TemporaryDirectory(dir=target.parent, prefix=".piper-download-") as folder:
        temporary = Path(folder)
        for name, expected in MODEL_FILES.items():
            checksum = hashlib.sha256()
            with urllib.request.urlopen(base + name) as response, (temporary / name).open("wb") as stream:
                while chunk := response.read(1024 * 1024):
                    checksum.update(chunk)
                    stream.write(chunk)
            if checksum.hexdigest() != expected:
                raise SystemExit(f"Checksum mismatch: {name}")
        with urllib.request.urlopen(base + "MODEL_CARD") as response:
            (temporary / "MODEL_CARD").write_bytes(response.read())
        temporary.rename(target)
    print("Piper Imre is ready.")


if __name__ == "__main__":
    prepare()

#!/usr/bin/env python3
"""Build the ARM64 macOS 26 personal-preview app and self-contained DMG."""
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import plistlib
import shutil
import subprocess
import sys
import tempfile
import tarfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.3.0"
parser = argparse.ArgumentParser()
parser.add_argument("--app-only", action="store_true")
args = parser.parse_args()

def run(*command, **kwargs):
    subprocess.run([str(item) for item in command], cwd=ROOT, check=True, **kwargs)

(ROOT / ".local/build-sources").mkdir(parents=True, exist_ok=True)
manifest = json.loads((ROOT / "packaging/third-party-sources.json").read_text())
for item in manifest:
    archive = ROOT / ".local/build-sources" / item["name"]
    if not archive.exists():
        run("curl", "--fail", "--location", "--retry", "3", item["url"], "--output", archive)
    if hashlib.sha256(archive.read_bytes()).hexdigest() != item["sha256"]:
        raise SystemExit(f"Source checksum mismatch: {item['name']}")

run("swift", "build", "-c", "release")
with (ROOT / ".local/ffmpeg-build.log").open("w") as log:
    run(sys.executable, "scripts/build-ffmpeg.py", stdout=log, stderr=subprocess.STDOUT)
with (ROOT / ".local/worker-build.log").open("w") as log:
    run(sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "--onedir",
        "--name", "HangosKonyvWorker", "--distpath", ".local/worker-dist", "--workpath", ".local/worker-build",
        "--specpath", ".local", "--paths", ".", "--collect-all", "piper", "--collect-all", "onnxruntime",
        "--collect-data", "certifi", "--copy-metadata", "piper-tts", "--copy-metadata", "onnxruntime",
        "--copy-metadata", "numpy", "scripts/worker-entry.py", stdout=log, stderr=subprocess.STDOUT)
artifacts = ROOT / "artifacts"
artifacts.mkdir(exist_ok=True)
app = artifacts / "HangosKonyv.app"
# Only this script's exact previous generated bundle is replaced.
if app.exists():
    shutil.rmtree(app)
macos = app / "Contents/MacOS"
resources = app / "Contents/Resources"
macos.mkdir(parents=True)
(resources / "tools").mkdir(parents=True)
shutil.copy2(ROOT / ".build/release/HangosKonyv", macos / "HangosKonyv")
shutil.copytree(ROOT / ".local/worker-dist/HangosKonyvWorker", resources / "worker", symlinks=True)
shutil.copy2(ROOT / ".local/tool-build/ffmpeg", resources / "tools/ffmpeg")
shutil.copy2(ROOT / "assets/brand/AppIcon.icns", resources / "AppIcon.icns")
with (app / "Contents/Info.plist").open("wb") as stream:
    plistlib.dump({"CFBundleIdentifier": "hu.szarkab.audio-book", "CFBundleName": "HangosKonyv",
                  "CFBundleDisplayName": "Hangoskönyv", "CFBundleExecutable": "HangosKonyv",
                  "CFBundlePackageType": "APPL", "CFBundleShortVersionString": VERSION,
                  "CFBundleVersion": "3", "CFBundleIconFile": "AppIcon", "LSMinimumSystemVersion": "26.0",
                  "NSHighResolutionCapable": True,
                  "NSDocumentsFolderUsageDescription": "A kiválasztott TXT és a mentett hanganyag eléréséhez."}, stream)
licenses = resources / "Licenses"
licenses.mkdir()
for name in ["piper-tts", "onnxruntime", "numpy", "certifi", "flatbuffers", "protobuf", "pathvalidate", "packaging", "typing-extensions"]:
    distribution = importlib.metadata.distribution(name)
    for entry in distribution.files or []:
        if "license" in str(entry).lower() or "copying" in str(entry).lower():
            source = distribution.locate_file(entry)
            if source.is_file():
                safe = str(entry).replace("../", "").replace("/", "_")
                folder = licenses / name
                folder.mkdir(exist_ok=True)
                shutil.copy2(source, folder / safe)
(licenses / "THIRD_PARTY_NOTICES.txt").write_text(
    "Piper 1.8.0 and eSpeak NG: GPL-3.0. FFmpeg 9.0.2 (audio-only LGPL configuration) and LAME 3.100: LGPL. "
    "Python: PSF. ONNX Runtime: MIT. NumPy: BSD and its bundled component notices. certifi: MPL-2.0.\n"
    "The DMG Sources directory supplies the application snapshot, build scripts, and the pinned copyleft component archives. "
    "The remaining runtime notices are included here.\n"
    "No separate license is specified for the application source. "
    "Third-party licenses retain their own terms.\n")
shutil.copy2(ROOT / "packaging/PYTHON-LICENSE.txt", licenses / "PYTHON-LICENSE.txt")
for filename, component in [("ffmpeg-9.0.2.tar.xz", "FFmpeg"), ("lame-3.100.tar.gz", "LAME"),
                            ("espeak-ng-724808c.tar.gz", "eSpeak")]:
    folder = licenses / component
    folder.mkdir()
    with tarfile.open(ROOT / ".local/build-sources" / filename) as archive:
        for member in archive.getmembers():
            relative = member.name.split("/", 1)[-1]
            if member.isfile() and "/" not in relative and relative.startswith(("COPYING", "LICENSE")):
                stream = archive.extractfile(member)
                if stream:
                    (folder / relative).write_bytes(stream.read())
run("codesign", "--force", "--sign", "-", resources / "tools/ffmpeg")
run("codesign", "--force", "--sign", "-", app)
run("codesign", "--verify", "--deep", "--strict", app)
print(app)
if args.app_only:
    raise SystemExit(0)

with tempfile.TemporaryDirectory(dir=artifacts, prefix=".dmg-stage-") as temporary:
    stage = Path(temporary)
    shutil.copytree(app, stage / app.name, symlinks=True)
    (stage / "Applications").symlink_to("/Applications")
    (stage / "Telepites.txt").write_text(
        "Hangoskönyv 0.3.0 — személyes előzetes\n\nApple Silicon (M1–M5), macOS 26 vagy újabb.\n"
        "Húzd a HangosKonyv alkalmazást az Applications mappába. Első alkalommal az appból tölthető le "
        "a 63,2 MB-os Imre-hang, utána a TXT → MP3 teljesen offline működik.\n\n"
        "A csomag ad-hoc aláírású, Apple Developer ID és notarizáció nélkül. "
        "Internetről letöltve a Gatekeeper blokkolhatja. Ez nem notarizált nyilvános kiadás.\n")
    sources = stage / "Sources"
    sources.mkdir()
    for item in manifest:
        shutil.copy2(ROOT / ".local/build-sources" / item["name"], sources / item["name"])
    shutil.copy2(ROOT / "packaging/third-party-sources.json", sources / "checksums.json")
    with (sources / "audio-book-source.tar.gz").open("wb") as stream:
        run("git", "archive", "--format=tar.gz", "--prefix=audio-book-source/", "HEAD", stdout=stream)
    (sources / "source-commit.txt").write_text(subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True))
    dmg = artifacts / f"HangosKonyv-{VERSION}-arm64.dmg"
    if dmg.exists():
        dmg.unlink()
    run("hdiutil", "create", "-volname", "HangosKonyv", "-srcfolder", stage,
        "-format", "UDZO", "-ov", dmg)
    checksum = hashlib.sha256(dmg.read_bytes()).hexdigest()
    (artifacts / f"{dmg.name}.sha256").write_text(f"{checksum}  {dmg.name}\n")
    print(dmg)

#!/usr/bin/env python3
"""Build the small ARM64 audio-only encoder; no Homebrew paths in the result."""
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import tarfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = "9.0.2"
SHA256 = "8c3850283eb25fa026482078a04051e0be17347b09ef81a0849bec15a96e002e"
archive = ROOT / f".local/build-sources/ffmpeg-{VERSION}.tar.xz"
archive.parent.mkdir(parents=True, exist_ok=True)
if not archive.exists():
    subprocess.run(["curl", "--fail", "--location", "--retry", "3", "--output", str(archive),
                    f"https://ffmpeg.org/releases/ffmpeg-{VERSION}.tar.xz"], check=True)
if hashlib.sha256(archive.read_bytes()).hexdigest() != SHA256:
    raise SystemExit("FFmpeg source checksum mismatch")
lame = Path(subprocess.check_output(["brew", "--prefix", "lame"], text=True).strip()).resolve()
if lame.name != "3.100":
    raise SystemExit("This build requires LAME 3.100")
work = ROOT / ".local/tool-build"
work.mkdir(parents=True, exist_ok=True)
static = work / "lame-static"
static.mkdir(exist_ok=True)
static_archive = static / "libmp3lame.a"
if static_archive.exists():
    static_archive.unlink()
shutil.copyfile(lame / "lib/libmp3lame.a", static_archive)
source = work / f"ffmpeg-{VERSION}"
if not source.exists():
    with tarfile.open(archive) as stream:
        stream.extractall(work, filter="data")
fingerprint = hashlib.sha256(Path(__file__).read_bytes() + (static / "libmp3lame.a").read_bytes()).hexdigest()
stamp = work / "ffmpeg-fingerprint"
output = work / "ffmpeg"
if not output.exists() or not stamp.exists() or stamp.read_text() != fingerprint:
    options = ["./configure", "--arch=arm64", "--cc=clang", "--disable-autodetect", "--disable-everything",
               "--disable-doc", "--disable-debug", "--disable-shared", "--enable-static", "--disable-avdevice",
               "--disable-swscale", "--disable-network", "--disable-ffplay", "--disable-ffprobe", "--enable-ffmpeg",
               "--enable-protocol=file,pipe", "--enable-demuxer=wav,pcm_s16le,mp3", "--enable-muxer=wav,mp3,null",
               "--enable-decoder=pcm_s16le,mp3float", "--enable-encoder=pcm_s16le,libmp3lame",
               "--enable-filter=aresample,aformat,anull,atempo", "--enable-swresample", "--enable-libmp3lame",
               f"--extra-cflags=-I{lame / 'include'} -mmacosx-version-min=26.0",
               f"--extra-ldflags=-L{static} -mmacosx-version-min=26.0"]
    subprocess.run(options, cwd=source, check=True)
    subprocess.run(["make", f"-j{min(os.cpu_count() or 2, 8)}"], cwd=source, check=True)
    shutil.copy2(source / "ffmpeg", output)
    stamp.write_text(fingerprint)
links = subprocess.check_output(["otool", "-L", str(output)], text=True)
dependencies = "\n".join(links.splitlines()[1:])
if "/opt/homebrew" in dependencies or "/Users/" in dependencies:
    raise SystemExit("The encoder still has external library dependencies")
print(output)

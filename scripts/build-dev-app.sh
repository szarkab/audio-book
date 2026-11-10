#!/bin/zsh
set -euo pipefail
TASK_ROOT="$(cd -- "$(dirname -- "$0")/.." && pwd)"
swift build --package-path "$TASK_ROOT"
python3 - "$TASK_ROOT" "${1:-omnivoice}" <<'PY'
from pathlib import Path
import plistlib
import shutil
import sys

root = Path(sys.argv[1])
engine = sys.argv[2]
if engine not in {'omnivoice', 'vibevoice'}:
    raise SystemExit('Use omnivoice or vibevoice')
name = 'HangosKonyv-VibeVoice' if engine == 'vibevoice' else 'HangosKonyv'
app = root / 'artifacts' / (name + '.app')
macos = app / 'Contents/MacOS'
macos.mkdir(parents=True, exist_ok=True)
staged = macos / '.HangosKonyv.pending'
shutil.copy2(root / '.build/debug/HangosKonyv', staged)
staged.replace(macos / 'HangosKonyv')
with (app / 'Contents/Info.plist').open('wb') as stream:
    plistlib.dump({
        'CFBundleIdentifier': 'hu.szarkab.audio-book.dev.vibevoice' if engine == 'vibevoice' else 'hu.szarkab.audio-book.dev',
        'AudioBookSpeechEngine': engine,
        'CFBundleName': 'HangosKonyv',
        'CFBundleDisplayName': 'Hangoskönyv VibeVoice' if engine == 'vibevoice' else 'Hangoskönyv',
        'CFBundleExecutable': 'HangosKonyv',
        'CFBundlePackageType': 'APPL',
        'CFBundleShortVersionString': '0.1.0',
        'CFBundleVersion': '1',
        'LSMinimumSystemVersion': '14.0',
        'NSHighResolutionCapable': True,
        'NSDocumentsFolderUsageDescription': 'A kiválasztott szöveg és a fejlesztői mappában tárolt helyi beszédmodell eléréséhez.',
    }, stream)
print(app)
PY
if [[ "${1:-omnivoice}" == "vibevoice" ]]; then
    codesign --force --sign - "$TASK_ROOT/artifacts/HangosKonyv-VibeVoice.app"
else
    codesign --force --sign - "$TASK_ROOT/artifacts/HangosKonyv.app"
fi

#!/bin/zsh
set -euo pipefail
TASK_ROOT="$(cd -- "$(dirname -- "$0")/.." && pwd)"
swift build --package-path "$TASK_ROOT"
python3 - "$TASK_ROOT" <<'PY'
from pathlib import Path
import plistlib
import shutil
import sys

root = Path(sys.argv[1])
app = root / 'artifacts/HangosKonyv.app'
macos = app / 'Contents/MacOS'
macos.mkdir(parents=True, exist_ok=True)
staged = macos / '.HangosKonyv.pending'
shutil.copy2(root / '.build/debug/HangosKonyv', staged)
staged.replace(macos / 'HangosKonyv')
with (app / 'Contents/Info.plist').open('wb') as stream:
    plistlib.dump({
        'CFBundleIdentifier': 'hu.szarkab.audio-book.dev',
        'CFBundleName': 'HangosKonyv',
        'CFBundleDisplayName': 'Hangoskönyv',
        'CFBundleExecutable': 'HangosKonyv',
        'CFBundlePackageType': 'APPL',
        'CFBundleShortVersionString': '0.2.0',
        'CFBundleVersion': '2',
        'CFBundleIconFile': 'AppIcon',
        'AUDIOBOOKDevelopmentRoot': str(root),
        'LSMinimumSystemVersion': '14.0',
        'NSHighResolutionCapable': True,
        'NSDocumentsFolderUsageDescription': 'A kiválasztott szöveg és a helyi Piper Imre modell eléréséhez.',
    }, stream)
resources = app / 'Contents/Resources'
resources.mkdir(parents=True, exist_ok=True)
shutil.copy2(root / 'assets/brand/AppIcon.icns', resources / 'AppIcon.icns')
print(app)
PY
codesign --force --sign - "$TASK_ROOT/artifacts/HangosKonyv.app"

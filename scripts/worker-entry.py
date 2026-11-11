"""The bundled worker uses only its own tools and certificate collection."""
import os
from pathlib import Path
import sys

import certifi

if getattr(sys, "frozen", False):
    tools = Path(sys.executable).resolve().parents[1] / "tools"
    os.environ["PATH"] = str(tools) + os.pathsep + "/usr/bin:/bin"
    os.environ["SSL_CERT_FILE"] = certifi.where()

from audiobook.__main__ import main

if __name__ == "__main__":
    raise SystemExit(main())

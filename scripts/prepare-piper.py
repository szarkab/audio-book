#!/usr/bin/env python3
"""Developer entry point to the same verified acquisition used by the app."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from audiobook.generation import GenerationService

if __name__ == "__main__":
    GenerationService().prepare_model()
    print("Piper Imre is ready.")

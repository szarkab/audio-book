"""JSON-lines transport for the native Mac application."""
import argparse
from contextlib import redirect_stdout
from dataclasses import asdict
import json
import os
from pathlib import Path
import sys
import resource
import time
import traceback

from .generation import GenerationError, GenerationService, JobEvent


MESSAGES = {
    "preparing": "A szöveg előkészítése…",
    "loading_model": "A narrátor betöltése…",
    "generating": "A magyar felolvasás készül…",
    "encoding": "Az MP3 mentése…",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["preview", "generate"])
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--expected-digest")
    parser.add_argument("--engine", choices=["omnivoice", "vibevoice"],
                        default=os.environ.get("AUDIOBOOK_ENGINE", "omnivoice"))
    parser.add_argument("--speed", type=float)
    args = parser.parse_args()
    protocol = sys.stdout

    def send(event: dict) -> None:
        print(json.dumps(event, ensure_ascii=False), file=protocol, flush=True)

    def progress(event: JobEvent) -> None:
        if event.state not in {"completed", "failed"}:
            send({**asdict(event), "message": MESSAGES.get(event.state, "Feldolgozás…")})

    started = time.perf_counter()
    try:
        service = GenerationService(engine=args.engine)
        if args.command == "preview":
            preview = service.preview(args.source)
            send({"state": "ready", **asdict(preview)})
        else:
            if args.output is None:
                raise GenerationError("Válaszd ki az MP3 mentési helyét.")
            with redirect_stdout(sys.stderr):
                result = service.generate(args.source, args.output, notify=progress,
                                          expected_digest=args.expected_digest,
                                          speed=args.speed if args.speed is not None else (1.0 if args.engine == "vibevoice" else 1.1))
            peak_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            metrics = {
                "audio_seconds": result.audio_seconds,
                "elapsed_seconds": time.perf_counter() - started,
                "peak_process_rss_bytes": peak_rss if sys.platform == "darwin" else peak_rss * 1024,
                "peak_temporary_audio_bytes": result.peak_temporary_audio_bytes,
                "mp3_bytes": result.output.stat().st_size,
            }
            print("GENERATION_METRICS " + json.dumps(metrics), file=sys.stderr, flush=True)
            send({"state": "completed", "output": str(result.output.resolve()), "message": "Elkészült az MP3.", **metrics})
        return 0
    except GenerationError as error:
        send({"state": "failed", "message": str(error)})
        return 1
    except Exception:
        traceback.print_exc(file=sys.stderr)
        send({"state": "failed", "message": "A helyi generálás nem sikerült. Próbáld újra; a részletek a munkanaplóban találhatók."})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

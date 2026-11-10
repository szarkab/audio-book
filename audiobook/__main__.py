"""JSON-lines transport for the native Mac application."""
import argparse
from contextlib import redirect_stdout
from dataclasses import asdict
import json
from pathlib import Path
import sys
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
    args = parser.parse_args()
    protocol = sys.stdout

    def send(event: dict) -> None:
        print(json.dumps(event, ensure_ascii=False), file=protocol, flush=True)

    def progress(event: JobEvent) -> None:
        if event.state not in {"completed", "failed"}:
            send({"state": event.state, "message": MESSAGES.get(event.state, "Feldolgozás…")})

    try:
        service = GenerationService()
        if args.command == "preview":
            preview = service.preview(args.source)
            send({"state": "ready", **asdict(preview)})
        else:
            if args.output is None:
                raise GenerationError("Válaszd ki az MP3 mentési helyét.")
            with redirect_stdout(sys.stderr):
                result = service.generate(args.source, args.output, notify=progress,
                                          expected_digest=args.expected_digest)
            send({"state": "completed", "output": str(result.output.resolve()), "message": "Elkészült az MP3."})
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

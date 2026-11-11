# Korábbi kísérleti komponensek

> Archív műszaki dokumentum, 2026-11-10–11. A jelenlegi működés leírása a [specifikációban](specification.md) található.

Az OmniVoice- és VibeVoice-kísérletek alábbi állományai nem részei az aktív Piper-alkalmazásnak. A Gitben korábban követett fájlok a `73fccdd` állapotból visszakereshetők.

| Korábbi fájl | Szerep |
| --- | --- |
| `audiobook/vibevoice.py` | VibeVoice-adapter |
| `scripts/prepare-vibevoice.py` | Modellkonverter |
| `scripts/audit_speech.py` | MLX/Whisper-diagnosztika |
| `scripts/voice_trial.py` | OmniVoice-hangpróba |
| `requirements-trial.lock` | MLX-próbakörnyezet függőségei |
| `assets/voices/README.md` | Szintetikus referencia leírása |
| `assets/voices/male-reference.json` | Referencia-metaadat |
| `assets/voices/male-reference.wav` | Szintetikus hangklónozási referencia |
| `tests/fixtures/README.md` | OmniVoice-regresszió leírása |
| `tests/fixtures/approved-male.mp3` | OmniVoice-regressziós hangminta |

A régi modellek, tesztalkalmazások, próbahangok és elkülönített környezetek nem szükségesek a Piper működéséhez. A megmaradó történeti dokumentumok a konfigurációkat, mérési eredményeket és a modellválasztás műszaki indokait rögzítik. Az aktív modell helyét és az előkészítését a [README](../README.md) tartalmazza.

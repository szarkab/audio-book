# Eltávolított régi források és tesztmaradványok

> Történeti feljegyzés: korábbi modellpróbák, mérések vagy fejlesztési ellenőrzések dokumentuma. Az aktuális alkalmazás működését a [specifikáció](specification.md) írja le.

Ezek az elutasított OmniVoice/VibeVoice-kísérletekhez tartoznak. A jelenlegi Piper-alkalmazás egyiküket sem használja. A nagy modellsúlyok már törölve vannak. A felhasználó 2026-11-10-én az alábbi pontos lista törlését kifejezetten jóváhagyta. Mind a tíz fájl eltávolítva.

1. `audiobook/vibevoice.py` — elvetett modelladapter.
2. `scripts/prepare-vibevoice.py` — elvetett modellkonverter.
3. `scripts/audit_speech.py` — már eltávolított MLX/Whisper-környezethez tartozó régi diagnosztika.
4. `scripts/voice_trial.py` — korábbi OmniVoice-hangpróba.
5. `requirements-trial.lock` — régi MLX-környezet függőségei.
6. `assets/voices/README.md` — korábbi szintetikus hangreferencia leírása.
7. `assets/voices/male-reference.json` — ugyanennek a metaadata.
8. `assets/voices/male-reference.wav` — elvetett hangklónozási referencia, a Pipernek nem kell.
9. `tests/fixtures/README.md` — korábbi OmniVoice-regresszió leírása.
10. `tests/fixtures/approved-male.mp3` — korábbi OmniVoice-próbaminta, nem az elfogadott Piper Imre.

A törlés az aktív munkapéldányból eltávolította őket; a Git történetéből a `73fccdd` állapot alapján visszaállíthatók. Könyvforrást, felhasználói MP3-at, más projektet, illetve a jelenlegi Piper modelljét és mintáját nem érinti.


## Saját, már Kukába helyezett kisebb tesztmaradványok

A felhasználó ugyanekkor e két saját elem végleges törlését is jóváhagyta; mindkettő eltávolítva. Kizárólag a következő két, a fejlesztés során általunk létrehozott elemről van szó, nem a Kuka teljes tartalmáról:

- `~/.Trash/audio-book-tesztmaradvanyok-20261110-200359` — lecserélt tesztalkalmazás, saját próbafájlok és naplók, félbehagyott saját kísérleti kód.
- `~/.Trash/HangosKonyv-korabbi-20261110-171510.app` — a korábban lecserélt HangosKonyv-alkalmazás.

E két elem tartalma a Kukából már nem állítható vissza. Az aktív Piper-alkalmazás, a jóváhagyott Imre-minta, az új Piper-kimenetek és a felhasználó könyvfájljai külön helyen maradnak.

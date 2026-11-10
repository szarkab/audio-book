# Hangoskönyv

Magyar TXT-fájlok helyi felolvasása férfi narrátorhanggal, Apple Silicon Macen. A jelenlegi első fejlesztői változat rövid, legfeljebb 600 karakteres UTF-8 TXT-fájlt alakít egyetlen mono, 96 kbit/s MP3-má. A beszédgenerálás a már letöltött OmniVoice-bfloat16 modellt használja MLX-szel, a GPU-n; nincs felhős beszédgenerálás.

## Fejlesztői indítás

Szükséges: Apple Silicon Mac, Xcode vagy Swift 6 eszközök, uv és FFmpeg. A modell beszerzéséhez internet szükséges; generáláskor nincs rá szükség.

```sh
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r requirements-dev.txt
```

A modell letöltési útja és rögzített revíziója a [hangpróba leírásában](docs/voice-trial.md) található. A már előkészített fejlesztői gépen a modell rendelkezésre áll.

```sh
./scripts/build-dev-app.sh
open artifacts/HangosKonyv.app
```

Az így létrejövő alkalmazásablakból választható ki a TXT-fájl, látható az előnézet, elindítható a generálás, és megnyitható a kész MP3. Meglévő célfájlt nem ír felül; új nevet kell választani. Ha az előnézet óta megváltozott a forrásszöveg, az alkalmazás új kiválasztást kér.

Ez fejlesztői alkalmazáscsomag: az aktuális forrásmappát, annak Python-környezetét, modelljét és a helyi FFmpeg-et használja. Nem önálló telepítő és nem a későbbi DMG. A hosszú fájlok, Markdown, megszakítás utáni folytatás, első modellletöltés és önálló csomagolás külön feladatok.

Generálás közben a normál kilépés figyelmeztetést ad, mert ez a változat még nem képes folytatni a megszakadt munkát. A kényszerített bezárás nem támogatott munkamenet. A helyi futtatónaplók a `.local/logs` mappába kerülnek; nem kerülnek Gitbe.

## Fejlesztői ellenőrzés

```sh
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m mypy audiobook --check-untyped-defs --ignore-missing-imports
swift build
```

Az automatizált ellenőrzések a teljes generálási feladat nyilvános határát használják. Csak a külső beszédmodell helyett adnak szabályozható teszthangot; a fájlkezelés és az MP3-kódolás valódi. A valódi GPU-s modellpróba, a felület és a böngészős lejátszás külön integrációs ellenőrzés.

## Projekt

- [Teljes specifikáció](https://github.com/szarkab/audio-book/issues/1)
- [Első alkalmazásfolyamat](https://github.com/szarkab/audio-book/issues/2)
- [Magyar hangpróba eredményei](docs/voice-trial-results.md)

A projekt saját használatra készül. Az eredeti modellsúlyok CC-BY-NC feltételeit a közösségi MLX-átalakítás nem írja felül; a források a hangpróba dokumentációjában találhatók.

# Hangoskönyv

Magyar TXT-fájlok helyi felolvasása férfi narrátorhanggal, Apple Silicon Macen. A fejlesztői változat magyar UTF-8 TXT-fájlokat alakít egyetlen mono, 96 kbit/s MP3-má, automatikus belső feldolgozással és szövegalapú haladásjelzéssel. A korábbi 600 karakteres korlát megszűnt. A beszédgenerálás a már letöltött OmniVoice-bfloat16 modellt használja MLX-szel, a GPU-n; nincs felhős beszédgenerálás.

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

Az így létrejövő alkalmazásablakból választható ki a TXT-fájl, látható az előnézet, elindítható a generálás, és a kész MP3 az ablak saját lejátszójával hallgatható meg. A lejátszás csak a Lejátszás gombra indul, bármikor szüneteltethető vagy leállítható; nincs automatikus átadás a Zene alkalmazásnak. Meglévő célfájlt nem ír felül; új nevet kell választani. Ha az előnézet óta megváltozott a forrásszöveg, az alkalmazás új kiválasztást kér.

A teljes kiválasztott szöveg automatikusan végigfut; belső részeket nem kell jóváhagyni és nincs külön részexport. A mondatok és önálló bekezdések határain dolgozik. A férfihang az eredetileg elfogadott hangtervezési beállítást használja; a hangreferenciás kísérletet a felhasználó által jelzett hibák miatt visszavontuk. A hosszú narráció hangállandósága és minősége további átvételt igényel.

A teljes hanganyag nem kerül egyszerre RAM-ba: a modell egy szövegrész hangját tartja memóriában, a hangrészek folyamatosan lemezre kerülnek, és egyszer, a végén készül el az MP3. Az átmeneti tárhely a hanghosszal nő, a teljes modell kontextusához szükséges memória a legnagyobb feldolgozott mondat méretétől is függ. Egyetlen rendkívül hosszú, mondat- és bekezdéshatár nélküli szöveg továbbra is elérheti a modell erőforráskorlátait; a rendszer nem csonkolja észrevétlenül.

Ez fejlesztői alkalmazáscsomag: az aktuális forrásmappát, annak Python-környezetét, modelljét és a helyi FFmpeg-et használja. Nem önálló telepítő és nem a későbbi DMG. A Markdown, megszakítás utáni folytatás, első modellletöltés és önálló csomagolás külön feladatok. A hosszú fájlok többperces minőségi átvétele folyamatban van.

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

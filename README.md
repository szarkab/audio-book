# Hangoskönyv — Piper Imre

Magyar UTF-8 TXT-fájlok helyi felolvasása az elfogadott **Piper Imre** férfihanggal. Egy fájlból egyetlen mono, 96 kbit/s MP3 készül, alapértelmezésben a korábban elfogadott tempóval. A kész Piper motor CPU-n fut; a generálás nem igényel internetet, felhőt, hangklónozást vagy GPU-t.

## Indítás

A jelenlegi fejlesztői gépen az egyetlen alkalmazás az `artifacts/HangosKonyv.app`. Első használatkor az **Imre-hang letöltése** gomb beszerzi az ellenőrzött 63,2 MB-os modellt; ehhez legalább 128 MB szabad hely kell. A felület jelzi a hiányzó, letöltés alatt álló, hibás és kész állapotot, hiba után a letöltés újrapróbálható. Az eredet és az adat-/motorlicenc hivatkozásai is elérhetők. A kész modell után a generálás offline működik. Válassz TXT-fájlt, ellenőrizd az előnézetet, majd indítsd az MP3-készítést. A kész hang csak a Lejátszás gombra indul; szüneteltethető, leállítható és tekerhető. Meglévő MP3-at nem ír felül, az előnézet óta megváltozott forrásnál új kiválasztást kér.

A **Felolvasás beállításai…** gombbal MP3-készítés előtt állítható a tempó, a ritmus és hang változatossága, a kimeneti hangerő, a hangerő-normalizálás és az extra mondatszünet. A kimeneti hangerő a mentett fájlt módosítja, a lejátszó hangerejétől függetlenül. A csúcskorlát megakadályozza a túlvezérlést. Az **Elfogadott alapértékek visszaállítása** minden értéket visszaállít: 1× tempó, 0,333 ritmus, 0,5 hangváltozatosság, 1× hangerő, bekapcsolt normalizálás, 0 s extra szünet. A választás az app bezárásáig marad meg, és a futó generálás alatt nem módosítható. Külön hangsúlyozás-szabályzó nincs.

A biztos sorszámos alakok 1–100 között betűs alakban jelennek meg az előnézetben és kerülnek felolvasásra (például `1. fejezet` → `első fejezet`). A felismerés csak a következő, kisbetűvel és pontosan így írt szavak előtt működik: fejezet, próba, versenyző, hely, alkalom, emelet, kötet, oldal, pont, rész, lépés. A dátumok, verziók, vezető nullás számok, 100 feletti számok és más bizonytalan alakok megmaradnak. Nagybetűs folytatások (`1. Fejezet`), toldalékos főnevek (`1. fejezetben`) és puszta listaelemek (`1. Első teendő`) nem kapnak automatikus átírást; ezek betűvel megadhatók a forrásban. Az eredeti fájl változatlan.

A teljes fájl köztes jóváhagyás nélkül feldolgozódik. A rövid belső egységek veszteségmentes PCM-ben állnak össze a lemezen, majd egyszer készül az MP3. A forrásfájl változatlan marad.

Ez fejlesztői alkalmazás: a projekt Python-környezetét, helyi modelljét és FFmpeg-jét használja. A további feladatok a sorszámkiejtés meghallgatásos elfogadása, valamint az önálló DMG saját arculattal, színekkel és appikonnal. A végső átvétel a telepített helyi alkalmazásban történik. A felhasználó kérésére az MD-beolvasás és a generálás szüneteltetése/tartós folytatása kikerült a tervből; böngészős felület vagy böngészős próba nem szükséges.

## Fejlesztői előkészítés

Szükséges: Apple Silicon Mac, Swift 6 eszközök, uv és FFmpeg.

```sh
uv venv --python 3.12 .venv
uv pip sync --python .venv/bin/python requirements-dev.txt
.venv/bin/python scripts/prepare-piper.py
./scripts/build-dev-app.sh
open artifacts/HangosKonyv.app
```

A rögzített Imre-modell és ellenőrzött modellkártya egyszeri letöltése körülbelül 63 MB; helye a felhasználó `~/Library/Application Support/HangosKonyv/models/piper-imre` mappája. Fejlesztői próbához az `AUDIOBOOK_MODEL_PATH` felülírhatja ezt. A letöltési tárhelyigény a meglévő és átmeneti példány együttesét is fedezi. A modell a projekt forrásmappájától függetlenül megmarad. A fájlok ellenőrzőösszegét az előkészítés és az első használat ellenőrzi. A generálás a Piper eredeti alapbeállításaival működik; a 22 050 Hz-es hang veszteségmentes belső formátumba alakítása megőrzi a tempót és hangmagasságot.

## Ellenőrzés

```sh
AUDIOBOOK_REAL_PIPER_TEST=1 .venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m mypy audiobook --check-untyped-defs --ignore-missing-imports
```

A tesztek a teljes generálási feladat nyilvános határát használják. A valódi Piper-próba a létrejövő hang hallhatóságát, dekódolását és időtartamát ellenőrzi; a kiejtés és természetesség meghallgatással fogadható el. A célgépes hosszú próba 5395 karakterből 9,64 másodperc alatt körülbelül 6 perces MP3-at készített; a felhasználó a Piper hangminőségét egyelőre elfogadta. [Megvalósítás és mérések](docs/implementation-issue-13.md).

A lecserélt nagy modellek és külön próbakörnyezetek kikerültek az aktív munkamappából; csak az Imre modell maradt. A kisebb tesztmaradványok visszaállíthatóan a Kukába kerültek. A további takarításnál a könyvforrások, a felhasználó által mentett hangok és más projektek megmaradnak.

## Projekt és források

- [Felolvasási beállítások](https://github.com/szarkab/audio-book/issues/14)
- [Piper Imre-feladat](https://github.com/szarkab/audio-book/issues/13)
- [Eredeti termékspecifikáció](https://github.com/szarkab/audio-book/issues/1)
- [Piper motor](https://github.com/OHF-Voice/piper1-gpl) — GPL-3.0
- [Imre-modellkártya](https://huggingface.co/rhasspy/piper-voices/blob/cf910fb59f1d79ab3b625a63993a108751c6c25d/hu/hu_HU/imre/medium/MODEL_CARD) — CC0 adathalmaz

A korábbi modellkísérletek dokumentumai történeti feljegyzések; az aktuális alkalmazás kizárólag Piper Imrét használ.

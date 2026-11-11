# Hangoskönyv — Piper Imre

Magyar UTF-8 TXT-fájlok helyi felolvasása **Piper Imre** magyar férfihanggal. Egy fájlból egyetlen mono, 96 kbit/s MP3 készül. A kész Piper motor CPU-n fut; a generálás nem igényel internetet, felhőt, hangklónozást vagy GPU-t.

## Telepítés és indítás

Apple Silicon Mac és **macOS 26 vagy újabb** szükséges.

1. Töltsd le a DMG-t a [GitHub-kiadásból](https://github.com/szarkab/audio-book/releases/tag/v0.3.0-preview).
2. Másold a **HangosKonyv** alkalmazást az Applications mappába, majd indítsd el.
3. Az **Imre-hang letöltése** gombbal töltsd le a 63,2 MB-os modellt. Ehhez internetkapcsolat és legalább 128 MB szabad hely szükséges.
4. Válassz egy magyar UTF-8 TXT-fájlt, ellenőrizd az előnézetet, majd indítsd el az MP3 készítését.

Az alkalmazás tartalmazza a futtatókörnyezetet: külön Python, Homebrew vagy projektmappa nem szükséges. A modell letöltése után a felolvasás teljesen offline működik.

Az előzetes ad-hoc aláírású, Apple-notarizáció nélkül, ezért a macOS az első indítást blokkolhatja. Megbízható példány esetén az első megnyitási kísérlet után a **Rendszerbeállítások → Adatvédelem és biztonság → Megnyitás mindenképpen** lehetőség használható. [Apple útmutató](https://support.apple.com/en-us/102445).

## Használat és beállítások

Egy TXT-fájlból egyetlen MP3 készül, köztes jóváhagyás nélkül. A kész hang a **Lejátszás** gombra indul; szüneteltethető, leállítható és tekerhető. A következő szöveg külön feladatban dolgozható fel. Az alkalmazás meglévő MP3-at nem ír felül.

A **Felolvasás beállításai…** gombbal MP3-készítés előtt állítható a tempó, a ritmus és hang változatossága, a kimeneti hangerő, a hangerő-normalizálás és az extra mondatszünet. A kimeneti hangerő a mentett fájlt módosítja, a lejátszó hangerejétől függetlenül. A csúcskorlát megakadályozza a túlvezérlést. Az **Elfogadott alapértékek visszaállítása** minden értéket visszaállít: 1× tempó, 0,333 ritmus, 0,5 hangváltozatosság, 1× hangerő, bekapcsolt normalizálás, 0 s extra szünet. A választás az app bezárásáig marad meg, és a futó generálás alatt nem módosítható. Külön hangsúlyozás-szabályzó nincs.

A biztos sorszámos alakok 1–100 között betűs alakban jelennek meg az előnézetben és kerülnek felolvasásra (például `1. fejezet` → `első fejezet`). A felismerés csak a következő, kisbetűvel és pontosan így írt szavak előtt működik: fejezet, próba, versenyző, hely, alkalom, emelet, kötet, oldal, pont, rész, lépés. A dátumok, verziók, vezető nullás számok, 100 feletti számok és más bizonytalan alakok megmaradnak. Nagybetűs folytatások (`1. Fejezet`), toldalékos főnevek (`1. fejezetben`) és puszta listaelemek (`1. Első teendő`) nem kapnak automatikus átírást; ezek betűvel megadhatók a forrásban. Az eredeti fájl változatlan.

A teljes fájl köztes jóváhagyás nélkül feldolgozódik. A rövid belső egységek veszteségmentes PCM-ben állnak össze a lemezen, majd egyszer készül az MP3. A forrásfájl változatlan marad.

A modell és a munkanaplók a macOS Library mappájában találhatók, a forrásprojekttől függetlenül. Az alkalmazás kizárólag TXT-bemenetet kezel. A generálás szüneteltetése és újraindítás utáni folytatása nem támogatott.

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

## Önálló csomag előállítása

A fejlesztői gépen Swift-eszközök, Python 3.12, uv és Homebrew LAME 3.100 szükséges. A telepített appnak ezekre nincs szüksége.

```sh
uv pip sync --python .venv/bin/python requirements-build.txt
.venv/bin/python scripts/build-release.py
```

Az audio-only FFmpeg 9.0.2 ellenőrzött forrásból, statikus LAME-könyvtárral épül. A PyInstaller 6.22.3 a Python-futtatót és a Piper függőségeit saját mappába gyűjti. A CA-tanúsítványok is a csomag részei. A modell külön, első letöltésben érkezik. Az ikon vektoros forrása a `scripts/make-icon.swift`; a PNG és ICNS kimenetek a `assets/brand` mappában vannak.

## Ellenőrzés

```sh
AUDIOBOOK_REAL_PIPER_TEST=1 .venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m mypy audiobook --check-untyped-defs --ignore-missing-imports
```

A tesztek a teljes TXT → MP3 folyamatot, a beállításokat és a hibakezelést vizsgálják. A valódi Piper-próba a hang hallhatóságát, dekódolhatóságát és időtartamát ellenőrzi; a kiejtés és a természetesség megítéléséhez meghallgatás szükséges. A telepített csomag teszteléséhez az `AUDIOBOOK_PACKAGED_APP` változóval adható meg az alkalmazás elérési útja.

Részletes eredmények: [ellenőrzési összefoglaló](docs/final-acceptance.md).

## Dokumentáció és források

- [Funkcionális specifikáció](docs/specification.md)
- [Felolvasási beállítások](https://github.com/szarkab/audio-book/issues/14)
- [Piper Imre-feladat](https://github.com/szarkab/audio-book/issues/13)
- [Eredeti termékspecifikáció](https://github.com/szarkab/audio-book/issues/1)
- [Piper motor](https://github.com/OHF-Voice/piper1-gpl) — GPL-3.0
- [Imre-modellkártya](https://huggingface.co/rhasspy/piper-voices/blob/cf910fb59f1d79ab3b625a63993a108751c6c25d/hu/hu_HU/imre/medium/MODEL_CARD) — CC0 adathalmaz

A korábbi modellkísérletek dokumentumai történeti feljegyzések; az aktuális alkalmazás kizárólag Piper Imrét használ.

A GitHub és az érzékenyadat-ellenőrzés összefoglalója: [ellenőrzési jegyzőkönyv](docs/security-check.md).

A külső komponensek licencszövegei az alkalmazásban, a kapcsolódó forráscsomagok és az alkalmazás forráspillanatképe a DMG `Sources` mappájában találhatók. A projekt saját forráskódjához nincs külön licenc megadva.

# #10 — Rövid magyar VibeVoice az M5-ön

Dátum: 2026-11-10. [Feladat](https://github.com/szarkab/audio-book/issues/10), [kiegészítő specifikáció](https://github.com/szarkab/audio-book/issues/9).

Állapot: a teljes rövid TXT → MP3 folyamat a célgépen, a külön natív alkalmazásból is működik. A helyi hang természetességének felhasználói elfogadása még nyitott, ezért #10 nincs lezárva. Hosszú VibeVoice-futás (#11), sorszámkiejtés (#12), tartós folytatás és DMG nem része ennek a készültségi állításnak.

## Kiválasztott változat

A teljes `Cseti/VibeVoice_7B_hun_v2` checkpoint revíziója `22434d6f261e2f231b3c358563bdf2d2e8caab57`. A 37,37 GB körüli F32-forrásból a helyi fejlesztői előkészítő egy súlyfájlon belül, súlyonként készít új változatot; nem materializálja egyszerre a teljes eredeti modellt. A forrás minden súlyfájljának SHA-256 értékét a rögzített HF-revízió metaadatával ellenőrzi. Mind az 1205 eredeti modellparaméter átkerült, a formátum- és alakkonverziókat szigorú ellenőrzés fedi.

A nyelvi modul és a kimeneti nyelvi fej mátrixai 4 bites affine kvantálást kaptak 64-es csoportmérettel; a nyelvi skalár-/normalizáló paraméterek FP16 alakúak. A teljes magyarra finomhangolt diffúziós fej, az akusztikus és szemantikus kodek, valamint a hangcsatlakoztató modulok az eredeti F32-pontosságukat őrzik. Az elkészült súlyfájlok mérete 11 195 416 856 byte, nyolc fájlban. Ez nem a teljes futási memória.

A tokenizáló az eredeti alapmodell előfeldolgozási leírásában megadott `Qwen/Qwen2.5-7B`, revíziója `d149729398750b98c0af14eb82c78cfe92750796`. Csak a szövegtokenizáló állományai kerültek mellé; a Qwen modellsúlyait nem töltjük le. A VibeVoice teljes nyelvi súlyai a magyar checkpointból származnak.

A futtató `mlx-audio==0.6.5`, `mlx==0.32.4`. Az adapter kizárólag a helyi tokenizálót tölti, szigorúan betölti a modell összes súlyát, ellenőrzi a rögzített magyar eredetjelölést, és kötelezően Apple GPU-eszközt választ. Nincs távoli tokenizáló-feloldás vagy észrevétlen CPU-visszaesés. Az eredetjelölés a fejlesztői csomag azonosítására szolgál; nem digitális aláírás. Az elkészült súlyfájlok ellenőrzőösszegeit az előkészítési jegyzék tartalmazza.

A férfi referencia a korábban elfogadott szintetikus férfiminta teljes első két mondata, 8,07 másodperces tiszta WAV. A fájl ellenőrzőösszegét az alkalmazás ellenőrzi. A VibeVoice saját referenciahang-kódolása fut; az OmniVoice belső hangtokenjei nem kerülnek át. A korábbi hang pontos megőrzését vagy az új hang természetességét ez önmagában nem igazolja.

Alapbeállítás: eredeti tempó, 1,0× export, CFG 1,3, 20 diffúziós lépés, rögzített véletlenmag. A generálási lépés-/kontextuskorlát elérése hibát okoz, nem késznek jelölt részleges hangot. A kész jel a meglévő veszteségmentes összeállításon és egyszeri 96 kbit/s mono MP3-kódoláson megy át.

## Célgépes eredmény

Célgép: Apple M5, 32 GB egyesített memória. Az első fejlesztői futás és a külön alkalmazásból indított futás is kikapcsolt HF/Transformers hálózati modellfeloldással, kizárólag már helyben meglévő komponensekből készült el. A helyi tokenizálóhoz kötelező a `local_files_only`; maga a modellbetöltés nem hív letöltő API-t. Ez a futtatási út offline működésének vizsgálata, nem az egész Mac hálózati forgalmának mérése.

A próba 118 karakter, két magyar mondat; szövege eltér a hangreferenciától. Mindkét futás 8,4 másodperces, 101 709 byte-os MP3-at adott, byte-ról byte-ra azonos tartalommal. Az alkalmazásfutás 65,72 másodpercig, az első CLI-futás 70,45 másodpercig tartott; ez rövid minta, nem hosszúkönyves sebességígéret.

Az alkalmazásfutás MLX által mért csúcsmemóriája 12 611 382 580 byte, a folyamat csúcs-RSS-e 8 746 893 312 byte. Eltérő mérési kategóriák; nem összeadandók és egyik sem a teljes rendszer memóriahasználata. Az átmeneti hangfájlok legnagyobb összeadott logikai mérete 806 444 byte volt. A modell beszerzésének és konverziójának tárhelye ebben nincs benne.

Helyi Whisper-átírás: 17 várt és 17 felismert szó; normalizált karakteres eltérés 1,01%. Az egyetlen eltérés „eleredt” / „elerett”; ezt az ASR önmagában nem dönti el kiejtési hibának. Nem volt kimutatott szókihagyás vagy ismétlés. Az átírás nem bizonyít természetes prozódiát, férfihang-azonosságot vagy hibátlan kiejtést.

A valódi alkalmazáspróba fájlválasztással, szövegelőnézettel, mentési panellel és haladásjelzéssel indult, végül „Elkészült az MP3.” és leállított saját lejátszó jelent meg. A lejátszás nem indult automatikusan. A teljes alkalmazásból készült fájl FFmpeg-dekódolása hibamentes. A korábbi lejátszógombok implementációja nem változott.

A helyi, Gitből kizárt eredmények az `artifacts/issue10-vibevoice` könyvtárban találhatók. A meghallgatható alkalmazásminta `ablakbol-ferfi.mp3`; a teljes mintát kevesebb mint kilenc másodperc meghallgatni. Nagy modellállományok nem kerülnek Gitbe.

## Fejlesztői reprodukció

A forrás egyszeri beszerzése a modellkártya aktuális feltételeivel összhangban, a fenti rögzített revízióból történjen. A forráskönyvtár legyen `.local/models/VibeVoice_7B_hun_v2-source`, és a konfiguráció, súlyindex és mind a nyolc safetensors legyen benne. A szükséges eredeti letöltés körülbelül 37,37 GB; a konverzió további munkaterületet igényel. A próbakezdéskor több mint 500 GiB szabad tárhely állt rendelkezésre.

```sh
.venv/bin/python scripts/prepare-vibevoice.py
./scripts/build-dev-app.sh vibevoice
open artifacts/HangosKonyv-VibeVoice.app
```

Az előkészítő hálózatot használ a rögzített forrás ellenőrzőösszegeihez és a szövegtokenizáló egyszeri beszerzéséhez. Meglévő végleges modellkönyvtárat nem ír felül. Félbehagyott kimenetből nem lesz használatra kész modell. Az alkalmazásnak ezután nincs szüksége hálózati modellfeloldásra vagy fejlesztői konverzióra generálás közben. Az önálló, felhasználói modellbeszerzés és DMG külön feladat.

```sh
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 AUDIOBOOK_REAL_VIBEVOICE_TEST=1 \
  .venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m mypy audiobook --check-untyped-defs --ignore-missing-imports
```

A valódi modellregresszió a teljes generálási szolgáltatást használja, majd helyi ASR-rel ellenőrzi a forrástartalmat. A korábbi OmniVoice-próba külön továbbra is az `AUDIOBOOK_REAL_MODEL_TEST=1` kapcsolóval futtatható; az új kapcsoló a kiválasztott VibeVoice-változatot ellenőrzi.

A félbehagyott, saját sorszám-/1,15× finomítások külön mentése a `.local/deferred/ordinal-before-vibevoice` könyvtárban maradt a #12 számára. Nem kerültek a #10-be; a VibeVoice-ra a gyorsítás nem örökölhető.

## Záró ellenőrzés és review

A végső teljes csomag mind a 22 tesztje sikeres, a valódi VibeVoice-modellregresszióval és helyi ASR-rel, kikapcsolt hálózati modellfeloldással: 70,305 másodperc. A dokumentált mypy-ellenőrzés 7 forrásfájlon sikeres. A Swift-fordítás, a külön VibeVoice-alkalmazás újraépítése és szigorú aláírásellenőrzése sikeres. A natív alkalmazásból mentett teljes MP3 hibamentesen dekódolható.

### Standards

A `80020d6...2ffe165` diff külön Standards-ellenőrzése 0 dokumentált szabálysértést és 0 javítást indokoló baseline kódszagot talált. A modelladapter, előkészítés és közös generálás felelőssége elkülönül, új tesztelési határ nem került be.

### Spec

A külön Spec-ellenőrzés 0 igazolt követelményhibát talált. A rögzített teljes magyar checkpoint, kvantálás, saját férfireferencia, helyi tokenizáló, kötelező GPU, külön alkalmazás, 1,0× tempó, biztonságos véglegesítés és kézi lejátszás megfelel a #10-nek. A felhasználó helyi meghallgatása az egyetlen nyitott átvételi feltétel; nem tekinthető az ASR-rel kiváltottnak.

Összesítés: Standards 0, Spec 0 fennmaradó finding. A #10 nyitva marad a férfiminta emberi elfogadásáig; a #11/#12 feladatokat nem tekintjük elkészültnek.

## Források

- [Magyar modell és feltételei](https://huggingface.co/Cseti/VibeVoice_7B_hun_v2)
- [Eredeti alapmodell előfeldolgozási konfigurációja](https://huggingface.co/aoi-ot/VibeVoice-Large/blob/1b81fecc784a076dcd935678db551871f4598ebf/preprocessor_config.json)
- [MLX VibeVoice-kód](https://github.com/Blaizzy/mlx-audio/tree/main/mlx_audio/tts/models/vibevoice)

# Piper Imre motor és mérések — #13

> Archív műszaki dokumentum, 2026-11-10–11. A jelenlegi működés leírása a [specifikációban](specification.md) található.

Kapcsolódó feladat: [#13](https://github.com/szarkab/audio-book/issues/13).

## Motor

A Piper 1.8.0 a `hu_HU-imre-medium` modellt használja, a `rhasspy/piper-voices` `cf910fb59f1d79ab3b625a63993a108751c6c25d` revíziójából. Az ONNX-modell mérete 63 221 984 byte; a modell és a konfiguráció integritását ellenőrzőösszeg védi. A motor espeak-ng fonemizálást és ONNX Runtime CPU-végrehajtást használ.

A 22 050 Hz-es PCM-hang 24 kHz-es veszteségmentes munkafolyamba alakul, a tempó és hangmagasság megváltoztatása nélkül. A rövid részek közös feldolgozáson és egyszeri, mono 96 kbit/s MP3-kódoláson mennek át. A modell feladatonként egyszer töltődik be. Az aktív alkalmazás nem tartalmaz alternatív motort vagy hangklónozást.

## Célgépes mérések

| Mért adat | Hosszabb minta | Rövid natív minta |
| --- | --- | --- |
| Bemenet | 5395 karakter, 38 belső rész | Rövid TXT |
| Generálási idő | 9,637 s | 1,023 s |
| Hanghossz | 360,827 s | 15,128 s |
| MP3 mérete | 4 330 989 byte | 182 637 byte |
| Folyamat csúcs-RSS | 618 348 544 byte | 266 731 520 byte |
| Logikai átmeneti hangméret | 21 650 699 byte | — |

Mindkét teljes MP3 hibamentesen dekódolható volt. A hosszabb minta helyi ASR-eltérése 5,31% karakteres és 15,30% szószintű volt, 876 várt és 869 felismert szóval. A 3%-os diagnosztikai karakterküszöb nem teljesült. A mérés nem bizonyít hibátlan kiejtést vagy szöveghűséget.

Az akkori tesztcsomag 21 sikeres próbát tartalmazott valódi Piperrel (2,466 s), hibamentes típusellenőrzéssel, Swift-fordítással és aláírás-ellenőrzéssel. A jelenlegi csomag eredményeit az [ellenőrzési összefoglaló](final-acceptance.md) tartalmazza.

## Szünet- és tempókísérlet

Egy elkülönített vizsgálat a Piper fonéma-időzítési kimenetét használta, a modell súlyainak módosítása nélkül. A három vesszőnél mért szakasz 69,66 / 81,27 / 116,10 ms volt. A kísérlet ezeket 180 ms-ra egészítette ki, a mondatvégen legalább 350 ms helyet hagyva. A csendbeszúrás a jelölt szakasz legcsendesebb 10 ms-os ablakában történt.

| Konfiguráció | Hanghossz |
| --- | --- |
| Összehasonlító alap | 11,32 s |
| Hozzáadott szünetek | 11,84 s |
| Hozzáadott szünetek, 1,08 length_scale | 12,31 s |

Minden eredeti nem nulla PCM-minta változatlan sorrendben maradt, de ez önmagában nem bizonyít hallhatatlan illesztést. Meghallgatáskor mindkét kísérleti változat gyorsított hatásúnak és az alapnál gyengébbnek tűnt. A különböző szöveg, véletlenmag és időzítési kimenet miatt a pontos akusztikai ok nem különült el. A kísérleti beállítások nem részei az alkalmazásnak; a Piper alapértékei maradtak érvényben.

## Miért gyors a Piper?

A VITS-alapú modell egy mondat fonémaazonosítóiból egyetlen ONNX-futtatással állít elő hangot. Nincs diffúziós lépésszám vagy több számítással nagyobb modellkapacitást biztosító minőségi kapcsoló. A tempó, a véletlenszerűségi paraméterek és a hangerő a megszólalást módosítják. Több CPU-szál vagy GPU-használat önmagában nem javítja a hangsúlyozást; a magasabb MP3-bitrátának a tömörítési veszteségre lehet hatása.

## Korábbi függőségek

Az OmniVoice-, VibeVoice-, Whisper- és beszélődiagnosztikai modellállományok összesített eltávolított logikai mérete 52 270 032 933 byte volt. Az MLX, Transformers és a régi hangkódolók nem aktív futtatási függőségek. A kis történeti források listája az [eltávolított komponenseknél](piper-retired-files.md) található.

## Források

- [VITS párhuzamos beszédszintézis](https://arxiv.org/abs/2106.06103)
- [Piper CLI](https://github.com/OHF-Voice/piper1-gpl/blob/main/docs/CLI.md)
- [Imre-modellkártya](https://huggingface.co/rhasspy/piper-voices/blob/cf910fb59f1d79ab3b625a63993a108751c6c25d/hu/hu_HU/imre/medium/MODEL_CARD)

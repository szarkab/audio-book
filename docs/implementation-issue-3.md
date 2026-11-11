# OmniVoice hosszúszöveges vizsgálat — #3

> Archív műszaki dokumentum, 2026-11-10–11. A jelenlegi működés leírása a [specifikációban](specification.md) található.

Kapcsolódó feladat: [#3](https://github.com/szarkab/audio-book/issues/3). A dokumentum az időközben megszüntetett OmniVoice-adapter eredményeit rögzíti.

## Feldolgozás

A hosszúszöveges út teljes UTF-8 TXT-t dolgozott fel, legfeljebb kétmondatos belső egységekben. A részek nyers PCM-fájlban álltak össze, 4096 képkockás blokkokban; a végén egyszeri mono, 24 kHz-es, 96 kbit/s MP3-kódolás történt. A modell feladatonként egyszer töltődött be. Üres vagy levágott hangrész hibát eredményezett.

A saját lejátszó kézi indítást, szünetet, leállítást, idővonalat és hangerőt biztosított. A fájl betöltése nem indított automatikus lejátszást.

## Referenciahang és szöveghűség

A levágott, átirat nélküli referenciahangos konfigurációnál kihagyások, újrakezdések és kiejtési hibák jelentkeztek. A referencia kikapcsolása ugyanazon a bemeneten jelentősen csökkentette az ASR-eltérést, de a hosszú hang beszélőazonossága és hangereje változó maradt.

A helyi ASR modellje `mlx-community/whisper-large-v3-turbo-asr-fp16`, revíziója `624c19c9af5603fa73b83bce14d4aeea96156d18`. A körülbelül 1,62 GB-os diagnosztikai modell nem volt futtatási függőség.

| Konfiguráció | Szószintű szerkesztési eltérés | Karakteres eltérés |
| --- | --- | --- |
| Eredeti rövid férfiminta | 5,41% | 0,00% |
| Hosszú minta, átirat nélküli referencia | 57,29% | 43,59% |
| Azonos hosszú szöveg, referencia nélkül | 2,08% | 0,20% |

A normalizálás a kis- és nagybetűt, az írásjeleket és a szóközöket egységesítette, az ékezeteket megtartotta. A szószintű mutatót egybeírási eltérések is növelték. Az ASR nem bizonyít természetes prozódiát vagy állandó narrátorhangot.

## Átirattal párosított referencia

A második konfiguráció 8,07 másodperces, két teljes mondatból álló szintetikus férfireferenciát használt, pontos átirattal. Három külön kétmondatos mintán a helyi ASR nem mutatott szövegeltérést.

A 28 MB-os sherpa-onnx CAMPPlus beszélődiagnosztika koszinusz-hasonlóságai:

| Összevetés | Párosított referencia | Referencia nélküli kontroll |
| --- | --- | --- |
| Részek az eredeti férfimintához | 0,945–0,955 | 0,497–0,611 |
| Részek egymáshoz | 0,959–0,970 | 0,759–0,781 |

A női kontroll és a férfiminta hasonlósága 0,383 volt. Ezek relatív összehasonlító mutatók, nem természetességi százalékok.

## Hosszú minták mérései

| Mért adat | Referencia nélküli változat | Párosított, kétmondatos változat |
| --- | --- | --- |
| Bemenet | 2446 karakter | 2446 karakter |
| Belső részek | 7 | 20 |
| Generálási idő | 236,95 s | 162,43 s |
| Folyamat csúcs-RSS | 2 305 277 952 byte | 2 310 963 200 byte |
| Legnagyobb logikai átmeneti hangméret | 14 643 501 byte | 14 391 501 byte |
| MP3 mérete | 2 929 581 byte | 2 666 061 byte |

Az első változattal részben párhuzamosan más vizsgálatok is futottak, ezért a két idő nem tiszta sebesség-összehasonlítás. Az első GUI-minta hanghossza 244,04 s volt. A párosított változat 1,1× exporttempónál körülbelül 222,07 s hangot adott, 384 várt és 384 felismert szóval; a karakteres eltérés 0,101%, a szószintű 2,60% volt.

A húsz rész beszélőhasonlósága az eredeti férfimintához minimum 0,907, átlag 0,943; szomszédos részek között minimum 0,897, átlag 0,944. A részenkénti beszédszint-kiegyenlítés 20 ms-os képkockák alapján, csúcskorláttal működött. A részek külön MP3-tömörítés nélkül álltak össze.

## Hibakezelés és korlátok

A számmal végződő mondatok túl tág dátumfelismerése négymondatos részt eredményezhetett; a javítás azonosítója `de641db`. A dokumentált ellenőrzési kör 20 sikeres tesztet, 6 forrásfájl hibamentes típusellenőrzését és sikeres Swift-fordítást tartalmazott.

A jó ASR- és beszélőhasonlósági értékek ellenére a hangminőség nem bizonyult elegendően stabilnak. Az OmniVoice nem része a jelenlegi Piper-alkalmazásnak. A régi hangminták és diagnosztikai környezetek nem részei az aktív projektnek.

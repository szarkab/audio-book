# OmniVoice rövidszöveges prototípus — #2

> Archív műszaki dokumentum, 2026-11-10–11. A jelenlegi működés leírása a [specifikációban](specification.md) található.

Kapcsolódó feladat: [#2](https://github.com/szarkab/audio-book/issues/2). Vizsgált változat: `8456016`.

## Működés és konfiguráció

A prototípus natív macOS-ablakból választott UTF-8 TXT-fájlt, szövegelőnézetet és helyi MP3-generálást biztosított. A bemeneti korlát 600 karakter volt. A végleges MP3 csak sikeres kódolás után jelent meg; a meglévő célfájl felülírása tiltott volt.

A motor OmniVoice-bfloat16, MLX Metal GPU-val, magyar nyelvvel, férfiprofillal, 42-es véletlenmaggal és 64 generálási lépéssel. A kimeneti hossz súlyozott szöveghossz-becsléshez igazodott.

| Minta | Hanghossz | MP3 mérete |
| --- | --- | --- |
| Teljes rövid minta | 23,0 s | 277 101 byte |
| Rövidebb szöveg | 4,8 s | 58 509 byte |

Mindkét fájl mono, 24 kHz-es, 96 kbit/s MP3; teljes dekódolásuk sikeres. A GUI kimenete byte-ról byte-ra azonos volt a rövid parancssori referenciával. A helyi böngészős lejátszási próbában az idő haladt, médiahiba nélkül, 4-es `readyState` értékkel.

## Ellenőrzés

Nyolc teszt fedte a teljes generálási feladatot: sikeres kimenet, hibás és üres bemenet, hosszkorlát, hiányzó modell, mentési és kódolási hiba, forrásváltozás, valamint a már létező vagy időközben létrejövő célfájl védelme. A fájlkezelés és az FFmpeg valós volt; a külső beszédmodell teszthelyettesítőt használt.

Eredmény: 8 sikeres teszt, hibamentes mypy 4 forrásfájlon és sikeres Swift-fordítás. A fejlesztői indító feloldott Python-futtatót és azonos környezetből származó csomagelérési utat használt a GUI-ból indított virtuális környezet elakadásának elkerülésére. Ez a prototípus külön fejlesztői környezetet igényelt, önálló DMG-t nem tartalmazott.

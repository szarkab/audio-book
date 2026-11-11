# OmniVoice hangpróba — mérési eredmények

> Archív műszaki dokumentum, 2026-11-10–11. A jelenlegi működés leírása a [specifikációban](specification.md) található.

Dátum: 2026-11-10.

## Környezet

Apple M5, 32 GB memória, MLX Metal GPU. Modell: OmniVoice-bfloat16, `6119f7072580cc30c3cbdf496269216b03ad9742` revízió. Python 3.12.13, MLX 0.32.4, MLX-Audio 0.6.5, Transformers 5.22.2. Letöltési méret körülbelül 2,04 GB, helyi modellkönyvtár körülbelül 1,9 GiB.

A generálás helyi fájlokból, offline modellfeloldással, magyar nyelvkóddal, 42-es véletlenmaggal és 64 lépéssel történt.

## Mérések

A futási idő modellbetöltés és MP3-kódolás nélkül értendő. A memória az MLX csúcsértéke, nem a teljes rendszer memóriahasználata.

| Minta | Hanghossz | Generálási idő | MLX-csúcsmemória |
| --- | --- | --- | --- |
| Narráció, férfihang | 23 s | 11,86 s | 4,67 GB |
| Narráció, női hang | 23 s | 9,00 s | 4,68 GB |
| Kiejtési próba, férfihang | 26 s | 11,82 s | 5,03 GB |
| Kiejtési próba, női hang | 26 s | 11,17 s | 5,03 GB |

Az első modellbetöltés 29,11 s, a bemelegített fájlgyorsítótárral végzett betöltés 2,02 s volt. A 23 másodperces mono, 24 kHz-es MP3 mérete 96 kbit/s-on 277 101 byte, 64 kbit/s-on 184 749 byte.

## Hangjel-ellenőrzés

A nyolc vizsgált MP3 teljesen dekódolható, megfelelő hosszúságú, véges és nem néma jelet tartalmazott. A férfi kiejtési minta első futásánál a nyers csúcs 1,2245 volt; a végső export egyenletes hangerőcsökkentéssel 0,95-ös csúcskorlátot alkalmazott. A korrekció nem módosította a tempót vagy a hangon belüli dinamikaarányokat.

A Transformers modelltipus-figyelmeztetést jelzett, de a betöltés, GPU-generálás és a hullámforma-ellenőrzés sikeres volt.

## Minőségi eredmény

A rövid meghallgatásban a férfiprofil kedvezőbb eredményt adott a női profilnál. Hosszú szövegnél azonban a hangtervezési utasítás és a véletlenmag nem biztosított állandó narrátorhangot. A hosszabb vizsgálatokat az [OmniVoice hosszúszöveges jelentés](implementation-issue-3.md) tartalmazza. A modell és a próbahangok nem részei az aktív alkalmazásnak.

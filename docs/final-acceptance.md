# Ellenőrzési összefoglaló

Dátum: 2026-11-11. Verzió: v0.3.0-preview.

## Funkcionális ellenőrzés

A telepített alkalmazásban ellenőrzött működés: TXT-kiválasztás, Piper Imre felolvasás, sorszámkiejtési minta, hosszabb szövegek feldolgozása, saját lejátszó, hat felolvasási beállítás, modellbeszerzés és önálló DMG-telepítés. Az alkalmazásikon a Finderben és a Dockban is megjelenik. A hangminőség és a hosszabb szöveg lejátszása kézi meghallgatással is ellenőrzött.

A teljes automatizált ellenőrzés 33/33 sikeres tesztet tartalmaz valódi Piperrel és a telepített alkalmazással. A mypy 8 forrásfájlra hibamentes. A második generálási feladat nem módosítja az első MP3 ellenőrzőösszegét.

## Teljesítménymérés

| Mért adat | Eredmény |
| --- | --- |
| Bemenet | 97 918 karakter |
| Generálási idő | 150,810 s |
| Hang hossza | 6162,860 s (1 óra 42 perc 43 s) |
| MP3 mérete | 73 955 276 byte |
| Generáló folyamat csúcs-RSS-e | 493 568 000 byte |
| Logikai átmeneti hangméret | 369 772 538 byte |

A teljes MP3 dekódolása sikeres. A memóriaadat a generáló folyamatot jelenti; az átmeneti hangméret nem a teljes gép fizikai lemezfoglalása. A próbafolyamatok hálózat és fejlesztői útvonalak elérése nélkül futottak. A nyers eredményeket az [acceptance-measurements.json](acceptance-measurements.json) tartalmazza.

A generált mérési hangok, részletek, ideiglenes szövegek és naplók nem részei a projektnek; csak a kis mérési jegyzőkönyv maradt meg. A fejlesztői ellenőrző alapértelmezése egyetlen rövid próba, legfeljebb három ismétléssel.

## Mérési korlátok

A haladásjelzés és a dekódolás a feldolgozást és a fájl épségét vizsgálja, nem minden kimondott szó helyességét. Egy korábbi ASR-mérés 5,31% karakteres és 15,30% szószintű eltérést mutatott; ez nem tekinthető hibátlan szöveghűségnek. A kiejtés és a természetesség továbbra is meghallgatással ítélhető meg.

A csomag Apple Silicon gépet és macOS 26 vagy újabb rendszert igényel. Ad-hoc aláírású, Apple-notarizáció nélkül; az első indításkor macOS-engedélyezésre lehet szükség. A DMG és az ellenőrzőösszeg a [GitHub-kiadásban](https://github.com/szarkab/audio-book/releases/tag/v0.3.0-preview) érhető el.

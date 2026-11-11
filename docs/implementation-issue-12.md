# Magyar sorszámok előkészítése — #12

> Archív műszaki dokumentum, 2026-11-10–11. A jelenlegi működés leírása a [specifikációban](specification.md) található.

Kapcsolódó feladat: [#12](https://github.com/szarkab/audio-book/issues/12).

## Felismerési szabályok

A szöveg-előkészítés az 1–100 közötti arab sorszámokat betűs alakra váltja a következő pontosan egyező, kisbetűs szavak előtt: fejezet, próba, versenyző, hely, alkalom, emelet, kötet, oldal, pont, rész, lépés.

Példák: `1. fejezet` → `első fejezet`; `2. próba` → `második próba`; `15. versenyző` → `tizenötödik versenyző`.

Nagybetűs folytatás, toldalékos főnév, vezető nulla, 100 feletti szám, verzió, pontozott számsor és puszta listaelem változatlan marad. A kívánt kiejtés a forrásban betűvel is megadható.

Az előnézet és a modellnek átadott szöveg azonos. Az eredeti fájl változatlan; a nyers forrásbájtok ellenőrzőösszege a felolvasott alaktól függetlenül észleli a forrás módosulását.

## Ellenőrzés és teljesítmény

Az akkori ellenőrzés 28/28 sikeres tesztet tartalmazott valódi Piperrel (3,897 s), hibamentes mypy-eredménnyel 7 forrásfájlon, sikeres Swift-fordítással és aláírás-ellenőrzéssel. A tesztek a modellbemenetet, az előnézetet, a dátumkivételeket és a forrásváltozás védelmét is vizsgálták.

A natív öt példás minta 138 karakterből 10,031 s / 121 293 byte MP3-at adott 0,852 s alatt. A folyamat csúcs-RSS-e 334 938 112 byte, a logikai átmeneti hangméret 963 058 byte volt. A teljes dekódolás és a rövid kiejtési minta meghallgatása sikeres; a lejátszó kézi indításig leállítva maradt.

A prefix teljes átvizsgálása helyett a közvetlenül megelőző szóközök és két karakter ellenőrzése történik. A 8000 sorszámos benchmark ideje 1,4399 s-ról 0,00283 s-ra csökkent. A mondatvégi tőszámokat tartalmazó „A darabszám 1. Próba következik.” és „Az eredmény 2. Hely már nincs.” változatlan marad.

## Értelmezési korlát

A sorszámtesztek nem minősítik a teljes narráció szöveghűségét. A korábbi hosszú Piper-mintán mért 5,31% karakteres és 15,30% szószintű ASR-eltérés külön mérés; a sorszámok javítása ezt nem írja felül.

## Nyelvi források

- [A magyar helyesírás szabályai, 292. pont](https://www.helyesiras.mta.hu/helyesiras/default/akh12)
- [Számnevek betűs alakja](https://www.helyesiras.mta.hu/helyesiras/default/numerals)

Futáskor nincs hálózati szövegfeldolgozás.

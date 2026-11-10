# Magyar sorszámkiejtés — #12

A Piper Imre elé konzervatív szöveg-előkészítés került. Ugyanaz a betűs szöveg jelenik meg az előnézetben és jut a modellhez; az eredeti fájl változatlan. A nyers forrásbájtok ellenőrzőösszege felismeri a változást akkor is, ha a felolvasandó alak ugyanaz maradna.

## Hatókör

Az 1–100 közötti arab sorszámok pontosan a következő kisbetűs szavak előtt alakulnak át: fejezet, próba, versenyző, hely, alkalom, emelet, kötet, oldal, pont, rész, lépés. Példák: első fejezet, második próba, tizenötödik versenyző, huszonegyedik hely, századik alkalom.

Nagybetűs folytatás, toldalékos főnév, vezető nulla, 100 feletti szám, verzió és pontozott számsor változatlanul marad. A puszta listaelem sem alakul át. Ez szándékos konzervatív korlát; az előnézetben látható, és a kívánt alak betűvel beírható a TXT-forrásba. Nincs új beállítópanel, modell vagy tempóváltozás. A #14 meglévő felolvasási beállításait megőrzi.

Nyelvi referencia: [A magyar helyesírás szabályai, 292. pont](https://www.helyesiras.mta.hu/helyesiras/default/akh12), [Számnevek betűs alakja](https://www.helyesiras.mta.hu/helyesiras/default/numerals). A forrásokat fejlesztéskor ellenőriztük; futáskor nincs hálózati szövegfeldolgozás.

## Ellenőrzés

- A jóváhagyott teljes fájl → MP3 határon előbb hibázó, majd sikeres teszt fedi az öt kért alakot és a modellhez ténylegesen átadott szöveg/előnézet azonosságát.
- Külön előbb hibázó, majd sikeres próbák fedik az azonos felolvasott alakú forrásváltozást és a pontozott dátum kivételét. Az új mondat előtti tőszám reviewhibáját is hibázó próbával rögzítettük, majd javítottuk.
- Végső teljes csomag: 28/28 teszt, valódi Piper-integrációval, 3,897 s. mypy: 7 forrásfájl hibamentes. Swift-fordítás, appaláírás és git diff --check sikeres.
- Natív próba: a hu-ordinals.txt kiválasztása után az öt betűs alak megjelent az előnézetben, 138 karakterrel. Az ablakból indított MP3-generálás sikeres; a lejátszó „Leállítva”, 0:00 állapotban maradt. Nem indult automatikus hang.
- A natív rövid minta 10,031 s / 121293 byte; 0,852 s generálás; 334938112 byte folyamatcsúcs-RSS; 963058 byte logikai átmeneti hangméret. Teljes MP3-dekódolás hibamentes. Mind a hat naplózott beállítás az elfogadott alapérték. A felhasználónak átadott egyetlen minta az artifacts/piper-ordinals/hu-ordinals-hang.mp3.

## Standards

A c1ed2aa...HEAD ellenőrzés 0 dokumentált szabálysértést talált. Egy külön P2 teljesítményhiba javítva: minden sorszámnál teljes könyvprefix keresése helyett csak a közvetlen megelőző szóközök és két karakter vizsgálata történik. A reviewbenchmark 8000 sorszámnál 1,4399 másodpercről 0,00283 másodpercre csökkent. Újraellenőrzés: 0 nyitott finding.

## Spec

Egy P2 téves átírás javítva: „A darabszám 1. Próba következik.” és „Az eredmény 2. Hely már nincs.” változatlan marad. A kisbetűs biztos alakok működnek. Újraellenőrzés: 0 nyitott kódhiba.

A rövid sorszámminta emberi meghallgatása még nyitott: a #12 nem zárható teljesítettként a felhasználó visszajelzése előtt.

## Hosszú hang auditja — #11 és #3

A korábbi, dokumentált többperces M5-futás, a felhasználó egyelőre elfogadott Piper-minősége és a hosszú tartalomsorrendi/hibakezelési tesztek megvannak. A régi ASR-eredmény azonban 5,31% karakteres és 15,30% szószintű eltérést jelzett; ezt nem minősítjük teljes szöveghűségi megfelelésnek. Nem készült új hosszú minőségi elfogadás ebben a feladatban, ezért #11/#3 nem lett automatikusan lezárva.

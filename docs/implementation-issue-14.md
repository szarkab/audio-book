# Felolvasási beállítások — #14

> Történeti feljegyzés: korábbi modellpróbák, mérések vagy fejlesztési ellenőrzések dokumentuma. Az aktuális alkalmazás működését a [specifikáció](specification.md) írja le.

Forrás: https://github.com/szarkab/audio-book/issues/14

A natív „Felolvasás beállításai…” ablak hat vezérlőt és egy alapérték-visszaállító gombot ad. Az értékek csak a munkamenetben élnek, a futó feladat saját pillanatképet kap. A Piper tempója a felületi tempó inverze; utólagos gyorsítás helyett a modell időzítését állítja. A kimeneti hangerő a normalizálás után érvényesül, csúcskorláttal. Az extra csend a Piper mondatchunkjai és a szolgáltatás részei közé kerül, hozzáadott záró szünet nélkül. Az elfogadott alapértékek változatlanok.

## Ellenőrzés

- A teljes fájl → MP3 határon előbb hibázó paraméterátadási és érvénytelenérték-próbák, majd sikeres megvalósítás.
- 25/25 teszt sikeres, bekapcsolt valódi Piper-próbával. A tényleges MP3-ból mért hangerő és a háromszor 0,25 másodperces hozzáadott szünet is ellenőrzött.
- mypy: 7 forrásfájl hibamentes. Swift-fordítás és a fejlesztői app aláírása sikeres. git diff --check hibamentes.
- Natív próba: egyéni értékek beállítása, ablak bezárása/újranyitása, TXT kiválasztása, MP3 mentése; nincs automatikus lejátszás. A napló a teljes hat értéket visszaigazolja: 0,85× felületi tempó → 1,176470588235294 length_scale; hangváltozatosság 0,6; ritmus 0,433; hangerő 0,8; normalizálás kikapcsolva; extra szünet 0,15 s. A 231 karakterből 17,389 másodperces, 209709 bájtos MP3 készült 1,054 másodperc alatt.
- Az alapérték-visszaállítás mind a hat értéket pontosan visszaállította, a ritmust 0,333-ra. Újraindításkor is alapértékek jelentek meg. Szokásos appmegnyitással az újabb TXT → MP3 próba is sikeres, a lejátszó leállított állapotban maradt.
- Az első két normál indításnál a Python még a szövegbeolvasás előtt, az inicializálásban várakozott. A saját tesztfolyamatok lezárása és újraindítás után a közvetlen, majd ismét a szokásos appindítás is sikeres volt. Ennek átmeneti okát nem tekintjük bizonyítottnak; nem módosult macOS-védelmi beállítás.

## Kódellenőrzés

Összehasonlítási alap: e39b2d3041fd292e5c7c8f9079d46dab2b4ccbf4. Megvalósítás: 8b3eaaf.

### Standards

0 dokumentált szabálysértés, 0 javítást indokoló kódszag. A beállítások önálló értékként utaznak; a felelősségek, a helyi működés és a Piper Imre kizárólagossága megmaradt.

### Spec

0 igazolt eltérés. A hat vezérlő, a visszaállítás, a munkamenet, a pillanatkép, a hangerő és a szünetek megvalósítása megfelel a #14 követelményeinek. A review után a végső natív próba is sikeres.

A hang természetességének változásáról nincs új emberi elfogadási állítás: a vezérlők lehetővé teszik a saját összehasonlítást.

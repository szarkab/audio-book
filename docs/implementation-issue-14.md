# Felolvasási beállítások — #14

> Archív műszaki dokumentum, 2026-11-10–11. A jelenlegi működés leírása a [specifikációban](specification.md) található.

Kapcsolódó feladat: [#14](https://github.com/szarkab/audio-book/issues/14).

## Működés

A „Felolvasás beállításai…” ablak hat vezérlőt és alapérték-visszaállítást biztosít. A beállítások a munkamenetben érvényesek. A futó feladat az indításkori értékeket használja; generálás alatt az értékek nem módosíthatók.

A Piper `length_scale` értéke a felületi tempó inverze: a tempó a modell időzítését állítja, nem utólagos gyorsítást alkalmaz. A kimeneti hangerő a normalizálás után érvényesül, csúcskorláttal. Az extra csend a mondatok és a belső szövegrészek közé kerül, hozzáadott záró szünet nélkül.

Alapértékek: 1× tempó, 0,333 ritmus, 0,5 hangváltozatosság, 1× hangerő, bekapcsolt normalizálás, 0 s extra szünet. Az újraindítás ezeket állítja vissza.

## Ellenőrzés

Az akkori tesztcsomag 25/25 sikeres próbát tartalmazott valódi Piperrel. A tesztek a paraméterátadást, az érvénytelen értékek elutasítását, a tényleges MP3 hangerejét és a háromszor 0,25 s hozzáadott szünetet vizsgálták. A mypy 7 forrásfájlon hibamentes; a Swift-fordítás és az alkalmazás aláírás-ellenőrzése sikeres.

A natív egyéni beállításos próba értékei:

| Paraméter | Érték |
| --- | --- |
| Felületi tempó | 0,85× |
| Piper length_scale | 1,176470588235294 |
| Hangváltozatosság | 0,6 |
| Ritmus | 0,433 |
| Hangerő | 0,8 |
| Normalizálás | Kikapcsolva |
| Extra mondatszünet | 0,15 s |

A 231 karakteres minta 17,389 s / 209 709 byte MP3-at adott 1,054 s alatt. Az ablak bezárása és újranyitása megtartotta az értékeket; az alapérték-visszaállítás mind a hat paramétert helyesen visszaállította. A lejátszás kézi indításig leállítva maradt.

Két alkalmazásindításkor a Python inicializálása átmenetileg várakozott. A tesztfolyamatok újraindítása után a közvetlen és a szokásos appindítás is sikeres volt; az átmeneti jelenség oka nem bizonyított. A beállítások műszaki ellenőrzése nem minősíti minden kombináció természetességét.

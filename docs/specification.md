# Hangoskönyv — funkcionális specifikáció

## Rendeltetés

Magyar UTF-8 TXT-fájlok helyi felolvasása Piper Imre férfihanggal, Apple Silicon Macen. Egy kiválasztott fájlból egyetlen mono, 96 kbit/s MP3 készül. A szöveg és a hang nem kerül felhős beszédszolgáltatáshoz.

## Munkafolyamat

1. Az alkalmazás DMG-ből telepíthető, és terminál vagy külön fejlesztői környezet nélkül indítható macOS 26 vagy újabb rendszeren.
2. A hiányzó modell az alkalmazásból tölthető le, látható mérettel és állapottal. A letöltött fájlokat ellenőrzőösszegek védik; sikertelen letöltés újrapróbálható.
3. A TXT kiválasztása után az előnézet a ténylegesen felolvasandó szöveget mutatja. Az eredeti fájl változatlan marad. Az előnézet óta módosult forrást újra ki kell választani.
4. A felolvasási beállítások a generálás előtt módosíthatók. A teljes szöveg köztes jóváhagyás nélkül készül el, haladásjelzéssel és érthető hibaüzenetekkel.
5. A kész MP3 kézzel indítható, szüneteltethető, leállítható és tekerhető a saját lejátszóban, valamint megkereshető a Finderben.
6. A következő TXT külön feladatban dolgozható fel. A korábbi MP3-ak nem íródnak felül.

## Hanggenerálás

A motor kizárólag Piper Imre, rögzített modellrevízióval. CPU-n fut; a modell letöltése után internet nélkül működik. A belső rövid szövegegységek hangja veszteségmentes PCM-formátumban, lemezen áll össze. A végső MP3-kódolás egyszer történik, a teljes könyv hangjának memóriában tárolása nélkül.

A sorszám-előkészítés csak az egyértelmű, támogatott 1–100 közötti alakokat írja betűvel. A dátumok, verziószámok és bizonytalan esetek változatlanok. A pontos felismerési korlátok a [README-ben](../README.md) találhatók.

## Beállítások

| Beállítás | Alapérték |
| --- | --- |
| Tempó | 1× |
| Ritmus változatossága | 0,333 |
| Hang változatossága | 0,5 |
| Kimeneti hangerő | 1× |
| Hangerő-normalizálás | Bekapcsolva |
| Extra mondatszünet | 0 s |

Az alapértékek egy gombbal visszaállíthatók. A beállítások az alkalmazás bezárásáig érvényesek; újraindításkor az alapértékek indulnak. Futó generálás alatt nem módosíthatók. A kimeneti hangerő a mentett fájlt érinti, a lejátszó hangerejétől függetlenül. Külön hangsúlyozás-szabályzó nincs.

## Telepítés és megjelenés

Az önálló alkalmazás tartalmazza a Python-futtatót, a Pipert és az MP3-kódolót. Nem függ a forrásprojekttől vagy a telepített Homebrew-tól. A modell külön, első letöltéssel érhető el. Az alkalmazás könyv–hanghullám ikont és kék–arany színvilágot használ; az ikon a Finderben és a Dockban is megjelenik.

Az előzetes ad-hoc aláírású, Apple-notarizáció nélkül. A macOS első indítási figyelmeztetése és az alkalmazásonkénti engedélyezés a [telepítési leírásban](../README.md#telepítés-és-indítás) szerepel.

## Ellenőrzés

Az automatizált ellenőrzés határa a forrásfájl és beállítások → feladatállapot és lejátszható MP3. A vizsgált működés: ékezetes szöveg, sorrend, sorszámok, forrásváltozás-védelem, beállítások, hibás és részleges kimenet kizárása, felülírás elleni védelem, modellletöltés és offline működés. A csomagolt alkalmazás külön is ellenőrizhető fejlesztői környezet nélkül. A természetesség és a kiejtés meghallgatást igényel; a dekódolhatóság önmagában nem bizonyítja a szöveghűséget.

Eredmények és mérési korlátok: [ellenőrzési összefoglaló](final-acceptance.md).

## Korlátok

Nem támogatott: Markdown-bemenet, generálási szüneteltetés és tartós folytatás, böngészős felület, automatikus feltöltés, alternatív narrátormodellek, hangklónozás, kötegelt feldolgozás, mondatonkénti szerkesztés, kiejtési szótár és további exportformátumok. Megszakított vagy hibás feladatból nem keletkezik késznek jelölt részleges MP3; a feldolgozás az elejéről indítható újra.

A korábbi modellkutatások és megvalósítási jegyzetek történeti feljegyzések; a jelenlegi alkalmazás működését ez a specifikáció írja le.

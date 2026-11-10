# Magyar hangoskönyv-készítő — aktuális specifikáció

Frissítve: 2026-11-10. A felhasználó legutóbbi döntése felülírja a korábbi Markdown-, folytathatósági és böngészős követelményeket. A hanggenerálás elfogadott alapja kizárólag a Piper Imre magyar férfihang. A korábbi modellpróbák történeti dokumentumok.

## Problem Statement

A felhasználó saját magyar TXT-fájljaiból szeretne kellemes férfihangos MP3-at készíteni a saját M5 MacBookján, felhős beszédszolgáltatás nélkül. Egy fájlt feldolgoztat, meghallgatja az eredményt, majd új feladatban kiválasztja a következő fájlt. A gyors Piper-generálás mellett már nincs igény a generálás szüneteltetésére vagy tartós folytatására.

## Solution

Önálló, DMG-ből telepíthető macOS-alkalmazás: TXT-fájl kiválasztása, a ténylegesen felolvasandó szöveg előnézete, opcionális felolvasási beállítások, majd egyetlen MP3 előállítása. A teljes fájl köztes jóváhagyás nélkül elkészül. Az alkalmazás saját lejátszójával hallgatható meg az eredmény, kizárólag kézi indítással.

A szükséges modell első alkalommal az alkalmazásból beszerezhető; utána a generálás offline történik. Az alkalmazás kapjon egységes, egyszerű arculatot, felismerhető logót/appikont és következetes színeket. A hangminőség egyelőre elfogadott, a további hangolás felhasználói összehasonlítással történik.

## User Stories

1. Felhasználóként szeretném DMG-ből telepíteni az appot, hogy egyszerűen használatba vehessem.
2. Felhasználóként szeretném terminál és fejlesztői környezet nélkül elindítani az appot.
3. Felhasználóként szeretnék magyar UTF-8 TXT-fájlt kiválasztani.
4. Felhasználóként szeretném előre látni a ténylegesen felolvasandó szöveget.
5. Felhasználóként szeretném megőrizni az eredeti forrásfájlt változatlanul.
6. Felhasználóként szeretném egy indítással a teljes fájlt feldolgoztatni, kézi darabolás nélkül.
7. Felhasználóként teljes könyvből is egyetlen MP3-at szeretnék kapni.
8. Felhasználóként az elfogadott magyar férfihangot szeretném hallani a teljes hanganyagban.
9. Felhasználóként szeretném MP3-készítés előtt állítani a tempót, a ritmus és a hang változatosságát.
10. Felhasználóként szeretném állítani a mentett MP3 hangerejét, a normalizálást és az extra mondatszünetet.
11. Felhasználóként szeretném egy gombbal visszaállítani az elfogadott alapértékeket.
12. Felhasználóként szeretném látni a generálás haladását és az érthető hibákat.
13. Felhasználóként szeretném saját döntéssel elindítani, szüneteltetni vagy leállítani a kész hang lejátszását.
14. Felhasználóként szeretném megtalálni a kész MP3-at a Finderben.
15. Felhasználóként szeretném külön feladatban feldolgozni a következő TXT-fájlt.
16. Felhasználóként szeretném megőrizni a korábban elkészült MP3-akat felülírás nélkül.
17. Felhasználóként szeretném a biztos sorszámos alakokat helyesen hallani, dátumok és verziószámok téves átírása nélkül.
18. Felhasználóként szeretném a hiányzó modellt az appból beszerezni, látható mérettel és állapottal.
19. Felhasználóként szeretném újrapróbálni a sikertelen letöltést.
20. Felhasználóként szeretném a modell beszerzése után internet nélkül használni az appot.
21. Felhasználóként szeretném egyedi ikonról felismerni az appot a Finderben és a Dockban.
22. Felhasználóként szeretnék egységes, olvasható színeket és egyszerű felületet.
23. Felhasználóként szeretném a telepített alkalmazásban is használni az összes elfogadott beállítást.

## Implementation Decisions

- Kizárólag helyi Piper Imre, rögzített modellrevízióval és ellenőrzött állományokkal. Más modell és felhős beszédszolgáltatás nincs a tervben.
- Egy TXT-fájl egy generálási feladat és egy MP3. Belső rövid részek automatikusan, veszteségmentesen állnak össze, egyszeri végső MP3-kódolással; a teljes könyv hangja nem halmozódik memóriában.
- A jelenlegi MP3-alap mono, 96 kbit/s. A magasabb bitráta vagy nagyobb hardverterhelés önmagában nem javítja a modell kiejtését.
- A hat felolvasási beállítás és a visszaállítás megmarad. Az induló értékek: tempó 1×, ritmus 0,333, hangváltozatosság 0,5, hangerő 1×, normalizálás bekapcsolva, extra mondatszünet 0 s. A futó generálás pillanatképet kap, közben az értékek nem módosíthatók; újraindításkor alapértékek indulnak.
- A szövegelőnézet és a tényleges felolvasás tartalma azonos. Az előnézet óta módosult forrás új kiválasztást igényel. A sorszám-előkészítés konzervatív marad.
- Nincs generálási szüneteltetés, tartós részmentés vagy újraindítás utáni folytatás. Megszakított vagy hibás feladatból nem lesz késznek jelölt részleges MP3; a feladat újraindítható az elejéről. Ez nem érinti a kész hang lejátszójának szüneteltetését.
- Az önálló app a futtatókörnyezetet és a hangkódolót is tartalmazza; nem függ a fejlesztő munkamappájától, Pythonjától vagy Homebrew-jától. A modell külön első letöltése elfogadott.
- A DMG része az egyszerű arculat: saját logó/appikon, visszafogott, következetes színpaletta és jól olvasható vezérlők. Az ikon a telepített appon, Finderben és Dockban is megjelenik. A vizuális irány a megvalósításkor bemutatható; konkrét új márkanév nincs előírva.
- Az aláírás, notarizáció és Gatekeeper-indítás a célgépen ellenőrizendő a rendelkezésre álló hozzáférés szerint; az akadályokat dokumentáljuk.
- A modell első letöltése hálózatot használhat, a szöveg és hang generálása nem igényel feltöltést.

## Testing Decisions

A már jóváhagyott legmagasabb teszthatár marad a teljes forrásfájl és beállítások → feladatállapot és lejátszható MP3. A tesztek külső viselkedést vizsgálnak, nem belső darabolási megoldást. Nincs új tesztelési határ.

- TXT, ékezetek, teljes szövegtartalom és sorrend, konzervatív sorszámkezelés, forrásváltozás-védelem és egyetlen dekódolható MP3.
- Beállítások hatása, alapérték-visszaállítás, hangerő és szünetek, felülírás elleni védelem és hibás kimenet kizárása.
- Valódi helyi rövid és hosszú Piper-próba; idő-, memória- és tárhelymérés. A természetességet és a folytonosságot célzott emberi meghallgatás fogadja el.
- Modellbeszerzés: hiányzó/letöltés/kész állapot, ellenőrzőösszegek, hibák és újrapróbálás, majd hálózat nélküli generálás.
- DMG-ből telepített app: fejlesztői környezettől független indítás, saját lejátszó, következő fájl külön feldolgozása. Az arculat és az ikon tényleges megjelenése, olvashatósága is ellenőrzött.
- Nincs Markdown-, generálásfolytatási vagy böngészős elfogadási teszt.

## Out of Scope

- Markdown/MD-beolvasás és -előfeldolgozás; kizárólag TXT-bemenet.
- Generálás szüneteltetése, tartós részmentés és újraindítás utáni folytatás.
- Böngészős felület, böngészős lejátszási átvétel, webes integráció és automatikus feltöltés.
- Felhős beszédszolgáltatás, alternatív narrátormodellek, hangklónozás és saját modell betanítása.
- Kötegelt feldolgozás, látható fejezetenkénti munkamenet, mondatonkénti szerkesztő, kiejtési szótár és további bemeneti/exportformátumok.
- App Store-megjelenés és más operációs rendszerek.

## Further Notes

Aktuális sorrend: hosszú Piper-felolvasás ellenőrzésének lezárása, sorszámkiejtés, alkalmazáson belüli modellbeszerzés, önálló DMG arculattal és ikonnal, végső helyi alkalmazásos átvétel. A felolvasási beállítások (#14) elkészültek. A #4 és #5 funkciókat a felhasználó kifejezetten elhagyta; ezek nem előfeltételei a kiadásnak.

A GitHub #1 és ez a specifikáció azonos aktuális követelményeket tartalmaz. A korábbi megvalósítási és modellkutatási feljegyzések történeti bizonyítékok, a bennük szereplő jövőbeli tervek nem írják felül ezt a specifikációt.

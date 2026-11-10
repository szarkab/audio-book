# Magyar hangoskönyv-készítő alkalmazás — specifikáció és megvalósítási terv

Állapot: elfogadott specifikáció, 2026-11-10. GitHub issue: https://github.com/szarkab/audio-book/issues/1. A felhasználó jóváhagyta a teljes generálási feladatra épülő tesztelési határt és a GitHub-issue-ként történő publikálást ready-for-agent címkével. A projekt issue trackere a GitHub Issues, az öt alapértelmezett triage-címkével. Az első megvalósítási lépés a helyi magyar hangpróba.

## Problem Statement

A felhasználó magyar TXT- és Markdown-fájlokból szeretne természetes, nyugodt narrátorhangú hanganyagot készíteni saját használatra, egy Apple M5 chipes, 32 GB memóriájú MacBookon. A hanganyagokat saját hangoskönyvprojektjének böngészős lejátszójában használja fel. A hang természetessége elsődleges, a fájlméret legyen hatékony, és a működéshez ne kelljen felhős beszédszolgáltatás vagy parancssori eszközök kezelése.

A felhasználó maga készíti elő és választja ki az egyes forrásszövegeket. Egy fájlt egyben szeretne feldolgoztatni, meghallgatni az eredményt, majd saját döntése szerint egy új generálási feladatban megnyitni a következő fájlt. Teljes könyv is lehet egyetlen forrásszöveg. Hosszú munka során az alkalmazás bezárása vagy váratlan leállása nem teheti semmissé az elkészült részeket.

## Solution

DMG-ből telepíthető macOS-alkalmazás: a felhasználó kiválaszt egy magyar TXT- vagy MD-fájlt, szükség esetén átnézi a felolvasandó szöveget, majd elindítja a generálást. Az alkalmazás köztes jóváhagyás nélkül végig feldolgozza a teljes fájlt, és egyetlen MP3-hanganyagot ment. A felhasználó meghallgatja az eredményt, majd külön feladatként választja ki a következő forrásszöveget.

Első használatkor a szükséges beszédmodell letölthető az internetről. A letöltött modellel a generálás teljesen helyben, offline fut. A narrátorhang és a minőségi alapbeállítás magyar hangminták meghallgatása után kerül kiválasztásra. A hosszú generálás szüneteltethető és tartósan folytatható.

## User Stories

1. Felhasználóként szeretném DMG-ből telepíteni az alkalmazást, hogy egyszerűen használatba vehessem.
2. Felhasználóként szeretném szokásos Mac-alkalmazásként elindítani, hogy ne kelljen terminált vagy fejlesztői környezetet használnom.
3. Felhasználóként szeretném látni az első modellletöltés méretét és állapotát, hogy tudjam, mikor kezdhetek dolgozni.
4. Felhasználóként szeretném újrapróbálni a sikertelen modellletöltést, hogy egy átmeneti hálózati hiba ne akadályozzon tartósan.
5. Felhasználóként szeretném a modell beszerzése után internet nélkül használni az alkalmazást, hogy a szövegem helyben maradjon.
6. Felhasználóként szeretnék magyar TXT-fájlt kiválasztani, hogy egyszerű szövegből készíthessek hanganyagot.
7. Felhasználóként szeretnék magyar MD-fájlt kiválasztani, hogy Markdown-forrást is használhassak.
8. Felhasználóként szeretném, hogy az ékezetes magyar szöveg helyesen jelenjen meg és hangozzon el.
9. Felhasználóként szeretném előre látni a ténylegesen felolvasandó szöveget, hogy ellenőrizhessem az előkészítést.
10. Felhasználóként szeretném hallani a Markdown címsorait és folyó szövegét, hogy az érdemi tartalom megmaradjon.
11. Felhasználóként szeretném elhagyni a Markdown formázási jeleit és a hivatkozások cél-webcímeit, hogy azok ne zavarják a narrációt.
12. Felhasználóként szeretném, hogy a kihagyott kódblokkok és táblázatok látható jelzést kapjanak, hogy tudjak a kihagyásukról.
13. Felhasználóként szeretnék magyar hangmintákból narrátorhangot választani, hogy a nekem megfelelő férfi vagy női hangot használhassam.
14. Felhasználóként szeretnék nyugodt és természetes narrációt, hogy a hosszabb hanganyag is kellemesen hallgatható legyen.
15. Felhasználóként szeretnék egyetlen indítással egy teljes fájlt feldolgoztatni, hogy közben ne kelljen részeket jóváhagynom.
16. Felhasználóként szeretnék teljes könyvet is feldolgoztatni, hogy a fájl hossza ne kényszerítsen kézi darabolásra.
17. Felhasználóként szeretném kihasználni az M5 elérhető számítási teljesítményét, hogy a jó minőségű helyi generálás hatékonyan fusson.
18. Felhasználóként szeretném látni a generálás állapotát, hogy megkülönböztessem a folyamatban lévő munkát a hibától.
19. Felhasználóként szeretném szüneteltetni a generálást, hogy később folytathassam.
20. Felhasználóként szeretném az alkalmazás bezárása és a gép újraindítása után folytatni a feladatot, hogy ne vesszen el a munkám.
21. Felhasználóként szeretném váratlan leállás után megőrizni az elkészült részeket, hogy legfeljebb a folyamatban lévő rövid rész készüljön újra.
22. Felhasználóként szeretném, hogy egy folytatott hanganyagban ne legyen ismétlés vagy kimaradás a megszakítás helyén.
23. Felhasználóként szeretnék egyetlen MP3-at kapni minden feldolgozott fájlból, hogy egyszerűen használhassam a böngészős projektemben.
24. Felhasználóként szeretnék jó beszédminőséget hatékony fájlmérettel, hogy a hanganyag tárolása és lejátszása gazdaságos legyen.
25. Felhasználóként szeretném könnyen megtalálni és meghallgatni a kész hanganyagot, hogy ellenőrizhessem a minőségét.
26. Felhasználóként szeretném külön generálási feladatként feldolgozni a következő fájlt, hogy saját tempómban haladhassak.
27. Felhasználóként szeretnék érthető hibaüzenetet kapni hibás vagy üres bemenetnél, illetve tárhelyhiánynál, hogy tudjam, mit kell javítanom.
28. Felhasználóként szeretném megőrizni az előzőleg elkészült MP3-at, hogy egy új feladat ne írja felül észrevétlenül.

## Implementation Decisions

### Egyeztetett viselkedés és korlátok

- Egy kiválasztott forrásfájl egy generálási feladat és egy elkészült MP3. Nincs felhasználónak látható automatikus bekezdésenkénti munkamenet, fejezetenkénti export vagy köztes jóváhagyás.
- A további forrásfájlokat a felhasználó kézzel, külön feladatként nyitja meg. Automatikus kötegelt sor nem szükséges.
- A minőség elsődleges; nincs előírt felső időkorlát. Ettől függetlenül a helyi sebességet és memóriahasználatot mérni kell.
- A beszédgenerálás kizárólag helyi. Egyszeri modellletöltés elfogadott. A generálás nem függhet aktív hálózati kapcsolattól.
- A Markdown-előkészítés megőrzi a címsorokat, a folyó szöveget és a hivatkozások látható szövegét. Elhagyja a formázási jeleket és a cél-webcímeket; a kódblokkokat és táblázatokat alapból kihagyja, látható jelzéssel.
- Nincs elvárt mondatonkénti szerkesztő, kiejtési szótár vagy alternatív felolvasások összehasonlító felülete. A felhasználó elsősorban jó minőségi alapbeállítást kér.
- A szüneteltetés és a folytatás alkalmazásbezárásra, újraindításra és váratlan leállásra is kiterjed.

### Javasolt műszaki megoldás — a minőségi próba eredményétől függően

- Natív macOS-felület és leválasztott helyi beszédgeneráló komponens javasolt. Első felületjelölt a SwiftUI; a futtatókörnyezet véglegesítését a helyi modellpróba és a csomagolhatóság dönti el.
- Egyetlen magas szintű feladatszolgáltatás fogja össze a forrásszöveg előkészítését, a beszédgenerálást, a tartós mentést és az MP3-előállítást. A felület ennek állapotát mutatja, és indítási, szüneteltetési, folytatási műveleteket kér.
- A hosszú szöveg feldolgozásához a beszédmodell korlátai és a tartós mentés miatt belső technikai egységek szükségesek lehetnek. Ezek nem jelentenek külön felhasználói feladatot vagy külön exportfájlt. A teljes forrásszöveg feldolgozása automatikusan történik. A részhatárok hallható folytonosságát külön vizsgálni kell.
- Egy feladat megőrzi az eredeti és az előkészített forrásszöveg pillanatképét, a modell és a narrátorhang azonosítóját, a generálási beállításokat, a tartósan elkészült részek sorrendjét és a célfájl adatait. Folytatáskor ezek nem változhatnak észrevétlenül.
- Belső állapotok: előkészítés, generálás, szüneteltetett, MP3 készítése, elkészült és hiba. Váratlan leállás után az utolsó tartósan mentett pontból kell visszaállni.
- Az elkészült belső részeket lehetőleg veszteségmentesen kell megőrizni az egyszeri végső MP3-kódolásig. Végleges kimenet csak sikeres összeállítás után jelenjen meg kész hanganyagként. A tárhelyigényt és a részfájlok élettartamát a hosszú próba során ellenőrizni kell.
- Az MP3 bitrátája még nem végleges. Több tömörítési beállítást kell ugyanazon a magyar hangmintán meghallgatni, majd a hangminőség és fájlméret alapján alapértéket választani. A forrásmodell tényleges hangminőségét a magasabb bitráta önmagában nem javítja.
- Az alkalmazás és a szükséges futtatókörnyezet együtt csomagolandó; a felhasználótól nem várható Python-, Homebrew- vagy terminálhasználat. A modell külön, alkalmazáson belüli első letöltéssel is beszerezhető.
- A telepíthető változatot a célgépen, fejlesztői környezettől független indítással kell ellenőrizni. Az aláírás és notarizáció pontos útját a rendelkezésre álló Apple-fejlesztői hozzáférés ellenőrzése után kell véglegesíteni; akadálymentes Gatekeeper-indulás nem ígérhető ellenőrzés nélkül.

### Modellválasztás

- Nincs még elfogadott vagy helyben kipróbált végleges modell. A „legjobb” minőség nem tekinthető bizonyítottnak pusztán a modell leírása alapján.
- Első vizsgálandó jelölt az OmniVoice, dokumentált magyar és Apple Silicon támogatása miatt. Lehetőség szerint összehasonlító helyi magyar próbát kell készíteni egy másik alkalmas modellel is; például az XTTS-v2 alkalmassága vizsgálható.
- Az aktuális modell- és futtatókörnyezet-licenceket a letöltés előtt ellenőrizni kell. A kód licence és a modellsúlyok licence nem feltétlenül azonos; a projekt saját használatra készül.
- Az Apple Silicon gyorsítás módja mérendő. MLX- vagy MPS-támogatásból nem következik az M5 Neural Engine használata vagy a chip minden egységének teljes kihasználása.
- A narrátorhangot ugyanazon magyar szövegek férfi és női mintái alapján a felhasználó választja ki. A hangminta eredetének és felhasználhatóságának tisztázottnak kell lennie.

## Testing Decisions

### Jóváhagyott elsődleges tesztelési határ

A teljes generálási feladat nyilvános felületén teszteljünk: bemenetként forrásszöveg, narrátorhang és beállítások; megfigyelhető eredményként feladatállapot és lejátszható MP3. Ugyanezen a határon történjen a szüneteltetés, a folyamat újraindítása és a folytatás ellenőrzése. A tesztek ne belső osztályokat vagy konkrét technikai darabolási módszert rögzítsenek.

A tárolóban még nincs alkalmazáskód vagy meglévő tesztelési gyakorlat. A felhasználó a fenti egyetlen elsődleges tesztelési határt jóváhagyta; a hangminőséget meghallgatással fogadja el.

### Ellenőrizendő külső viselkedés

- TXT és Markdown bemenetből a várt szövegtartalom kerül a teljes feldolgozási folyamatba; az ékezetek, hivatkozások és a kihagyott szerkezetek kezelése helyes.
- Egy forrásfájlból egy dekódolható, nem üres MP3 készül, amely böngészőben lejátszható; a generálás nem kér köztes jóváhagyást.
- A kész hanganyag tartalmilag lefedi a forrásszöveget. A megfelelőség megítéléséhez meghallgatás szükséges; egy létező MP3-fájl önmagában nem bizonyítja a jó felolvasást.
- Szüneteltetés és valódi folyamatleállítás után a már tartósan elkészült részek megmaradnak, a folytatott eredményben nincs kimaradó vagy duplázott szöveg.
- A modell letöltése után hálózat nélküli környezetben is sikeres a helyi generálás.
- Üres, sérült vagy nem támogatott bemenet és tárhelyhiány esetén érthető hiba keletkezik, korábbi kész hanganyag nem sérül.
- A DMG-ből telepített alkalmazás a szükséges helyi komponensekkel elindul, és képes a teljes munkamenetre fejlesztői eszközök nélkül.

### Valódi modell és emberi minőségi próba

A rendszer viselkedésének gyors tesztjeihez szabályozható helyettesítő beszédgenerátor használható ugyanazon a feladathatáron. Ez nem helyettesíti a célgépen futtatott, valódi modelles integrációs próbát és a felhasználó meghallgatását.

A magyar próbaszöveg tartalmazzon hosszú magánhangzókat, párbeszédet, számokat, dátumokat, rövidítéseket, tulajdonneveket, idegen szavakat és hosszabb mondatokat. Értékelendő a kiejtés, természetesség, nyugodt előadás, hangazonosság, szünetek, valamint a szavak kihagyása, ismétlése vagy betoldása. Rövid minták mellett hosszabb összefüggő próba is szükséges, beleértve a belső részhatárokat.

A végleges modellt és alapbeállításokat a felhasználó hallás alapján fogadja el. A futási időt, memóriahasználatot, átmeneti tárhelyet és a kész MP3 méretét rögzíteni kell. Teljes könyves terhelésnél a befejezhetőséget és a folytatást is mérni kell; konkrét sebességígéret a mérés előtt nincs.

## Out of Scope

- Felhős beszédgenerálás vagy szövegfeltöltés külső beszédszolgáltatásnak.
- Böngészős könyvlejátszó fejlesztése, tárhelyszolgáltatás vagy automatikus feltöltés a hangoskönyvprojektbe.
- Felhasználónak látható bekezdésenkénti jóváhagyás és automatikus fejezetenkénti export.
- Több bemeneti fájl automatikus sorba rendezése és kötegelt feldolgozása.
- Mondatonkénti hangszerkesztő, kiejtési szótár és változatkezelő felület.
- Kötelező hangklónozás, saját modell betanítása vagy tetszőleges hang utánzása.
- PDF, EPUB és OCR-bemenet; az első változat TXT- és MD-fájlokat kezel.
- MP3-on kívüli exportformátumok, könyvtárkezelés, fejezetmetaadatok és webes integrációs API.
- Nyilvános App Store-megjelenés, kereskedelmi terjesztés és más operációs rendszerek támogatása.

## Further Notes

### Megvalósítási sorrend és készültségi feltételek

1. **Magyar hangminőségi és M5-próba.** Telepítés előtt ellenőrizzük a jelöltek aktuális támogatását, licenceit és letöltési méretét. Készítsünk azonos magyar szövegből helyi férfi/női hangmintákat; mérjük a futási időt és memóriát. Kész, ha a felhasználó elfogad egy narrátorhangot és minőségi alapbeállítást. Ha egyik jelölt sem megfelelő, az alkalmazás teljes megépítése előtt térjünk vissza a modellkutatáshoz.
2. **Teljes fájl → MP3 működő alap.** Valós modelllel végig fusson egy TXT/MD forrásszöveg, előnézettel és egyetlen MP3-kimenettel. Kész, ha az eredmény meghallgatható és böngészőben lejátszható, az alapértelmezett tömörítés elfogadott.
3. **Tartós folytatás és hosszú bemenet.** Automatikus részmentés, szüneteltetés, folyamatleállításból helyreállás és végső összeállítás. Kész, ha hosszú szövegnél a kényszerített leállítás után nincs elveszett kész munka, kimaradás vagy duplázás, és teljes könyves próba is befejezhető.
4. **Egyszerű Mac-felület.** Fájlválasztás, szövegelőnézet, narrátorhang, indítás, állapot, szüneteltetés/folytatás és kész MP3 megnyitása. Kész, ha a felhasználó végigviszi a munkamenetet terminál nélkül.
5. **Önálló alkalmazás és DMG.** Függőségek csomagolása, alkalmazáson belüli modellbeszerzés, telepítés és offline indítás. Kész, ha a telepített változat fejlesztői környezet nélkül is generál, és az indítás feltételei a célgépen igazoltak.
6. **Végső átvétel.** Saját magyar szöveg feldolgozása, meghallgatás, böngészős MP3-lejátszás és egy új fájl külön feladatként történő feldolgozása. Kész, ha a felhasználó a hangminőséget és a teljes munkamenetet elfogadja.

### Kutatási kiindulópontok

Ezek jelöltekhez tartozó dokumentációk, nem a célgépen végzett mérés bizonyítékai:

- OmniVoice: https://github.com/k2-fsa/OmniVoice
- Magyar nyelvi támogatás: https://github.com/k2-fsa/OmniVoice/blob/master/docs/languages.md
- OmniVoice modellkártya és licenc: https://huggingface.co/k2-fsa/OmniVoice
- XTTS-v2 modellkártya: https://huggingface.co/coqui/XTTS-v2

### Publikálás

A projekt issue trackere a szarkab/audio-book GitHub Issues felülete. Az öt alapértelmezett triage-címke elfogadott. A felhasználó jóváhagyta e specifikáció GitHub-issue-ként történő publikálását ready-for-agent címkével.

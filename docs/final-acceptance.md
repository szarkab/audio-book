# Személyes használatú alkalmazás — záró átvétel

2026-11-11. A felhasználó kérte a projekt lezárását. Az elfogadott hatókör: helyi Piper Imre férfihang, TXT → egy MP3, saját lejátszó, sorszám-előkészítés, hat felolvasási beállítás, alkalmazáson belüli modellbeszerzés, önálló Apple Silicon/macOS 26+ DMG és saját arculat. MD, generálási folytatás és böngészős átvétel nincs a hatókörben.

## Elfogadások

- A Piper alapminősége korábban egyelőre elfogadott; a sorszámmintára a felhasználó visszajelzése: „sorszámminta is jól sikerült”.
- A telepített app saját ikonjára a Finderben és Dockban: „Igen, mindkét helyen rendben”. A #7 ezzel lezárult.
- A felhasználó friss saját terhelési próbája: „a terheléses hosszu hangot is teszteltem, működik hosszabb szövegeknél”. A végső személyes átvételt a korábban elfogadott minőséggel és ezzel a saját hosszú teszttel rögzítjük. Nem kérünk újabb mintasorozatot vagy teljes hangmeghallgatást.
- A fájlválasztó a felületvezérlő kattintására nem nyílt meg a mostani körben, de a felhasználó közvetlenül megerősítette: „Igen, megnyílik”. Ezt nem minősítettük apphibának, és nem változtattuk meg a működést. A korábbi #7 natív teljes folyamat bizonyítéka megmarad.

## Technikai ellenőrzések

A meglévő csomagolt fájl → MP3 próba hosszabb szövegre és második külön feladatra bővült. Az első MP3 ellenőrzőösszege a következő munka után változatlan. A végső teljes csomag 33/33 tesztje valódi Piperrel és a telepített appal sikeres (9,601 s), a mypy 8 forrásfájlra hibamentes. A mostani kör nem módosította a termék futtatási kódját, ezért új DMG vagy ismételt teljes build nem szükséges.

A külön, saját generált könyvméretű technikai mérés 97918 karaktert dolgozott fel 150,810 s alatt. A hang 6162,860 s (1 óra 42 perc 43 s), a fájl 73955276 byte, a generáló folyamat csúcs-RSS-e 493568000 byte. A logikai átmeneti hangméret 369772538 byte; ez nem a teljes gép memória- vagy fizikai lemezfoglalási mérése. A teljes MP3-dekódolás sikeres, a második fájl nem módosította az elsőt. A hálózat és a fejlesztői útvonalak csak a próbafolyamatoknál voltak tiltva. A kis nyers mérési jelentés: acceptance-measurements.json.

Ez a kétórás közeli mesterséges próba a felhasználó szerint felesleges volt. A saját teljes hang, részletek, ideiglenes források és napló törölve; 74418597 byte tesztállomány került eltávolításra, csak az 1421 byte-os mérési jegyzőkönyv maradt. Az ellenőrző alapértéke most egyetlen rövid próbaszöveg, a tesztismétlés legfeljebb három lehet. Nem indult újabb hanggenerálás e módosítás után. A felhasználó könyvei, mentett hangjai, a telepített app és az aktív modell megmaradtak.

## Bizonyítási határ és ismert korlát

A haladás és a dekódolhatóság a teljes bemenet feldolgozását és a fájl épségét ellenőrzi, nem bizonyítja minden kimondott szó hibátlanságát. A korábbi ASR 5,31% karakteres és 15,30% szószintű eltérése történeti, nem sikeres ASR-átvétel és nem utólag javított mérés. A személyes hangminőségi átvétel a felhasználó saját meghallgatásán és hosszú tesztjén alapul; nem vállal minden jövőbeli könyvre hibátlan kiejtési garanciát.

A kiadás ad-hoc aláírású, nem Apple-notarizált. A Gatekeeper elutasítása dokumentált; nincs akadálymentes nyilvános telepítési ígéret. A GitHub továbbra is privát. A saját kód nyilvános licence, a commitokban lévő név/e-mail közzététele és az Apple-fejlesztői aláírás külön későbbi döntés, nem nyitott személyes implementációs feladat.

## Kódellenőrzés

Standards: 0 dokumentált szabálysértés vagy nyitott kódhiba. Spec: 0 igazolt kódhiba vagy scope-bővítés. A két független review különválasztotta a műszaki bizonyítékot és az emberi elfogadást. A hosszú teszt utáni módosítás csak a fejlesztői ellenőrző rövid alapértéke és dokumentáció; szintaktikailag ellenőrzött, további generálás nélkül.

A személyes használatú alkalmazás implementációja ezzel lezárva. A telepített példány: ~/Applications/HangosKonyv.app. A DMG a privát v0.3.0-preview GitHub-kiadásban elérhető.

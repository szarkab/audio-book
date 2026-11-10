# #3 — Hosszú TXT és a felolvasási regresszió javítása

Dátum: 2026-11-10. Feladat: https://github.com/szarkab/audio-book/issues/3

Állapot: a hosszú feldolgozás és az alkalmazáson belüli lejátszó megvalósult, a tartalmi regresszió visszaellenőrzött. A hosszú hang természetességét és beszélőazonosságát a felhasználó még nem fogadta el; a #3 nyitva marad. Az első hosszú mintát kifejezetten elutasította.

## Működés

Egy kiválasztott UTF-8 TXT teljes tartalma automatikusan, egyetlen MP3-ba kerül. Nincs 600 karakteres fájlkorlát, kézi darabolás vagy köztes jóváhagyás. Belsőleg mondat- és önálló bekezdéshatárokon készülnek a modell bemenetei; a magyar rövidítések, dátumok, névkezdőbetűk és az idézett beszédhez tartozó közlés egyben marad. A szövegrészek összefűzése az eredeti előnézeti szöveget adja.

A modell egy feladaton belül egyszer töltődik be. A hangrészek 4096 képkockás blokkokban nyers PCM-fájlhoz kerülnek, nem a teljes könyv hangja halmozódik RAM-ban. A végén egyszer készül el a mono, 24 kHz-es, 96 kbit/s MP3, felülírást kizáró véglegesítéssel. Üres vagy levágott hangrész hibát okoz, csonka könyv nem kap kész állapotot. A százalék a feldolgozott szövegre vonatkozik; az MP3-összeállítás külön állapot.

A természetes mondatok hossza továbbra is befolyásolja a modell csúcsmemóriáját. Egyetlen szélsőségesen hosszú, mondat- és bekezdéshatár nélküli bemenet erőforráskorlátba ütközhet; nem csonkoljuk észrevétlenül. Teljes könyves átvétel külön feladat.

## Jelzett hiba és reprodukció

A felhasználó az első hosszú mintában kihagyásokat, ismétlésszerű befagyásokat, újrakezdéseket, kitalált szavakat és hibás kiejtést hallott. A Zene alkalmazásban indult el a lejátszás, amelyet a saját ablakunkból nem lehetett vezérelni. A külső lejátszást leállítottuk.

A bevezetett, elfogadott szintetikus mintából képzett hangreferenciás módot különválasztottuk a hosszabb szövegrészektől és az időbecsléstől. Az azonos szövegen végzett valódi M5-regressziós próba az új referencia-kondicionálással hibázott; kizárólag a referencia-kondicionálás kikapcsolásával az eredeti, elfogadott mintával pontosan azonos kimenet állt helyre. A referencia-kódolást és a hozzá tartozó futtatási állományokat ezután eltávolítottuk. Ez a konkrét konfiguráció hibáját igazolja, nem általános állítás a hangklónozásról.

A jó minta tartós regressziós tesztje: `AUDIOBOOK_REAL_MODEL_TEST=1 .venv/bin/python -m unittest discover -s tests -p test_voice_regression.py -v`. A rögzített M5-környezetben az elfogadott férfimintával egyező dekódolt hangot követeli meg. Ez nem természetességi pontozó más szövegekre.

## Helyi tartalmi ellenőrzés

A diagnosztikai `scripts/audit_speech.py` helyben futó MLX-Whisperrel átírja a hangot és összeveti a forrással. Modell: `mlx-community/whisper-large-v3-turbo-asr-fp16`, revízió: `624c19c9af5603fa73b83bce14d4aeea96156d18`. A diagnosztikai modell letöltése körülbelül 1,62 GB; nem került Gitbe és nem része az alkalmazás generálási függőségeinek. Nincs felhős átírás.

| Minta | Szószintű szerkesztési eltérés | Karakterszintű eltérés |
| --- | --- | --- |
| Elfogadott, eredeti rövid férfiminta | 5,41% | 0,00% |
| Elutasított hosszú, referenciahangos kísérlet | 57,29% | 43,59% |
| Ugyanaz a hosszú szöveg, eredeti hangmóddal | 2,08% | 0,20% |

A karakteres összevetés normalizálja a kis/nagybetűt, írásjeleket és szóközöket; az ékezeteket megtartja. A rövid jó mintán a szószintű eltérés oka a „végiggondolni” / „végig gondolni” egybeírása. A javított hosszú átírásban néhány kis eltérés marad, például „gondosan” / „gondossan”, „moharéteg” / „moharétek” és egy névelő. Ezeket pusztán az ASR alapján nem lehet biztosan kiejtési vagy átírási hibának minősíteni.

A diagnosztika ismert jó és ismert rossz mintát egyaránt megkülönböztetett. A hárommintás összehasonlítás hibakódja szándékosan 1, mert tartalmazza az elutasított kontrollt; a javított minta önálló ellenőrzése külön fut. Az ASR nem bizonyít természetes prozódiát vagy hibátlan felolvasást, és nem része az alkalmazás automatikus elfogadási döntésének.

## Valódi hosszú próba

A Mac-ablakból 2446 karakteres magyar szövegből 244,04 másodperces MP3 készült, hét automatikus modellbemenettel. A felület 0%-tól a kész állapotig működött. A javított, ugyanilyen hosszú változat is végig elkészült. A teljes fájl dekódolható.

A javított futás 236,95 másodpercig tartott; más helyi vizsgálatok részben párhuzamosan futottak, ezért nem tiszta sebesség-összehasonlítás az első futással. A folyamat mért csúcs-RSS-e 2 305 277 952 byte; ez nem a teljes rendszer- vagy GPU-memória. Az átmeneti hangfájlok együttes logikai méretének mért maximuma 14 643 501 byte, a kész MP3 2 929 581 byte. A modellállományok és az operációs rendszer háttértára nem részei ennek a tárhelymérésnek.

A helyi `artifacts/issue3-smoke` mappában a `hosszu-ferfi.mp3` az elutasított kísérlet, a `hosszu-ferfi-javitott.mp3` a visszaállított hangmód eredménye. A `rovid-javitott-proba.mp3` körülbelül 12 másodperces részlet a javított hangból, újratömörítés nélkül. A teljes hangot nem kell végighallgatni a következő rövid minőségi visszajelzéshez.

## Saját lejátszó

A külső Zene alkalmazást indító gombot kiváltottuk. A saját lejátszóban Lejátszás/Szünet, Leállítás, idővonal és hangerő található. A kész fájl betöltése nem indít lejátszást. Új forrás vagy generálás megállítja a saját korábbi lejátszást. A Finder-gomb megmaradt.

Valódi felületi próba: némított lejátszás elindult, a Szünet gomb megállította, a Leállítás 0:00-ra állította az időt és „Leállítva” állapotot mutatott. A hangerőt visszaállítottuk; az alkalmazás leállított állapotban maradt. A felületről készített rövid MP3 byte-ról byte-ra azonos az eredeti elfogadott mintával.

## Záró ellenőrzés

A célzott generálási és hosszúszöveg-tesztek, a Python-típusellenőrzés és a Swift-fordítás sikeresek. A végső két tengelyű review és teljes tesztfutás eredménye lezáráskor rögzítendő. A természetességi átvétel továbbra is nyitott.

# #13 — Kizárólag Piper Imre

2026-11-10. [Aktuális feladat](https://github.com/szarkab/audio-book/issues/13). A felhasználó a három új helyi mintából a Piper Imrét fogadta el; Supertonic M2/M5 és a hosszú VibeVoice-eredmény elutasított.

## Megvalósítás

Az egyetlen alkalmazás `HangosKonyv.app`. Az összes aktív generálási út közvetlenül a kész Piper 1.8.0 motort használja, a rögzített `hu_HU-imre-medium` hanggal, eredeti tempóval. Modellválasztó, hangklónozás és régi gyorsítás nincs az aktív folyamatban. A saját lejátszó kézzel indul és leállítható.

A modell a `rhasspy/piper-voices` `cf910fb59f1d79ab3b625a63993a108751c6c25d` revíziójából származik. A modell és konfiguráció ellenőrzőösszege a futtatóban rögzített, az első betöltés ellenőrzi. Másik hang vagy sérült fájl nem használható észrevétlenül. A 63 221 984 byte-os ONNX-modell és a kis konfiguráció a `.local/models/piper-imre` alatt található. A helyi Piper saját espeak-ng komponensét és az ONNX Runtime CPU-végrehajtóját használja, letöltési API nélkül.

Az eredeti Piper 22 050 Hz-es PCM-jét FFmpeg alakítja a meglévő 24 kHz-es veszteségmentes összeállításhoz. Ez a mintavételt változtatja, a tempót és hangmagasságot nem. A meglévő részenkénti beszédszint-kiegyenlítés és az egyszeri 96 kbit/s mono MP3-kódolás marad. A teljes forrásfájl sorrendjét és teljességét a közös feladatszolgáltatás kezeli; a modell egy feladaton belül egyszer töltődik be.

A tisztított fő környezet 218 MB körüli, az Imre-modell 60 MiB körüli. Az MLX, Transformers, Hugging Face és korábbi hangkódolók kikerültek a futtatási függőségekből. A régi, kis forrásállományok a felhasználó külön, tételes jóváhagyása után eltávolítva.

## Célgépes hosszú próba

A korábbi felhasználói forrásból, változatlan fájlból 5395 karakter és 38 belső rész került feldolgozásra. A generálás 9,637 másodpercig tartott; a kész MP3 hossza 360,827 másodperc, mérete 4 330 989 byte. A folyamat csúcs-RSS-e 618 348 544 byte; ez nem a teljes gép memóriája. Az átmeneti hanganyag legnagyobb logikai mérete 21 650 699 byte. E rövid célgépes mérésből nem ígérünk minden teljes könyvre azonos sebességet.

A régi diagnosztikai környezet eltávolítása előtti egyszeri helyi ASR-vizsgálatban a normalizált karakteres eltérés 5,31%, a szószintű eltérés 15,30% lett; 876 várt és 869 felismert szóval. Az eltérések között számok betűs alakja, idegen nevek és írásmód mellett közönséges szavak eltérései is vannak. Az ellenőrzés a korábbi 3%-os karakterküszöbön nem ment át; nem tekintjük tartalmi vagy természetességi átvételnek. A hosszú hang tényleges kiejtése emberi ellenőrzésre vár. A felhasználó csak a korábbi rövid Piper-mintát fogadta el.

A tartós automatizált valódi modellpróba most a Piper teljes fájl → MP3 útját ellenőrzi: nem üres, hallható, véges és megfelelő időtartamú dekódolt hang. Nem állít ASR-tartalmi megfelelést. A gyors tesztek szabályozható külső hanggenerátorral továbbra is a teljes feladatnál ellenőrzik a forrássorrendet, kétmondatos feldolgozást, hibákat, véglegesítést és felülírásvédelmet.

## Takarítás

A kizárólag a régi kísérletekhez letöltött OmniVoice-, teljes VibeVoice-forrás-, átalakított VibeVoice-, Whisper- és beszélődiagnosztikai modellekből összesen 52 270 032 933 logikai byte törölve. Ez fájlméretösszeg, nem független lemezfoglalási mérés. Az újra előállítható alternatív tesztkörnyezet és modellmásolatok is törölve. Csak az Imre modell maradt aktív.

A régi tesztalkalmazás és kisebb saját próbafájlok visszaállíthatóan a Kukába kerültek. A korábbi könyvforrások, a Downloads mappába felhasználó által mentett hangok, más projektek és a Git története változatlanok. A felhasználó a pontos [törlési listát](piper-retired-files.md) külön jóváhagyta; a tíz régi forrás-/referenciafájl és a két saját kukabeli tesztmaradvány eltávolítva. A futó Piper-alkalmazás és a felhasználó új hosszú tesztje nem változott. A takarítási munkaszabály az AGENTS.md-be is bekerült.

## Ellenőrzés

A teljes csomag 21 tesztje valódi Piper-integrációval sikeres, 2,466 másodperc alatt. A dokumentált típusellenőrzés sikeres. A fejlesztői alkalmazás fordítása és szigorú aláírásellenőrzése sikeres. A natív fájlválasztás és előnézet után az ablakból indított generálás elkészült; az eredmény 0:15 hosszú MP3-ként, „Leállítva” állapotban jelent meg. Automatikus lejátszás nem indult. A rövid natív futás 1,023 másodperc alatt 15,128 másodperces, 182 637 byte-os MP3-at készített; a csúcs-RSS 266 731 520 byte. Mind a rövid, mind a hosszú teljes MP3 hibamentesen dekódolható.

## Standards

A `73fccdd...095bdd4` diff külön Standards-reviewja 0 dokumentált szabálysértést és 0 javítandó baseline kódszagot talált. A kizárólagos Piper-adapter és a közös feladatszolgáltatás felelőssége elkülönül, a takarítási kivételek pontosan megnevezettek.

## Spec

A külön Spec-review 0 igazolt kódhibát talált az aktív #13-folyamatban. A rögzített eredeti Piper, a normál tempó, a helyi futás, a saját lejátszó és a biztonságos kimenet megfelel az új felhasználói döntésnek. A hosszú hang emberi átvétele és a fennmaradó pontos törlési lista külön lezárandó; az ASR-tartalmi eltérés nincs sikernek minősítve.

Összesítés: Standards 0, Spec 0 fennmaradó kódhiba. A takarítás lezárva; a #13 a hosszú hang visszajelzéséig marad nyitva. Az elvetett #9/#10 VibeVoice-feladatok not_planned állapottal lezárva, a #11/#12 és a további feladatok Piperre és az új függőségekre igazítva.


## Felhasználói visszajelzés és szünetpróba

A nagyobb Piper-teszt a felhasználó szerint nagyon biztató és gyors, a hangminőség az eddigi legjobb. Ugyanakkor kapkodónak érzi, rövid vesszőszünetekkel és hibás hangsúlyokkal. Ez további természetességi finomítás, nem végleges hosszúanyag-átvétel.

A rögzített Imre-modell a Piper 1.8.0 hivatalos, memóriában hozzáadott fonéma-időzítési kimenetét támogatja. A modellfájl súlyai nem változnak. Három vesszőnél a próba 69,66 / 81,27 / 116,10 ms időzítést adott. Egy elkülönített hangpróba ezeket 180 ms-os jelölt szünetre egészítette ki, és a mondatvégi modellfarokkal együtt legalább 350 ms helyet hagyott. A beszúrás a jelölt vesszőszakasz legcsendesebb 10 ms-os ablaka közepén történik, tisztán beszélt régiót nem vágunk szét. A szünetes változat minden eredeti nem nulla PCM-mintát változatlan sorrendben megtartott; csak csend került közéjük. Ez nem bizonyítja, hogy a bevágás teljesen hallhatatlan; a meghallgatás a döntő.

Az eredeti összehasonlítás 11,32 s, a szünetes minta 11,84 s, az ugyanezzel és 1,08-as Piper length_scale beállítással készített enyhén lassított minta 12,31 s. A szöveg és a hangprofil közös. A kísérleti minták az `artifacts/piper-prosody` alatt vannak. Az alkalmazás kódja és alapbeállítása változatlan; a felhasználó visszajelzése után választható végleges irány. Az ideiglenes WAV-ok eltávolítva, az MP3-minták és kis mérési jegyzék maradtak. A próbához átmenetileg szükséges ONNX-szerkesztő csomagok kikerültek az aktív környezetből.


## Szünetpróba elutasítva

A felhasználó mindkét szünetpróbát gyorsított hatásúnak hallotta, és a korábbi változatot jobbnak ítélte. A próba nem tiszta összehasonlítás az elfogadott korábbi mintával: más szöveg és rögzített véletlenmag is szerepelt, a fonéma-időzítéshez pedig a Piper kiegészítő kimenetét használtuk. Az eredeti modell length_scale alapértéke valóban 1,0; a próbában 1,0 és 1,08 szerepelt. Exportgyorsítás nem történt, de ez nem cáfolja a gyorsított hangzásról adott visszajelzést. A pontos akusztikai ok nincs okságilag elkülönítve.

Az alkalmazás nem kapta meg ezeket a beállításokat, a korábban jobbnak hallott Piper alapváltozat marad. A két elutasított hang, a hozzájuk tartozó kísérleti referencia, jegyzék és saját generáló próbakód eltávolítva. Következő hallásalapú összehasonlításnál ugyanazt a forrást és eredeti generálási alapot kell használni, egyszerre egy tényezőt változtatva.

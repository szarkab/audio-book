# #13 — Kizárólag Piper Imre

2026-11-10. [Aktuális feladat](https://github.com/szarkab/audio-book/issues/13). A felhasználó a három új helyi mintából a Piper Imrét fogadta el; Supertonic M2/M5 és a hosszú VibeVoice-eredmény elutasított.

## Megvalósítás

Az egyetlen alkalmazás `HangosKonyv.app`. Az összes aktív generálási út közvetlenül a kész Piper 1.8.0 motort használja, a rögzített `hu_HU-imre-medium` hanggal, eredeti tempóval. Modellválasztó, hangklónozás és régi gyorsítás nincs az aktív folyamatban. A saját lejátszó kézzel indul és leállítható.

A modell a `rhasspy/piper-voices` `cf910fb59f1d79ab3b625a63993a108751c6c25d` revíziójából származik. A modell és konfiguráció ellenőrzőösszege a futtatóban rögzített, az első betöltés ellenőrzi. Másik hang vagy sérült fájl nem használható észrevétlenül. A 63 221 984 byte-os ONNX-modell és a kis konfiguráció a `.local/models/piper-imre` alatt található. A helyi Piper saját espeak-ng komponensét és az ONNX Runtime CPU-végrehajtóját használja, letöltési API nélkül.

Az eredeti Piper 22 050 Hz-es PCM-jét FFmpeg alakítja a meglévő 24 kHz-es veszteségmentes összeállításhoz. Ez a mintavételt változtatja, a tempót és hangmagasságot nem. A meglévő részenkénti beszédszint-kiegyenlítés és az egyszeri 96 kbit/s mono MP3-kódolás marad. A teljes forrásfájl sorrendjét és teljességét a közös feladatszolgáltatás kezeli; a modell egy feladaton belül egyszer töltődik be.

A tisztított fő környezet 218 MB körüli, az Imre-modell 60 MiB körüli. Az MLX, Transformers, Hugging Face és korábbi hangkódolók kikerültek a futtatási függőségekből. A régi, kis forrásállományok külön jóváhagyásig megmaradnak, de az alkalmazás nem importálja és nem futtatja őket.

## Célgépes hosszú próba

A korábbi felhasználói forrásból, változatlan fájlból 5395 karakter és 38 belső rész került feldolgozásra. A generálás 9,637 másodpercig tartott; a kész MP3 hossza 360,827 másodperc, mérete 4 330 989 byte. A folyamat csúcs-RSS-e 618 348 544 byte; ez nem a teljes gép memóriája. Az átmeneti hanganyag legnagyobb logikai mérete 21 650 699 byte. E rövid célgépes mérésből nem ígérünk minden teljes könyvre azonos sebességet.

A régi diagnosztikai környezet eltávolítása előtti egyszeri helyi ASR-vizsgálatban a normalizált karakteres eltérés 5,31%, a szószintű eltérés 15,30% lett; 876 várt és 869 felismert szóval. Az eltérések között számok betűs alakja, idegen nevek és írásmód mellett közönséges szavak eltérései is vannak. Az ellenőrzés a korábbi 3%-os karakterküszöbön nem ment át; nem tekintjük tartalmi vagy természetességi átvételnek. A hosszú hang tényleges kiejtése emberi ellenőrzésre vár. A felhasználó csak a korábbi rövid Piper-mintát fogadta el.

A tartós automatizált valódi modellpróba most a Piper teljes fájl → MP3 útját ellenőrzi: nem üres, hallható, véges és megfelelő időtartamú dekódolt hang. Nem állít ASR-tartalmi megfelelést. A gyors tesztek szabályozható külső hanggenerátorral továbbra is a teljes feladatnál ellenőrzik a forrássorrendet, kétmondatos feldolgozást, hibákat, véglegesítést és felülírásvédelmet.

## Takarítás

A kizárólag a régi kísérletekhez letöltött OmniVoice-, teljes VibeVoice-forrás-, átalakított VibeVoice-, Whisper- és beszélődiagnosztikai modellekből összesen 52 270 032 933 logikai byte törölve. Ez fájlméretösszeg, nem független lemezfoglalási mérés. Az újra előállítható alternatív tesztkörnyezet és modellmásolatok is törölve. Csak az Imre modell maradt aktív.

A régi tesztalkalmazás és kisebb saját próbafájlok visszaállíthatóan a Kukába kerültek. A korábbi könyvforrások, a Downloads mappába felhasználó által mentett hangok, más projektek és a Git története változatlanok. Az automatikus ellenőrzés a régi, Gitben követett referencia- és forrásfájlok törlését elutasította; pontos [törlési lista](piper-retired-files.md) készült külön jóváhagyáshoz. A takarítási munkaszabály az AGENTS.md-be is bekerült.

## Ellenőrzés

A teljes csomag 21 tesztje valódi Piper-integrációval sikeres, 2,466 másodperc alatt. A dokumentált típusellenőrzés sikeres. A fejlesztői alkalmazás fordítása és szigorú aláírásellenőrzése sikeres. A natív fájlválasztás és előnézet után az ablakból indított generálás elkészült; az eredmény 0:15 hosszú MP3-ként, „Leállítva” állapotban jelent meg. Automatikus lejátszás nem indult. A végső két tengelyű kódellenőrzés eredménye még rögzítendő.

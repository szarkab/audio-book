# Alkalmazáson belüli Piper Imre-beszerzés — #6

Lezárás: 2026-11-11. A megvalósítás a #13-ban elfogadott, változatlan Imre-modellt használja; a #11 külön hosszú szöveghűségi átvételét nem zárja le.

## Működés

A natív felület külön jelzi a hiányzó, letöltés alatt álló, hiányos/sérült és használatra kész modellt. A letöltés 63227862 byte (63,2 MB); a szükséges szabad hely 127504300 byte, kerekítve legalább 128 MB. A letöltési előrehaladás látható, hiba után újrapróbálható. A modell eredete, a rögzített modellkártya és a Piper licence közvetlen hivatkozást kap.

A rögzített cf910fb59f1d79ab3b625a63993a108751c6c25d revízióból származó ONNX-modell, konfiguráció és modellkártya külön várt méretet és SHA-256 ellenőrzőösszeget kap. A beszerzés ideiglenes mappába történik, kizáró fájlzárral; csak a teljes ellenőrzött fájlkészlet kerül a modell helyére. Hálózati hiba, hiányos állomány vagy tárhelyhiba nem eredményez használatra kész hibás modellt.

A tartós hely a felhasználó Library/Application Support/HangosKonyv/models/piper-imre mappája. A fejlesztői előkészítő ugyanazt a beszerzési útvonalat használja, mint az app. A generálás önmagában nem tölt le és nem tölt fel szöveget. A szükséges Piper/espeak-ng és MP3-kódoló a jelenlegi fejlesztői környezet része; az önálló terjeszthető csomag továbbra is #7.

## Tesztelés

A meglévő teljes feladatszolgáltatás nyilvános felületén vizsgáltuk a modellbeszerzés → offline MP3 folyamatot. Az első hálózati hibás újrapróbálási teszt a hiányzó képesség miatt hibázott, majd a megvalósítással sikeres lett. Csak külső hálózati/fájlrendszeri határokat helyettesítenek a gyors próbák.

- Hálózati hiba után nincs kész állapot, és újabb letöltés indítható.
- Hiányos letöltésből nem készül használható modell vagy MP3; az ideiglenes adatok eltűnnek.
- Elégtelen tárhelynél hálózati hozzáférés előtt érthető hiba keletkezik.
- Valódi rögzített modellfájlokkal a beszerzés, sérült modell javító újraletöltése és új szolgáltatáspéldányból, tiltott HTTP-hívásokkal végzett MP3-generálás sikeres.
- A végső teljes csomag 32/32 tesztje valódi Piper-integrációval sikeres (5,422 s). mypy: 8 forrásfájl hibamentes. Swift-fordítás, szigorú appaláírás-ellenőrzés és git diff --check sikeres.

## Natív első letöltés és offline újraindítás

Az üres tartós modellhelyet a natív app hiányzóként jelezte, 63,2 MB mérettel és letöltési gombbal. Az ablakból indított valódi internetes beszerzés után „használatra kész” állapot jelent meg.

Az alkalmazást ezután bezártuk és újraindítottuk kizárólag erre a tesztfolyamatra érvényes macOS-profillal, amely minden hálózati műveletet tiltott. Ugyanezzel a profillal egy HTTPS-próbakérés ténylegesen hibázott. A gép globális hálózati és biztonsági beállításai nem változtak.

Az újraindított app a letöltött modellt felismerte, a TXT-t előnézetben megmutatta és egyetlen MP3-at készített. Eredmény: 15,093 s hang, 182061 byte MP3, 0,982 s futás, 272121856 byte folyamatcsúcs-RSS, 1137486 byte logikai átmeneti hangméret. A lejátszó „Leállítva”, 0:00 állapotban maradt; automatikus hang nem indult. A próba végén a tesztpéldányt lezártuk, az appot szokásosan újranyitottuk.

Az új tartós példány ellenőrzése után a projekt .local/models/piper-imre mappájában lévő, azonos és újra előállítható régi másolatot eltávolítottuk. A könyvforrások és felhasználói hanganyagok megmaradtak.

## Standards

Összehasonlítás: 7296aa7...c83db8c. 0 dokumentált szabálysértés és 0 javítást indokoló kódszag. A közös modelljegyzék és beszerzési út megszünteti a korábbi kettős letöltési logikát; konkrét integritási vagy konkurenciakezelési hibát a review nem talált.

## Spec

0 igazolt eltérés, 0 azonosított hiány. A hiányzó/letöltés/kész állapot, méret, tárhelyigény, ellenőrzött fájlkészlet, újrapróbálás, eredet/licenc és a natív offline újraindítás igazolt. A DMG és a #11 minőségi átvétele külön marad.

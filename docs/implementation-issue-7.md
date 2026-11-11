# Önálló DMG és arculat — #7

2026-11-11. Személyes előzetes: Hangoskönyv 0.3.0, ARM64, macOS 26 vagy újabb. A projekt továbbra is privát. A hangmodell és az elfogadott alapértékek változatlanok.

## Csomag

A SwiftUI alkalmazás saját, PyInstaller 6.22.3-mal összegyűjtött Python 3.12/Piper 1.8.0/ONNX Runtime futtatót, CA-tanúsítványokat és statikus, audio-only FFmpeg 9.0.2 + LAME 3.100 kódolót tartalmaz. A kódoló csak rendszerkönyvtárakra hivatkozik; a Homebrew kizárólag buildfüggőség. A kiadási appban nincs fejlesztői gyökérmappa vagy virtuális környezetre visszaeső út. A naplók a felhasználó Library/Logs/HangosKonyv mappájába kerülnek.

A DMG-ben Applications-hivatkozás, magyar telepítési szöveg, saját appikon és forráscsomagok vannak. A külső komponensek licencszövegei az app Resources/Licenses mappájában is szerepelnek. A modell továbbra is külön első letöltés, rögzített revízióval és ellenőrzőösszegekkel. A kiadás minimális rendszere macOS 26, a statikus buildfüggőség tényleges minimumához igazítva; nem állítunk macOS 14-es kiadási támogatást.

A saját alkalmazásforrás nyilvános terjesztési licence még nincs kiválasztva. Ez személyes, privát előzetes; nem kész nyilvános terjesztés. A külső licencek és azok rögzített forrásai mellékeltek.

## Arculat

A könyv és arany hanghullám kék hátteren jelenik meg. A vektoros forrás a make-icon.swift; a PNG és a macOS ICNS méretsor ebből áll elő. Az appon a CFBundleIconFile erre mutat, az ablakban a rendszer által feloldott alkalmazásikon jelenik meg. A saját kék kiemelés és modellállapot-panel világos módban is olvasható.

A telepített alkalmazásablakban az ikon vizuálisan ellenőrzött. A Dock külön gépi felületi olvasása időtúllépéssel megállt. A felhasználó 2026-11-11-én megerősítette: „Igen, mindkét helyen rendben” a Finder és a Dock saját ikonjára. A vizuális átvétel ezzel teljesült.

## Ellenőrzés

- A legmagasabb fájl → MP3 teszthatáron előbb hiányzó önálló futtató miatt hibázó csomagpróba készült. Az első elkészült csomagban a minimális FFmpeg-ből hiányzó PCM-demuxer ugyanezen a próbán derült ki. Javítás után a tényleges csomagolt futtató külső Python/Homebrew PATH nélkül sikeresen dolgozik.
- A végső teljes csomag 33/33 tesztje valódi Piperrel és a ~/Applications alá telepített appal sikeres (6,965 s). mypy: 8 forrásfájl hibamentes, tiszta elemzéssel. A Swift release-build, a mély/szigorú aláírás-ellenőrzés és git diff --check sikeres.
- Friss, .local nélküli forrásexportból, csak az előkészített buildeszköz-környezettel, a teljes önálló app-build sikeresen lefutott. Az összes forrásarchívum ténylegesen újra beszerzésre és ellenőrzésre került.
- A DMG ténylegesen felcsatolva, az app onnan a felhasználó Applications mappájába másolva. Új modellmappával a telepített ablak hiányzó állapotot mutatott; az Imre-hang letöltése gombra valódi beszerzés és kész állapot következett.
- Újraindítás után a próbafolyamat nem olvashatta a projektet, a Homebrew-t vagy a külső uv-Pythont, és a hálózat is tiltott volt. A tiltásokat külön cat/Homebrew-próba is visszaigazolta. A telepített app így is előnézetet és egy MP3-at készített a projekten kívüli TXT-ből.
- Az offline natív minta 4,168 s hang / 51020 byte MP3; 0,741 s futás; 218267648 byte folyamatcsúcs-RSS; 400206 byte átmeneti hangméret. A mellékelt kódoló teljesen dekódolja. A saját lejátszó leállított, 0:00 állapotban maradt, hang nem indult automatikusan.
- A telepített app hat beállítása az elfogadott 1× / 0,333 / 0,5 / 1× / normalizálás bekapcsolva / 0 s értékekkel megjelent.

## Aláírás és Gatekeeper

A gépen 0 használható kódaláíró identitás van. Az app és a mellékelt Mach-O kód ad-hoc aláírást kap, ami a helyi futást lehetővé teszi. A tényleges spctl --assess eredménye rejected; Developer ID és Apple-notarizáció nincs. Ez a dokumentált előzetes nem állít akadálymentes internetes telepítést. Nem kapcsoltuk ki a Gatekeepert, és nem töröltünk karanténjelzést. Az Apple-fejlesztői hozzáférés és a nyilvános terjesztési döntések későbbi feladatok.

## Standards

Alap: 324aeeb. Egy P2 build-bootstrap hibát talált a review: a munkamappa és licencforrások létrehozásuk/beszerzésük előtt kerültek használatba. A c31444e előrehozta a mkdir és a teljes ellenőrzött forrásbeszerzés lépéseit. Tiszta forrásból igazolt, az újraellenőrzésben 0 nyitott finding.

## Spec

Ugyanez az előkészítési sorrend sértette a reprodukálható build feltételét; javítva. Az újraellenőrzés 0 fennmaradó Spec-kódhibát talált. A Dock/Finder végső vizuális visszaigazolását a felhasználó megadta; a Gatekeeper/notarizáció korlátja kifejezetten dokumentált.

## Átadás

A végleges DMG és SHA-256 melléklete a privát [v0.3.0-preview kiadásban](https://github.com/szarkab/audio-book/releases/tag/v0.3.0-preview) elérhető. A végleges csomag újraépítése után a csomagolt MP3-próba ismét sikeres. Az app a végleges DMG-ből a felhasználó Applications mappájába frissítve és szokásosan újranyitva, kész modellel. A saját ideiglenes app-, modell- és buildmásolatok eltávolítva; a tartós modell és a könyvforrások megmaradtak.

# Önálló macOS-csomag — #7

> Archív műszaki dokumentum, 2026-11-10–11. A jelenlegi működés leírása a [specifikációban](specification.md) található.

Kapcsolódó feladat: [#7](https://github.com/szarkab/audio-book/issues/7). Verzió: 0.3.0, ARM64, macOS 26 vagy újabb.

## Csomagtartalom

A SwiftUI alkalmazás Python 3.12, Piper 1.8.0, ONNX Runtime és CA-tanúsítványok csomagolt példányát tartalmazza, PyInstaller 6.22.3-mal. A hangkódoló statikus, audio-only FFmpeg 9.0.2 és LAME 3.100; csak rendszerkönyvtárakra hivatkozik. A telepített app nem igényel Homebrew-t, külön Pythont vagy projektmappát.

A DMG Applications-hivatkozást, magyar telepítési leírást, alkalmazásikont és forráscsomagokat tartalmaz. A külső licencszövegek az alkalmazás `Resources/Licenses` mappájában is elérhetők. A saját alkalmazásforráshoz nincs külön licenc megadva. A Piper Imre modell első használatkor, külön letöltéssel érhető el.

A macOS 26-os rendszerkövetelményt a statikus buildfüggőség minimuma határozza meg. A munkanaplók helye `~/Library/Logs/HangosKonyv`.

## Megjelenés

A könyv–hanghullám ikon kék hátteret és arany hullámvonalat használ. Vektoros forrása a `scripts/make-icon.swift`; ebből készül a PNG és a macOS ICNS méretsor. A `CFBundleIconFile` a mellékelt ikonra mutat. Az ikon megjelenése az alkalmazásablakban, a Finderben és a Dockban ellenőrzött.

## Csomagellenőrzés

- 33/33 sikeres teszt valódi Piperrel és a telepített alkalmazással (6,965 s); hibamentes mypy 8 forrásfájlon.
- Sikeres Swift release-build, mély és szigorú aláírás-ellenőrzés.
- Sikeres teljes build friss, `.local` nélküli forrásexportból, rögzített és ellenőrzött forrásarchívumokkal.
- Telepítés a felcsatolt DMG-ből, modellletöltés üres modellkönyvtárba, majd sikeres natív TXT → MP3 generálás.
- Sikeres generálás a próbafolyamat projekt-, Homebrew-, külső Python- és hálózati hozzáférésének tiltása mellett. A tiltásokat külön hozzáférési próbák ellenőrizték.

| Offline csomagpróba | Eredmény |
| --- | --- |
| Hanghossz | 4,168 s |
| MP3 mérete | 51 020 byte |
| Futási idő | 0,741 s |
| Folyamat csúcs-RSS | 218 267 648 byte |
| Logikai átmeneti hangméret | 400 206 byte |

A mellékelt kódoló a teljes MP3-at hibamentesen dekódolta. A lejátszó leállított állapotban maradt. Mind a hat beállítás a dokumentált alapértékkel jelent meg.

A build-előkészítés könyvtár- és licencforrás-sorrendjének hibáját a `c31444e` javítja. A minimális FFmpeg-konfiguráció tartalmazza a csomagpróbához szükséges PCM-demuxert.

## Aláírás

Az alkalmazás és a mellékelt Mach-O állományok ad-hoc aláírásúak. Developer ID és Apple-notarizáció nincs; a `spctl --assess` eredménye `rejected`. Az első indítás ezért külön macOS-engedélyezést igényelhet. A telepítési lépések a [README-ben](../README.md) találhatók.

A DMG és a SHA-256 melléklet a [v0.3.0-preview kiadásban](https://github.com/szarkab/audio-book/releases/tag/v0.3.0-preview) érhető el.

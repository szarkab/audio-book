# Piper Imre modellbeszerzés — #6

> Archív műszaki dokumentum, 2026-11-10–11. A jelenlegi működés leírása a [specifikációban](specification.md) található.

Kapcsolódó feladat: [#6](https://github.com/szarkab/audio-book/issues/6). Dátum: 2026-11-11.

## Modell és integritás

A beszerzés az ONNX-modellt, a konfigurációt és a modellkártyát tölti le a `rhasspy/piper-voices` `cf910fb59f1d79ab3b625a63993a108751c6c25d` revíziójából. A fájlokhoz rögzített méret és SHA-256 ellenőrzőösszeg tartozik.

A teljes letöltés 63 227 862 byte; a szükséges szabad hely 127 504 300 byte, kerekítve legalább 128 MB. A célkönyvtár `~/Library/Application Support/HangosKonyv/models/piper-imre`.

A letöltés kizáró fájlzárral, ideiglenes könyvtárba történik. Csak a teljes és ellenőrzött fájlkészlet válik használhatóvá. A natív felület külön jelzi a hiányzó, letöltés alatt álló, hiányos vagy sérült és használatra kész állapotot, a méretet és az előrehaladást. Hiba után újrapróbálható.

## Ellenőrzési eredmények

- Hálózati hiba és hiányos letöltés esetén nincs használatra kész modell; az ideiglenes adatok törlődnek.
- Elégtelen tárhely esetén a hiba a hálózati hozzáférés előtt jelentkezik.
- Sérült modell újraletöltése és az ezt követő offline MP3-generálás sikeres.
- A natív alkalmazás üres modellkönyvtárból indulva sikeresen letöltötte a modellt, majd újraindítás után, a próbafolyamat hálózati elérését tiltó macOS-profillal is generált MP3-at. A tiltás működését külön sikertelen HTTPS-kérés igazolta.
- Az akkori tesztcsomag 32/32 próbája sikeres (5,422 s); a mypy 8 forrásfájlon hibamentes, a Swift-fordítás és az aláírás-ellenőrzés sikeres.

| Offline natív minta | Eredmény |
| --- | --- |
| Hanghossz | 15,093 s |
| MP3 mérete | 182 061 byte |
| Futási idő | 0,982 s |
| Folyamat csúcs-RSS | 272 121 856 byte |
| Logikai átmeneti hangméret | 1 137 486 byte |

A kész fájl betöltése után a lejátszó leállított, 0:00 állapotban maradt. A letöltés és a generálás közös modelljegyzéket használ; a generálás nem végez automatikus modellletöltést vagy szövegfeltöltést.

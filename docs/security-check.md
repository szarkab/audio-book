# Biztonság és adatkezelés

## Helyi adatfeldolgozás

A TXT-fájlok feldolgozása és a hanggenerálás helyben történik. A Piper Imre modell első letöltése internetkapcsolatot igényel; a szöveg és a kész hang nem kerül felhős beszédszolgáltatáshoz. A munkanaplók a macOS `~/Library/Logs/HangosKonyv` mappájában találhatók.

A `.gitignore` kizárja a helyi `.env` fájlokat és a tipikus kulcs- és aláírófájlokat. A kizárás nem távolít el korábban verziókezelt tartalmat.

## Repository-vizsgálat

A 2026-11-11-i mintakeresés terjedelme:

| Vizsgált tartalom | Mennyiség |
| --- | --- |
| Git-commit | 36 |
| Szöveges Git-objektumváltozat | 180 |
| GitHub-issue | 14 |
| Issue-hozzászólás | 7 |

A keresés privátkulcs-fejlécekre, ismert szolgáltatói tokenmintákra, hitelesítési adatot tartalmazó URL-ekre és tipikus titokérték-hozzárendelésekre terjedt ki. A keresés eredménye: **0 találat**. A vizsgált fájllistában helyi hitelesítő fájl sem szerepelt.

A mintakeresés nem teljes körű sérülékenységvizsgálat, és nem elemzi a külső binárisok belső tartalmát. Az eredmény a fenti tartalomra és a megadott időpontra vonatkozik.

A repository nyilvános. A Git-előzményekben a szerzői név és e-mail-cím, valamint két korábbi szintetikus hangminta is elérhető. A minták nem részei a jelenlegi alkalmazásnak.

## Kiadási fájlok

A `v0.3.0-preview` DMG SHA-256 ellenőrzőösszege:

```text
7c6b666b3a717bf9313876091e80163fedcee07cf310452f90d8fd6f95e86162
```

A helyi fájl, a GitHub által jelzett érték és a kiadás `.sha256` melléklete az ellenőrzéskor egyezett. A telepített alkalmazás működésének eredményei az [ellenőrzési összefoglalóban](final-acceptance.md) találhatók.

## macOS-engedélyezés

Az alkalmazás ad-hoc aláírású, Apple Developer ID és notarizáció nélkül. A macOS ezért blokkolhatja az első indítást. Megbízható példánynál az első megnyitási kísérlet után a **Rendszerbeállítások → Adatvédelem és biztonság → Megnyitás mindenképpen** lehetőség használható, ha elérhető. [Apple útmutató](https://support.apple.com/en-us/102445).

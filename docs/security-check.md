# GitHub- és érzékenyadat-ellenőrzés

Dátum: 2026-11-11. A repository nyilvános. Ez a jegyzőkönyv a lent megadott körben végzett mintakeresést és a kiadási fájlok ellenőrzését foglalja össze.

## Ellenőrzött állapot

- A GitHub-repo PUBLIC. A korábbi hozzáférés-ellenőrzés egy együttműködőt mutatott; az ellenőrzés idején minden issue lezárt volt.
- A v0.3.0-preview kiadás nem draft; a DMG és a SHA-256 melléklet teljesen feltöltött.
- A GitHub által jelzett, a helyben számolt és a mellékelt DMG-ellenőrzőösszeg egyezik: 7c6b666b3a717bf9313876091e80163fedcee07cf310452f90d8fd6f95e86162.
- A README dokumentálja a telepítést, a használatot, a buildet és a teszteket. A 33 sikeres próba és a mérési korlátok az [ellenőrzési összefoglalóban](final-acceptance.md) szerepelnek.

## Adatvizsgálat

A vizsgálat 36 meglévő commitot és 180 szöveges Git-blobváltozatot, továbbá 14 issue-t és 7 hozzászólást érintett. Privátkulcs-fejlécet, ismert szolgáltatói tokenmintákat, hitelesítést tartalmazó URL-eket és tipikus titokérték-hozzárendeléseket keresése történt. Az ellenőrzött mintákra 0 találat volt; a jelenleg követett fájlok között helyi hitelesítő fájlnév sem szerepelt. Ez mintakeresés, nem minden lehetséges titok hiányának vagy a teljes alkalmazás sérülékenységmentességének garanciája. A külső binárisok belső tartalmát ez a szöveges vizsgálat nem minősíti.

A Gitben a commitok szerzői neve és e-mail-címe megmaradt. Két korábbi szintetikus hangminta fájlútvonala az előzményekben továbbra is elérhető. Ezek nem kerültek újra az aktív munkamappába. A nyilvános repositoryban az előzmények, az issue-k és a kiadási mellékletek is elérhetők.

A .gitignore kizárja a helyi .env fájlokat és a tipikus kulcs-/aláírófájlokat a véletlen hozzáadás ellen. Ez már feltöltött fájlok eltávolítására nem szolgál; a vizsgálat ilyet nem azonosított.

## Indítás

A saját, megbízható app első megnyitási kísérlete után a Rendszerbeállítások → Adatvédelem és biztonság → Megnyitás mindenképpen lehetőség használható, ha azt a macOS felajánlja. Az engedélyezés a felhasználó saját döntése; globális védelem kikapcsolása nem szükséges. [Apple útmutató](https://support.apple.com/en-us/102445).

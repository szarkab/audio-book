# GitHub- és érzékenyadat-ellenőrzés

2026-11-11. A projekt személyes használatú alkalmazásként lezárt, nyilvános alkalmazáskiadás nem cél. Az Apple-notarizáció hiányát és az első indítás macOS-figyelmeztetését a felhasználó elfogadta; ez nem nyitott implementációs feladat.

## Ellenőrzött állapot

- A GitHub-repo PRIVATE. A jogosult együttműködők listája egy bejegyzést mutat. Nincs nyitott issue; a munkamappa tiszta és a main szinkronban volt.
- A v0.3.0-preview kiadás nem draft; a DMG és a SHA-256 melléklet teljesen feltöltött.
- A GitHub által jelzett, a helyben számolt és a mellékelt DMG-ellenőrzőösszeg egyezik: 7c6b666b3a717bf9313876091e80163fedcee07cf310452f90d8fd6f95e86162.
- A README dokumentálja a telepítést, a használatot, a buildet és a teszteket. A végső felhasználói átvétel és a 33 sikeres próba a final-acceptance.md-ben szerepel.

## Adatvizsgálat

A vizsgálat 36 meglévő commitot és 180 szöveges Git-blobváltozatot, továbbá 14 issue-t és 7 hozzászólást érintett. Privátkulcs-fejlécet, ismert szolgáltatói tokenmintákat, hitelesítést tartalmazó URL-eket és tipikus titokérték-hozzárendeléseket kerestünk. Az ellenőrzött mintákra 0 találat volt; a jelenleg követett fájlok között helyi hitelesítő fájlnév sem szerepelt. Ez mintakeresés, nem minden lehetséges titok hiányának vagy a teljes alkalmazás sérülékenységmentességének garanciája. A külső binárisok belső tartalmát ez a szöveges vizsgálat nem minősíti.

A Gitben a commitok szerzői neve és e-mail-címe megmaradt. Két korábbi szintetikus hangminta fájlútvonala az előzményekben továbbra is elérhető. Ezek nem kerültek újra az aktív munkamappába. A repo publikussá tétele a történetet, issue-kat és a már feltöltött kiadási mellékleteket is láthatóvá tenné; az ellenőrzés nem változtatta meg a láthatóságot és nem írta át az előzményeket.

A .gitignore kiegészült a helyi .env fájlokkal és tipikus kulcs-/aláírófájlokkal, a véletlen jövőbeli hozzáadás ellen. Ez már feltöltött fájlok eltávolítására nem szolgál; a vizsgálat ilyet nem azonosított.

## Indítás

A saját, megbízható app első megnyitási kísérlete után a Rendszerbeállítások → Adatvédelem és biztonság → Megnyitás mindenképpen lehetőség használható, ha azt a macOS felajánlja. Az engedélyezés a felhasználó saját döntése; globális védelmet nem kapcsoltunk ki. [Apple útmutató](https://support.apple.com/en-us/102445).

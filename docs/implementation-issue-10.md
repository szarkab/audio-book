# VibeVoice magyar MLX-vizsgálat — #10

> Archív műszaki dokumentum, 2026-11-10–11. A jelenlegi működés leírása a [specifikációban](specification.md) található.

Kapcsolódó dokumentumok: [#10](https://github.com/szarkab/audio-book/issues/10), [#9](https://github.com/szarkab/audio-book/issues/9). A VibeVoice nem része a jelenlegi alkalmazásnak.

## Modellkonfiguráció

- Magyar checkpoint: `Cseti/VibeVoice_7B_hun_v2`, revízió: `22434d6f261e2f231b3c358563bdf2d2e8caab57`.
- Eredeti F32-súlyok: körülbelül 37,37 GB; 1205 paraméterbejegyzés. A konverzió súlyonként dolgozott, rögzített forrásellenőrzőösszegekkel és szigorú alakellenőrzéssel.
- Nyelvi mátrixok és kimeneti fej: 4 bites affine kvantálás, 64-es csoportméret. Nyelvi skalár- és normalizáló paraméterek: FP16. Diffúziós fej, kodekek és hangcsatlakoztatók: eredeti F32.
- Konvertált súlyok: 11 195 416 856 byte, nyolc fájlban.
- Tokenizáló: `Qwen/Qwen2.5-7B`, revízió: `d149729398750b98c0af14eb82c78cfe92750796`, kizárólag helyi fájlokból. Qwen modellsúlyok nélkül.
- Futtató: `mlx-audio==0.6.5`, `mlx==0.32.4`, Apple GPU.
- Referencia: 8,07 másodperces, kétmondatos szintetikus férfihang, ellenőrzőösszeggel.
- Generálás: CFG 1,3; 20 diffúziós lépés; rögzített véletlenmag; 1,0× exporttempó; egyszeri 96 kbit/s mono MP3-kódolás.

A lépés- vagy kontextuskorlát elérése hibát eredményezett, nem késznek jelölt részleges hangot. A helyi modellbetöltés nem használt letöltő API-t vagy távoli tokenizáló-feloldást.

## Rövid M5-minta

Célgép: Apple M5, 32 GB egyesített memória. Bemenet: 118 karakter, két magyar mondat, a referenciától eltérő szöveggel.

| Mért adat | Eredmény |
| --- | --- |
| Hanghossz | 8,4 s |
| MP3 mérete | 101 709 byte |
| Natív alkalmazás futási ideje | 65,72 s |
| Első parancssori futás | 70,45 s |
| MLX-csúcsmemória | 12 611 382 580 byte |
| Folyamat csúcs-RSS | 8 746 893 312 byte |
| Logikai átmeneti hangméret | 806 444 byte |

A két kimenet byte-ról byte-ra azonos és teljesen dekódolható volt. A memóriaértékek eltérő mérési kategóriák, nem összeadandók. A helyi Whisper-átírás 17 várt és 17 felismert szót, 1,01% normalizált karakteres eltérést mutatott. Az „eleredt” / „elerett” eltérés önmagában nem különíti el a kiejtési hibát az ASR-hibától.

A natív fájlválasztás, előnézet, mentés, haladásjelzés és kézzel indítható lejátszó működött. Az akkori ellenőrzésben 22/22 teszt sikeres volt (70,305 s), a mypy 7 forrásfájlon hibamentes; a Swift-fordítás és az aláírás-ellenőrzés sikeres.

## Hosszú minta és következtetés

A hosszú futás 2977,21 másodpercet (49,62 percet) igényelt, és 629,07 másodpercnyi hangot adott. Meghallgatáskor hangváltások, szaggatás és erős hangtorzulások jelentkeztek. A konfiguráció hosszú narrációra alkalmatlannak bizonyult, a rövid ASR-eredmény ellenére.

Az eltérés pontos oka nem különült el a modell, a referencia és az MLX-megvalósítás között. A nagy modellsúlyok, a kísérleti alkalmazás és a konverter nem részei az aktív projektnek. Az alternatív motorok összehasonlítása a [helyi magyar megoldások](existing-hungarian-tts-solutions.md) dokumentumában található.

## Források

- [Magyar modell](https://huggingface.co/Cseti/VibeVoice_7B_hun_v2)
- [Az alapmodell előfeldolgozási konfigurációja](https://huggingface.co/aoi-ot/VibeVoice-Large/blob/1b81fecc784a076dcd935678db551871f4598ebf/preprocessor_config.json)
- [MLX VibeVoice](https://github.com/Blaizzy/mlx-audio/tree/main/mlx_audio/tts/models/vibevoice)

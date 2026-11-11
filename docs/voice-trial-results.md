# Első helyi magyar hangpróba — mérési eredmények

> Történeti feljegyzés: korábbi modellpróbák, mérések vagy fejlesztési ellenőrzések dokumentuma. Az aktuális alkalmazás működését a [specifikáció](specification.md) írja le.

Dátum: 2026-11-10. Kapcsolódó specifikáció: https://github.com/szarkab/audio-book/issues/1

Állapot: a helyi generálás és MP3-dekódolás ellenőrzött. A felhasználó meghallgatta mindkét hangot: a férfihangot szinte tökéletesnek ítélte, és kizárólag azt választotta a folytatáshoz; a női hang nem kerül az első alkalmazásváltozatba. Az OmniVoice-bfloat16 férfiprofil a fejlesztési alap. A hosszú szövegek hangállandósága, teljes szöveghűsége és a végleges MP3-bitrátája még ellenőrizendő.

## Környezet

Apple M5, 32 GB memória; MLX Metal GPU. OmniVoice-bfloat16, `6119f7072580cc30c3cbdf496269216b03ad9742` modellrevízió. Python 3.12.13; MLX 0.32.4, MLX-Audio 0.6.5, Transformers 5.22.2. A teljes függőséglista a próba lock fájljában szerepel. A modell és a teljes hangdekódoló letöltése körülbelül 2,04 GB; a tényleges helyi modellmappa körülbelül 1,9 GiB.

A generálás helyi modellfájlokból, a Hugging Face és Transformers offline módjában történt. Nem használt felhős beszédszolgáltatást. Hangtervezési mód, magyar nyelvkód, 42-es véletlenmag, 64 generálási lépés. A hangutasítások és pontos szövegek a minták melletti JSON-jelentésekben szerepelnek.

## Mérések

A futási idő a modell betöltését és az MP3-kódolást nem tartalmazza. A memória az MLX által jelentett csúcsérték, nem a teljes rendszer memóriahasználata.

| Minta | Hanghossz | Generálási idő | MLX-csúcsmemória |
| --- | --- | --- | --- |
| Narráció, Férfihang-jelölt | 23 s | 11.86 s | 4.67 GB |
| Narráció, Nőihang-jelölt | 23 s | 9.00 s | 4.68 GB |
| Kiejtési próba, Férfihang-jelölt | 26 s | 11.82 s | 5.03 GB |
| Kiejtési próba, Nőihang-jelölt | 26 s | 11.17 s | 5.03 GB |

Az első modellbetöltés 29,11 másodperc volt; egy későbbi, már bemelegített fájlgyorsítótárral futó betöltés 2,02 másodperc. A rövid próbákból teljes könyvre megbízható futásidő még nem következik.

## Meghallgatható eredmények

A repo helyi `artifacts/voice-trial` mappájában a 23 másodperces narrációs minták találhatók. A javított kiejtési minták az `artifacts/voice-trial-pronunciation-safe` mappában vannak. Mindkét mappában `male-96k.mp3` és `female-96k.mp3` a jobb minőségű exportjelölt, valamint `male-64k.mp3` és `female-64k.mp3` a kisebb exportjelölt. A forrás-WAV és a mérési JSON megmaradt.

Egy 23 másodperces, mono, 24 kHz-es minta 96 kbit/s-on 277 101 byte, 64 kbit/s-on 184 749 byte. A bitráták közötti hallható különbséget meg kell hallgatni; nincs még elfogadott végleges bitráta.

## Ellenőrzések és javítás

Mind a nyolc átadott MP3 teljesen dekódolható, mono, 24 kHz-es, a kért hosszúságú, véges és nem néma hangjelet tartalmaz. A dekódolt MP3-ak csúcsai a torzítást okozó teljes skálán belül maradnak. Ez nem bizonyítja a magyar kiejtés vagy a narráció minőségét; tényleges böngészős lejátszás még nincs külön ellenőrizve.

A kiejtési férfiminta első futásánál a modell 1,2245-es nyers csúcsamplitúdót adott. A mentési lépés szükség szerinti, egyenletes hangerőcsökkentést kapott 0,95-ös csúcsra, és a kiejtési próbát újrafuttattuk. Az első, hibás csúcsú próba nem a meghallgatásra átadott változat. Ez a korrekció nem változtat a szövegen, tempón vagy a beszéd dinamikáján belüli arányokon.

A Transformers betöltéskor modelltipus-figyelmeztetést adott. A konkrét modell és hangdekódoló betöltése, a GPU-generálás és a hullámforma-ellenőrzés sikeres volt; a figyelmeztetést nem rejtettük el. A hosszú feladatok és a végleges csomagolás alkalmassága további ellenőrzést igényel.

## Következő minőségi kapu

A rövid férfihangos minta elfogadott fejlesztési kiindulópont. Következő lépés a kiválasztott férfihang hosszabb, egybefüggő szövegen történő ellenőrzése: maradjon állandó a narrátorhang és a nyugodt előadás, ne legyen kihagyás, ismétlés vagy rosszul ejtett szó. A hangtervezési utasítás és a véletlenmag önmagában nem bizonyít tartós beszélőazonosságot; a végleges megoldásnak ezt hosszabb próbán kell igazolnia. A korábbi női minták történeti összehasonlításként maradnak meg. A rövid próba nem teljes könyves, folytathatósági vagy DMG-átvételi teszt.

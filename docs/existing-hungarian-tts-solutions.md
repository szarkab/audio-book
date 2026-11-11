# Meglévő helyi magyar felolvasó megoldások

> Történeti feljegyzés: korábbi modellpróbák, mérések vagy fejlesztési ellenőrzések dokumentuma. Az aktuális alkalmazás működését a [specifikáció](specification.md) írja le.

Vizsgálat: 2026-11-10. Cél: saját használatú, magyar férfi narrátorhangú hanganyag, M5/32 GB Macen, felhő nélkül. A saját VibeVoice-változat hosszú próbáját a felhasználó elutasította: szaggatás, hangváltás, torz hangok és túl hosszú generálás. A korábbi rövid siker és ASR-eredmény nem igazolta a hosszú hang természetességét.

A dokumentum első része elsődleges források vizsgálata; az alábbi záró rész külön, tényleges célgépes rövid próbát rögzít. A meglévő alkalmazás kódja nem módosult. A hangminőség felhasználói elfogadása továbbra is meghallgatást igényel.

## Rövidlista

| Megoldás | Kész elem | Magyar férfihang és Mac-bizonyíték | Megítélés |
| --- | --- | --- | --- |
| Piper + Imre | Kész helyi motor, Python API/CLI és ONNX-hangmodell | Hivatalos hu_HU Imre-hang; natív macOS ARM64 telepítőcsomag | Egyszerű összehasonlítási alap, a természetesség meghallgatandó |
| Supertonic 3 | Kész ONNX-futtató, Python- és Swift-példa, férfi presetek | Magyar `hu` hivatalosan szerepel; Swift-példa macOS 13+-ra | Első minőségi jelölt meglévő motorral, de a projekt archivált |
| ebook2audiobook | Kész helyi könyvkonvertáló webes felület Mac-indítóval | Piper és más motorok, magyar Piper-preset; az alap magyar hang Anna | Kész alkalmazás lehetősége, férfi Imre külön modellként ellenőrizendő |

## Piper + Imre

Az aktív Piper-projekt az OHF-Voice/piper1-gpl. Gyors helyi motor, beépített espeak-ng fonemizálással, fájlbemenettel, WAV-kimenettel és újrahasználható Python API-val. A PyPI 1.8.0 kiadás macOS 11+ ARM64 wheelje kifejezett telepítési bizonyíték Apple Siliconra. Ez nem saját M5-sebességmérés. [Projekt](https://github.com/OHF-Voice/piper1-gpl), [hivatalos CLI](https://github.com/OHF-Voice/piper1-gpl/blob/main/docs/CLI.md), [PyPI-csomagok](https://pypi.org/project/piper-tts/1.8.0/#files)

A hivatalos hangrepo `hu_HU-imre-medium` modellje körülbelül 63,2 MB, egy beszélővel, 22 050 Hz mintavétellel. A modellkártya Piper 1.5+-t és 0,5 / 0,333 alap zajparamétereket ír; az adathalmaz CC0. A magyar hangprojekt Imrét férfihangként azonosítja. A kisebb modell és a „medium” megjelölés nem jelenti, hogy természetes hangoskönyvhangként már elfogadható. [Modellkártya](https://huggingface.co/rhasspy/piper-voices/blob/main/hu/hu_HU/imre/medium/MODEL_CARD), [hangfájlok](https://huggingface.co/rhasspy/piper-voices/tree/main/hu/hu_HU/imre/medium), [magyar hangprojekt](https://rhvoice.hu/en/voices/), [hivatalos mintafelület](https://rhasspy.github.io/piper-samples/)

## Supertonic 3

A kiadó 99M-paraméteres ONNX-modellje 31 nyelvet, köztük magyart támogat, helyi futtatással. A modellcsomag előre rögzített hangprofilokat ad; nem szükséges új hangklónozó futtatást írni. A modell OpenRAIL-M, a példakód MIT-licencű. A gyorsaságra és olvasási stabilitásra vonatkozó kiadói állítás nem saját magyar M5-eredmény. [Modellkártya](https://huggingface.co/supertone-oss-archive/supertonic-3)

Öt férfi preset van. Az M2-t mély, nyugodt hangként, az M5-öt meleg, halkabb hangoskönyves narrátorként jellemzik; ezek kiadói hangkarakter-leírások. [Hangprofilok](https://github.com/supertone-oss-archive/supertonic-py/blob/main/docs/voices.md)

A hivatalos Swift-példa macOS 13+-t és Swift 5.9+-t ír elő. Hosszú szöveget belül bont, szünetekkel egyetlen hangfájlba egyesít; dokumentációja szerint a GPU-mód még nem támogatott. A Python-változat ONNX Runtime-motorja szintén kész. A CPU-s út a kis modellnél érdemi jelölt, nem szükséges a gép minden egységét terhelni az elfogadható sebességhez. [Swift-példa](https://github.com/supertone-oss-archive/supertonic/blob/main/swift/README.md), [Python-példa](https://github.com/supertone-oss-archive/supertonic/blob/main/py/README.md)

Fontos karbantartási korlát: a kiadó 2026. szeptember 9-én archiválta a repót, támogatása megszűnt. A fennmaradt forrás és modellek explicit letöltéssel, hosted szolgáltatás nélkül használhatók. A dokumentált modellrevízió `aafc6e32416a594460b32413efc49d7fe4ce6d46`. A mintához az eredeti ONNX-példát és a rögzített archív állományokat kell használni; a régi SDK automatikus letöltése a korábbi névtérre mutathat. [Archívum és helyi indítás](https://github.com/supertone-oss-archive/supertonic#quick-start)

## ebook2audiobook

A DrewThomasson/ebook2audiobook meglévő, helyi Gradio-alkalmazás Mac-indítóval, TXT-bemenettel és MP3-kimenettel. Sok motor integrációját tartalmazza, köztük a Pipert, Supertonicot és F5-TTS-t. Ez valódi alkalmazásjelölt, de nem igazolja minden kombináció helyes magyar kiejtését. A „1696 nyelv” összesített állítás, nem az összes motor azonos nyelvi képessége. [Projekt és helyi indítás](https://github.com/DrewThomasson/ebook2audiobook)

A kódban a magyar Piper-alapprofil jelenleg Anna; a külön Imre-modell használatához a meglévő egyéni modellbetöltést kell kipróbálni. A férfihang nem állítható késznek pusztán a magyar menüpont alapján. [Piper-presetek](https://github.com/DrewThomasson/ebook2audiobook/blob/main/lib/classes/tts_engines/presets/piper_presets.py), [meglévő Piper-adapter és custom model út](https://github.com/DrewThomasson/ebook2audiobook/blob/main/lib/classes/tts_engines/piper.py)

## Amit nem választanánk bizonyíték nélkül

- A Qwen3-TTS hivatalos 10 nyelve között nincs magyar. A kész Mac-alkalmazásba csomagolás ezt nem változtatja meg. [Kiadói nyelvlista](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice)
- A Chatterbox hivatalosan felsorolt 23 nyelve között sincs magyar; a többnyelvű jelölés nem elegendő ajánlás. [Kiadói modellkártya](https://huggingface.co/ResembleAI/chatterbox)
- Magyar F5-TTS-checkpointok léteznek, de egy jelenlegi modellkártya kifejezetten dokumentál kezdeti torz hangot és időbecslési hibákat, a benchmark pedig NVIDIA-mérés. Ez nem kész, bizonyított M5-ös hosszú narráció. [Magyar F5-TTS modell](https://huggingface.co/Maxdorger29/f5-tts-hungarian)
- A külön VibeVoice Mac-futtatók a saját port helyett vizsgálandó meglévő kódok; általános angol modellbenchmarkjuk nem bizonyítja a Cseti magyar checkpoint helyes hosszú narrációját. Ez külön kompatibilitási vizsgálat marad.

## Javasolt továbblépés

Elsőként az eredeti Supertonic 3-futtató M2/M5 profilja és az eredeti Piper Imre készüljön el ugyanabból a rövid saját magyar szövegből, változtatás és automatikus lejátszás nélkül. Rögzítsük a tényleges futási időt és a teljes megszólalást; a felhasználó a természetességet meghallgatással válassza ki. Csak elfogadott hanggal következzen néhányperces, több szakaszt érintő próba. A hosszú teszt elutasítása után nem állítható helyre a készültség rövid ASR-ellenőrzéssel.

Ha a hang elfogadható, két használható út van: a kész motor megtartása a jelenlegi egyszerű felület alatt, vagy a már kész ebook2audiobook alkalmazás használata az elfogadott modellel. Egyik út sem igényel új beszédgeneráló algoritmus írását. Teljes könyves munkát és új alkalmazásintegrációt csak a tényleges hangpróba után érdemes elindítani.

Vizsgált forrásrevíziók: Piper `0471299744417dae497991f859dd0d3c1daab170`; Supertonic `1e9799e964ea4c0dad7cde993b65c3c813a7b373`; ebook2audiobook `5d40b6d2c27f62c0dcf535b7b13d75e783a02f60`. Az ebook2audiobook alkalmazás nem került helyben telepítésre; az eredeti Piper és Supertonic motor alábbi próbája ettől külön értékelendő.


## Tényleges rövid M5-próba

2026-11-10-én külön környezetben az eredeti Piper 1.8.0 macOS ARM64 csomag és a Supertonic eredeti Python/ONNX-példájának változatlan segédmodulja futott. Nincs saját modellkonverzió, hangklónozás vagy alkalmazásintegráció. A próbaszöveg három saját magyar mondat, 26 szó; ugyanaz a bemenet mindhárom hangnál. Az eredeti tempó maradt, a hang nem indult automatikusan.

| Motor/hang | Kész hang hossza | Mért futási idő a célgépen |
| --- | --- | --- |
| Piper Imre | 12,31 s | 1,06 s, folyamatindítással és modellbetöltéssel együtt |
| Supertonic 3 M2 | 14,72 s | 2,51 s generálás; előtte 0,24 s közös modellbetöltés |
| Supertonic 3 M5 | 15,00 s | 2,45 s generálás, már betöltött modellel |

Mindhárom CPU-n futott. A Supertonic-mérés 8 hangképzési lépést és 1,0× tempót használ. A letöltés és telepítés nincs benne a fenti futási időkben; ezek rövid minták, nem teljes könyves sebességígéretek. A WAV-okból egyszeri, 96 kbit/s mono MP3 készült; a minták nincsenek az alkalmazásba beépítve.

A helyi Whisper-átírás normalizált karakteres eltérése Piper Imre esetén 2,67%, Supertonic M2 esetén 0,67%, M5 esetén 1,33%. Ezekben az egybeírás, szóhatár és mássalhangzó eltérések is szerepelnek. Az átírás nem bizonyítja a természetes prozódiát vagy a hibátlan kiejtést, és nem váltja ki a hosszabb próba meghallgatását. A jelenlegi VibeVoice-hosszúpróba elutasítása éppen azt mutatja, hogy a rövid ASR-eredmény nem elég.

A helyi eredmények a Gitből kizárt `artifacts/existing-engines` könyvtárban vannak: közös `forras.txt`, három WAV/MP3, mérési jegyzék és tartalmi jelentés. A külön környezet és a változatlan hivatalos segédmodul a `.local/alternatives` alatt marad, a használt csomagverziókkal és forrásrevízióval együtt. Piper-hangrepo revízió: `cf910fb59f1d79ab3b625a63993a108751c6c25d`; Supertonic-modellrev: `aafc6e32416a594460b32413efc49d7fe4ce6d46`. A magyar férfihangok meghallgatásos elfogadása még nyitott.

## Egyéb VibeVoice Mac-futtatók

A [gafiatulin/vibevoice-mlx](https://github.com/gafiatulin/vibevoice-mlx) külön Apple Silicon-futtató, saját referenciahang-gyorsítótárral és M4 Maxon közölt mérésekkel. Az [EmZod-fork](https://github.com/EmZod/vibevoice-mlx) gyorsabb indulást és hangprofil-gyorsítótárat ad hozzá. A [mlx-speech](https://github.com/appautomaton/mlx-speech) szintén meglévő, helyi könyvtár. Ezek kódújrahasználati lehetőségek, de a vizsgált forrásokban nem találtunk olyan bizonyítékot, amely a pontos Cseti magyar checkpoint hosszú, stabil férfinarrációját igazolná. Az angol alapmodell másik Macen közölt sebességét nem vetítjük át a magyar M5-feladatra. Ezek nem kerültek telepítésre vagy mérésre.

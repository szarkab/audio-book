# Meglévő helyi magyar felolvasó megoldások

> Történeti feljegyzés: korábbi modellpróbák, mérések vagy fejlesztési ellenőrzések dokumentuma. Az aktuális alkalmazás működését a [specifikáció](specification.md) írja le.

Vizsgálat: 2026-11-10. Célkörnyezet: Apple M5, 32 GB egyesített memória, helyi magyar férfinarráció. A dokumentum forrásvizsgálatot és külön célgépes rövid méréseket tartalmaz.

A VibeVoice hosszú mintáján szaggatás, hangváltás, torzulás és nagy futási idő jelentkezett. A vizsgálat ezért kész helyi motorokra és meglévő alkalmazásokra terjedt ki. A végső motor Piper Imre; az alábbi összehasonlítás a kiválasztás műszaki háttere.

## Rövidlista

| Megoldás | Kész elem | Magyar férfihang és Mac-bizonyíték | Megítélés |
| --- | --- | --- | --- |
| Piper + Imre | Kész helyi motor, Python API/CLI és ONNX-hangmodell | Hivatalos hu_HU Imre-hang; natív macOS ARM64 telepítőcsomag | Helyben mért, végül kiválasztott motor |
| Supertonic 3 | Kész ONNX-futtató, Python- és Swift-példa, férfi presetek | Magyar `hu` hivatalosan szerepel; Swift-példa macOS 13+-ra | Helyben mérhető jelölt; archivált projekt |
| ebook2audiobook | Kész helyi könyvkonvertáló webes felület Mac-indítóval | Piper és más motorok, magyar Piper-preset; az alap magyar hang Anna | Forrásvizsgálat; Imre-integráció helyben nem tesztelt |

## Piper + Imre

Az aktív Piper-projekt az OHF-Voice/piper1-gpl. Gyors helyi motor, beépített espeak-ng fonemizálással, fájlbemenettel, WAV-kimenettel és újrahasználható Python API-val. A PyPI 1.8.0 kiadás macOS 11+ ARM64 wheelje kifejezett telepítési bizonyíték Apple Siliconra. Ez nem saját M5-sebességmérés. [Projekt](https://github.com/OHF-Voice/piper1-gpl), [hivatalos CLI](https://github.com/OHF-Voice/piper1-gpl/blob/main/docs/CLI.md), [PyPI-csomagok](https://pypi.org/project/piper-tts/1.8.0/#files)

A hivatalos hangrepo `hu_HU-imre-medium` modellje körülbelül 63,2 MB, egy beszélővel, 22 050 Hz mintavétellel. A modellkártya Piper 1.5+-t és 0,5 / 0,333 alap zajparamétereket ír; az adathalmaz CC0. A magyar hangprojekt Imrét férfihangként azonosítja. A modellméret és a „medium” kategória önmagában nem minősíti a prozódiát. [Modellkártya](https://huggingface.co/rhasspy/piper-voices/blob/main/hu/hu_HU/imre/medium/MODEL_CARD), [hangfájlok](https://huggingface.co/rhasspy/piper-voices/tree/main/hu/hu_HU/imre/medium), [magyar hangprojekt](https://rhvoice.hu/en/voices/), [hivatalos mintafelület](https://rhasspy.github.io/piper-samples/)

## Supertonic 3

A kiadó 99M-paraméteres ONNX-modellje 31 nyelvet, köztük magyart támogat, helyi futtatással. A modellcsomag előre rögzített hangprofilokat ad; nem szükséges új hangklónozó futtatást írni. A modell OpenRAIL-M, a példakód MIT-licencű. A gyorsaságra és olvasási stabilitásra vonatkozó kiadói állítás nem saját magyar M5-eredmény. [Modellkártya](https://huggingface.co/supertone-oss-archive/supertonic-3)

Öt férfi preset van. Az M2-t mély, nyugodt hangként, az M5-öt meleg, halkabb hangoskönyves narrátorként jellemzik; ezek kiadói hangkarakter-leírások. [Hangprofilok](https://github.com/supertone-oss-archive/supertonic-py/blob/main/docs/voices.md)

A hivatalos Swift-példa macOS 13+-t és Swift 5.9+-t ír elő. Hosszú szöveget belül bont, szünetekkel egyetlen hangfájlba egyesít; dokumentációja szerint a GPU-mód még nem támogatott. A Python-változat ONNX Runtime-motorja szintén kész. A vizsgált Python-futtató CPU-n működik. [Swift-példa](https://github.com/supertone-oss-archive/supertonic/blob/main/swift/README.md), [Python-példa](https://github.com/supertone-oss-archive/supertonic/blob/main/py/README.md)

Fontos karbantartási korlát: a kiadó 2026. szeptember 9-én archiválta a repót, támogatása megszűnt. A fennmaradt forrás és modellek explicit letöltéssel, hosted szolgáltatás nélkül használhatók. A dokumentált modellrevízió `aafc6e32416a594460b32413efc49d7fe4ce6d46`. A mintához az eredeti ONNX-példát és a rögzített archív állományokat kell használni; a régi SDK automatikus letöltése a korábbi névtérre mutathat. [Archívum és helyi indítás](https://github.com/supertone-oss-archive/supertonic#quick-start)

## ebook2audiobook

A DrewThomasson/ebook2audiobook meglévő, helyi Gradio-alkalmazás Mac-indítóval, TXT-bemenettel és MP3-kimenettel. Sok motor integrációját tartalmazza, köztük a Pipert, Supertonicot és F5-TTS-t. Ez valódi alkalmazásjelölt, de nem igazolja minden kombináció helyes magyar kiejtését. A „1696 nyelv” összesített állítás, nem az összes motor azonos nyelvi képessége. [Projekt és helyi indítás](https://github.com/DrewThomasson/ebook2audiobook)

A vizsgált kódban a magyar Piper-alapprofil Anna. Az Imre-hanghoz egyéni modellbetöltés szükséges; ez helyi vizsgálatban nem szerepelt. [Piper-presetek](https://github.com/DrewThomasson/ebook2audiobook/blob/main/lib/classes/tts_engines/presets/piper_presets.py), [meglévő Piper-adapter és custom model út](https://github.com/DrewThomasson/ebook2audiobook/blob/main/lib/classes/tts_engines/piper.py)

## További jelöltek korlátai

- A Qwen3-TTS hivatalos 10 nyelve között nincs magyar. A kész Mac-alkalmazásba csomagolás ezt nem változtatja meg. [Kiadói nyelvlista](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice)
- A Chatterbox hivatalosan felsorolt 23 nyelve között sincs magyar; a többnyelvű jelölés nem elegendő ajánlás. [Kiadói modellkártya](https://huggingface.co/ResembleAI/chatterbox)
- Magyar F5-TTS-checkpointok léteznek, de egy jelenlegi modellkártya kifejezetten dokumentál kezdeti torz hangot és időbecslési hibákat, a benchmark pedig NVIDIA-mérés. Ez nem kész, bizonyított M5-ös hosszú narráció. [Magyar F5-TTS modell](https://huggingface.co/Maxdorger29/f5-tts-hungarian)
- A külön VibeVoice Mac-futtatók angol modellbenchmarkjai nem igazolják a Cseti magyar checkpoint kompatibilitását vagy hosszú narrációjának minőségét.

## Vizsgálati módszer

A rövid összehasonlítás az eredeti Piper Imre és Supertonic 3 M2/M5 motorokat használta, közös magyar szöveggel és natív tempóval. A kimenetek egyszeri MP3-kódolással készültek. A futási idő és az ASR mellett a meghallgatás adta a minőségi összehasonlítás alapját. Az ebook2audiobook csak forrásvizsgálatban szerepelt, helyi telepítés nélkül.

Vizsgált forrásrevíziók: Piper `0471299744417dae497991f859dd0d3c1daab170`; Supertonic `1e9799e964ea4c0dad7cde993b65c3c813a7b373`; ebook2audiobook `5d40b6d2c27f62c0dcf535b7b13d75e783a02f60`. Az ebook2audiobook forrásvizsgálata és a Piper/Supertonic célgépes mérése külön eredmény.


## Tényleges rövid M5-próba

2026-11-10-én külön környezetben az eredeti Piper 1.8.0 macOS ARM64 csomag és a Supertonic eredeti Python/ONNX-példájának változatlan segédmodulja futott. Nincs saját modellkonverzió, hangklónozás vagy alkalmazásintegráció. A próbaszöveg három saját magyar mondat, 26 szó; ugyanaz a bemenet mindhárom hangnál. Az eredeti tempó maradt, a hang nem indult automatikusan.

| Motor/hang | Kész hang hossza | Mért futási idő a célgépen |
| --- | --- | --- |
| Piper Imre | 12,31 s | 1,06 s, folyamatindítással és modellbetöltéssel együtt |
| Supertonic 3 M2 | 14,72 s | 2,51 s generálás; előtte 0,24 s közös modellbetöltés |
| Supertonic 3 M5 | 15,00 s | 2,45 s generálás, már betöltött modellel |

Mindhárom CPU-n futott. A Supertonic-mérés 8 hangképzési lépést és 1,0× tempót használ. A letöltés és telepítés nincs benne a fenti futási időkben; ezek rövid minták, nem teljes könyves sebességígéretek. A WAV-okból egyszeri, 96 kbit/s mono MP3 készült; a minták nincsenek az alkalmazásba beépítve.

A helyi Whisper-átírás normalizált karakteres eltérése Piper Imre esetén 2,67%, Supertonic M2 esetén 0,67%, M5 esetén 1,33%. Ezekben az egybeírás, szóhatár és mássalhangzó eltérések is szerepelnek. Az átírás nem bizonyítja a természetes prozódiát vagy a hibátlan kiejtést, és nem váltja ki a hosszabb próba meghallgatását. A VibeVoice hosszú mintájának minőségi hibáit a rövid ASR-próba nem jelezte előre.

Piper-hangrepo revízió: `cf910fb59f1d79ab3b625a63993a108751c6c25d`; Supertonic-modellrevízió: `aafc6e32416a594460b32413efc49d7fe4ce6d46`. A meghallgatásban a Piper Imre adta a kedvezőbb eredményt. A Supertonic M2 és M5 az „eleredt” szó végén kiejtési hibát mutatott. A külön próbakörnyezetek, alternatív modellek és generált minták nem részei az aktív projektnek.

## Egyéb VibeVoice Mac-futtatók

A [gafiatulin/vibevoice-mlx](https://github.com/gafiatulin/vibevoice-mlx) külön Apple Silicon-futtató, saját referenciahang-gyorsítótárral és M4 Maxon közölt mérésekkel. Az [EmZod-fork](https://github.com/EmZod/vibevoice-mlx) gyorsabb indulást és hangprofil-gyorsítótárat ad hozzá. A [mlx-speech](https://github.com/appautomaton/mlx-speech) szintén meglévő, helyi könyvtár. A vizsgált források nem igazolták a pontos Cseti magyar checkpoint hosszú, stabil férfinarrációját. A másik Macen, angol alapmodellel mért sebesség nem magyar M5-eredmény. Ezek a futtatók csak forrásvizsgálatban szerepeltek, helyi telepítés és mérés nélkül.

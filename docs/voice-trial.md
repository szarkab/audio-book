# Helyi magyar hangpróba

A specifikáció: https://github.com/szarkab/audio-book/issues/1

Ez elkülönített minőségi és teljesítménypróba, nem az alkalmazás kész backendje. A modell, a futtatókörnyezet és a helyben generált hanganyag nem kerül Gitbe.

## Reprodukálás

Apple Silicon Mac, Python 3.12, uv és FFmpeg szükséges a fejlesztői próbához. A végleges alkalmazás használatának ezek nem felhasználói előfeltételei.

1. Hozz létre `.venv` környezetet: `uv venv --python 3.12 .venv`.
2. Telepítsd a próba függőségeit: `uv pip install --python .venv/bin/python -r requirements-trial.lock`. A `requirements-trial.txt` a közvetlen függőséget, a lock fájl az első próba teljes csomaglistáját rögzíti.
3. A Hugging Face `snapshot_download` függvényével töltsd le a `mlx-community/OmniVoice-bfloat16` modellt a `6119f7072580cc30c3cbdf496269216b03ad9742` revízióból a `.local/models/OmniVoice-bfloat16` mappába.
4. Futtasd: `.venv/bin/python scripts/voice_trial.py`. A script a Hugging Face és Transformers offline módját állítja be, és a helyi modellből generál Metal GPU-n.
5. Hallgasd meg az `artifacts/voice-trial` könyvtár férfi és női MP3-mintáit. A WAV az összehasonlításhoz megmarad. Azonos hangból 64 és 96 kbit/s MP3 készül; ezek még nem elfogadott végleges exportbeállítások.

Az első futás mérési eredményei és ellenőrzései: [eredményjelentés](voice-trial-results.md).

A mentés a túl magas nyers csúcsokat szükség szerint egyenletes hangerőcsökkentéssel 0,95-re korlátozza; a nyers csúcs és az alkalmazott szorzó a JSON-ban megmarad.

## A próba korlátai

A hangok referenciafelvétel nélküli, leírásból generált hangjelöltek, nem előre bizonyított magyar narrátorhangok. A modell dokumentációja szerint a hangtervezés főként angol és kínai adatokra épül; magyarul a stabilitását ellenőrizni kell. A rögzített célidő a próba paramétere, nem a végleges alkalmazás hosszkezelése. Túl rövid célidő beszédhibát vagy kihagyást okozhat; ezt meghallgatással kell kiszűrni.

A JSON-jelentés a pontos szöveget, hangutasítást, véletlenmagot, modellrevíziót, csomagverziókat, tényleges futási időt, MLX-memóriát és fájlméreteket tartalmazza. A nem üres hullámforma nem bizonyítja a természetességet vagy a szöveghűséget. A hangot a felhasználó fogadja el.

## Elsődleges források és licenc

- Hivatalos modell és Apple Silicon útmutató: https://github.com/k2-fsa/OmniVoice
- A hivatalos modellkártya szerint a kód Apache-2.0, az előtanított modell CC-BY-NC: https://huggingface.co/k2-fsa/OmniVoice
- MLX-Audio OmniVoice-integráció: https://github.com/Blaizzy/mlx-audio/tree/main/mlx_audio/tts/models/omnivoice
- Ajánlott MLX-változat, teljes hangdekódolóval, körülbelül 2,04 GB: https://huggingface.co/mlx-community/OmniVoice-bfloat16

A közösségi átalakítás modellkártyájának Apache-2.0 metaadata nem írja felül az eredeti modellsúlyok nem kereskedelmi feltételét. A mostani próba a megadott saját használati célra készül.

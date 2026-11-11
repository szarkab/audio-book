# OmniVoice hangpróba — módszertan

> Archív műszaki dokumentum, 2026-11-10–11. A jelenlegi működés leírása a [specifikációban](specification.md) található.

## Vizsgálati környezet

Az elkülönített hangpróba Apple Silicon Macen, Python 3.12, MLX Metal GPU és FFmpeg használatával vizsgálta az `mlx-community/OmniVoice-bfloat16` modellt. A rögzített modellrevízió `6119f7072580cc30c3cbdf496269216b03ad9742`.

A modell előzetes helyi letöltés után, a Hugging Face és Transformers offline módjában futott. A férfi és női jelöltek referenciafelvétel nélküli, leírásból generált hangok voltak. Azonos hullámformából 64 és 96 kbit/s MP3-export készült. A nyers csúcsamplitúdó szükség esetén egyenletes hangerőcsökkentéssel legfeljebb 0,95-re korlátozódott.

A mérési jelentés szöveget, hangutasítást, véletlenmagot, modellrevíziót, csomagverziókat, futási időt, MLX-memóriát és fájlméreteket rögzített. Az eredmények a [mérési összefoglalóban](voice-trial-results.md) találhatók.

## Korlátok

A hangtervezés dokumentáltan főként angol és kínai adatokra épült. A magyar hangállandóságot és kiejtést a nem üres hullámforma nem igazolja. A rögzített célidő túl rövid értéke kihagyást vagy beszédhibát okozhat. A rövid minta nem teljes könyves stabilitásmérés.

A kísérleti futtató, a lock fájl, a modellsúlyok és a generált hangok nem részei a jelenlegi projektnek. A módszer történeti dokumentáció; az aktív modell Piper Imre.

## Források és licenc

- [OmniVoice projekt](https://github.com/k2-fsa/OmniVoice)
- [Eredeti modellkártya](https://huggingface.co/k2-fsa/OmniVoice): Apache-2.0 kód, CC-BY-NC modellsúlyok.
- [MLX-Audio integráció](https://github.com/Blaizzy/mlx-audio/tree/main/mlx_audio/tts/models/omnivoice)
- [MLX-változat](https://huggingface.co/mlx-community/OmniVoice-bfloat16), teljes hangdekódolóval körülbelül 2,04 GB.

A közösségi átalakítás Apache-2.0 metaadata nem írja felül az eredeti modellsúlyok nem kereskedelmi feltételét.

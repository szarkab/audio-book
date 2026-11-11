# VibeVoice magyar modell — architektúra és Mac-kompatibilitás

> Archív forrásvizsgálat, 2026-11-10. A későbbi célgépes eredményeket a [VibeVoice mérési jelentés](implementation-issue-10.md) tartalmazza. A jelenlegi alkalmazás Piper Imrét használ.

## Modell

A `Cseti/VibeVoice_7B_hun_v2` magyarra finomhangolt nyelvi modult és diffúziós fejet tartalmaz. Vizsgált revízió: `22434d6f261e2f231b3c358563bdf2d2e8caab57`. [Modellkártya](https://huggingface.co/Cseti/VibeVoice_7B_hun_v2).

A 7B megjelölés a nyelvi modulosztályra utal. A teljes csomag 9 343 355 361 F32-paraméter, nyolc súlyfájlban körülbelül 37,37 GB. A Qwen2 dekóder 3584-es rejtett méretet, 28 réteget, 28 figyelemfejet, 4 KV-fejet és 32768-as kontextust használ. A diffúziós fej 3584 méretű, négy réteggel és 64-es latens mérettel. [Metaadat](https://huggingface.co/api/models/Cseti/VibeVoice_7B_hun_v2?blobs=true), [rögzített konfiguráció](https://huggingface.co/Cseti/VibeVoice_7B_hun_v2/blob/22434d6f261e2f231b3c358563bdf2d2e8caab57/config.json).

A 32 GB egyesített memóriájú M5 gépen a teljes F32-súlyhalmaz önmagában meghaladja a fizikai memóriát. Az FP16-paraméterek elméleti mérete körülbelül 18,69 GB; az aktivációk, a gyorsítótárak és az operációs rendszer ezen felül igényelnek memóriát. A kvantált futtatás nem csökkenti az eredeti checkpoint letöltési méretét.

## Mac-futtatók

A közösségi eredeti futtató Apple gépen MPS-t, FP16-ot és SDPA figyelmet választ, `model.to("mps")` használatával. A modellkártya CUDA-példája ezért nem kizárólagos NVIDIA-követelmény. [MPS-futtató](https://github.com/vibevoice-community/VibeVoice/blob/main/demo/inference_from_file.py).

Az MLX Audio 0.6.5 nem streaming VibeVoice-modult tartalmaz Qwen2 dekóderrel, diffúziós fejjel, akusztikus és szemantikus tokenizálóval, valamint referenciahang-bemenettel. A magyar konfiguráció helyi feldolgozása sikeres volt: 3584-es dekóder, 28 réteg, 3584-es diffúziós fej és 24 kHz. A konfiguráció betölthetősége önmagában nem bizonyít hibátlan súlykonverziót vagy hangminőséget. [MLX-modell](https://github.com/Blaizzy/mlx-audio/blob/main/mlx_audio/tts/models/vibevoice/vibevoice.py), [konfiguráció](https://github.com/Blaizzy/mlx-audio/blob/main/mlx_audio/tts/models/vibevoice/config.py).

## Konverziós feltételek

A teljes magyar checkpoint nyelvi súlyai, diffúziós feje és mindkét kodekága szükséges. A modell nem egy angol 1,5B-változathoz adható magyar LoRA. A hiányzó tokenizer- és processor-fájlokhoz megfelelő, rögzített alapmodellverzió párosítása szükséges; offline futtatáskor minden állománynak helyben kell lennie. [Konverter](https://github.com/Blaizzy/mlx-audio/blob/main/mlx_audio/convert.py), [fájllista](https://huggingface.co/Cseti/VibeVoice_7B_hun_v2/tree/main).

A 7B alapmodell közzétett kerete 32K kontextus és körülbelül 45 perc. Ez névleges alapmodell-adat, nem magyar M5-mérés. A 4 bites minták és a kvantálás nélküli változatra vonatkozó szerzői minőségi állítás sem célgépes összehasonlítás. [Képességtábla](https://github.com/vibevoice-community/VibeVoice#model-zoo).

A későbbi helyi vizsgálat rövid szövegen működő generálást, hosszú szövegen azonban erős hangtorzulást és nagy futási időt mutatott. Részletek: [mérési jelentés](implementation-issue-10.md).

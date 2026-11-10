# Cseti VibeVoice magyar modell — előzetes Mac-értékelés

Dátum: 2026-11-10. Ez forráskód- és metaadatvizsgálat, nem helyi hangminőségi vagy teljesítményteszt. A működő alkalmazás modellje nem változott; nagy modellsúlyt nem töltöttünk le.

## Döntési javaslat

Érdemes külön helyi próbát készíteni, de még nem állítható, hogy jobb a jelenlegi OmniVoice-nál. A modell szerzője magyarra finomhangolt LLM-et és diffúziós fejet egyesített az alapmodellbe. Ez célzott magyar fejlesztés, nem puszta általános többnyelvű képesség. A minták 4 bites futtatással készültek; a szerző a kvantálás nélküli változatot jobbnak tartja, de ez nem összehasonlító M5-mérés. [Szerzői modellkártya](https://huggingface.co/Cseti/VibeVoice_7B_hun_v2)

## Pontos modell és memória

A vizsgált revízió `22434d6f261e2f231b3c358563bdf2d2e8caab57`. A névben szereplő 7B az LLM-osztályra utal; a teljes csomag 9 343 355 361 F32-paraméter, nyolc súlyfájlban körülbelül 37,37 GB. Qwen2 dekóder: 3584 rejtett méret, 28 réteg, 28 figyelemfej, 4 KV-fej, 32768 kontextus. A diffúziós fej is 3584 méretű, négy réteggel és 64-es latens mérettel. [HF-metaadat](https://huggingface.co/api/models/Cseti/VibeVoice_7B_hun_v2?blobs=true), [rögzített konfiguráció](https://huggingface.co/Cseti/VibeVoice_7B_hun_v2/blob/22434d6f261e2f231b3c358563bdf2d2e8caab57/config.json)

A célgép helyi leltára M5 és 32 GB egyesített memória. Következtetés: a teljes F32-súlyhalmaz már önmagában nagyobb a fizikai memóriánál. FP16-ban a paraméterek elméleti mérete körülbelül 18,69 GB; ez nem a teljes futási igény, a gyorsítótárak, aktivációk és a rendszer további memóriát használnak. A sebesség és a hosszabb szöveg memóriabiztonsága mérés nélkül ismeretlen.

## Mac-futtatási lehetőségek

A modellkártya CUDA-példája nem jelent kizárólag NVIDIA-támogatást. A közösségi eredeti futtató már kifejezetten választ MPS-t Apple gépen: automatikus FP16, SDPA figyelem, FlashAttention helyett, `model.to("mps")`. Ez konkrét helyi út, de a Cseti-változat ezen a gépen még nem futott. [MPS-t kezelő futtató](https://github.com/vibevoice-community/VibeVoice/blob/main/demo/inference_from_file.py)

Az upstream MLX Audio jelenlegi kódjában nem streaming VibeVoice is van, parametrizált Qwen2- és diffúziós fejjel, akusztikus/szemantikus tokenizálóval és referenciahang-bemenettel. Ez a 7B architektúrához ígéretes, nem bizonyíték a pontos Cseti-checkpoint hibátlan konverziójára. A projekt telepített `mlx-audio==0.6.5` verziójában is van VibeVoice TTS-modul. A pontos Cseti-konfiguráció helyi, súlyletöltés nélküli feldolgozása sikeres: nem streaming VibeVoice, 3584-es dekóder, 28 réteg, 3584-es diffúziós fej és 24 kHz. Ez konfigurációs kompatibilitást igazol, nem végrehajtási vagy hangminőségi próbát. [MLX modell](https://github.com/Blaizzy/mlx-audio/blob/main/mlx_audio/tts/models/vibevoice/vibevoice.py), [konfiguráció](https://github.com/Blaizzy/mlx-audio/blob/main/mlx_audio/tts/models/vibevoice/config.py)

A konverter a teljes modell súlyait tölti, és általános kvantálási predikátumot használhat; a magyarra teljesen finomhangolt diffúziós fejet és mindkét kodekágat is meg kell őrizni. Nem elegendő egy angol 1,5B-s modellt magyar LoRA-ként kezelni. A tokenizer/processor fájlok nincsenek a Cseti-repó felsorolásában: ezeket a megfelelő alapmodellből, rögzített változatból kell párosítani; offline próbához előre helyben kell lenniük. [Konverter](https://github.com/Blaizzy/mlx-audio/blob/main/mlx_audio/convert.py), [fájllista](https://huggingface.co/Cseti/VibeVoice_7B_hun_v2/tree/main)

## Narrátor és hosszú hanganyag

A 7B alapmodell közzétett névleges kerete 32K kontextus és körülbelül 45 perc, nem a 1,5B-hez megadott 90 perc. Ezek nem igazolt magyar M5-határok. A referenciahangos generálás alapján a saját, tiszta férfi WAV technikailag kipróbálható; ugyanazon hang pontos megőrzése még nem igazolt. [Közösségi modell- és képességtábla](https://github.com/vibevoice-community/VibeVoice#model-zoo)

## Külön próba menete

1. Külön környezet és könyvtár, a működő OmniVoice-alkalmazás módosítása nélkül; pontos forrásrevíziók rögzítése.
2. A teljes Cseti-checkpointot megőrző Mac-futtatási út kiválasztása. A 37 GB-os beszerzés és konverziós munkaterület külön kapacitásigény; a kvantálás nem jelenti, hogy az eredeti letöltés is kicsi.
3. Ugyanaz a férfi referencia és két rövid saját magyar szöveg, sorszámokkal is. Automatikus lejátszás nélkül, a modellek natív tempójával, azonos kimeneti szinttel összehasonlítva.
4. Csak jobb rövid próba után többperces szöveg: tartalom, ismétlések, hangállandóság, csúcsmemória és futási idő mérése. A modellváltás alapja a felhasználó meghallgatása legyen, ne a paraméterszám.

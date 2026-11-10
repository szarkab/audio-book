# Teljes mondatokkal és átirattal párosított férfi hangreferencia

A WAV a felhasználó által elfogadott szintetikus férfiminta teljes első két mondata, 8,07 másodperc. A mellette lévő JSON a pontos elhangzott szöveget és ellenőrzőösszeget tartalmazza. Az alkalmazás az audio-tokeneket és a hozzájuk tartozó pontos referencia-átiratot együtt adja a modellnek. Nem vágja le automatikusan a referenciát, és nem távolít el belőle szüneteket.

Ez eltér a korábbi, elutasított, tíz másodpercnél mondat közben levágott és átirat nélkül használt kísérlettől. A profil három különböző, kétmondatos szövegen helyi tartalmi és összehasonlító beszélőhang-ellenőrzést kapott. A modell azonos hangutasítása és véletlenmagja önmagában nem tekintendő beszélőazonossági garanciának.

A referencia nem valós személy felvételéből készült. Saját, nem kereskedelmi használatra szolgál, az OmniVoice modellsúlyok CC-BY-NC feltételeivel. Modell: https://huggingface.co/k2-fsa/OmniVoice

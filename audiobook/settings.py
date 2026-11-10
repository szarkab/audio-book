"""Immutable narration choices captured for one complete MP3 job."""
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class NarrationSettings:
    length_scale: float = 1.0
    noise_scale: float = 0.5
    noise_w_scale: float = 0.333
    volume: float = 1.0
    normalize_audio: bool = True
    sentence_silence: float = 0.0

    def validate(self) -> None:
        bounds = [
            ("Beszédhossz", self.length_scale, 0.5, 2.0),
            ("Hangváltozatosság", self.noise_scale, 0.0, 1.0),
            ("Ritmusváltozatosság", self.noise_w_scale, 0.0, 1.0),
            ("Kimeneti hangerő", self.volume, 0.1, 2.0),
            ("Mondatszünet", self.sentence_silence, 0.0, 1.5),
        ]
        for name, value, minimum, maximum in bounds:
            if not math.isfinite(value) or not minimum <= value <= maximum:
                raise ValueError(f"{name}: {minimum} és {maximum} közötti érték szükséges.")
        if not isinstance(self.normalize_audio, bool):
            raise ValueError("A hangerő-normalizálás beállítása be vagy ki lehet.")

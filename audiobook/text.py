"""Lossless, sentence-aligned inputs for the speech model."""
from collections.abc import Iterator
import re


_ABBREVIATIONS = {
    "dr", "prof", "ifj", "id", "pl", "stb", "kb", "ún", "ill", "vö", "sz", "krt", "kft",
    "jan", "febr", "márc", "ápr", "jún", "júl", "aug", "szept", "okt", "nov", "dec",
}
_BOUNDARY = re.compile(r'[.!?…]+[”»"\')\]]*(?:\s+|$)|\n[ \t]*\n+')


def _sentence_end(text: str, boundary: re.Match[str]) -> bool:
    punctuation = boundary.group()
    following = text[boundary.end():boundary.end() + 8]
    if any(quote in punctuation for quote in '”»"') and re.match(r"[–—-]\s", following):
        return False  # Keep dialogue and its reporting clause together.
    if punctuation.startswith(".") and not punctuation.startswith(".."):
        if following and following[0].islower():
            return False  # A lowercase continuation is not a new prose sentence.
        before = text[max(0, boundary.start() - 32):boundary.start()]
        token = re.search(r"(\w+)$", before)
        if token:
            word = token.group()
            if word.casefold() in _ABBREVIATIONS:
                return False
            if word.isdecimal() and following[:1].isdecimal():
                return False  # Numeric date components continue the same sentence.
            if len(word) == 1 and word.isalpha():
                return False
            if re.fullmatch(r"[IVXLCDM]+", word):
                return False
    return True


def speech_parts(text: str) -> Iterator[str]:
    start = 0
    current = ""
    sentences = 0
    for boundary in _BOUNDARY.finditer(text):
        if not _sentence_end(text, boundary):
            continue
        sentence = text[start:boundary.end()]
        if current and (sentences >= 2 or len(current) + len(sentence) > 400):
            yield current
            current = ""
            sentences = 0
        current += sentence
        sentences += 1
        start = boundary.end()
    tail = text[start:]
    if current and tail and (sentences >= 2 or len(current) + len(tail) > 400):
        yield current
        current = ""
    if current or tail:
        yield current + tail


# Restrict expansion to unmistakable ordinal phrases, not arbitrary dotted numbers.
_ORDINAL_PHRASE = re.compile(
    r"(?<![\w.,:/+−-])([1-9][0-9]{0,2})\.([ \t]+)"
    r"(?=(?:fejezet|próba|versenyző|hely|alkalom|emelet|kötet|oldal|pont|rész|lépés)\b)",
    re.IGNORECASE,
)
_ORDINAL_UNITS = ("", "egyedik", "kettedik", "harmadik", "negyedik", "ötödik",
                  "hatodik", "hetedik", "nyolcadik", "kilencedik")
_ORDINAL_TENS = {10: "tizedik", 20: "huszadik", 30: "harmincadik", 40: "negyvenedik",
                 50: "ötvenedik", 60: "hatvanadik", 70: "hetvenedik", 80: "nyolcvanadik",
                 90: "kilencvenedik", 100: "századik"}
_TENS_PREFIX = {1: "tizen", 2: "huszon", 3: "harminc", 4: "negyven", 5: "ötven",
                6: "hatvan", 7: "hetven", 8: "nyolcvan", 9: "kilencven"}


def prepare_narration(text: str) -> str:
    """Expand only 1–100 before a documented ordinal noun; preserve other text."""
    def expand(match: re.Match[str]) -> str:
        number = int(match[1])
        if number > 100 or re.search(r"\d\.[ \t]+$", text[:match.start()]):
            return match[0]
        if number == 1:
            word = "első"
        elif number == 2:
            word = "második"
        elif number in _ORDINAL_TENS:
            word = _ORDINAL_TENS[number]
        else:
            tens, unit = divmod(number, 10)
            word = (_TENS_PREFIX[tens] if tens else "") + _ORDINAL_UNITS[unit]
        return word + match[2]
    return _ORDINAL_PHRASE.sub(expand, text)

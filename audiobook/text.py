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
            if word.casefold() in _ABBREVIATIONS or word.isdecimal():
                return False
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

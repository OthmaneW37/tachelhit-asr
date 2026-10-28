"""Text normalisation used before computing metrics."""

import re
import unicodedata

_ARABIC_DIACRITICS = re.compile(r"[ً-ْٰـ]")  # harakat, dagger alef, tatweel
_PUNCT = re.compile(r"[^\w\s]", re.UNICODE)
_SPACES = re.compile(r"\s+")


def normalize_arabic(text: str) -> str:
    """Normalise Arabic text so metrics ignore spelling variants that carry no meaning."""
    text = unicodedata.normalize("NFKC", text)
    text = _ARABIC_DIACRITICS.sub("", text)
    text = re.sub("[إأآٱ]", "ا", text)
    text = text.replace("ى", "ي").replace("ة", "ه").replace("ؤ", "و").replace("ئ", "ي")
    text = text.replace("؟", " ").replace("،", " ").replace("؛", " ")
    text = _PUNCT.sub(" ", text)
    return _SPACES.sub(" ", text).strip()


def normalize_latin_transcript(text: str) -> str:
    """Normalise IRCAM-Latin Tachelhit transcripts (keeps special letters like ɣ, ḍ, ɛ)."""
    text = unicodedata.normalize("NFC", text.lower())
    text = text.replace("-", " ")
    text = _PUNCT.sub(" ", text)
    return _SPACES.sub(" ", text).strip()


NORMALIZERS = {
    "arabic": normalize_arabic,
    "latin": normalize_latin_transcript,
}

"""Latin (IRCAM convention) -> Neo-Tifinagh transliteration.

Transcriptions are written in the IRCAM Latin alphabet (easier to type and learn);
Tifinagh is derived from it deterministically, so a model only needs to learn one script.
"""

# Ordered so that multi-character sequences (labialised consonants) match first.
_LATIN_TO_TIFINAGH: list[tuple[str, str]] = [
    ("gʷ", "ⴳⵯ"), ("kʷ", "ⴽⵯ"), ("ɣʷ", "ⵖⵯ"), ("xʷ", "ⵅⵯ"), ("qʷ", "ⵇⵯ"),
    ("a", "ⴰ"), ("b", "ⴱ"), ("g", "ⴳ"), ("d", "ⴷ"), ("ḍ", "ⴹ"), ("e", "ⴻ"),
    ("f", "ⴼ"), ("k", "ⴽ"), ("h", "ⵀ"), ("ḥ", "ⵃ"), ("ɛ", "ⵄ"), ("x", "ⵅ"),
    ("q", "ⵇ"), ("i", "ⵉ"), ("j", "ⵊ"), ("l", "ⵍ"), ("m", "ⵎ"), ("n", "ⵏ"),
    ("u", "ⵓ"), ("r", "ⵔ"), ("ṛ", "ⵕ"), ("ɣ", "ⵖ"), ("s", "ⵙ"), ("ṣ", "ⵚ"),
    ("c", "ⵛ"), ("t", "ⵜ"), ("ṭ", "ⵟ"), ("w", "ⵡ"), ("y", "ⵢ"), ("z", "ⵣ"),
    ("ẓ", "ⵥ"), ("ʷ", "ⵯ"),
]

# Common ASCII-friendly spellings people type instead of the IRCAM letters.
_ASCII_FALLBACKS = {"gh": "ɣ", "ch": "c", "3": "ɛ", "ε": "ɛ", "γ": "ɣ"}


def normalize_latin(text: str) -> str:
    """Lowercase and map common informal spellings to IRCAM letters."""
    text = text.lower()
    for src, dst in _ASCII_FALLBACKS.items():
        text = text.replace(src, dst)
    return text


def latin_to_tifinagh(text: str) -> str:
    """Transliterate IRCAM Latin text to Neo-Tifinagh. Unknown characters pass through."""
    text = normalize_latin(text)
    out: list[str] = []
    i = 0
    while i < len(text):
        for latin, tifinagh in _LATIN_TO_TIFINAGH:
            if text.startswith(latin, i):
                out.append(tifinagh)
                i += len(latin)
                break
        else:
            out.append(text[i])
            i += 1
    return "".join(out)

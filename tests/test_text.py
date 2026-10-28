from tachelhit_asr.metrics import score
from tachelhit_asr.text import normalize_arabic, normalize_latin_transcript
from tachelhit_asr.tifinagh import latin_to_tifinagh


def test_tifinagh_basic_word():
    assert latin_to_tifinagh("azul") == "ⴰⵣⵓⵍ"


def test_tifinagh_emphatics_and_labialised():
    assert latin_to_tifinagh("aḍaṛ") == "ⴰⴹⴰⵕ"
    assert latin_to_tifinagh("agʷmar") == "ⴰⴳⵯⵎⴰⵔ"


def test_tifinagh_ascii_fallbacks():
    # "gh" -> ɣ, "3" -> ɛ
    assert latin_to_tifinagh("tighrmt") == latin_to_tifinagh("tiɣrmt")
    assert latin_to_tifinagh("3li") == "ⵄⵍⵉ"


def test_normalize_arabic_removes_diacritics_and_variants():
    assert normalize_arabic("أَهْلاً، يا رقية؟") == "اهلا يا رقيه"


def test_normalize_latin_keeps_special_letters():
    assert normalize_latin_transcript("Ad-iɣ, ḍaṛ!") == "ad iɣ ḍaṛ"


def test_score_perfect_match():
    m = score(["اهلا بك"], ["أهلاً بك"])
    assert m["wer"] == 0 and m["cer"] == 0 and m["n"] == 1

"""WER / CER / chrF on normalised text."""

import jiwer
import sacrebleu

from .text import NORMALIZERS


def score(predictions: list[str], references: list[str], normalizer: str = "arabic") -> dict:
    norm = NORMALIZERS[normalizer]
    preds = [norm(p) for p in predictions]
    refs = [norm(r) for r in references]
    # jiwer rejects empty references; keep pairs with a non-empty reference only.
    pairs = [(p, r) for p, r in zip(preds, refs) if r]
    preds, refs = [p for p, _ in pairs], [r for _, r in pairs]
    return {
        "wer": 100 * jiwer.wer(refs, preds),
        "cer": 100 * jiwer.cer(refs, preds),
        # chrF suits the speech-translation setting, where many wordings are valid.
        "chrf": sacrebleu.corpus_chrf(preds, [refs]).score,
        "n": len(refs),
    }

"""Evaluate a Whisper checkpoint (local folder or Hub id) on Tachelhit test sets.

Usage:
    python -m tachelhit_asr.evaluate --model openai/whisper-small --sources dahimi tutlait_souss
"""

import argparse
import json
from pathlib import Path

import torch
from transformers import WhisperForConditionalGeneration, WhisperProcessor

from .data import SAMPLING_RATE, decode_audio, load_source
from .metrics import score


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--sources", nargs="+", default=["dahimi", "tutlait_souss"])
    parser.add_argument("--split", default="test")
    parser.add_argument("--language", default="arabic")
    parser.add_argument("--task", default="transcribe")
    parser.add_argument("--normalizer", default="arabic")
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--max-samples", type=int)
    parser.add_argument("--out", default="outputs/eval")
    args = parser.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"  # ROCm builds also report "cuda"
    dtype = torch.bfloat16 if device == "cuda" else torch.float32
    processor = WhisperProcessor.from_pretrained(args.model)
    model = WhisperForConditionalGeneration.from_pretrained(args.model, torch_dtype=dtype).to(device)
    model.eval()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    results = {}
    for name in args.sources:
        ds = load_source(name, args.split, args.max_samples)
        preds, refs = [], []
        for start in range(0, len(ds), args.batch_size):
            batch = ds[start : start + args.batch_size]
            arrays = [decode_audio(a) for a in batch["audio"]]
            feats = processor.feature_extractor(
                arrays, sampling_rate=SAMPLING_RATE, return_tensors="pt"
            ).input_features.to(device, dtype)
            with torch.inference_mode():
                ids = model.generate(feats, language=args.language, task=args.task, max_new_tokens=225)
            preds += processor.batch_decode(ids, skip_special_tokens=True)
            refs += batch["text"]
        results[name] = score(preds, refs, args.normalizer)
        print(name, results[name])
        with open(out_dir / f"{name}_predictions.jsonl", "w", encoding="utf-8") as f:
            f.writelines(
                json.dumps({"prediction": p, "reference": r}, ensure_ascii=False) + "\n"
                for p, r in zip(preds, refs)
            )

    with open(out_dir / "metrics.json", "w", encoding="utf-8") as f:
        json.dump({"model": args.model, "split": args.split, "results": results}, f, indent=2)


if __name__ == "__main__":
    main()

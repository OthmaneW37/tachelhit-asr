"""Fine-tune Whisper on Tachelhit speech.

Usage:
    python -m tachelhit_asr.train --config configs/whisper-small-shi2ar.yaml
"""

import argparse
from dataclasses import dataclass
from typing import Any

import torch
import yaml
from transformers import (
    Seq2SeqTrainer,
    Seq2SeqTrainingArguments,
    WhisperForConditionalGeneration,
    WhisperProcessor,
)

from .data import SAMPLING_RATE, decode_audio, load_mixture
from .metrics import score

MAX_LABEL_TOKENS = 448  # Whisper decoder context
MAX_AUDIO_SECONDS = 30.0  # Whisper encoder window


@dataclass
class SpeechSeq2SeqCollator:
    processor: Any
    decoder_start_token_id: int

    def __call__(self, features: list[dict]) -> dict[str, torch.Tensor]:
        batch = self.processor.feature_extractor.pad(
            [{"input_features": f["input_features"]} for f in features], return_tensors="pt"
        )
        labels_batch = self.processor.tokenizer.pad(
            [{"input_ids": f["labels"]} for f in features], return_tensors="pt"
        )
        labels = labels_batch["input_ids"].masked_fill(labels_batch.attention_mask.ne(1), -100)
        # The model prepends the start token itself during training.
        if (labels[:, 0] == self.decoder_start_token_id).all():
            labels = labels[:, 1:]
        batch["labels"] = labels
        return batch


def prepare_dataset(ds, processor, num_proc: int | None):
    def prepare(example):
        array = decode_audio(example["audio"])
        example["input_features"] = processor.feature_extractor(
            array, sampling_rate=SAMPLING_RATE
        ).input_features[0]
        example["duration"] = len(array) / SAMPLING_RATE
        example["labels"] = processor.tokenizer(example["text"]).input_ids
        return example

    ds = ds.map(prepare, remove_columns=ds.column_names, num_proc=num_proc)
    return ds.filter(
        lambda d, labels: 0 < d <= MAX_AUDIO_SECONDS and len(labels) < MAX_LABEL_TOKENS,
        input_columns=["duration", "labels"],
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    with open(args.config, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    processor = WhisperProcessor.from_pretrained(
        cfg["model_name"], language=cfg["language"], task=cfg["task"]
    )
    model = WhisperForConditionalGeneration.from_pretrained(cfg["model_name"])
    model.generation_config.language = cfg["language"]
    model.generation_config.task = cfg["task"]
    model.generation_config.forced_decoder_ids = None
    model.config.use_cache = False  # incompatible with gradient checkpointing

    num_proc = cfg.get("num_proc")
    train_ds = prepare_dataset(
        load_mixture(
            cfg["train_sources"], cfg.get("train_split", "train"), cfg.get("max_train_samples")
        ),
        processor, num_proc,
    )
    eval_ds = prepare_dataset(
        load_mixture(cfg["eval_sources"], cfg.get("eval_split", "test"), cfg.get("max_eval_samples")),
        processor, num_proc,
    )
    print(f"train: {len(train_ds)} examples, eval: {len(eval_ds)} examples")

    def compute_metrics(pred):
        label_ids = pred.label_ids
        label_ids[label_ids == -100] = processor.tokenizer.pad_token_id
        preds = processor.batch_decode(pred.predictions, skip_special_tokens=True)
        refs = processor.batch_decode(label_ids, skip_special_tokens=True)
        return score(preds, refs, cfg.get("normalizer", "arabic"))

    trainer = Seq2SeqTrainer(
        model=model,
        args=Seq2SeqTrainingArguments(**cfg["training"]),
        train_dataset=train_ds,
        eval_dataset=eval_ds,
        data_collator=SpeechSeq2SeqCollator(processor, model.config.decoder_start_token_id),
        compute_metrics=compute_metrics,
        processing_class=processor,
    )
    processor.save_pretrained(trainer.args.output_dir)
    trainer.train()
    trainer.save_model()
    print(trainer.evaluate())
    if trainer.args.push_to_hub:
        trainer.push_to_hub()


if __name__ == "__main__":
    main()

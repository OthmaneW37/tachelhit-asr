# Tachelhit ASR ⵜⴰⵛⵍⵃⵉⵜ

Open speech recognition and speech translation for **Tachelhit** (Tashelhit, *tašlḥiyt*, ISO 639-3 `shi`),
the Amazigh language of the Souss region of Morocco, spoken by millions of people but rarely written.

> 🤗 Model: [huggingface.co/OthmaneW/tachelhit-asr](https://huggingface.co/OthmaneW/tachelhit-asr) · 🚧 work in progress

## Why

Most Tachelhit speakers use the language orally. Existing open resources pair Tachelhit **audio with
Arabic translations**; there is, to our knowledge, no open benchmark for **transcribing** Tachelhit into
its own script. This project aims to:

1. **Phase A — speech translation:** Tachelhit speech → Arabic text, fine-tuning Whisper on existing data.
2. **Phase B — transcription:** build the first open Tachelhit transcription test set (IRCAM Latin script,
   Tifinagh derived automatically) and a model that transcribes Tachelhit speech.

Everything is trained on a single consumer AMD GPU (Radeon RX 9060 XT, 16 GB) with ROCm.

## Data

| Source | Content | Licence | Used as |
|---|---|---|---|
| [SoufianeDahimi/Tamazight-ASR-Dataset-v2](https://huggingface.co/datasets/SoufianeDahimi/Tamazight-ASR-Dataset-v2) | ~15 h Tachelhit from subtitled films, Arabic text | Apache-2.0 | `dahimi` |
| [Ma-OpenHub/Tutlait-v1](https://huggingface.co/datasets/Ma-OpenHub/Tutlait-v1) | Crowdsourced Moroccan Tamazight, Arabic text, accent labels | CC-BY-4.0 | `tutlait_souss` (Souss accent only) |

## Quick start

```bash
# 1. Install PyTorch for your hardware first (ROCm: see docs/SETUP_ROCM.md)
# 2. Install the project
pip install -e ".[dev]"
python scripts/check_gpu.py

# 3. Check the pipeline end to end (tiny model, a few samples)
python -m tachelhit_asr.train --config configs/smoke-test.yaml

# 4. Baseline: zero-shot Whisper, then fine-tune
python -m tachelhit_asr.evaluate --model openai/whisper-small --max-samples 200
python -m tachelhit_asr.train --config configs/whisper-small-shi2ar.yaml
```

## Results

| Model | Test set | WER ↓ | CER ↓ | chrF ↑ |
|---|---|---|---|---|
| whisper-small (zero-shot) | dahimi | – | – | – |
| whisper-small (fine-tuned) | dahimi | – | – | – |

*Metrics are computed on normalised Arabic text (diacritics and alef/ya/ta-marbuta variants removed).*

## Project layout

```
configs/              training configs (YAML -> Seq2SeqTrainingArguments)
src/tachelhit_asr/
  data.py             dataset sources, 16 kHz audio decoding
  train.py            Whisper fine-tuning
  evaluate.py         evaluation + prediction dumps
  metrics.py          WER / CER / chrF
  text.py             Arabic and Latin text normalisation
  tifinagh.py         IRCAM Latin -> Tifinagh transliteration
docs/                 ROCm setup, roadmap, transcription guide
```

## Roadmap

See [docs/ROADMAP.md](docs/ROADMAP.md).

## Licence

Code under MIT. Datasets and models keep the licences of their sources.

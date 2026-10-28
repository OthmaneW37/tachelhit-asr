---
language:
- shi
- ar
license: mit
library_name: transformers
pipeline_tag: automatic-speech-recognition
base_model: openai/whisper-small
datasets:
- SoufianeDahimi/Tamazight-ASR-Dataset-v2
- Ma-OpenHub/Tutlait-v1
tags:
- tachelhit
- tashelhit
- amazigh
- berber
- whisper
- speech-translation
- low-resource
---

# Tachelhit ASR ⵜⴰⵛⵍⵃⵉⵜ

🚧 **Work in progress — no trained weights yet.**

Speech recognition and speech translation for **Tachelhit** (Souss Amazigh, `shi`).

- **Phase A:** Tachelhit speech → Arabic text (Whisper fine-tuned on existing open data).
- **Phase B:** first open Tachelhit transcription benchmark (IRCAM Latin, Tifinagh derived automatically).

Code, configs and roadmap: [github.com/OthmaneW37/tachelhit-asr](https://github.com/OthmaneW37/tachelhit-asr)

## Training data

| Dataset | Licence |
|---|---|
| [SoufianeDahimi/Tamazight-ASR-Dataset-v2](https://huggingface.co/datasets/SoufianeDahimi/Tamazight-ASR-Dataset-v2) | Apache-2.0 |
| [Ma-OpenHub/Tutlait-v1](https://huggingface.co/datasets/Ma-OpenHub/Tutlait-v1) (Souss accent) | CC-BY-4.0 |

## Results

Coming soon.

## Hardware

Trained on a single AMD Radeon RX 9060 XT (16 GB) with ROCm.

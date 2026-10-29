#!/usr/bin/env bash
# Phase A end to end on WSL: zero-shot baseline, then Whisper-small fine-tuning, then evaluation.
# Run as root in the ROCm distro:  wsl -d Ubuntu-24.04 -u root -- bash scripts/run_phase_a.sh
set -euo pipefail
cd "$(dirname "$0")/.."
source /opt/tachelhit-venv/bin/activate
export HSA_ENABLE_DXG_DETECTION=1
# Reuse files already downloaded on Windows; keep the large processed Arrow cache on the Linux disk.
export HF_HUB_CACHE=${HF_HUB_CACHE:-/mnt/c/Users/othma/.cache/huggingface/hub}
mkdir -p outputs

echo "== zero-shot baseline $(date)"
python -W ignore -m tachelhit_asr.evaluate --model openai/whisper-small \
    --max-samples 500 --out outputs/eval/whisper-small-zeroshot

echo "== fine-tuning $(date)"
python -W ignore -m tachelhit_asr.train --config configs/whisper-small-shi2ar.yaml

echo "== fine-tuned evaluation $(date)"
python -W ignore -m tachelhit_asr.evaluate --model outputs/whisper-small-shi2ar \
    --max-samples 500 --out outputs/eval/whisper-small-shi2ar
echo "== done $(date)"

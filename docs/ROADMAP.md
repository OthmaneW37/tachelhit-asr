# Roadmap

## Phase A — Speech translation (Tachelhit audio → Arabic text)
- [x] Project skeleton, data loaders, training and evaluation scripts
- [x] ROCm environment working on RX 9060 XT (`scripts/setup_wsl_rocm.sh`, `scripts/check_gpu.py`)
- [x] Smoke test passes on GPU (`configs/smoke-test.yaml`)
- [ ] Zero-shot baselines: whisper-small, whisper-medium, MMS
- [ ] Fine-tune whisper-small; report WER / CER / chrF per test set
- [ ] Error analysis by a native speaker (what is lost in translation?)
- [ ] Publish model + model card on the Hub

## Phase B — Transcription benchmark (Tachelhit audio → Tachelhit text)
- [ ] Learn the IRCAM Latin orthography ([TRANSCRIPTION_GUIDE.md](TRANSCRIPTION_GUIDE.md))
- [ ] Transcribe 2–5 h of audio (licensed sources + consented recordings)
- [ ] Have a sample reviewed by a literate Tachelhit speaker; measure inter-annotator agreement
- [ ] Publish `tachelhit-asr-bench` dataset (test set first)
- [ ] Fine-tune Whisper / MMS for transcription; Tifinagh output via `tifinagh.py`
- [ ] Gradio demo on Hugging Face Spaces
- [ ] Short technical report

## Ideas for later
- Multi-task model: transcribe **and** translate (Arabic / French)
- Whisper-medium or large-v3 with LoRA
- Speaker / accent robustness study (Souss sub-regions)

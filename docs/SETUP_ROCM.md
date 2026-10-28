# Setup on AMD Radeon RX 9060 XT (RDNA4, gfx1200) with ROCm

ROCm is most reliable on **Linux**. On Windows, use **WSL2 (Ubuntu)**; native-Windows PyTorch-ROCm
exists but is less mature. Always check AMD's current compatibility matrix for your GPU first.

## Option 1 — WSL2 Ubuntu (recommended on this PC)

1. Update the **AMD Adrenalin** Windows driver to the latest version (it provides GPU access to WSL).
2. In Ubuntu (WSL), install ROCm for WSL following AMD's guide
   ("Install Radeon software for WSL with ROCm"), typically:
   ```bash
   sudo apt update
   # download the amdgpu-install .deb from AMD's site for your Ubuntu version, then:
   sudo apt install ./amdgpu-install_*.deb
   amdgpu-install -y --usecase=wsl,rocm --no-dkms
   rocminfo | grep -i gfx      # should list gfx1200
   ```
3. Create an environment and install the PyTorch ROCm build (pick the newest ROCm index on pytorch.org):
   ```bash
   uv venv --python 3.12 && source .venv/bin/activate
   uv pip install torch torchaudio --index-url https://download.pytorch.org/whl/rocm6.4
   uv pip install -e ".[dev]"
   python scripts/check_gpu.py
   ```
   On WSL, AMD sometimes recommends replacing the `libhsa-runtime64.so` bundled in the torch wheel with
   the system one; follow their guide if `torch.cuda.is_available()` is `False`.

## Option 2 — native Linux (dual boot)

Same as above with `--usecase=rocm` (no `wsl`). Add your user to the `render` and `video` groups.

## Memory budget (16 GB, bf16)

| Model | Params | Setting |
|---|---|---|
| whisper-small | 244 M | full fine-tune, batch 16, gradient checkpointing |
| whisper-medium | 769 M | full fine-tune, batch 4–8, gradient checkpointing, 8-bit Adam if needed |
| whisper-large-v3 | 1.55 B | LoRA only |

`bitsandbytes` and FlashAttention support on ROCm varies by version; the default configs don't need them.

## Troubleshooting

- `torch.cuda.is_available() == False`: ROCm runtime not visible; rerun `rocminfo`, check driver version.
- Out of memory: halve `per_device_train_batch_size`, double `gradient_accumulation_steps`.
- Slow data prep: raise `num_proc` in the config (CPU cores).

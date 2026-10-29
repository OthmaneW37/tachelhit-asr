# Setup on AMD Radeon RX 9060 XT (RDNA4, gfx1200) with ROCm

Tested setup: Windows 11 + WSL2, **Ubuntu 24.04**, ROCm **7.2.1**, librocdxg **1.2.2**,
PyTorch **2.9.1+rocm7.2.1** (AMD wheels), Python 3.12.

## WSL2 (Windows) — automated

Since ROCm 7.2.1, WSL uses AMD's **ROCDXG** bridge (`librocdxg`) instead of
`amdgpu-install --usecase=wsl`, which no longer exists.

1. Update the **AMD Adrenalin** Windows driver (26.2.2 or newer).
2. Use **Ubuntu 22.04 or 24.04** — newer Ubuntu releases are not supported by ROCm on WSL.
   A dedicated distro keeps things clean:
   ```powershell
   wsl --install -d Ubuntu-24.04
   ```
3. Run the setup script as root inside it (idempotent, safe to re-run):
   ```powershell
   wsl -d Ubuntu-24.04 -u root -- bash /mnt/c/path/to/tachelhit-asr/scripts/setup_wsl_rocm.sh
   ```
   It installs the ROCm runtime (no kernel driver), `librocdxg`, sets `HSA_ENABLE_DXG_DETECTION=1`
   (needed before ROCm 7.13), creates `/opt/tachelhit-venv` with AMD's PyTorch wheels, installs this
   project and runs `scripts/check_gpu.py`.
4. Use it:
   ```bash
   source /opt/tachelhit-venv/bin/activate
   cd /mnt/c/path/to/tachelhit-asr
   python -m tachelhit_asr.train --config configs/smoke-test.yaml
   ```

Expected `rocminfo` output includes `gfx1200` / `AMD Radeon RX 9060 XT`.

## Native Linux (dual boot)

Install ROCm with `amdgpu-install -y --usecase=rocm` (kernel driver included), add your user to the
`render` and `video` groups, then install the same PyTorch wheels as in the script. No `librocdxg` needed.

## Memory budget (16 GB, bf16)

| Model | Params | Setting |
|---|---|---|
| whisper-small | 244 M | full fine-tune, batch 16, gradient checkpointing |
| whisper-medium | 769 M | full fine-tune, batch 4–8, gradient checkpointing, 8-bit Adam if needed |
| whisper-large-v3 | 1.55 B | LoRA only |

`bitsandbytes` and FlashAttention support on ROCm varies by version; the default configs don't need them.

## Troubleshooting

- `rocminfo` shows only the CPU: check the Adrenalin driver version, `ls /dev/dxg`, and that
  `HSA_ENABLE_DXG_DETECTION=1` is set.
- `torch.cuda.is_available() == False`: make sure you use the venv's Python with AMD's ROCm wheels.
- WSL gets about half of the PC's RAM by default; raise `memory=` in `%UserProfile%\.wslconfig` if data
  preparation runs out of memory.
- Out of GPU memory: halve `per_device_train_batch_size`, double `gradient_accumulation_steps`.
- Reading data from `/mnt/c` is slower than the Linux filesystem; the Hugging Face cache lives in
  `~/.cache/huggingface` inside WSL by default, which is fine.

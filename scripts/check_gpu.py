"""Check that PyTorch sees the AMD GPU through ROCm and can run bf16 matmuls."""

import torch

print("torch:", torch.__version__)
print("HIP (ROCm):", torch.version.hip)
print("GPU available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("device:", torch.cuda.get_device_name(0))
    print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    a = torch.randn(4096, 4096, device="cuda", dtype=torch.bfloat16)
    print("bf16 matmul OK:", (a @ a).float().abs().mean().item() > 0)

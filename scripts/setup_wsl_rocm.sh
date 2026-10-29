#!/usr/bin/env bash
# Set up ROCm 7.2.1 + PyTorch on WSL2 Ubuntu 24.04 for Radeon RX 9000 GPUs (ROCDXG path).
# Run as root inside the distro:  wsl -d Ubuntu-24.04 -u root -- bash scripts/setup_wsl_rocm.sh
# Each step is skipped if already done, so the script can be re-run safely.
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive

ROCM_VERSION=7.2.1
ROCDXG_VERSION=1.2.2
WHEELS=https://repo.radeon.com/rocm/manylinux/rocm-rel-${ROCM_VERSION}
VENV=${VENV:-/opt/tachelhit-venv}
PROJECT_DIR=$(cd "$(dirname "$0")/.." && pwd)

if ! command -v amdgpu-install >/dev/null; then
    echo "== amdgpu-install"
    wget -q -P /tmp "https://repo.radeon.com/amdgpu-install/${ROCM_VERSION}/ubuntu/noble/amdgpu-install_${ROCM_VERSION}.70201-1_all.deb"
    apt-get install -y -qq "/tmp/amdgpu-install_${ROCM_VERSION}.70201-1_all.deb"
fi

if [ ! -x /opt/rocm/bin/rocminfo ]; then
    echo "== ROCm runtime (no kernel driver on WSL)"
    amdgpu-install -y --usecase=rocm --no-dkms
fi

if [ ! -e /opt/rocm/lib/librocdxg.so ]; then
    echo "== librocdxg ${ROCDXG_VERSION} (WSL <-> Windows GPU bridge)"
    wget -q -P /tmp "https://github.com/ROCm/librocdxg/releases/download/v${ROCDXG_VERSION}/rocdxg-roct_${ROCDXG_VERSION}_amd64.deb"
    dpkg -i "/tmp/rocdxg-roct_${ROCDXG_VERSION}_amd64.deb"
fi

# Required for ROCm releases before 7.13.
grep -q HSA_ENABLE_DXG_DETECTION /etc/environment || echo "HSA_ENABLE_DXG_DETECTION=1" >> /etc/environment
export HSA_ENABLE_DXG_DETECTION=1

echo "== GPU agents"
/opt/rocm/bin/rocminfo | grep -E "Marketing Name|Name: +gfx" || true

if [ ! -x "${VENV}/bin/python" ]; then
    echo "== Python venv + PyTorch ROCm wheels"
    apt-get install -y -qq python3-venv
    python3 -m venv "${VENV}"
fi
if ! "${VENV}/bin/python" -c "import torch" 2>/dev/null; then
    "${VENV}/bin/pip" install -q --upgrade pip wheel
    "${VENV}/bin/pip" install -q \
        "${WHEELS}/torch-2.9.1%2Brocm7.2.1.lw.gitff65f5bc-cp312-cp312-linux_x86_64.whl" \
        "${WHEELS}/torchaudio-2.9.0%2Brocm7.2.1.gite3c6ee2b-cp312-cp312-linux_x86_64.whl" \
        "${WHEELS}/triton-3.5.1%2Brocm7.2.1.gita272dfa8-cp312-cp312-linux_x86_64.whl"
fi
"${VENV}/bin/pip" install -q -e "${PROJECT_DIR}[dev]"

echo "== PyTorch check"
"${VENV}/bin/python" "${PROJECT_DIR}/scripts/check_gpu.py"

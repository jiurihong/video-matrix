#!/usr/bin/env bash
set -euo pipefail

echo "Setting up virtualenv and installing Python dependencies..."
PYTHON=python3
if ! command -v $PYTHON >/dev/null 2>&1; then
  echo "python3 not found. Please install Python 3.10+"
  exit 1
fi

VENV_DIR=".venv"
$PYTHON -m venv $VENV_DIR
source $VENV_DIR/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

cat <<'EOF'
Next steps:
1) Install CUDA-enabled PyTorch matching your CUDA driver. Example for CUDA 11.8:
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
2) If you plan to use quantized LLMs, install bitsandbytes and accelerate:
   pip install bitsandbytes accelerate
3) For Stable Diffusion/SD pipelines, follow diffusers/transformers install instructions.
4) Put model weights under /data/models/video-matrix/ (or set VIDEO_MATRIX_MODELS_DIR env)
EOF

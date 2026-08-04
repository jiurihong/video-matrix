#!/usr/bin/env bash
set -euo pipefail

# Usage: ./model_downloader.sh --outdir /path/to/models
OUTDIR="${1:-./models}"
mkdir -p "$OUTDIR"

echo "Model downloader - run this on a machine with internet access."

echo "Downloading ChatGLM-6B (示例). If requires auth, set HF_TOKEN env before running."
python - <<PY
from huggingface_hub import snapshot_download
import os
out = os.path.join("$OUTDIR","chatglm-6b")
print('Downloading to', out)
snapshot_download(repo_id="THUDM/chatglm-6b", cache_dir=out, allow_patterns=['*'], resume_download=True)
PY

echo "Downloading Stable Diffusion v1.5 (runwayml/stable-diffusion-v1-5)"
python - <<PY
from huggingface_hub import snapshot_download
import os
out = os.path.join("$OUTDIR","sd-v1-5")
print('Downloading to', out)
snapshot_download(repo_id="runwayml/stable-diffusion-v1-5", cache_dir=out, allow_patterns=['*'], resume_download=True)
PY

echo "Downloading Real-ESRGAN weights (示例: xinntao/Real-ESRGAN)"
python - <<PY
from huggingface_hub import snapshot_download
import os
out = os.path.join("$OUTDIR","realesrgan")
print('Downloading to', out)
# If not present on HF, fallback to git clone or GH release manual download
try:
    snapshot_download(repo_id="xinntao/Real-ESRGAN", cache_dir=out, allow_patterns=['*'], resume_download=True)
except Exception as e:
    print('Real-ESRGAN not found on HF, please download from GitHub releases and place in', out)
PY

echo "Downloading RIFE interpolation implementation (placeholder)"
mkdir -p "$OUTDIR/rife"
echo "Please obtain a preferred RIFE implementation and place weights under $OUTDIR/rife"

echo "MiniMax H3 (optional, large ~42GB). If you want it, run the following with HF_TOKEN set:"
cat <<EOF
python - <<PY
from huggingface_hub import snapshot_download
import os
out = os.path.join("$OUTDIR","minimax-h3")
print('Downloading to', out)
snapshot_download(repo_id="MiniMaxAI/MiniMax-H3", cache_dir=out, allow_patterns=['*'], resume_download=True)
PY
EOF

echo "All downloads attempted. Create tarball to transport to MARVIS host, e.g.:
  tar -czvf video-matrix-models.tar.gz -C $OUTDIR .
Then scp/rsync the tarball to the MARVIS host and extract under /data/models/video-matrix/"

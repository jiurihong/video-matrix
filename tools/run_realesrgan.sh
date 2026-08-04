#!/usr/bin/env bash
set -euo pipefail

IN=$1
OUT=${2:-${IN%.*}_esr.mp4}

if [ ! -f "$IN" ]; then
  echo "input not found: $IN"
  exit 1
fi

# Try a common Real-ESRGAN inference script path
if [ -f "tools/realesrgan/infer_video.py" ]; then
  python3 tools/realesrgan/infer_video.py --input "$IN" --output "$OUT" || true
else
  echo "Real-ESRGAN infer script not found; attempting ffmpeg upscale fallback"
  ffmpeg -i "$IN" -vf scale=1080:1920 -c:v libx264 -crf 23 "$OUT" -y
fi

echo "$OUT"

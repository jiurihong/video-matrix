#!/usr/bin/env bash
set -euo pipefail

IN=$1
OUT=${2:-${IN%.*}_rife.mp4}

if [ ! -f "$IN" ]; then
  echo "input not found: $IN"
  exit 1
fi

# Try a common RIFE implementation path if available
if [ -f "tools/rife/interpolate.py" ]; then
  python3 tools/rife/interpolate.py --input "$IN" --output "$OUT" || true
else
  echo "RIFE interpolate script not found; skipping. Copy a RIFE implementation into tools/rife/"
  # fallback: copy input to output
  cp "$IN" "$OUT"
fi

echo "$OUT"

#!/usr/bin/env bash
set -euo pipefail

# Example compose runner that reads segments JSON produced by script_service
# and stitches audio + simple visuals into a draft video using ffmpeg.

INPUT_AUDIO="$1"
DURATION=${2:-60}
OUT_VIDEO=${3:-/tmp/draft_compose.mp4}
WIDTH=1080
HEIGHT=1920

if [ -z "$INPUT_AUDIO" ]; then
  echo "Usage: $0 <audio.wav> [duration_sec] [out.mp4]"
  exit 1
fi

# Create a black background video with the same duration
ffmpeg -hide_banner -loglevel error -f lavfi -i color=c=black:s=${WIDTH}x${HEIGHT}:d=${DURATION} -i "$INPUT_AUDIO" -c:v libx264 -c:a aac -shortest -pix_fmt yuv420p -vf "format=yuv420p" "$OUT_VIDEO" -y

echo "Draft video generated: $OUT_VIDEO"

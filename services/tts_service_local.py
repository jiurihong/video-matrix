"""
TTS Service (local Coqui TTS example)
Requires: Coqui TTS installed and a model downloaded under $VIDEO_MATRIX_MODELS_DIR/coqui
This script uses the TTS Python API if available.
"""
from flask import Flask, request, jsonify
import os

app = Flask(__name__)
MODEL_DIR = os.environ.get('VIDEO_MATRIX_MODELS_DIR','/data/models/video-matrix')
COQUI_MODEL = os.path.join(MODEL_DIR,'coqui')

@app.route('/generate-audio', methods=['POST'])
def generate_audio():
    data = request.json or {}
    text = data.get('text','')
    duration = data.get('duration',60)
    out_path = f"/tmp/tts_{abs(hash(text))%100000}.wav"
    # Try to use Coqui TTS if installed
    try:
        from TTS.api import TTS
        # list_models() to find local model name if needed
        tts = TTS(model_name_or_path=COQUI_MODEL)
        tts.tts_to_file(text=text, file_path=out_path)
        return jsonify({"audio_path": out_path, "duration": duration})
    except Exception as e:
        # fallback: generate silent wav
        import subprocess
        subprocess.run(f"ffmpeg -f lavfi -i anullsrc=r=16000:cl=mono -t {duration} -q:a 9 -acodec pcm_s16le {out_path} -y", shell=True)
        return jsonify({"audio_path": out_path, "duration": duration, "note":"fallback silent audio - install Coqui TTS and place model in $VIDEO_MATRIX_MODELS_DIR/coqui"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002)

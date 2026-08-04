"""
Post-process service - wrapper to call Real-ESRGAN and RIFE if available.
Expects input draft video and outputs final upscaled/processed video.
Model weights should be located under $VIDEO_MATRIX_MODELS_DIR/realesrgan and $VIDEO_MATRIX_MODELS_DIR/rife
"""
from flask import Flask, request, jsonify
import os, subprocess

app = Flask(__name__)
MODEL_DIR = os.environ.get('VIDEO_MATRIX_MODELS_DIR','/data/models/video-matrix')
REALSRGAN_DIR = os.path.join(MODEL_DIR,'realesrgan')
RIFE_DIR = os.path.join(MODEL_DIR,'rife')

@app.route('/post-process', methods=['POST'])
def post_process():
    data = request.json or {}
    video = data.get('video_path')
    target = data.get('final_path') or f"{video.rsplit('.',1)[0]}_final.mp4"
    # 1) Optional: run frame interpolation (RIFE) - placeholder
    rife_cmd = f"python3 tools/rife/interpolate.py --input {video} --output {video.rsplit('.',1)[0]}_rife.mp4 || true"
    # 2) Optional: run Real-ESRGAN upscaling - placeholder
    esrg_cmd = f"python3 tools/realesrgan/infer_video.py --input {video.rsplit('.',1)[0]}_rife.mp4 --output {target} || ffmpeg -i {video} -vf scale=1080:1920 -c:v libx264 -crf 23 {target}"
    try:
        subprocess.run(rife_cmd, shell=True)
        subprocess.run(esrg_cmd, shell=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"final_path": target})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8004)

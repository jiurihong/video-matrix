from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/compose-video', methods=['POST'])
def compose_video():
    data = request.json or {}
    audio = data.get('audio_path')
    template = data.get('template', 'default')
    out = f"/tmp/draft_{os.getpid()}.mp4"
    # 简单合成示例：空白画面 + 音频
    cmd = f"ffmpeg -f lavfi -i color=c=black:s=1080x1920:d=60 -i {audio} -c:v libx264 -c:a aac -shortest {out} -y"
    subprocess.run(cmd, shell=True)
    return jsonify({"draft_video_path": out})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8003)

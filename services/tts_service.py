from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/generate-audio', methods=['POST'])
def generate_audio():
    data = request.json or {}
    text = data.get('text', '')
    voice = data.get('voice', 'xiaoyan')
    out_path = f"/tmp/{abs(hash(text)) % 100000}.wav"
    # 示例：这里仅生成静音的 wav 占位，实际应调用 TTS SDK/API
    duration = data.get('duration', 60)
    # create a silent wav as placeholder
    os.system(f"ffmpeg -f lavfi -i anullsrc=r=16000:cl=mono -t {duration} -q:a 9 -acodec pcm_s16le {out_path} -y >/dev/null 2>&1")
    return jsonify({"audio_path": out_path, "duration": duration})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002)

from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

@app.route('/generate-script', methods=['POST'])
def generate_script():
    data = request.json or {}
    topic = data.get('topic', '冷知识')
    length = data.get('length_sec', 60)
    # 简单示例：分段脚本，实际应调用 LLM
    script = f"这是关于{topic}的简短视频脚本，时长 {length} 秒。"
    segments = [
        {"start":0, "end":6, "text":"开场钩子：快速引入话题"},
        {"start":6, "end":30, "text":"主体说明：详细说明要点"},
        {"start":30, "end":60, "text":"结尾：总结+CTA"}
    ]
    resp = {"script": script, "segments": segments, "title": topic+"的三个要点", "tags": [topic]}
    return jsonify(resp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)

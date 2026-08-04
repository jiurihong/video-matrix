"""
Script Service (local LLM) - example using Hugging Face transformers or ChatGLM local model.
Requires: models placed under $VIDEO_MATRIX_MODELS_DIR/chatglm-6b or set MODEL_PATH env var.
"""
from flask import Flask, request, jsonify
import os

app = Flask(__name__)
MODEL_DIR = os.environ.get('VIDEO_MATRIX_MODELS_DIR','/data/models/video-matrix')
CHATGLM_DIR = os.path.join(MODEL_DIR,'chatglm-6b')

# Lazy import to avoid heavy startup if model not present
model = None
tokenizer = None

def load_model():
    global model, tokenizer
    if model is not None:
        return
    try:
        from transformers import AutoModelForCausalLM, AutoTokenizer
        print('Loading local ChatGLM model from', CHATGLM_DIR)
        tokenizer = AutoTokenizer.from_pretrained(CHATGLM_DIR, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(CHATGLM_DIR, trust_remote_code=True, device_map='auto')
    except Exception as e:
        print('Failed to load local LLM model:', e)
        model = None

@app.route('/generate-script', methods=['POST'])
def generate_script():
    data = request.json or {}
    topic = data.get('topic','冷知识')
    length = data.get('length_sec',60)
    style = data.get('style','short_knowledge')
    load_model()
    if model is None:
        # fallback simple template
        script = f"这是关于{topic}的短视频脚本（占位），时长 {length} 秒。"
        segments = [
            {"start":0, "end":6, "text":"开场钩子：迅速引入话题"},
            {"start":6, "end":45, "text":"主体：详细说明要点"},
            {"start":45, "end":length, "text":"结尾：总结并 CTA"}
        ]
        return jsonify({"script":script, "segments":segments, "title":topic+" 的三个要点", "tags":[topic]})
    # Example simple generation
    prompt = f"为主题{topic}生成一个适合{length}秒竖屏短视频的分镜脚本，包含开场钩子、主体要点和结尾CTA，输出 JSON 格式。\n"
    inputs = tokenizer(prompt, return_tensors='pt').to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=256)
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Very naive parse - in practice build a robust parser
    script = text
    segments = [{"start":0,"end":length,"text":text}]
    return jsonify({"script":script, "segments":segments, "title":topic, "tags":[topic]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)

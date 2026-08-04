# API Specification (简要)

服务列表：

1. Script Service
   - POST /generate-script
     - body: {"topic": "string", "style": "short_knowledge|hosted|creative", "length_sec": 60}
     - returns: {"script": "...", "segments": [{"start":0,"end":6,"text":"..."}], "title":"...", "tags": []}

2. TTS Service
   - POST /generate-audio
     - body: {"text": "...", "voice": "xiaoyan", "speed": 1.0}
     - returns: {"audio_path": "/tmp/..wav", "duration": 60}

3. Asset Generator (可选)
   - POST /generate-assets
     - body: {"prompts": ["..."], "style": {...}}
     - returns: {"assets": [{"path":"/tmp/asset1.mp4","type":"clip"}]}

4. Composer
   - POST /compose-video
     - body: {"segments": [...], "audio_path": "", "template": "default"}
     - returns: {"draft_video_path": "/tmp/draft.mp4"}

5. Postprocess
   - POST /post-process
     - body: {"video_path":"/tmp/draft.mp4","target_resolution":"1080p","fps":30}
     - returns: {"final_path":"/tmp/final.mp4"}

6. Publisher
   - POST /publish
     - body: {"video_path":"/tmp/final.mp4","platform":"douyin","meta":{...}}
     - returns: {"publish_id":"...","status":"ok"}

7. Job status
   - GET /status/{job_id}


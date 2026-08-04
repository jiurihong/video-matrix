#!/usr/bin/env python3
"""
Simple local runner that exercises the pipeline by calling local service endpoints.
"""
import requests
import time

SCRIPT_URL = "http://localhost:8001/generate-script"
TTS_URL = "http://localhost:8002/generate-audio"
COMPOSE_URL = "http://localhost:8003/compose-video"
POST_URL = "http://localhost:8004/post-process"


def run_sample():
    # 1. generate script
    r = requests.post(SCRIPT_URL, json={"topic":"冷知识","length_sec":60})
    script = r.json()
    print('script:', script['title'])

    # 2. generate tts
    combined_text = ' '.join([s['text'] for s in script['segments']])
    r = requests.post(TTS_URL, json={"text": combined_text, "duration": 60})
    audio = r.json()['audio_path']
    print('audio:', audio)

    # 3. compose
    r = requests.post(COMPOSE_URL, json={"audio_path": audio, "template":"default"})
    draft = r.json()['draft_video_path']
    print('draft:', draft)

    # 4. post process
    r = requests.post(POST_URL, json={"video_path": draft})
    final = r.json()['final_path']
    print('final:', final)

    print('Done.')

if __name__ == '__main__':
    run_sample()

"""
Worker tasks using Celery. High-level task: generate_pipeline
This task orchestrates: script generation -> tts -> compose -> postprocess -> publish (optional)
It calls local service endpoints (assumes services are reachable via HTTP on localhost ports).
"""
from celery_app import celery_app
import requests
import os

SCRIPT_SVC = os.environ.get('SCRIPT_SERVICE_URL','http://localhost:8001/generate-script')
TTS_SVC = os.environ.get('TTS_SERVICE_URL','http://localhost:8002/generate-audio')
COMPOSE_SVC = os.environ.get('COMPOSE_SERVICE_URL','http://localhost:8003/compose-video')
POST_SVC = os.environ.get('POST_SERVICE_URL','http://localhost:8004/post-process')

@celery_app.task(bind=True, acks_late=True)
def generate_pipeline(self, topic, length_sec=60, style='short_knowledge'):
    job = {'topic': topic, 'length_sec': length_sec, 'style': style}
    try:
        # 1. script
        r = requests.post(SCRIPT_SVC, json=job, timeout=60)
        r.raise_for_status()
        script = r.json()
        # 2. tts
        combined_text = ' '.join([s.get('text','') for s in script.get('segments',[])])
        r = requests.post(TTS_SVC, json={'text': combined_text, 'duration': length_sec}, timeout=120)
        r.raise_for_status()
        audio = r.json().get('audio_path')
        # 3. compose
        r = requests.post(COMPOSE_SVC, json={'audio_path': audio, 'template':'default'}, timeout=300)
        r.raise_for_status()
        draft = r.json().get('draft_video_path')
        # 4. post process
        r = requests.post(POST_SVC, json={'video_path': draft}, timeout=600)
        r.raise_for_status()
        final = r.json().get('final_path')
        return {'status':'success','final': final}
    except Exception as e:
        # let Celery handle retries/failed
        raise self.retry(exc=e, countdown=30, max_retries=3)

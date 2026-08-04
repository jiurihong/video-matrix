"""
Celery application factory for Video-Matrix tasks.
Configure via environment variables:
- CELERY_BROKER_URL (e.g., redis://localhost:6379/0)
- CELERY_RESULT_BACKEND (e.g., redis://localhost:6379/1)
"""
from celery import Celery
import os

broker = os.environ.get('CELERY_BROKER_URL','redis://localhost:6379/0')
backend = os.environ.get('CELERY_RESULT_BACKEND','redis://localhost:6379/1')

celery_app = Celery('video_matrix', broker=broker, backend=backend)
celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='Asia/Shanghai',
    enable_utc=False,
)

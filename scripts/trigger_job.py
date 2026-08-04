#!/usr/bin/env python3
"""
Simple enqueue script to trigger a Celery task locally.
Usage: python3 scripts/trigger_job.py "topic text" [length_sec]
"""
import sys
from services.celery_app import celery_app

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: trigger_job.py "topic" [length_sec]')
        sys.exit(1)
    topic = sys.argv[1]
    length = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    res = celery_app.send_task('services.worker.generate_pipeline', args=(topic, length))
    print('Enqueued:', res.id)

Stage 2 plan: integrate post-processing, task queue, and quality gate

This document describes the Stage-2 work that has been implemented on the branch and what remains to be done.

Implemented in this commit:
- Celery app + worker task that orchestrates the pipeline (services/celery_app.py, services/worker.py)
- Trigger script to enqueue tasks (scripts/trigger_job.py)
- Updated requirements to include celery, redis, prometheus_client and other libs
- Documentation placeholders and instructions for running Redis/Celery on a non-Docker host

Remaining tasks (what I will continue working on):
- Integrate Real-ESRGAN and RIFE callable scripts into post_process_local.py (wrappers provided; need model path config)
- Add Prometheus metrics endpoints in services and a small exporter (metrics: tasks_started, tasks_failed, avg_task_time)
- Implement lightweight job dashboard (simple /jobs endpoint or a small sqlite DB to store job metadata)
- Add automatic content-safety checks (NSFW detector) as a pre-publish gate
- Provide systemd unit for Celery worker and a sample Redis install guide for Ubuntu 22.04

Runbook (Redis + Celery on Ubuntu 22.04):
- Install redis-server: sudo apt update && sudo apt install -y redis-server
- Start and enable: sudo systemctl enable --now redis-server
- Verify: redis-cli ping => PONG
- Start Celery worker: .venv/bin/celery -A services.celery_app.celery_app worker --loglevel=info -Q default
- Alternatively create systemd unit for celery worker (example provided later)

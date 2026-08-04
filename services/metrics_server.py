from prometheus_client import start_http_server, Counter, Gauge, Histogram
import os

METRICS_PORT = int(os.environ.get('VIDEO_MATRIX_METRICS_PORT','9102'))

tasks_started = Counter('video_matrix_tasks_started_total', 'Total number of tasks started')
tasks_succeeded = Counter('video_matrix_tasks_succeeded_total', 'Total number of tasks succeeded')
tasks_failed = Counter('video_matrix_tasks_failed_total', 'Total number of tasks failed')
queue_depth = Gauge('video_matrix_queue_depth', 'Current queue depth')
task_duration = Histogram('video_matrix_task_seconds', 'Task duration in seconds')

def start_metrics_server():
    try:
        start_http_server(METRICS_PORT)
        print(f"Prometheus metrics server started on :{METRICS_PORT}")
    except Exception as e:
        print('Failed to start metrics server:', e)

# helper wrappers
from contextlib import contextmanager
import time

@contextmanager
def track_task():
    tasks_started.inc()
    start = time.time()
    try:
        yield
n    except Exception:
        tasks_failed.inc()
        raise
    else:
        tasks_succeeded.inc()
    finally:
        duration = time.time() - start
        task_duration.observe(duration)

"""
Post-process wrapper service: runs RIFE -> Real-ESRGAN and updates job DB / metrics.
"""
from flask import Flask, request, jsonify
import os, subprocess, uuid
from services.job_db import create_job, update_job
from services.metrics_server import start_metrics_server, tasks_started, tasks_failed, tasks_succeeded, task_duration
import threading

app = Flask(__name__)
MODEL_DIR = os.environ.get('VIDEO_MATRIX_MODELS_DIR','/data/models/video-matrix')

# ensure metrics server started in background
threading.Thread(target=start_metrics_server, daemon=True).start()

@app.route('/post-process', methods=['POST'])
def post_process():
    data = request.json or {}
    video = data.get('video_path')
    job_id = data.get('job_id') or str(uuid.uuid4())
    create_job(job_id, data.get('topic','unknown'))
    update_job(job_id, status='post_processing')
    try:
        tasks_started.inc()
        # 1) RIFE
        rife_out = video.rsplit('.',1)[0] + '_rife.mp4'
        cmd = ["/bin/bash","tools/run_rife.sh", video, rife_out]
        subprocess.run(cmd, check=False)
        # 2) Real-ESRGAN
        esr_out = video.rsplit('.',1)[0] + '_final.mp4'
        cmd2 = ["/bin/bash","tools/run_realesrgan.sh", rife_out, esr_out]
        subprocess.run(cmd2, check=False)
        update_job(job_id, status='succeeded', final_path=esr_out)
        tasks_succeeded.inc()
        return jsonify({'final_path': esr_out, 'job_id': job_id})
    except Exception as e:
        update_job(job_id, status='failed', error=str(e))
        tasks_failed.inc()
        return jsonify({'error': str(e), 'job_id': job_id}), 500

@app.route('/jobs', methods=['GET'])
def jobs_list():
    from services.job_db import list_jobs
    return jsonify(list_jobs())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8004)

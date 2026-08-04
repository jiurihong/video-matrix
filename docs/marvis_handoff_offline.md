# Update marvis_handoff for offline/no-docker deployment

This file explains how to deploy the Video-Matrix services on a MARVIS host that does not have Docker and cannot access the public internet.

Key points:
- OS: Ubuntu 22.04 (systemd available)
- Models directory: /data/models/video-matrix (ensure sufficient disk space)
- Python virtualenv: .venv in the repo root (install.sh sets it up)

Steps:
1) On an internet-connected machine, run `./model_downloader.sh /tmp/vm-models` to download required models (see README for list). This will download:
   - ChatGLM-6B (THUDM/chatglm-6b)
   - Stable Diffusion v1.5 (runwayml/stable-diffusion-v1-5)
   - Real-ESRGAN (xinntao/Real-ESRGAN) or equivalent weights
   - RIFE implementation weights (user-provided)
   - Optional: MiniMax H3 (very large ~42GB)

2) Tar and transfer to MARVIS host:
   tar -czvf video-matrix-models.tar.gz -C /tmp/vm-models .
   scp video-matrix-models.tar.gz user@marvis-host:/tmp/
   ssh user@marvis-host 'sudo mkdir -p /data/models/video-matrix && sudo tar -xzvf /tmp/video-matrix-models.tar.gz -C /data/models/video-matrix && sudo chown -R ubuntu:ubuntu /data/models/video-matrix'

3) On MARVIS host, run:
   ./install.sh
   # edit /etc/video-matrix/env to provide needed env vars e.g. VIDEO_MATRIX_MODELS_DIR=/data/models/video-matrix
   sudo cp services/*.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable --now script_service.service tts_service.service compose_service.service post_process.service

4) Smoke test:
   Run the sample pipeline locally (services must be running):
     python3 scripts/run_generate.py --sample
   Check /tmp for generated final.mp4

5) Logs & monitoring:
   systemctl status script_service.service
   journalctl -u script_service.service -f

Notes on credentials & tokens:
- If any HuggingFace token or other secret is needed for model downloads, do NOT commit it to git. Place it in /etc/video-matrix/env (systemd EnvironmentFile) or use a secure vault.


# README update: Stage1 offline-focused instructions

This branch (video-matrix-prod) contains Stage-1 work to enable non-Docker, offline deployment on MARVIS host (Ubuntu 22.04).

Quick start overview:
1) On an internet-connected machine, run:
   ./model_downloader.sh /tmp/vm-models
2) Transfer models to MARVIS host (see docs/marvis_handoff_offline.md)
3) On MARVIS host, run ./install.sh and then enable systemd services.
4) Run smoke test: python3 scripts/run_generate.py --sample


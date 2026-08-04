# Real-ESRGAN and RIFE integration notes

This document gives actionable steps to integrate the Real-ESRGAN and RIFE tools into the post-processing pipeline.

1) Real-ESRGAN
- Recommended repo: https://github.com/xinntao/Real-ESRGAN
- Place weights under: $VIDEO_MATRIX_MODELS_DIR/realesrgan/weights
- Example invocation (python): python inference_realesrgan.py --input in.mp4 --output out.mp4 --model path/to/weights

2) RIFE
- Several implementations exist; pick one compatible with your CUDA/PyTorch.
- Place weights under: $VIDEO_MATRIX_MODELS_DIR/rife/weights
- Example invocation: python inference_rife.py --input in.mp4 --output out_rife.mp4 --scale 2

3) Workflow in post_process_local.py
- Step A: run RIFE interpolation -> generate intermediate video
- Step B: run Real-ESRGAN upscaling on intermediate video
- Step C: format/encode final file with ffmpeg

4) Performance tips for 4080 Super (16GB)
- Run both tools with FP16 where supported
- Process in chunks if memory limited (split video into segments)
- Use --tta or --tile options in Real-ESRGAN to reduce VRAM peak

# Video-Matrix — 自动化短视频流水线（MVP）

本仓库为“Video Matrix”项目的 MVP 骨架，目标：在本地 MARVIS 调度下实现 24/7 自动化生成 60s+、1080p 的短视频并自动发布到国内平台（抖音/快手等）。

主要功能：
- 文案/分镜脚本生成（LLM）
- 语音合成（TTS）
- 关键画面或短片段 AI 生成（可选）
- 模板化视频合成（FFmpeg）
- 插帧/超分后期（RIFE / Real-ESRGAN）
- 发布接口（抖音/快手 API）
- 调度与监控（用于交付给 MARVIS 的说明）

快速开始
1. 克隆仓库并安装依赖
   ```bash
   git clone https://github.com/jiurihong/video-matrix.git
   cd video-matrix
   pip install -r requirements.txt
   ```
2. 在 `docs/keys.example.env` 中填写你的 API Key、TTS 配置及 COS/存储信息（切勿提交真实密钥到仓库）。
3. 本地运行示例生成流程（模拟发布）
   ```bash
   python3 scripts/run_generate.py --sample
   ```

交付给 MARVIS
- 我们提供了 `docs/marvis_handoff.md`，包含容器镜像说明、调度建议与 K8s job 示例，MARVIS 可直接根据此文档部署并调度。

目录结构说明请参见 `architecture.md` 和 `api.md`。

License: MIT

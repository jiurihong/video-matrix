# Architecture — Video Matrix

概览：

1. Idea Engine (LLM)
   - 负责生成脚本、标题、标签、封面文案、分镜。可调用 OpenAI/GPT/本地 LLM。
2. Media Engine
   - TTS 服务：生成语音文件（wav/mp3）。
   - Asset generator：可选的 AI 画面/短片段生成（仅用于关键钩子帧）。
3. Composer
   - 按模板把画面、配音、字幕、B-roll 合成初版视频（FFmpeg）。
4. Post-process
   - 插帧（RIFE）、超分（Real-ESRGAN）、色彩校正、去噪、稳定。
5. Publisher
   - 上传并发布到目标平台（抖音/快手 API），获取发布结果并记录。
6. Orchestration
   - 任务队列 + 调度（MARVIS / Kubernetes / Celery），并行化生成任务和并发控制。
7. Monitoring & Feedback
   - 采集分发后指标（播放/完播/点赞），将表现数据反馈到 Idea Engine 做自动化迭代。

质量闸与验收规则：
- 音频完整且无静音段
- 视频时长符合模板（±2s）
- 分辨率 >= 1080p
- 无明显跳帧（插帧后）
- 封面清晰且有标题


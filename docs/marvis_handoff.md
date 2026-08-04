# MARVIS 部署交接说明

目的：给 MARVIS 团队的可执行交接指南，便于在本地环境（含 GPU）上部署并 24/7 调度 Video-Matrix 服务。

准备
- 确认环境能访问模型权重下载地址（或提前把权重放在内部仓库）。
- GPU 驱动与 nvidia-docker 需可用（若使用 GPU 容器）。
- 为服务准备一个用于存储生成文件的共享路径或 COS 桶，MARVIS 需能访问该路径。

容器化
- 我们提供了 Dockerfile 模板（docker/）和示例 K8s manifests（k8s/）。推荐使用镜像仓库保存镜像。
- 服务设计为 stateless，持久化文件放 COS 或网络共享存储。

调度建议
- 使用队列（例如 RabbitMQ / Redis + Celery）承接生成任务，MARVIS 可以根据队列长度触发 worker 扩缩容。
- 针对 4080 Super，每个 GPU worker 推荐如下资源限制：
  - requests: cpu: 4, memory: 24Gi
  - limits: cpu: 8, memory: 60Gi
  - GPU: 1

批量策略
- 批量任务请分镜头并行生成（每个 worker 处理若干镜头），然后由 Composer 合并。
- 设置每日/每小时并发上限，以避免触发平台反滥用限制。

监控
- 暴露基本 Prometheus 指标：tasks_started, tasks_succeeded, tasks_failed, avg_task_time_seconds。
- 报警：失败率 > 5% 或 avg_task_time 超过阈值时触发人工介入。

验证与验收
- MARVIS 部署完成后运行 smoke tests：运行 `scripts/run_generate.py --sample` 并检查输出文件是否合规。


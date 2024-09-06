---
hide:
  - toc
---

# 功能特性

模型中心的功能特性参见下表：

| 一级功能 | 二级功能 | 描述 |
| ------- | ------ | ------ |
| 模型支持 | 生成式 Transformer 模型支持 | 大语言模型： Llama-2-13B ChatGLM3-6B ChatGLM4-9B Qwen-14B-Chat Qwen2-7B-Chat Baichuan2-13B-Chat 多模态模型： Qwen-VL-Chat |
| 模型部署 | 多样化部署方式 | 支持通过镜像或文件挂载的方式部署 HuggingFace Transformers 上的模型 |
| | Embedding 模型部署 | 支持如 BGE-Large-Zh-v1.5 和 BGE-Large-En-v1.5 等 Embedding 模型的部署 |
| | Rerank 模型部署 | 支持如 BGE-Reranker-Large 等 Rerank 模型的部署 |
| | 多类型模型服务支持 | 支持大语言模型和多模态模型的在线对话服务 |
| | GPU 部署支持  | 支持在 Nvidia 和 昇腾 Ascend 系列 GPU 上部署模型，包括 Nvidia 的整卡和 vGPU 部署 |
| 服务监控 | 大语言模型服务监控 | 提供 GPU 使用率、Token 处理延迟、服务健康状态等多项指标的监控功能 |
| 水平自动扩展（HPA） | 自动扩展支持  | 根据 GPU 使用率和 Token 延迟自动调整服务规模，确保服务高效运行 |
| 微调模型 | 模型微调部署  | 支持部署模型微调导出的 checkpoint |
| | 模型微调部署  | 支持多个微调模型服务的部署，并提供对话结果比对功能，帮助评估和选择最优模型 |
| 在线模型服务集成与管理 | API Key 管理  | 提供主流在线模型服务的 API Key 管理功能 |
| | 权限管理 | 支持 API 密钥的权限设置和使用限制 |
| | 支持的在线服务 | 豆包、阿里通义千问、Azure、OpenAI、百度文心千帆、智谱、ChatGLM、讯飞星火认知、商汤商量、财跃星辰 |

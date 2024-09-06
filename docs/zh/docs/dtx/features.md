---
hide:
  - toc
---

# 功能特性

模型微调的功能特性参见下表：

| 一级功能 | 二级功能 | 描述 |
| ------- | ------ | ---- |
| 数据集 | 可视化创建数据集 | 提供直观的界面，支持创建训练、验证和测试数据集 |
| | S3存储支持 | 支持从S3存储中直接拉取文件，提升数据接入的便捷性 |
| | 本地文件上传 | 支持本地文件上传，提供多样化的数据接入方式 |
| 参数组 | 可视化创建超参数组 | 通过直观的界面配置超参数组，包括调度器（Scheduler）、优化器（Optimizer）、学习率（Learning Rate）、训练周期（Epochs）和批次大小（Batch Size）等 | 
| 微调实验 | 可视化模型微调 | 支持 LoRA、全量微调（full）、冻结微调（freeze）等多种模型微调方式的可视化管理 |
| | 矩阵式微调 | 支持使用不同的参数组和数据集创建微调实验，进行矩阵式微调 |
| | 实时监控 | 支持查看微调过程中的学习率、训练损失和验证损失等关键数据，实时监控模型训练状态 |
| | 检查点评估 | 支持对微调过程中的检查点（checkpoint）进行评估打分，确保模型质量 |
| | 模型导出与部署 | 支持将微调后的模型导出到模型中心，便于部署模型推理服务 |
| 模型微调 | 多种微调方法 | 支持（增量）预训练、多模态指令监督微调、奖励模型训练、PPO训练、DPO训练、KTO训练、ORPO训练等多种集成方法 | 
| | 精度支持 | 支持 16 比特全参数微调、冻结微调、LoRA 微调，以及基于 AQLM/AWQ/GPTQ/LLM.int8/HQQ/EETQ 的 2/3/4/5/6/8 比特 QLoRA 微调 | 
| | 先进算法集成 | 支持 GaLore、BAdam、DoRA、LongLoRA、LLaMA Pro、Mixture-of-Depths、LoRA+、LoftQ、PiSSA 和 Agent 微调等先进算法 | 
| | 实用技巧支持 | 集成 FlashAttention-2、Unsloth、RoPE scaling、NEFTune 和 rsLoRA 等实用技巧 |
| 模型推理 | 推理支持 | 提供基于 vLLM 的 OpenAI 风格 API，支持模型推理服务 |
| 支持的基础模型 | 支持的模型 | 包括 Baichuan 2、BLOOM/BLOOMZ、ChatGLM3、Command R、DeepSeek (Code/MoE)、Falcon、Gemma/Gemma 2/CodeGemma、GLM-4、InternLM2、Llama、Llama 2、Llama 3、LLaVA-1.5、Mistral/Mixtral、OLMo、PaliGemma、Phi-1.5/Phi-2、Phi-3、Qwen/Qwen1.5/Qwen2 (Code/MoE)、StarCoder 2、XVERSE、Yi/Yi-1.5、Yi-VL 和 Yuan 2 等众多基础模型。 |

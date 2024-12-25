---
hide:
  - toc
---

# Nvidia Triton 推理服务器

Triton 推理服务器使团队能够部署来自多个深度学习和机器学习框架的任何 AI 模型，包括 TensorRT、TensorFlow、PyTorch、ONNX、OpenVINO、Python、RAPIDS FIL 等。
Triton 支持在云端、数据中心、边缘和嵌入式设备上进行推理，兼容 NVIDIA GPU、x86 和 ARM CPU 以及 AWS Inferentia。
Triton 推理服务器为多种查询类型（如实时、批处理、集成和音视频流）提供优化的性能。
Triton 推理服务器是 NVIDIA AI Enterprise 的一部分，这是一个加速数据科学管道并简化生产 AI 开发和部署的软件平台。

主要特性包括：

- 支持多种深度学习框架
- 支持多种机器学习框架
- 并发模型执行
- 动态批处理
- 为有状态模型提供序列批处理和隐式状态管理
- 提供后端 API，允许添加自定义后端和前/后处理操作
- 使用集成或业务逻辑脚本（BLS）进行模型管道化
- 基于社区开发的 KServe 协议的 HTTP/REST 和 GRPC 推理协议
- 提供 C API 和 Java API，使 Triton 能够直接链接到您的应用程序中，用于边缘和其他进程内使用场景
- 指示 GPU 利用率、服务器吞吐量、服务器延迟等的指标

<div>
<iframe width="560" height="315" src="https://www.youtube.com/embed/NQDtfSi5QF4" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

## 参考

- [Nvidia Triton 推理服务器官网](https://developer.nvidia.com/triton-inference-server)

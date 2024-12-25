---
hide:
  - toc
---

# Ray

Ray 是一个开源的统一计算框架，使扩展 AI 和 Python 工作负载变得容易，涵盖的范围从强化学习到深度学习，再到调优和模型服务。

Ray 旨在提供一个通用的分布式计算 API。实现这一目标的核心部分是提供简单但通用的编程抽象，让系统处理所有复杂的工作。
这种理念使开发者能够将 Ray 与现有的 Python 库和系统结合使用。

Ray 程序员使用一些简单的 Python 原语来表达他们的逻辑，而系统则管理诸如并行性和分布式内存管理等物理执行问题。
Ray 用户从资源的角度考虑集群管理，而系统则根据这些资源请求管理调度和自动扩展。

![ray-padded](./images/ray-padded.svg)

Ray 提供了一个通用的 API，包括 task、actor 和 object，用于构建分布式应用。

## 参考

- [Ray 仓库](https://github.com/ray-project/ray)
- [ray.io 官网](https://www.ray.io/)

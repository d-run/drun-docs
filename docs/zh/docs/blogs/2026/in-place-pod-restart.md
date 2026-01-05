# Kubernetes v1.35 引入原地重启所有容器，强化 AI 训练与加速计算能力

在 Kubernetes v1.35 的众多更新中，有一个看似不起眼，却正在 AI Infra 领域引发关注的 Alpha 特性：
**Restart All Containers（原地重启所有容器）**

从传统微服务的角度，它可能只是“更灵活的重启策略”；
但放到 **AI Infra** 场景，你会发现：这是 Kubernetes 第一次真正对齐 AI 训练与加速计算的失败模型。

## AI Infra 的核心矛盾：失败不可避免，但恢复代价高昂

在 AI 训练集群中，失败时常发生，但真正昂贵的是 **恢复过程** 。
常见问题包括：

- NCCL/RDMA 通信进入错误状态
- GPU Context 锁死但进程仍存活
- Python Runtime 卡死、无法优雅退出
- 共享内存、HugePage、临时目录污染
- 单个 Worker 异常导致同步训练整体失败

这些问题有一个共同点：
**单独重启一个容器几乎无效；删除并重建 Pod 又代价太高。**

在 v1.35 之前，Kubernetes 只有两种选择：

| 方法 | 对 AI Infra 的影响 |
| --- | ----------------- |
| 容器级重启 | 状态未清，训练无法继续 |
| Pod 删除重建 | GPU 释放 + 重新调度，分钟级空转 |

这正是 AI Infra 长期存在的系统性矛盾。

## 新特性详解：RestartAllContainers

v1.35 引入了全新的 **RestartAllContainers** 动作：
当某个容器退出且满足规则时，Pod 内所有容器将 **原地重启** 。

### 特性状态与启用要求

- Alpha 特性，默认关闭，需要显式开启
- 依赖 `ContainerRestartRules` 功能
- 需在 API 服务器与 kubelet 上启用 `RestartAllContainersOnContainerExits`

### 触发机制

通过 `restartPolicyRules`，可在容器级别定义：

- `action: RestartAllContainers`
- `onExit` 条件（如退出码匹配）

当容器退出并满足规则时，kubelet 会触发 **原地重启** 。

### 原地重启的执行流程

1. **快速终止所有容器**

    - 不执行 preStop Hook
    - 忽略 terminationGracePeriodSeconds

2. **保留 Pod 关键资源**

    - Pod UID、Pod IP
    - 网络命名空间和 Sandbox
    - 所有 Volume 挂载（emptyDir、PVC 等）

3. **状态可观测性增强**

    Pod Condition `AllContainersRestarting`

    - 触发时为 True
    - 容器准备重启后为 False

4. **完整重启序列**

    - 所有 Init Container 按顺序重新执行
    - Sidecar 和主容器依次启动
    - 容器重启计数正确累加

### 核心行为对比

| 行为维度 | 传统 Pod 重建 | RestartAllContainers 原地重启 |
| ------ | ------------ | ---------------------------- |
| Pod UID | 改变 | 保留 |
| Pod IP | 改变 | 保留 |
| 重新调度 | 需要 | 不需要 |
| Init Container | 不重跑 | 会重新执行 |
| preStop Hook | 会执行 | 不执行 |
| 网络/卷 | 可能重建 | 保持不变 |
| CPU/GPU 资源 | 重新分配 | 保留 |

### 官方使用建议

- 重新执行 Init Container 来恢复 Pod 环境
- 由 Sidecar 监测逻辑判断失败并触发 Pod 重启
- 适用于调度和资源敏感的批处理或 AI/ML 任务

!!! caution "注意事项"

    - 所有容器需具备可重入设计
    - 外部工具需支持 Init Container 多次运行
    - preStop 不执行，容器需安全应对突发终止

## 为什么 AI Infra 迫切需要 RestartAllContainers

### GPU 是稀缺资源：保留热缓存，减少等待

| 操作方式       | GPU 状态 | 缓存状态                     | 恢复时间 |
|----------------|---------|-----------------------------|---------|
| Pod 重建       | GPU 释放 | Page Cache、模型缓存失效     | 分钟级  |
| 原地重启       | GPU 保留 | 所有缓存保留                 | 秒级    |

利用 GPU 级快速复位能力，训练恢复时间可以大幅缩短。

### 分布式训练要求同步：秒级恢复全局一致

- 任意一个 Worker 异常 → 全体 Worker 必须回到一致状态  
- 传统模式：整批 Pod 删除 → 重新调度 → 分钟级恢复  
- RestartAllContainers：异常 Pod 原地重启，其他 Pod 无需调度 → 秒级恢复  

秒级恢复意味着训练作业几乎不中断，极大提升资源利用率。

### Init Container 可重复执行：支持数据/缓存热重置

- Init Container 负责：模型下载、数据准备、NCCL/CUDA 初始化、缓存预热  
- 过去：只在 Pod 创建时运行一次  
- 现在：RestartAllContainers 支持在不删除 Pod 的情况下重新执行 Init Container  

数据准备和缓存预热无需重复浪费时间或 GPU 资源。

### Sidecar/Watcher 实现自动自愈

- Watcher/Agent 监控 NCCL、GPU、进程状态  
- 当状态不可恢复 → 特定 exit code 触发 Pod 原地重启  
- 无需 Job 或 Operator 介入  

AI 作业的自愈逻辑下沉到 Pod 内部，减少运维干预。

### 快速恢复优先于优雅终止：优化 MTTR

| 设计选择           | 传统方式 | RestartAllContainers |
|-------------------|---------|------------------|
| preStop 执行       | ✅       | ❌               |
| 强制终止           | ❌       | ✅               |
| 重启速度           | 分钟级   | 秒级             |
| 从 checkpoint 恢复 | ✅       | ✅               |

目标是最大化作业恢复速度（MTTR），即使牺牲优雅终止，也能保证 AI 训练连续性。

## 示例：AI Worker Pod 的原地快速恢复

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: ml-worker-pod
spec:
  restartPolicy: Never
  initContainers:
    - name: setup-environment
      image: my-repo/setup-worker:1.0
  containers:
    - name: watcher
      image: my-repo/watcher:1.0
      restartPolicy: Always
      restartPolicyRules:
        - action: RestartAllContainers
          onExit:
            exitCodes:
              operator: In
              values: [88]
    - name: trainer
      image: my-repo/training-app:1.0
```

触发流程：

1. Watcher 检测到不可恢复错误，以退出码 `88` 退出
2. kubelet 触发 `RestartAllContainers`
3. Pod 内所有容器被终止
4. Init Container 重新执行
5. Trainer 从 checkpoint 恢复训练

## DaoCloud 的实践与展望

`RestartAllContainers` 标志着 Kubernetes 正在从面向 Web 服务的容器编排系统，迈向面向加速计算与 AI 训练的基础设施操作系统的关键一步。

DaoCloud 将在 DCE 平台中：

- 引入 RestartAllContainers 能力
- 与 AI 作业、批处理、JobSet 等场景结合
- 提供企业级实验、验证与落地方案

建议 AI Infra 用户：

- 在测试集群启用 Alpha 特性
- 结合 Sidecar/Init Container 架构验证
- 向社区与 DaoCloud 反馈实践经验

!!! tip "结语"

    RestartAllContainers 不是简单的重启功能，
    而是 Kubernetes 第一次真正理解 AI Infra 的失败模式。

    看似微小，却对降低成本、提升算力利用率意义深远。

**参考信息：**

- [重启所有容器的步骤描述](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#restart-all-containers)
- [KEP: Restart all containers on container exits](https://github.com/kubernetes/enhancements/issues/5532)
- [Issue: Investigate restarting pods in-place](https://github.com/kubernetes-sigs/jobset/issues/467)
- [Kubernetes blog: New level of efficiency with in-place Pod restart](https://kubernetes.io/blog/2026/01/02/kubernetes-v1-35-restart-all-containers/)
- [DaoCloud 是 Kubernetes 认证服务商](https://docs.daocloud.io/dce/kcsp/)

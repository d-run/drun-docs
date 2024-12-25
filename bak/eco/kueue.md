---
hide:
  - toc
---

# Kueue

Kueue 是一个 Kubernetes 原生的系统，用于管理配额及 Job 如何消耗配额的使用。
Kueue 决定 Job 何时应该等待，何时可以启动（即创建 Pod），以及何时需要抢占（即删除活动的 Pod）。

## 为什么使用 Kueue

你可以在一个标准的 Kubernetes 集群上安装 Kueue。
Kueue 不会替换任何现有的 Kubernetes 组件。Kueue 适用于以下云环境：

- 计算资源具有弹性，可以扩容和缩容。
- 计算资源是异构的（在架构、可用性、价格等方面存在差异）。

Kueue API 允许你定义：

- 在租户之间公平分享的配额和策略。
- 资源的可替代性：如果某种资源类型已被完全使用，Kueue 可以使用另一种资源类型来允许 Job 进行。

Kueue 的核心设计原则是避免重复 Kubernetes 组件和成熟第三方控制器中的功能。
自动扩展、Pod 到节点的调度和 Job 生命周期管理分别由 cluster-autoscaler、kube-scheduler 和 kube-controller-manager 负责。
高级的准入控制可以交给如 gatekeeper 这样的控制器。

## 功能概述

- **Job 管理：** 支持基于[优先级](https://kueue.sigs.k8s.io/docs/concepts/workload/#priority)的 Job 排队，
  并提供不同的[策略](https://kueue.sigs.k8s.io/docs/concepts/cluster_queue/#queueing-strategy)：`StrictFIFO` 和 `BestEffortFIFO`。
- **资源管理：** 支持资源的公平分享和[抢占](https://kueue.sigs.k8s.io/docs/concepts/cluster_queue/#preemption)，在不同租户之间提供多种策略。
- **动态资源回收：** 提供一种机制，当 Job 的 Pod 完成时，[释放](https://kueue.sigs.k8s.io/docs/concepts/workload/#dynamic-reclaim)配额。
- **资源类型的可替代性：** 在 ClusterQueue 和 Cohort 中实现配额的[借用或抢占](https://kueue.sigs.k8s.io/docs/concepts/cluster_queue/#flavorfungibility)。
- **集成：** 内置对流行 Job 的支持，例如 [BatchJob](https://kueue.sigs.k8s.io/docs/tasks/run/jobs/)、
  [Kubeflow 训练 Job ](https://kueue.sigs.k8s.io/docs/tasks/run/kubeflow/)、
  [RayJob](https://kueue.sigs.k8s.io/docs/tasks/run/rayjobs/)、
  [RayCluster](https://kueue.sigs.k8s.io/docs/tasks/run/rayclusters/)、
  [JobSet](https://kueue.sigs.k8s.io/docs/tasks/run/jobsets/)、
  [普通 Pod](https://kueue.sigs.k8s.io/docs/tasks/run/plain_pods/)。
- **系统洞察：** 内置的 [Prometheus 指标](https://kueue.sigs.k8s.io/docs/reference/metrics/)帮助监控系统状态，以及条件。
- **AdmissionChecks：** 提供一种机制，允许内部或外部组件影响 Job 是否可以被[允许](https://kueue.sigs.k8s.io/docs/concepts/admission_check/)。
- **高级自动扩展支持：** 通过 AdmissionChecks 与 cluster-autoscaler 的
  [provisioningRequest](https://kueue.sigs.k8s.io/docs/admission-check-controllers/provisioning/#job-using-a-provisioningrequest) 集成。
- **顺序准入：** 简单实现[全有或全无调度](https://kueue.sigs.k8s.io/docs/tasks/setup_sequential_admission/)。
- **部分准入：** 如果应用支持，允许 Job 以[较小的并行度](https://kueue.sigs.k8s.io/docs/tasks/run/jobs/#partial-admission)运行，基于可用的配额。

## Kueue 的高级操作

![高级 Kueue 操作](./images/theory-of-kueue.svg)

## 参考

- [Kueue 仓库](https://github.com/kubernetes-sigs/kueue)
- [Kueue 网站](https://kueue.sigs.k8s.io/)

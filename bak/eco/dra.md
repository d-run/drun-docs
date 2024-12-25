# 动态资源分配 DRA

动态资源分配（Dynamic Resource Allocation, DRA）是 Kubernetes v1.26 发布的一个 Alpha 特性。

动态资源分配是一个用于在 Pod 之间和 Pod 内部容器之间请求和共享资源的 API。
它是持久卷 API 的通用资源化。第三方资源驱动程序负责跟踪和分配资源，
Kubernetes 通过**结构化参数**（在 Kubernetes 1.30 中引入）提供了额外的支持。
当驱动程序使用结构化参数时，Kubernetes 可以处理调度和资源分配，而无需与驱动程序通信。
而不同类型的资源，可支持用于“定义需求”和“初始化”的任意参数。

## 准备工作

Kubernetes v1.30 包含用于动态资源分配的集群级 API 支持，但它需要被显式启用。
你还必须为此 API 要管理的特定资源安装资源驱动程序。
如果你未运行 Kubernetes v1.30，请查看旧版本的 Kubernetes 文档。

## API

`resource.k8s.io/v1alpha2` API 组提供了以下类型：

- ResourceClass: 定义由哪个资源驱动程序处理某种资源，并为其提供通用参数。
  集群管理员在安装资源驱动程序时创建 ResourceClass。

- ResourceClaim: 定义工作负载所需的特定资源实例。
  由用户创建（手动管理生命周期，可以在不同的 Pod 之间共享），
  或者由控制平面基于 ResourceClaimTemplate 为特定 Pod 创建
  （自动管理生命周期，通常仅由一个 Pod 使用）。

- ResourceClaimTemplate: 定义用于创建 ResourceClaim 的 spec 和一些元数据。
  部署工作负载时由用户创建。

- PodSchedulingContext: 供控制平面和资源驱动程序内部使用，
  在需要为 Pod 分配 ResourceClaim 时协调 Pod 调度。

- ResourceSlice: 与结构化参数一起使用，发布集群中可用资源的信息。

- ResourceClaimParameters: 包含影响调度的 ResourceClaim 参数，
  以 Kubernetes 理解的格式（“结构化参数模型”）呈现。
  提供了供应商驱动程序，在设置底层资源时，使用的不透明扩展中可能嵌入其他参数。

- ResourceClassParameters: 类似于 ResourceClaimParameters，ResourceClassParameters 为 Kubernetes 理解的 ResourceClass 参数提供了一种类型。

ResourceClass 和 ResourceClaim 的参数存储在单独的对象中，通常使用安装资源驱动程序时创建的
CustomResourceDefinition 所定义的类型。

资源驱动程序的开发者决定他们是要在自己的外部控制器中处理这些参数，
还是依赖 Kubernetes 通过使用结构化参数来处理它们。
自定义控制器提供更多的灵活性，但对于节点本地资源，集群自动缩放可能无法可靠工作。
结构化参数使集群自动缩放成为可能，但可能无法满足所有用例。

当驱动程序使用结构化参数时，仍然可以让最终用户使用供应商特定的 CRD 指定参数。
在这种情况下，驱动程序需要将这些自定义参数转换为内部类型。
或者，驱动程序也可以直接使用内部类型的文档。

`core/v1` 的 `PodSpec` 在 `resourceClaims` 字段中定义 Pod 所需的 ResourceClaim。
该列表中的条目引用 ResourceClaim 或 ResourceClaimTemplate。
当引用 ResourceClaim 时，使用此 PodSpec 的所有 Pod
（例如 Deployment 或 StatefulSet 中的 Pod）共享相同的 ResourceClaim 实例。
引用 ResourceClaimTemplate 时，每个 Pod 都有自己的实例。

容器资源的 `resources.claims` 列表定义容器可以访问的资源实例，
从而可以实现在一个或多个容器之间共享资源。

下面是一个虚构的资源驱动程序的示例。
该示例将为此 Pod 创建两个 ResourceClaim 对象，每个容器都可以访问其中一个。

```yaml
apiVersion: resource.k8s.io/v1alpha2
kind: ResourceClass
name: resource.example.com
driverName: resource-driver.example.com
---
apiVersion: cats.resource.example.com/v1
kind: ClaimParameters
name: large-black-cat-claim-parameters
spec:
  color: black
  size: large
---
apiVersion: resource.k8s.io/v1alpha2
kind: ResourceClaimTemplate
metadata:
  name: large-black-cat-claim-template
spec:
  spec:
    resourceClassName: resource.example.com
    parametersRef:
      apiGroup: cats.resource.example.com
      kind: ClaimParameters
      name: large-black-cat-claim-parameters
–--
apiVersion: v1
kind: Pod
metadata:
  name: pod-with-cats
spec:
  containers:
  - name: container0
    image: ubuntu:20.04
    command: ["sleep", "9999"]
    resources:
      claims:
      - name: cat-0
  - name: container1
    image: ubuntu:20.04
    command: ["sleep", "9999"]
    resources:
      claims:
      - name: cat-1
  resourceClaims:
  - name: cat-0
    source:
      resourceClaimTemplateName: large-black-cat-claim-template
  - name: cat-1
    source:
      resourceClaimTemplateName: large-black-cat-claim-template
```

## 调度

### 不使用结构化参数

与原生资源（CPU、RAM）和扩展资源（由设备插件管理，并由 kubelet 公布）不同，
如果没有结构化参数，调度器无法知道集群中有哪些动态资源，
也不知道如何将它们拆分以满足特定 ResourceClaim 的要求。
资源驱动程序负责这些任务。
资源驱动程序在为 ResourceClaim 保留资源后将其标记为“已分配（Allocated）”。
然后告诉调度器集群中可用的 ResourceClaim 的位置。

ResourceClaim 可以在创建时就进行分配（“立即分配”），不用考虑哪些 Pod 将使用它。
默认情况下采用延迟分配，直到需要 ResourceClaim 的 Pod 被调度时
（即“等待第一个消费者”）再进行分配。

在这种模式下，调度器检查 Pod 所需的所有 ResourceClaim，并创建一个 PodScheduling 对象，
通知负责这些 ResourceClaim 的资源驱动程序，告知它们调度器认为适合该 Pod 的节点。
资源驱动程序通过排除没有足够剩余资源的节点来响应调度器。
一旦调度器有了这些信息，它就会选择一个节点，并将该选择存储在 PodScheduling 对象中。
然后，资源驱动程序为分配其 ResourceClaim，以便资源可用于该节点。
完成后，Pod 就会被调度。

作为此过程的一部分，ResourceClaim 会为 Pod 保留。
目前，ResourceClaim 可以由单个 Pod 独占使用或不限数量的多个 Pod 使用。

除非 Pod 的所有资源都已分配和保留，否则 Pod 不会被调度到节点，这是一个重要特性。
这避免了 Pod 被调度到一个节点但无法在那里运行的情况，
这种情况很糟糕，因为被挂起 Pod 也会阻塞为其保留的其他资源，如 RAM 或 CPU。

!!! note

    由于需要额外的通信，使用 ResourceClaim 的 Pod 的调度将会变慢。
    请注意，这也可能会影响不使用 ResourceClaim 的 Pod，因为一次仅调度一个
    Pod，在使用 ResourceClaim 处理 Pod 时会进行阻塞 API 调用，
    从而推迟调度下一个 Pod。

### 使用结构化参数

当驱动程序使用结构化参数时，调度器负责在 Pod 需要资源时为 ResourceClaim 分配资源。
通过从 ResourceSlice 对象中检索可用资源的完整列表，
跟踪已分配给现有 ResourceClaim 的资源，然后从剩余的资源中进行选择。
所选资源受与 ResourceClaim 关联的 ResourceClaimParameters 或 ResourceClassParameters 提供的约束的影响。

所选资源与供应商特定参数一起被记录在 ResourceClaim 状态中，
因此当 Pod 即将在节点上启动时，节点上的资源驱动程序具有准备资源所需的所有信息。

通过使用结构化参数，调度器能够在不与 DRA 资源驱动程序通信的情况下做出决策。
它还能够通过将 ResourceClaim 分配信息保存在内存中，并在同时将 Pod 绑定到节点的同时将此信息写入 ResourceClaim 对象中，
快速调度多个 Pod。

## 监控资源

kubelet 提供了一个 gRPC 服务，以便发现正在运行的 Pod 的动态资源。
有关 gRPC 端点的更多信息，请参阅[资源分配报告](https://kubernetes.io/zh-cn/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/#monitoring-device-plugin-resources)。

## 预调度的 Pod

当你（或别的 API 客户端）创建设置了 `spec.nodeName` 的 Pod 时，调度器将被绕过。
如果 Pod 所需的某个 ResourceClaim 尚不存在、未被分配或未为该 Pod 保留，那么 kubelet
将无法运行该 Pod，并会定期重新检查，因为这些要求可能在以后得到满足。

这种情况也可能发生在 Pod 被调度时调度器中未启用动态资源分配支持的时候（原因可能是版本偏差、配置、特性门控等）。
kube-controller-manager 能够检测到这一点，并尝试通过触发分配和/或预留所需的 ResourceClaim 来使 Pod 可运行。

!!! note

    这仅适用于不使用结构化参数的资源驱动程序。

绕过调度器并不是一个好的选择，因为分配给节点的 Pod 会锁住一些正常的资源（RAM、CPU），
而这些资源在 Pod 被卡住时无法用于其他 Pod。为了让一个 Pod 在特定节点上运行，
同时仍然通过正常的调度流程进行，请在创建 Pod 时使用与期望的节点精确匹配的节点选择算符：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-with-cats
spec:
  nodeSelector:
    kubernetes.io/hostname: name-of-the-intended-node
  ...
```

你还可以在准入时变更传入的 Pod，取消设置 `.spec.nodeName` 字段，并改为使用节点选择算符。

## 启用动态资源分配

动态资源分配是一个 **Alpha 特性**，只有在启用 `DynamicResourceAllocation`
[特性门控](https://kubernetes.io/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)
和 `resource.k8s.io/v1alpha2` API 组 时才启用。
有关详细信息，参阅 `--feature-gates` 和 `--runtime-config`
[kube-apiserver 参数](https://kubernetes.io/zh-cn/docs/reference/command-line-tools-reference/kube-apiserver/)。
kube-scheduler、kube-controller-manager 和 kubelet 也需要设置该特性门控。

快速检查 Kubernetes 集群是否支持该功能的方法是列出 ResourceClass 对象：

```shell
kubectl get resourceclasses
```

如果你的集群支持动态资源分配，则响应是 ResourceClass 对象列表或：

```
No resources found
```

如果不支持，则会输出如下错误：

```
error: the server doesn't have a resource type "resourceclasses"
```

kube-scheduler 的默认配置仅在启用特性门控且使用 v1 配置 API 时才启用 "DynamicResources" 插件。
自定义配置可能需要被修改才能启用它。

除了在集群中启用该功能外，还必须安装资源驱动程序。
欲了解详细信息，请参阅驱动程序的文档。

## 参考

- 参阅 [K8s 官网 DRA 论述](https://kubernetes.io/zh-cn/docs/concepts/scheduling-eviction/dynamic-resource-allocation/)
- 参阅[动态资源分配 KEP](https://github.com/kubernetes/enhancements/blob/master/keps/sig-node/3063-dynamic-resource-allocation/README.md)
  和[结构化参数 KEP](https://github.com/kubernetes/enhancements/tree/master/keps/sig-node/4381-dra-structured-parameters)。
